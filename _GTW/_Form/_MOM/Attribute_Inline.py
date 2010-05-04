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
#    GTW.Form.MOM.Attribute_Inline
#
# Purpose
#    Handle the creation/modification of an object inside of a other form.
#    The attribute inline will be treated like a `Field` of a form and not
#    like a inline group
#
# Revision Dates
#    15-Apr-2010 (MG) Creation
#    ««revision-date»»···
#--

from   _TFL                                 import TFL
import _TFL._Meta.Once_Property
from   _TFL.predicate                       import all_true
from   _GTW                                 import GTW
import _GTW._Form.Field
import _GTW._Form.Widget_Spec
import _GTW._Form._MOM
import _GTW._Form._MOM.Inline_Instance

class _Attribute_Inline_ (TFL.Meta.Object) :
    """The `field` instance for attribute inline editing."""

    electric = False

    def __init__ (self, name, form_cls, form = None) :
        self.name      = self.html_name = name
        self.form_cls  = form_cls
        self.form      = form
    # end def __init__

    def create_object (self, form) :
        self.form.create_object (form)
        ec = self.form.error_count
        if not ec :
            ### the instance has been created/updaed successfully -> update
            ### the raw_attr_dict of the parent
            form.raw_attr_dict [self.name] = self.form.get_object_raw (form)
        if ec or not self.form.instance :
            ### an error was detected or the instance has not been created ->
            ### delete the values for this attribute from parent's raw_attr_dict
            form.raw_attr_dict.pop (self.name, None)
        form.inline_errors += ec
    # end def create_object

    def clone (self, form) :
        instance = getattr (form.instance, self.name, None)
        return self.__class__ \
            (self.name, self.form_cls, self.form_cls (instance))
    # end def clone

    def get_raw (self, form, defaults) :
        return self.form.get_object_raw (defaults)
    # end def get_raw

    def prepare_request_data (self, form, request_data) :
        self.form.request_data = request_data
    # end def prepare_request_data

    def setup_raw_attr_dict (self, form) :
        self.form.setup_raw_attr_dict (form)
    # end def setup_raw_attr_dict

    def update_object (self, form) :
        pass
    # end def setup_raw_attr_dict

    def update_raw_attr_dict (self, form) :
        pass
    # end def setup_raw_attr_dict

# end class _Attribute_Inline_

class An_Attribute_Inline (_Attribute_Inline_) :
    """Inline of an An_Entity."""


    Form_Class = GTW.Form.MOM.An_Attribute_Inline_Instance

# end class An_Attribute_Inline

class Id_Attribute_Inline (_Attribute_Inline_) :
    """Inline for a ID_Entity."""

    Form_Class = GTW.Form.MOM.Id_Attribute_Inline_Instance

# end class Id_Attribute_Inline

if __name__ != "__main__" :
    GTW.Form.MOM._Export ("*", "_Attribute_Inline_")
### __END__ GTW.Form.MOM.Attribute_Inline
