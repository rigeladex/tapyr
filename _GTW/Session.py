# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010-2011 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.
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
#    GTW.Session
#
# Purpose
#    Base class for sessions.
#
# Revision Dates
#    25-Jan-2010 (MG) Creation
#    19-Feb-2010 (MG) Moved from `GTW.Tornado` into `GTW`
#    20-Feb-2010 (MG) `__contains__` added
#     5-Aug-2010 (MG) `New_ID` factored from `_new_sid`, `setdefault` added
#     8-Aug-2010 (MG) `setdefault` added
#    10-Mar-2011 (CT) `__setattr__` added
#    11-Mar-2011 (CT) `Login`, `expiry`, `hash`, and `username` added
#    ««revision-date»»···
#--

from   _GTW                     import GTW

from   _TFL                     import TFL
import _TFL._Meta.Object
import _TFL._Meta.M_Auto_Combine_Sets

import base64
import datetime
import hashlib
import os
import random
import time
import uuid

### session key generation is based on the version found in Django
### (www.djangoproject.com)

MAX_SESSION_KEY = 18446744073709551616L     # 2 << 63
# Use the system (hardware-based) random number generator if it exists.
if hasattr(random, "SystemRandom") :
    randrange = random.SystemRandom ().randrange
else:
    randrange = random.randrange

class Login (TFL.Meta.Object) :
    """Encapsulate login information for session."""

    expiry    = None
    hash      = None
    _username = None

    def __init__ (self) :
        self.username = None
    # end def __init__

    @property
    def username (self) :
        return self._username
    # end def username

    @username.setter
    def username (self, value) :
        if value is None or value != self._username :
            self._username = value
            self.sessions  = {}
    # end def username

    def __nonzero__ (self) :
        return self._username is not None
    # end def __nonzero__

# end class Login

class M_Session (TFL.Meta.M_Auto_Combine_Sets, TFL.Meta.Object.__class__) :
    """Meta class for Session."""

# end class M_Session

class Session (TFL.Meta.Object) :
    """Base class for sessions

       >>> from _GTW.Session import *
       >>> session  = Session( None, "salt")
       >>> session2 = Session( None, "salt")
       >>> session.sid != session2.sid
       True
    """

    __metaclass__      = M_Session
    _data_dict         = None
    _non_data_attrs    = set \
        (("_data", "_data_dict", "_hasher", "_sid", "_settings", "username"))
    _sets_to_combine   = ("_non_data_attrs", )

    def __init__ (self, sid = None, settings = {}, hasher = None) :
        self._settings = settings
        self._hasher   = hasher or (lambda x : x)
        if sid is None :
            self._sid     = self._new_sid (settings.get ("cookie_salt"))
            self._data    = dict (login = Login ())
            self.username = None
        else :
            self._sid     = sid
    # end def __init__

    @property
    def username (self) :
        return self.login.username
    # end def username

    @username.setter
    def username (self, value) :
        self._change_username (self.login, value)
    # end def username

    @property
    def _data (self) :
        loaded = False
        result = self._data_dict
        if result is None :
            result = self._data_dict = loaded = self._load ()
        login   = result ["login"]
        expired = \
            (  (login.hash != self._hasher (login.username))
            or self._expired (login.expiry)
            )
        if expired :
            self._change_username (login, None)
        elif loaded :
            for id in list (login.sessions) :
                try :
                    self.edit_session (id)
                except LookupError :
                    pass
        return result
    # end def _data

    @_data.setter
    def _data (self, value) :
        self._data_dict = value
    # end def _data

    @property
    def sid (self) :
        return self._sid
    # end def sid

    @classmethod
    def New_ID (cls, check = None, salt = "") :
        try :
            pid = os.getpid ()
        except AttributeError :
            # No getpid() in Jython, for example
            pid = 1
        while True :
            id = hashlib.md5 \
                ( "%s%s%s%s"
                % ( randrange (0, MAX_SESSION_KEY), pid, time.time (), salt)
                ).hexdigest ()
            if check is None or not check (id) :
                return id
    # end def New_ID

    def edit_session (self, id) :
        login = self.login
        expiry, hash = login.sessions [id]
        if self._expired (expiry) :
            login.sessions.pop (id, None)
            raise LookupError \
                ( "Edit session expired since %s"
                % (expiry.strftime ("%Y/%m/%d %H:%M"), )
                )
        return hash
    # end def edit_session

    def exists (self, sid) :
        ### must be implemented by concrete backends
        return False
    # end def exists

    def new_edit_session (self, hash_sig, ttl = None) :
        assert self.login
        expiry = self._expiry (ttl, "edit_session_ttl")
        id     = uuid.uuid4 ().hex
        hash   = base64.b64encode \
            (hashlib.sha224 (str ((hash_sig, expiry))).digest ())
        self.login.sessions [id] = (expiry, hash)
        return id, hash
    # end def new_edit_session

    def pop_edit_session (self, id) :
        result = self.edit_session (id)
        if result is not None :
            self.login.sessions.pop (id, None)
        return result
    # end def pop_edit_session

    def _new_sid (self, salt) :
        return self.New_ID (self.exists, salt)
    # end def _new_sid

    def _change_username (self, login, value) :
        login.username = value
        login.hash     = self._hasher (value)
        login.expiry   = None if value is None else self._expiry ()
    # end def _change_username

    def _expired (self, expiry) :
        if expiry :
            return datetime.datetime.utcnow () > expiry
    # end def _expired

    def _expiry (self, ttl = None, ttl_name = "user_session_ttl") :
        if ttl is None :
            ttl = self._settings.get (ttl_name, 3600)
        if not isinstance (ttl, datetime.timedelta) :
            ttl  = datetime.timedelta (seconds = ttl)
        return datetime.datetime.utcnow () + ttl
    # end def _expiry

    ### dict interface
    def get (self, key, default = None) :
        return self._data.get (key, default)
    # end def get

    def pop (self, name, default = None) :
        return self._data.pop (name, default)
    # end def pop

    def setdefault (self, key, default = None) :
        if key not in self._data :
            self._data [key] = default
        return self._data [key]
    # end def setdefault

    def __contains__ (self, item) :
        return item in self._data
    # end def __contains__

    def __delitem__ (self, key) :
        self._data.pop (key, None)
    # end def __delitem__

    def __getitem__ (self, key) :
        return self._data [key]
    # end def __getitem__

    def __setitem__ (self, key, value) :
        self._data [key] = value
    # end def __setitem__

    ### allow attribute like access
    def __delattr__ (self, name) :
        del self [name]
    # end def

    def __getattr__ (self, name) :
        return self.get (name)
    # end def __getattr__

    def __setattr__ (self, name, value) :
        if name in self._non_data_attrs :
            return self.__super.__setattr__ (name, value)
        else :
            self._data [name] = value
            return value
    # end def __setattr__

# end class Session

if __name__ != "__main__" :
    GTW._Export ("Session")
### __END__ GTW.Session
