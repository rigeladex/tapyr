# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.Tornado.
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
#    GTW.Tornado.Session
#
# Purpose
#    Base class for sessions.
#
# Revision Dates
#    25-Jan-2010 (MG) Creation
#    ««revision-date»»···
#--

from   _GTW                     import GTW
import _GTW._Tornado

from   _TFL                     import TFL
import _TFL._Meta.Object

import  base64
import  os
import  random
import  time
import  hashlib

### session key generation is based on the version found in Django
### (www.djangoproject.com)

# Use the system (hardware-based) random number generator if it exists.
MAX_SESSION_KEY = 18446744073709551616L     # 2 << 63
if hasattr(random, "SystemRandom") :
    randrange = random.SystemRandom ().randrange
else:
    randrange = random.randrange

class Session (TFL.Meta.Object) :
    """Base class for sessions

       >>> from _GTW._Tornado.Session import *
       >>> session  = Session( None, "salt")
       >>> session2 = Session( None, "salt")
       >>> session.sid != session2.sid
       True
    """

    _data_dict = None

    def __init__ (self, sid = None, salt = "_GTW._Tornado") :
        if not sid :
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

    def _new_sid (self, salt) :
        try :
            pid = os.getpid ()
        except AttributeError :
            # No getpid() in Jython, for example
            pid = 1
        while True :
            sid = hashlib.md5 \
                ( "%s%s%s%s"
                % ( randrange (0, MAX_SESSION_KEY), pid, time.time(), salt)
                ).hexdigest ()
            if not self.exists (sid) :
                return sid
    # end def _new_sid

    def exists (self, sid) :
        ### must be implemented by concrete backends
        return False
    # end def exists

    ### dict interface
    def get (self, key, default = None) :
        return self._data.get (key, default)
    # end def get

    def __getitem__ (self, key) :
        return self._data [key]
    # end def __getitem__

    def __setitem__ (self, key, value) :
        self._data [key] = value
    # end def __setitem__

    def __delitem__ (self, key) :
        self._data.pop (key, None)
    # end def __delitem__

    ### allow attribute like access
    def __getattr__ (self, name) :
        return self.get (name)
    # end def __getattr__

    def __delattr__ (self, name) :
        del self [name]
    # end def

# end class Session

if __name__ != "__main__" :
    GTW.Tornado._Export ("*")
### __END__ GTW.Tornado.Session
