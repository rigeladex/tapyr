# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.Form.
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
#    GTW.Form._Form_
#
# Purpose
#    Base class for forms
#
# Revision Dates
#    19-Jan-2010 (MG) Creation
#    20-Jan-2010 (MG) `get_id` allow string as parameter as well
#    ««revision-date»»···
#--

from   _TFL               import TFL
import _TFL.I18N
import _TFL._Meta.Object
import _TFL._Meta.Once_Property
import _TFL.defaultdict

from   _GTW              import GTW
import _GTW._Form.Field_Error

class _Form_ (TFL.Meta.Object) :
    """Base class for forms"""

    prefix        = None
    hidden_fields = ()

    def __init__ (self, instance = None) :
        self.instance = instance
        self.errors              = GTW.Form.Error_List ()
        self.field_errors        = TFL.defaultdict     (GTW.Form.Error_List)
        self.request_data        = {}
    # end def __init__

    def get_errors (self, field = None) :
        if field :
            field = getattr (field, "html_name", field)
            return self.field_errors [field]
        return self.errors
    # end def get_errors

    def get_id (self, field) :
        if isinstance (field, basestring) :
            field = self.fields [field]
        if self.prefix :
            return "-".join ((self.prefix, field.html_name))
        return field.html_name
    # end def get_id

    def get_raw (self, field) :
        if isinstance (field, basestring) :
            field = self.fields [field]
        html_name = self.get_id (field)
        if html_name in self.request_data :
            value = self.request_data [html_name]
            return value
        return self._get_raw (field)
    # end def get_raw

    @TFL.Meta.Once_Property
    def fields (self) :
        result = {}
        for fg in (  fg for fg in self.field_groups
                  if isinstance (fg, GTW.Form.Field_Group)
                  ) :
            result.update (fg.fields)
        return result
    # end def fields

# end class _Form_

if __name__ != "__main__" :
    GTW.Form._Export ("*")
### __END__ GTW.Form._Form_


