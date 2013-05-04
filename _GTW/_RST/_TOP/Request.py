# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012-2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.RST.TOP.
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
#    GTW.RST.TOP.Request
#
# Purpose
#    Extend GTW.RST.Request with session handling
#
# Revision Dates
#    20-Jun-2012 (CT) Creation
#    16-Jul-2012 (CT) Pass `bytes ("~@")` to `b64decode`
#    24-Jul-2012 (CT) Fix `locale_codes`
#    24-Jul-2012 (CT) Add `use_language`
#     4-Aug-2012 (MG) Don't save session on language change
#     4-Aug-2012 (MG) Allow setting of `username`
#    16-Jan-2013 (CT) Consider `ssl_authorized_user` in `username` methods
#     2-May-2013 (CT) Factor `cookie_encoding`, `cookie`, `secure_cookie`,
#                     `_cookie_signature`, to `GTW.RST.Request`
#     4-May-2013 (CT) Change `username` to use `__super.username`
#     4-May-2013 (CT) Redefine `apache_authorized_user` to disable it
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

from   _TFL._Meta.Once_Property import Once_Property

import _GTW.File_Session
import _GTW._RST._TOP
import _GTW._RST.Request

class _RST_TOP_Request_ (GTW.RST.Request) :
    """Extend GTW.RST.Request with session handling."""

    _real_name        = "Request"

    @Once_Property
    def apache_authorized_user (self) :
        ### Don't want to support this in TOP context
        pass
    # end def apache_authorized_user

    @Once_Property
    def locale_codes (self) :
        """The locale-code for the current session."""
        codes = self.get_user_locale_codes ()
        if not codes :
            codes = self.__super.locale_codes
        return codes
    # end def locale_codes

    @Once_Property
    def session (self) :
        cookie_name = self.session_cookie_name
        S_Class     = self.settings.get  ("Session_Class", GTW.File_Session)
        sid         = self.secure_cookie (cookie_name)
        session     = S_Class (sid, self.settings, self._session_hasher)
        return session
    # end def session

    @Once_Property
    def session_cookie_name (self) :
        return self.settings.get ("session_id",  "SESSION_ID")
    # end def session_cookie_name

    @property
    def username (self) :
        result = self.__super.username
        if result is None :
            result = self.session.username
        return result
    # end def username

    @username.setter
    def username (self, value) :
        sau = self.ssl_authorized_user
        if sau :
            raise TypeError \
                ( "Can't set username of ssl-authorized session from %s to %s"
                % (sau, value)
                )
        self.session.username = value
    # end def username

    def get_user_locale_codes (self) :
        supported = getattr (self.root, "languages", set ())
        result    = tuple \
            (l for l in self.session.get ("language", ()) if l in supported)
        return result
    # end def get_user_locale_codes

    def use_language (self, langs) :
        self.__super.use_language (langs)
        self.session ["language"] = langs
    # end def use_language

    def _session_hash (self, sig) :
        root   = self.root
        hash   = root.hash_fct     (str (sig)).digest ()
        result = root.b64_encoded  (hash, altchars = "~@")
        return result
    # end def _session_hash

    def _session_hasher (self, username) :
        return self._session_hash (self._session_sig (username))
    # end def _session_hash

    def _session_sig (self, user) :
        root  = self.root
        scope = root.scope
        if isinstance (user, basestring) :
            user = root._get_user (user)
        return \
            ( getattr (user, "password", user)
            , scope.db_meta_data.dbid
                  if scope is not None else self.settings ["cookie_salt"]
            )
    # end def _session_sig

Request = _RST_TOP_Request_ # end class

if __name__ != "__main__" :
    GTW.RST.TOP._Export ("Request")
### __END__ GTW.RST.TOP.Request
