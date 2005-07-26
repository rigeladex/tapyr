# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.cluster
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
#++
# Name
#    PMA._Status_
#
# Purpose
#    Root class for various status encapsulators
#
# Revision Dates
#    25-Jul-2005 (CT) Creation (factored from `Msg_Status`)
#    26-Jul-2005 (CT) `__setattr__` fixed to handle `property` properly
#    26-Jul-2005 (CT) `load` and `save` moved back to `Msg_Status`
#    26-Jul-2005 (CT) `_ini_attr` added
#    26-Jul-2005 (CT) `_Status_C_` and `_Status_I_` factored
#    ««revision-date»»···
#--

from   _TFL                    import TFL
from   _PMA                    import PMA
import _TFL._Meta.Object

import cPickle                 as     pickle

class _Status_ (TFL.Meta.Object) :

    def __init__ (self, ** attr) :
        self._ini_attr (** attr)
    # end def __init__

    def _ini_attr (self, ** attr) :
        self.__dict__ ["_attr"] = dict (** attr)
    # end def _ini_attr

    def _set_attr (self, ** attr) :
        self.__dict__ ["_attr"].update (attr)
    # end def _set_attr

    def __contains__ (self, item) :
        return item in self._attr
    # end def __contains__

    def __delattr__ (self, name) :
        try :
            del self._attr [name]
        except KeyError :
            raise AttributeError, name
    # end def __delattr__

    def __getattr__ (self, name) :
        try :
            return self._attr [name]
        except KeyError :
            raise AttributeError, name
    # end def __getattr__

    def __getstate__ (self) :
        return self._attr
    # end def __getstate__

    def __nonzero__ (self) :
        return bool (self._attr)
    # end def __nonzero__

    def __setattr__ (self, name, value) :
        p = self.__class__.__dict__.get (name, None)
        if p is None :
            self._set_attr (** {name : value})
        elif isinstance (p, property) :
            p.__set__ (self, value)
        else :
            raise AttributeError, \
                "can't set attribute %s to %s" % (name, value)
    # end def __setattr__

    def __setstate__ (self, attr) :
        self.__dict__ ["_attr"] = attr
    # end def __setstate__

# end class _Status_

class _Status_C_ (_Status_) :

    @classmethod
    def load (cls, filename) :
        try :
            f = open (filename)
        except IOError :
            pass
        else :
            try :
                try :
                    cls._Table = pickle.load (f)
                except EOFError :
                    pass
            finally :
                f.close ()
    # end def load

    @classmethod
    def new (cls, name) :
        result = cls._Table.get (name)
        if result is None :
            result = cls._Table [name] = cls ()
        return result
    # end def new

    @classmethod
    def save (cls, filename) :
        f = open    (filename, "wb")
        pickle.dump (cls._Table, f, pickle.HIGHEST_PROTOCOL)
        f.close     ()
    # end def save

# end class _Status_C_

class _Status_I_ (_Status_) :

    def load (self, filename) :
        try :
            f = open (filename)
        except IOError :
            pass
        else :
            try :
                try :
                    attrs = pickle.load (f)
                except EOFError :
                    pass
                else :
                    self._set_attr (** attrs)
            finally :
                f.close ()
    # end def load

    def save (self, filename) :
        f = open    (filename, "wb")
        pickle.dump (self._attr, f, pickle.HIGHEST_PROTOCOL)
        f.close     ()
    # end def save

# end class _Status_I_

if __name__ != "__main__" :
    PMA._Export ("_Status_", "_Status_C_", "_Status_I_")
### __END__ PMA._Status_
