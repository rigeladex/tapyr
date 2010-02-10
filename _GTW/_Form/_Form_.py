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
#     5-Feb-2010 (MG) `M_Form` added
#    10-Feb-2010 (MG) `prefix_sub` added
#    10-Feb-2010 (MG) `get_raw`: As soon as we have `request_data` use the
#                     values from there or empty string (empty strings are
#                     not part of the request data!)
#    ««revision-date»»···
#--

from   _TFL               import TFL
import _TFL.I18N
import _TFL._Meta.Object
import _TFL._Meta.Once_Property
import _TFL.defaultdict

from   _GTW              import GTW
import _GTW._Form.Field_Error

class M_Form (TFL.Meta.Object.__class__) :
    """Meta class for forms."""

    def _setup_fields (cls, field_groups) :
        result = TFL.NO_List ()
        for fg in (  fg for fg in field_groups
                  if isinstance (fg, GTW.Form.Field_Group)
                  ) :
            result.update (fg.fields)
        return result
    # end def _setup_fields

# end class M_Form

class _Form_ (TFL.Meta.Object) :
    """Base class for forms"""

    prefix        = ""
    __metaclass__ = M_Form
    instance      = None

    def __init__ (self, instance = None, prefix_sub = None) :
        if instance != None :
            self.instance        = instance
        self.errors              = GTW.Form.Error_List ()
        self.field_errors        = TFL.defaultdict     (GTW.Form.Error_List)
        self.prefix_sub          = prefix_sub
        if prefix_sub :
            self.prefix          = "%s%s" % (self.prefix , prefix_sub)
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
        if self.request_data :
            return self.request_data.get (html_name, u"")
        return field.get_raw (self, self.instance)
    # end def get_raw

# end class _Form_

if __name__ != "__main__" :
    GTW.Form._Export ("*")
### __END__ GTW.Form._Form_


