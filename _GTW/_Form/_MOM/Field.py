# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
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
#    GTW.Form.MOM.Field
#
# Purpose
#    A single field of a MOM form
#
# Revision Dates
#    25-Feb-2010 (CT) Creation
#    ««revision-date»»···
#--

from   _GTW               import GTW
from   _MOM               import MOM
from   _TFL               import TFL

import _GTW._Form._MOM

import _GTW._Form.Field
import _GTW._Form.Widget_Spec

import _MOM._Attr.Type
import _MOM.Error

import _TFL._Meta.Object

WS                           = GTW.Form.Widget_Spec
MAT                          = MOM.Attr
MAT.A_Attr_Type.widget       = WS ("html/field.jnj, string")
MAT._A_Number_.widget        = WS ("html/field.jnj, number")
MAT.A_Date.widget            = WS ("html/field.jnj, date")
MAT.A_Date_Time.widget       = WS ("html/field.jnj, datetime")
MAT.A_Email.widget           = WS ("html/field.jnj, email")
MAT.A_Text.widget            = WS ("html/field.jnj, text")
MAT._A_Named_Object_.widget  = WS ("html/field.jnj, named_object")

MER                          = MOM.Error
MER.Invalid_Attribute.widget = WS ("html/mom_errors.jnj, invalide_attribute")

class Field (TFL.Meta.Object) :
    """A wrapper around the attribute of the MOM object used in field groups"""

    hidden = False

    def __init__ (self, et_man, attr_name) :
        self.html_name      = attr_name
        if "." in attr_name :
            scope           = et_man.home_scope
            role, attr_name = attr_name.split (".")
            et_man          = getattr \
                (scope, getattr (et_man, role).role_type.type_name)
        self.et_man         = et_man
        self.name           = attr_name
        self.attr_kind      = getattr (et_man._etype, attr_name)
    # end def __init__

    @property
    def choices (self) :
        attr = self.attr_kind.attr
        if isinstance (attr, MOM.Attr._A_Named_Object_) :
            return sorted (attr.Table)
        return ()
    # end def choices

    def get_raw (self, form, instance) :
        return self.attr_kind.get_raw (instance)
    # end def get_raw

    def __getattr__ (self, name) :
        return getattr (self.attr_kind, name)
    # end def __getattr__

# end class Field

if __name__ != "__main__" :
    GTW.Form.MOM._Export ("*")
### __END__ GTW.Form.MOM.Field
