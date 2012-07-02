# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.RST.
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
#    GTW.RST.Request
#
# Purpose
#    Wrap and extend wsgi-specific Request class
#
# Revision Dates
#    19-Jun-2012 (CT) Creation
#    28-Jun-2012 (CT) Add `verbose`
#     2-Jul-2012 (CT) Factor `has_option` to `GTW.Request_Data`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._RST

from   _TFL._Meta.Once_Property import Once_Property

import _TFL._Meta.Object

class _RST_Request_ (TFL.Meta.Object) :
    """Wrap and extend wsgi-specific Request class."""

    _real_name = "Request"

    def __init__ (self, root, environ) :
        self.root     = root
        self._request = root.HTTP.Request (environ)
    # end def __init__

    def __getattr__ (self, name) :
        if name == "request" : ### XXX remove after porting of GTW.Werkzeug.Error
            return self._request
        elif name != "_request" :
            result = getattr (self._request, name)
            setattr (self, name, result)
            return result
        raise AttributeError (name)
    # end def __getattr__

    @Once_Property
    def locale_codes (self) :
        """The locale-code for the current session."""
        return self.get_browser_locale_codes ()
    # end def locale_codes

    @property
    def settings (self) :
        return self.root._kw
    # end def settings

    @Once_Property
    def username (self) :
        auth = self.authorization
        return auth and auth.username
    # end def username

    @Once_Property
    def verbose (self) :
        return self.req_data.has_option ("verbose")
    # end def verbose

    def get_browser_locale_codes (self) :
        """Determines the user's locale from Accept-Language header."""
        languages = self.accept_languages
        supported = getattr (self.root, "languages", set ())
        if supported :
            locales   = list (l for l, p in languages if l in supported)
            if locales :
                return locales
        return getattr (self.root, "default_locale_code", "en")
    # end def get_browser_locale_codes

Request = _RST_Request_ # end class

if __name__ != "__main__" :
    GTW.RST._Export ("Request")
### __END__ GTW.RST.Request
