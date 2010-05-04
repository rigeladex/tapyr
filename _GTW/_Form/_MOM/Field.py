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
#    25-Feb-2010 (CT) Factored from GTW.Form.MOM.Instance and
#                     GTW.Form.MOM.Field_Group_Description
#    25-Feb-2010 (CT) `css_class` added
#    26-Feb-2010 (MG) `get_cooked` added
#    10-Mar-2010 (CT) s/named_object/named_value/
#     3-May-2010 (MG) New form handling implemented
#    ««revision-date»»···
#--

from   _GTW               import GTW
from   _MOM               import MOM
from   _TFL               import TFL

import _GTW._Form._MOM

import _GTW._Form.Field
from   _GTW._Form.Widget_Spec import Widget_Spec as WS

import _MOM._Attr.Kind
import _MOM._Attr.Type
import _MOM.Error

import _TFL._Meta.Object
import _TFL.Decorator
import _TFL.Ival_Map

MAT                            = MOM.Attr
MAT.A_Attr_Type.widget         = WS ("html/field.jnj, string")
MAT._A_Number_.widget          = WS ("html/field.jnj, number")
MAT.A_Boolean.widget           = WS ("html/field.jnj, boolean")
MAT.A_Date.widget              = WS ("html/field.jnj, date")
MAT.A_Date_Time.widget         = WS ("html/field.jnj, datetime")
MAT.A_Email.widget             = WS ("html/field.jnj, email")
MAT.A_Text.widget              = WS ("html/field.jnj, text")
MAT._A_Named_Value_.widget     = WS ("html/field.jnj, named_value")

MAT.Kind.css_class             = ""
MAT.Primary.css_class          = "Mandatory"
MAT.Primary_Optional.css_class = "Optional"
MAT.Mandatory.css_class        = "Mandatory"
MAT.Required.css_class         = "Required"
MAT.Optional.css_class         = "Optional"

MER                            = MOM.Error
MER.Invalid_Attribute.widget   = WS ("html/mom_errors.jnj, invalide_attribute")

_css_len_classes = TFL.Ival_Map \
    ( (    7, "Short")
    , (   13, "Moderate-Len")
    , (   21, "Medium-Len")
    , (   61, "")
    , (   81, "Long")
    , (2**31, "Very-Long")
    )

@TFL.Add_Method (MAT.A_Attr_Type, decorator = property)
def css_class_len (self) :
    return _css_len_classes [self.ui_length]
# end def css_class_len

class Field (GTW.Form._Field_) :
    """A wrapper around the attribute of the MOM object used in field groups"""

    hidden = False

    def __init__ (self, et_man, attr_name, default = u"") :
        self.html_name      = attr_name
        if "." in attr_name :
            scope           = et_man.home_scope
            role, attr_name = attr_name.split (".")
            et_man          = getattr \
                (scope, getattr (et_man, role).role_type.type_name)
        self.__super.__init__ (attr_name, default)
        self.et_man         = et_man
        self.attr_kind      = getattr (et_man._etype, attr_name)
    # end def __init__

    def choices (self, form) :
        attr = self.attr_kind.attr
        if isinstance (attr, MOM.Attr._A_Named_Value_) :
            return sorted (attr.Table)
        return ()
    # end def choices

    @property
    def css_class (self) :
        ak     = self.attr_kind
        result = " ".join (c for c in (ak.css_class, ak.css_class_len) if c)
        return result
    # end def css_class

    def get_cooked (self, form) :
        return getattr (form.instance, self.attr_kind.ckd_name, None)
    # end def get_cooked

    def get_raw (self, form, defaults) :
        raw_value = self.attr_kind.get_raw (form.instance)
        if not raw_value :
            raw_value = self.default (form, defaults)
        return raw_value
    # end def get_raw

    def __getattr__ (self, name) :
        return getattr (self.attr_kind, name)
    # end def __getattr__

    def __repr__ (self) :
        return "<%s for %s.%s>" \
            % ( self.__class__.__name__
              , self.et_man.type_name
              , self.attr_kind.name
              )
    # end def __repr__

# end class Field

if __name__ != "__main__" :
    GTW.Form.MOM._Export ("*")
### __END__ GTW.Form.MOM.Field
