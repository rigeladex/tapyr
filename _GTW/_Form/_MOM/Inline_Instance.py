# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.Form.MOM.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    Inline_Instance
#
# Purpose
#    Edit or create an MOM instance inside a form for a related MOM instance
#
# Revision Dates
#    19-Jan-2010 (MG) Creation
#     2-Feb-2010 (MG) `Lid_and_State_Field` added
#     3-Feb-2010 (MG) `widget` change to allow multiple field groups in one
#                     table row
#     3-Feb-2010 (MG) Unlinking of inline instances added
#     5-Feb-2010 (MG) `Attribute_Inline_Instance` and `Link_Inline_Instance`
#                     added
#     6-Feb-2010 (MG) `_Inline_Instance_.instances` advance the db_instance
#                     in any case
#     8-Feb-2010 (MG) `Lid_and_State_Field`: guard against entities which
#                     have no `lid` (An_Entity's)
#     9-Feb-2010 (MG) `Lid_and_State_Field.get_raw` fixed
#    10-Feb-2010 (MG) `_Inline_Instance_.instance` fixed to get correct
#                     instance for `An_Entity`
#    11-Feb-2010 (MG) Changed handling of instance to form assignment (to
#                     make sure that each posted form gets assing the correct
#                     instance)
#    22-Feb-2010 (MG) `_create_instance` added to `Attribute_Inline_Instance`
#    27-Feb-2010 (MG) `add_internal_fields` changed
#     6-Mar-2010 (MG) Error handling changed
#    11-Mar-2010 (MG) Use new `Attribute_Inline.instance_as_raw`
#    12-May-2010 (CT) Use `pid`, not `lid`
#    ««revision-date»»···
#--

from   _TFL                                 import TFL
import _TFL._Meta.Once_Property
from   _TFL.predicate                       import all_true
from   _GTW                                 import GTW
import _GTW._Form.Field
import _GTW._Form.Widget_Spec
import _GTW._Form._MOM
import _GTW._Form._MOM._Instance_

class Pid_and_State_Field (GTW.Form.Field) :
    """Stores the state of the line form and the pid of edited object/link."""

    hidden   = True
    electric = True
    widget   = GTW.Form.Widget_Spec ("html/field.jnj, hidden")

    def get_raw (self, form, defaults = {}) :
        state = "N"
        pid   = getattr (form.instance, "pid", "")
        if pid :
            state = "L"
        elif form.prototype :
            state = "P"
        return "%s:%s" % (pid, state)
    # end def get_raw

# end class Pid_and_State_Field

class M_Inline_Instance (GTW.Form.MOM._Instance_.__class__) :
    """Add additional internal fields"""

    def add_internal_fields (cls, et_man) :
        cls.__m_super.add_internal_fields (et_man)
        cls.pid_and_state_field = Pid_and_State_Field \
            ("_pid_a_state_", et_man = et_man)
        cls.hidden_fields.append (cls.pid_and_state_field)
    # end def add_internal_fields

# end class M_Inline_Instance

class _Inline_Instance_ (GTW.Form.MOM._Instance_) :
    """Base class for form which are part of a outer form."""

    __metaclass__ = M_Inline_Instance

    def __init__ ( self, * args, ** kw) :
        self.prototype = kw.pop ("prototype", False)
        self.__super.__init__ (* args, ** kw)
    # end def __init__

    @TFL.Meta.Once_Property
    def pid (self) :
        pid, state = self.request_data.get \
            (self.get_id (self.pid_and_state_field), ":X").split (":")
        self.state = state
        return pid
    # end def pid

    def _prepare_form (self) :
        pid, state = self.pid, self.state
        return True
    # end def _prepare_form

    @TFL.Meta.Once_Property
    def state (self) :
        pid, state = self.request_data.get \
            (self.get_id (self.pid_and_state_field), ":X").split (":")
        self.pid   = pid
        return state
    # end def state

# end class _Inline_Instance_

class An_Attribute_Inline_Instance (_Inline_Instance_) :
    """A form which handles an attribute of an An_Entity as a seperate form."""

    instance = None

    def get_object_raw (self, defaults) :
        return dict (getattr (self.instance, "raw_attr_dict", ()), raw = True)
    # end def get_object_raw

# end class An_Attribute_Inline_Instance

class Id_Attribute_Inline_Instance (_Inline_Instance_) :
    """A form which handles an attribute of an Id_Entity as a seperate form."""

    def _create_instance (self, on_error) :
        if self.raw_attr_dict :
            ### if raw data is provided for this form -> let's check if we
            ### find an instance with this raw data before we try to create
            ### a new one
            cooked_attrs = self.et_man._etype.cooked_attrs (self.raw_attr_dict)
            instance     = self.et_man.query (** cooked_attrs).first ()
            if instance :
                return instance
        return self.__super._create_instance (on_error)
    # end def _create_instance

# end class Id_Attribute_Inline_Instance

class Link_Inline_Instance (_Inline_Instance_) :
    """A form which handles an inline link"""

    def create_object (self, * args, ** kw) :
        state = self.state
        if state == "U" :
            if self.instance :
                ### this form handles an link which should be destroyed
                ### we need to destroy the instance in the database
                self.instance.destroy ()
                ### and mark that this form does not have a valid instance
                ### (needed for the min/max count check's)
                self.instance = None
                ### XXX handle deleting of links object's
            return
        if state == "L" :
            ### this instance is still linked and was not changed -> no need
            ### to do anything for this form
            return
        if self.raw_attr_dict and (not self.instance or self.state == "r") :
            ### this is not a rename ->
            ### set the owner role before we create the link
            self.raw_attr_dict [self.owner_role_name] = \
                self.parent.get_object_raw ()
        self.__super.create_object (* args, ** kw)
    # end def create_object

# end class Link_Inline_Instance

class Collection_Inline_Instance (An_Attribute_Inline_Instance) :
    """XXX"""

    def create_object (self, * args, ** kw) :
        state = self.state
        if state == "U" :
            if self.instance :
                self.instance = None
                ### XXX handle deleting of links object's
            return
        if state == "L" :
            ### this instance is still linked and was not changed -> no need
            ### to do anything for this form
            return
        self.__super.create_object (* args, ** kw)
    # end def create_object

# end class Collection_Inline_Instance

if __name__ != "__main__" :
    GTW.Form.MOM._Export ("*")
### __END__ GTW.Form.MOM.Inline_Instance
