# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.Werkzeug.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.Werkzeug.Request
#
# Purpose
#    Extend werkzeug's Request class
#
# Revision Dates
#    19-Jun-2012 (CT) Creation
#    29-Jun-2012 (CT) Redefine `json` to add exception handler
#     2-Jul-2012 (CT) Add `has_option`
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _GTW                       import GTW
from   _TFL                       import TFL

import _GTW.Request_Data
import _GTW._Werkzeug

from   _TFL._Meta.Once_Property   import Once_Property

import _TFL._Meta.M_Class

from   werkzeug.contrib.wrappers     import \
           JSONRequestMixin, DynamicCharsetRequestMixin
from   werkzeug.security             import safe_str_cmp
from   werkzeug.wrappers             import Request

import json

class _WZG_Request_ (DynamicCharsetRequestMixin, JSONRequestMixin, Request) :
    """Extend werkzeug's Request class."""

    __metaclass__        = TFL.Meta.M_Class
    _real_name           = "Request"

    url_charset          = "utf-8"

    max_content_length   = 1024 * 1024 * 4
    max_form_memory_size = 1024 * 1024 * 2

    @Once_Property
    def body (self) :
        return self.data
    # end def body

    @Once_Property
    def path_x (self) :
        query  = self.query_string
        result = self.path
        if query :
            result = "%s?%s" % (result, query)
        return result
    # end def path_x

    @property
    def json (self) :
        try :
            return self.__super.json
        except Exception as exc :
            return {}
    # end def json

    @Once_Property
    def req_data (self) :
        result = GTW.Request_Data (self.values)
        result.files = self.files
        return result
    # end def req_data

    @Once_Property
    def req_data_list (self) :
        result = GTW.Request_Data_List (self.values)
        result.files = self.files
        return result
    # end def req_data_list

    def has_option (self, key) :
        return self.req_data.has_option (key)
    # end def get

Request = _WZG_Request_ # end class

if __name__ != "__main__" :
    GTW.Werkzeug._Export ("Request", "safe_str_cmp")
### __END__ GTW.Werkzeug.Request
