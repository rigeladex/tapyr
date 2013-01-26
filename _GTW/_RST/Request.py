# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012-2013 Mag. Christian Tanzer All rights reserved
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
#    17-Jul-2012 (CT) Add property `user`
#    24-Jul-2012 (CT) Add `use_language`
#     6-Aug-2012 (CT) Add attribute `lang`
#     2-Oct-2012 (CT) Add property `brief`
#    16-Oct-2012 (CT) Add properties `ckd` and `raw`
#    16-Jan-2013 (CT) Add `ssl_authorized_user` and `ssl_client_verified`
#    26-Jan-2013 (CT) Add and use `http_server_authorized_user`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._RST

from   _TFL                     import I18N
from   _TFL._Meta.Once_Property import Once_Property

import _TFL._Meta.Object

class _RST_Request_ (TFL.Meta.Object) :
    """Wrap and extend wsgi-specific Request class."""

    _real_name = "Request"
    _user      = None

    lang              = None
    original_resource = None

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
    def brief (self) :
        return self.req_data.has_option ("brief")
    # end def brief

    @Once_Property
    def ckd (self) :
        req_data = self.req_data
        if "ckd" in req_data :
            return req_data.has_option ("ckd")
        elif self.method == "GET" :
            ### for `GET`, `ckd` is default
            return not req_data.has_option ("raw")
    # end def ckd

    @Once_Property
    def http_server_authorized_user (self) :
        result = self.ssl_authorized_user
        if result is None :
            result = self.environ.get ("REMOTE_USER")
        return result
    # end def http_server_authorized_user

    @Once_Property
    def locale_codes (self) :
        """The locale-code for the current session."""
        return self.get_browser_locale_codes ()
    # end def locale_codes

    @Once_Property
    def raw (self) :
        req_data = self.req_data
        if "raw" in req_data :
            return req_data.has_option ("raw")
        elif self.method != "GET" :
            ### for all methods but `GET`, `raw` is default
            return not req_data.has_option ("ckd")
    # end def raw

    @property
    def settings (self) :
        return self.root._kw
    # end def settings

    @Once_Property
    def ssl_authorized_user (self) :
        return self.environ.get ("SSL_CLIENT_S_DN_Email")
    # end def ssl_authorized_user

    @Once_Property
    def ssl_client_verified (self) :
        return self.environ.get ("SSL_CLIENT_VERIFY") == "SUCCESS"
    # end def ssl_client_verified

    @property
    def user (self) :
        result = self._user
        if result is None and self.username :
            self._user = self.root._get_user (self.username)
        return self._user
    # end def user

    @user.setter
    def user (self, value) :
        self._user = value
    # end def user

    @Once_Property
    def username (self) :
        result = self.http_server_authorized_user
        if result is None :
            auth   = self.authorization
            result = auth and auth.username
        return result
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

    def use_language (self, langs) :
        self.lang = langs
        I18N.use (* langs)
    # end def use_language

Request = _RST_Request_ # end class

if __name__ != "__main__" :
    GTW.RST._Export ("Request")
### __END__ GTW.RST.Request
