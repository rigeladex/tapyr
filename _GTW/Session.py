# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2013 Martin Glueck All rights reserved
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
#     2-May-2011 (CT) `edit_session` and `new_edit_session` changed to
#                     support `hard_expiry` and `soft_expiry`
#    11-May-2011 (MG) `Session.__init__`: create new sid of passed `sid` does
#                     not exists
#                     `renew_session_id` added
#    11-May-2011 (MG) Alphabatically sorted
#     5-Apr-2012 (CT) Sort alphabetically, `_...` at end,
#                     properties right after `__init__`
#     5-Apr-2012 (CT) Add stubs for `remove` and `save`
#     5-Apr-2012 (CT) Rename `Login` to `User`
#    26-Apr-2012 (CT) Change `_date` to create `User()` if `._load` returns `{}`
#    23-Jul-2012 (CT) Call `renew_session_id` in `username.setter`
#     4-Aug-2012 (MG) Don't save session on session id renewal
#    19-Aug-2012 (MG) Add repr for User class
#     2-May-2013 (CT) Convert `New_ID` to instance method,
#                     use `settings ["hash_fct"]`, if any
#     5-May-2013 (CT) Add change guard to `username.setter`
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

MAX_SESSION_KEY = 340282366920938463463374607431768211456L     # 2 ** 128
# Use the system (hardware-based) random number generator if it exists.
if hasattr(random, "SystemRandom") :
    randrange = random.SystemRandom ().randrange
else:
    randrange = random.randrange

class User (TFL.Meta.Object) :
    """Encapsulate user information for session."""

    expiry = None
    hash   = None
    _name  = None

    def __init__ (self) :
        self.name = None
    # end def __init__

    @property
    def name (self) :
        return self._name
    # end def name

    @name.setter
    def name (self, value) :
        if value is None or value != self._name :
            self._name    = value
            self.sessions = {}
    # end def name

    def __nonzero__ (self) :
        return self._name is not None
    # end def __nonzero__

    def __repr__ (self) :
        return "GTW.Session.User (%s)" % self._name
    # end def __repr__

# end class User

class M_Session (TFL.Meta.M_Auto_Combine_Sets, TFL.Meta.Object.__class__) :
    """Meta class for Session."""

# end class M_Session

