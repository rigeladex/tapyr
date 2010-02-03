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
#    ««revision-date»»···
#--

from   _TFL                                 import TFL
import _TFL._Meta.Once_Property

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
        lid   = ""
        state = "L"
        if instance :
            lid = instance.lid
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

class Inline_Instance (GTW.Form.MOM._Instance_) :
    """A form which is embedded in a `Instance` form."""

    __metaclass__ = M_Inline_Instance
    widget        = GTW.Form.Widget_Spec \
        ( "html/form.jnj, field_groups"
        , tr_head = "html/form.jnj, fgs_tr_head"
        , tr_body = "html/form.jnj, fgs_tr_body"
        )

    def __init__ ( self, * args, ** kw) :
        self.prototype = kw.pop ("prototype", False)
        self.__super.__init__ (* args, ** kw)
    # end def __init__

    def _prepare_form (self) :
        lid, state = self.get_raw (self.lid_and_state_field).split (":")
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
        return True
    # end def _prepare_form

# end class Inline_Instance

if __name__ != "__main__" :
    GTW.Form.MOM._Export ("*")

### __END__ GTW.Form.MOM.Inline_Instance
