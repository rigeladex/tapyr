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

class Lid_and_State_Field (GTW.Form.Field) :
    """Stores the state of the line form and the lid of edited object/link."""

    hidden = True

    widget = GTW.Form.Widget_Spec ("html/field.jnj, hidden")

    def get_raw (self, form, instance) :
        state = "N"
        lid   = getattr (instance, "lid", "")
        if lid :
            state = "L"
        elif form.prototype :
            state = "P"
        return "%s:%s" % (lid, state)
    # end def get_raw

# end class Lid_and_State_Field

class M_Inline_Instance (GTW.Form.MOM._Instance_.__class__) :
    """Add additional internal fields"""

    def add_internal_fields (cls, et_man, field_groups) :
        cls.__m_super.add_internal_fields (et_man, field_groups)
        fg = field_groups [0]
        cls.lid_and_state_field = Lid_and_State_Field \
            ("_lid_a_state_", et_man = et_man)
        fg.fields.append (cls.lid_and_state_field)
    # end def add_internal_fields

# end class M_Inline_Instance

class _Inline_Instance_ (GTW.Form.MOM._Instance_) :
    """Base class for form which are part of a outer form."""

    __metaclass__ = M_Inline_Instance
    widget        = GTW.Form.Widget_Spec \
        ( "html/form.jnj, field_groups"
        , inline_table_tr_head = "html/form.jnj, inline_table_tr_head"
        , inline_table_tr_body = "html/form.jnj, inline_table_tr_body"
        )

    def __init__ ( self, * args, ** kw) :
        self.prototype = kw.pop ("prototype", False)
        self.__super.__init__ (* args, ** kw)
    # end def __init__

    @TFL.Meta.Once_Property
    def instance (self) :
        if self.prototype :
            return None
        lid, state  = self.lid, self.state
        db_instance = self.parent.Instances.next ()
        if not lid :
            if state == "X" :
                ### no post data -> try to get the instance from the
                ### database
                return db_instance
            return None
        pid = self.et_man.pid_from_lid (lid)
        return self.et_man.pid_query   (pid)
    # end def instance

    @TFL.Meta.Once_Property
    def lid (self) :
        lid, state = self.request_data.get \
            (self.get_id (self.lid_and_state_field), ":X").split (":")
        self.state = state
        return lid
    # end def lid

    def _prepare_form (self) :
        lid, state = self.lid, self.state
        if state == "U" :
            ### this from handles an instance which should be unlinked
            if not lid :
                ### since this instance was never saved to the database no
                ### further processing is required
                return False
            ### we need to destroy the instance in the database
            self.instance.destroy ()
            ### and mark that this form does not have a valid instance
            ### (needed for the min/max count check's)
            self.instance = None
            ### XXX handle deleting of links object's
            return False
        if state == "L" :
            ### this instance is still linked and was not changed -> no need
            ### to do anything for this form
            return False
        return True
    # end def _prepare_form

    @TFL.Meta.Once_Property
    def state (self) :
        lid, state = self.request_data.get \
            (self.get_id (self.lid_and_state_field), ":X").split (":")
        self.lid   = lid
        return state
    # end def state

# end class _Inline_Instance_

class Attribute_Inline_Instance (_Inline_Instance_) :
    """A form which handles an attribute of an entity as a seperate form"""

    pass

# end class Attribute_Inline_Instance

class Link_Inline_Instance (_Inline_Instance_) :
    """A form which handles an inline link"""

    def __call__ (self, request_data) :
        self.request_data = request_data
        if not self._prepare_form () :
            ### this form does not need any further processing
            return 0
        ### for links we need to handle the inline roles first
        error_count = 0
        attr_map    = \
            {self.parent.genric_role : self.parent.parent.instance.epk_raw}
        for ig in self.inline_groups :
            error_count  += ig (request_data)
            if ig.instance and not ig.error_count :
                ### looks like we have a valid inline attribute form
                ### let's add it to our attribute map
                attr_map [ig.generic_name] = ig.instance.epk_raw
        ### let's check if all roles are in the attr_map
        all_roles_correct = all_true \
            (   r.generic_role_name in attr_map
            for r in self.et_man.Roles
            )
        if all_roles_correct and not error_count :
            ### if no errors are found for the roles, let's try to
            ### create/update the link itself
            ### if the link already exists, filter all identical roles
            if self.instance :
                attr_map = dict \
                    ( (k, v) for k, v in attr_map.iteritems ()
                          if v != getattr (self.instance, k).epk_raw
                    )
            self.instance = self._create_or_update  (attr_map)
            error_count  += len (self.errors) + len (self.field_errors)
        self.error_count  = error_count
        return error_count
    # end def __call__

# end class Link_Inline_Instance

if __name__ != "__main__" :
    GTW.Form.MOM._Export ("*")

### __END__ GTW.Form.MOM.Inline_Instance