class Session (TFL.Meta.Object) :
    """Base class for sessions

       >>> from _GTW.Memory_Session import Memory_Session
       >>> session  = Memory_Session (None, dict (cookie_salt = "salt"))
       >>> session2 = Memory_Session (None, dict (cookie_salt = "salt"))
       >>> session.sid != session2.sid
       True
    """

    __metaclass__      = M_Session

    _data_dict         = None
    _non_data_attrs    = set \
        (("_data", "_data_dict", "_hasher", "_sid", "_settings", "username"))
    _sets_to_combine   = ("_non_data_attrs", )

    class Expired (LookupError) :
        pass
    # end class Expired

    def __init__ (self, sid = None, settings = {}, hasher = None) :
        self._settings = settings
        self._hasher   = hasher or (lambda x : x)
        if sid is None or not self.exists (sid) :
            self._sid     = self._new_sid (settings.get ("cookie_salt"))
            self._data    = dict (user = User ())
            self.username = None
        else :
            self._sid     = sid
    # end def __init__

    @property
    def sid (self) :
        return self._sid
    # end def sid

    @property
    def username (self) :
        return self.user.name
    # end def username

    @username.setter
    def username (self, value) :
        if self.user.name != value :
            self._change_user     (self.user, value)
            self.renew_session_id ()
    # end def username

    @property
    def _data (self) :
        loaded = False
        result = self._data_dict
        if result is None :
            result = self._data_dict = loaded = self._load ()
        user   = result.get ("user")
        if user is None :
            user = result ["user"] = User ()
        expired = \
            (  (user.hash != self._hasher (user.name))
            or self._expired (user.expiry)
            )
        if expired :
            self._change_user (user, None)
        elif loaded :
            for id in list (user.sessions) :
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

    def edit_session (self, id) :
        user = self.user
        data = user.sessions [id]
        if len (data) == 2 :
            hard_expiry, soft_expiry, hash = data [0], None, data [1]
        else :
            hard_expiry, soft_expiry, hash = data
        if self._expired (hard_expiry) :
            user.sessions.pop (id, None)
            raise LookupError \
                ( "Edit session expired since %s"
                % (hard_expiry.strftime ("%Y/%m/%d %H:%M"), )
                )
        if soft_expiry and self._expired (soft_expiry) :
            raise self.Expired \
                ( "Edit session expired since %s"
                % (soft_expiry.strftime ("%Y/%m/%d %H:%M"), )
                )
        return hash
    # end def edit_session

    def exists (self, sid) :
        raise NotImplementedError \
            ("%s must implement `exists`" % (self.__class__, ))
    # end def exists

    def get (self, key, default = None) :
        return self._data.get (key, default)
    # end def get

    def new_edit_session (self, hash_sig, ttl = None) :
        assert self.user
        hard_expiry = self._expiry (ttl, "user_session_ttl")
        soft_expiry = self._expiry (ttl, "edit_session_ttl")
        hash_fct    = self._settings.get ("hash_fct", hashlib.sha224)
        id     = uuid.uuid4 ().hex
        hash   = base64.b64encode \
            (hash_fct (str ((hash_sig, hard_expiry, soft_expiry))).digest ())
        self.user.sessions [id] = (hard_expiry, soft_expiry, hash)
        return id, hash
    # end def new_edit_session

    def New_ID (self, check = None, salt = "") :
        try :
            getpid = os.getpid
        except AttributeError :
            pid = 1
        else :
            pid = getpid ()
        hash_fct = self._settings.get ("hash_fct", hashlib.sha224)
        while True :
            id = hash_fct \
                ( "%s%s%s%s"
                % ( randrange (0, MAX_SESSION_KEY), pid, time.time (), salt)
                ).hexdigest ()
            if check is None or not check (id) :
                return id
    # end def New_ID

    def pop (self, name, default = None) :
        return self._data.pop (name, default)
    # end def pop

    def pop_edit_session (self, id) :
        return self.user.sessions.pop (id, (None, )) [-1]
    # end def pop_edit_session

    def remove (self) :
        raise NotImplementedError \
            ("%s must implement `remove`" % (self.__class__, ))
    # end def remove

    def renew_session_id (self, n_sid = None) :
        n_sid     = n_sid or self._new_sid (self._settings.get ("cookie_salt"))
        o_sid     = self._sid
        self._sid = n_sid
        try :
            with self.LET (_sid = o_sid) :
                self.remove ()
        except :
            pass
        return self
    # end def renew_session_id

    def save (self) :
        raise NotImplementedError \
            ("%s must implement `save`" % (self.__class__, ))
    # end def save

    def setdefault (self, key, default = None) :
        if key not in self._data :
            self._data [key] = default
        return self._data [key]
    # end def setdefault

    def _change_user (self, user, value) :
        user.name   = value
        user.hash   = self._hasher (value)
        user.expiry = None if value is None else self._expiry ()
    # end def _change_user

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

    def _new_sid (self, salt) :
        return self.New_ID (self.exists, salt)
    # end def _new_sid

    def __contains__ (self, item) :
        return item in self._data
    # end def __contains__

    def __delattr__ (self, name) :
        del self [name]
    # end def

    def __delitem__ (self, key) :
        self._data.pop (key, None)
    # end def __delitem__

    def __getattr__ (self, name) :
        return self.get (name)
    # end def __getattr__

    def __getitem__ (self, key) :
        return self._data [key]
    # end def __getitem__

    def __setattr__ (self, name, value) :
        if name in self._non_data_attrs :
            return self.__super.__setattr__ (name, value)
        else :
            self._data [name] = value
            return value
    # end def __setattr__

    def __setitem__ (self, key, value) :
        self._data [key] = value
    # end def __setitem__

# end class Session

if __name__ != "__main__" :
    GTW._Export ("Session")
### __END__ GTW.Session
