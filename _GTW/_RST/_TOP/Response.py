# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
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
#    GTW.RST.TOP.Response
#
# Purpose
#    Extend GTW.RST.Response with session handling
#
# Revision Dates
#    20-Jun-2012 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

from   _TFL._Meta.Once_Property import Once_Property

import _GTW._RST._TOP
import _GTW._RST.Response

import base64
import time

class _RST_TOP_Response_ (GTW.RST.Response) :
    """Extend GTW.RST.Response with session handling."""

    @Once_Property
    def session (self) :
        return self._request.session
    # end def session

    @property
    def username (self) :
        return self.session.username
    # end def username

    @username.setter
    def username (self, value) :
        if value != self.username :
            self.session.username = value
            self._set_session_cookie (self.session.renew_session_id ())
    # end def username

    def add_notification (self, noti) :
        notifications = self.session.notifications
        if notifications is not None :
            if not isinstance (noti, GTW.Notification) :
                noti = GTW.Notification (noti)
            notifications.append (noti)
    # end def add_notification

    def clear_cookie (self, name, * args, ** kw) :
        self._response.delete_cookie (name, * args, ** kw)
    # end def clear_cookie

    def set_cookie (self, key, value = "", ** kw) :
        if isinstance (value, unicode) :
            value = value.encode (self._request.cookie_encoding)
        return self._response.set_cookie (key, value, ** kw)
    # end def set_cookie

    def set_secure_cookie (self, name, data, ** kw) :
        requ      = self._request
        timestamp = str (int (time.time ()))
        if isinstance (data, unicode) :
            data  = data.encode (requ.cookie_encoding)
        data      = base64.b64encode       (data)
        signature = requ._cookie_signature (data, timestamp)
        cookie    = "|".join               ((data, timestamp, signature))
        self.set_cookie (name, cookie, ** kw)
    # end def set_secure_cookie

    def _set_session_cookie (self, session) :
        requ        = self._request
        cookie_name = requ.session_cookie_name
        self.set_secure_cookie \
            (cookie_name, session.sid, max_age = requ.user_session_ttl)
        GTW.Notification_Collection (session)
    # end def _set_session_cookie

Response = _RST_TOP_Response_ # end class

if __name__ != "__main__" :
    GTW.RST.TOP._Export ("Response")
### __END__ GTW.RST.TOP.Response
