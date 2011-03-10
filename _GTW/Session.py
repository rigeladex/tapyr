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
#    ««revision-date»»···
#--

from   _GTW                     import GTW

from   _TFL                     import TFL
import _TFL._Meta.Object
import _TFL._Meta.M_Auto_Combine_Sets

import  base64
import  os
import  random
import  time
import  hashlib

### session key generation is based on the version found in Django
### (www.djangoproject.com)

MAX_SESSION_KEY = 18446744073709551616L     # 2 << 63
# Use the system (hardware-based) random number generator if it exists.
if hasattr(random, "SystemRandom") :
    randrange = random.SystemRandom ().randrange
else:
    randrange = random.randrange

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

    __metaclass__     = M_Session
    _data_dict        = None
    _non_data_attrs   = set (("sid", "_data", "_data_dict"))
    _sets_to_combine  = ("_non_data_attrs", )

    def __init__ (self, sid = None, salt = "_GTW.Session") :
        if sid is None :
            self._data = {}
            sid        = self._new_sid (salt or "")
        self.sid       = sid
    # end def __init__

    @property
    def _data (self) :
        if self._data_dict is None :
            self._data_dict = self._load ()
        return self._data_dict
    # end def _data

    @_data.setter
    def _data (self, value) :
        self._data_dict = value
    # end def _data

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

    def _new_sid (self, salt) :
        return self.New_ID (self.exists, salt)
    # end def _new_sid

    def exists (self, sid) :
        ### must be implemented by concrete backends
        return False
    # end def exists

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
            d = self.__dict__
        else :
            d = self._data
        d [name] = value
    # end def __setattr__

# end class Session

if __name__ != "__main__" :
    GTW._Export ("*")
### __END__ GTW.Session
