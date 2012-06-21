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
#    GTW.Werkzeug.Response
#
# Purpose
#    Extend werkzeug's Response class
#
# Revision Dates
#    20-Jun-2012 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW                       import GTW
from   _TFL                       import TFL

import _GTW._Werkzeug

from   _TFL._Meta.Once_Property   import Once_Property

import _TFL._Meta.M_Class

from    werkzeug.wrappers             import Response
from    werkzeug.contrib.wrappers     import DynamicCharsetResponseMixin

class _WZG_Response_ (DynamicCharsetResponseMixin, Response) :
    """Extend werkzeug's Response class."""

    __metaclass__        = TFL.Meta.M_Class
    _real_name           = "Response"

    default_charset      = "utf-8"

    def clear (self) :
        self.headers.clear ()
        self.response = []
        self.status   = self.default_status
    # end def clear

    def write (self, data) :
        self.response.append (data)
    # end def write

    def write_json (self, __data = None, ** kw) :
        data = dict (kw)
        if __data is not None :
            data.update (__data)
        self.set_header ("Content-Type", "text/javascript; charset=UTF-8")
        self.write      (json.dumps (data))
    # end def write_json

Response = _WZG_Response_ # end class

if __name__ != "__main__" :
    GTW.Werkzeug._Export ("Response")
### __END__ GTW.Werkzeug.Response
