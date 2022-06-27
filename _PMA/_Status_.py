# -*- coding: utf-8 -*-
# Copyright (C) 2005-2020 Christian Tanzer. All rights reserved
# tanzer@gg32.com                                      https://www.gg32.com
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <https://www.gg32.com/license/bsd_3c.html>.
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
#    14-Aug-2005 (MG) Moved from `PMA` package to the `TGL` package
#    05-Jan-2006 (MG) Open the files in binary mode in the `load` functions
#                     (they are stored in binary mode too)
#    10-Nov-2009 (CT) Use `pickle` instead of `cPickle` to silence `-3`
#    29-Oct-2015 (CT) Improve Python 3 compatibility
#     9-Oct-2016 (CT) Move back to `PMA`
#    31-Mar-2020 (CT) Def `__bool__`, not `__nonzero__` (Py-3)
#    ««revision-date»»···
#--

from   _TFL                     import TFL
from   _PMA                     import PMA

from   _TFL.pyk                 import pyk

import _TFL._Meta.Object

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
            raise AttributeError (name)
    # end def __delattr__

    def __getattr__ (self, name) :
        try :
            return self._attr [name]
        except KeyError :
            raise AttributeError (name)
    # end def __getattr__

    def __getstate__ (self) :
        return self._attr
    # end def __getstate__

    def __bool__ (self) :
        return bool (self._attr)
    # end def __bool__

    def __setattr__ (self, name, value) :
        p = self.__class__.__dict__.get (name, None)
        if p is None :
            self._set_attr (** {name : value})
        elif isinstance (p, property) :
            p.__set__ (self, value)
        else :
            raise AttributeError \
                ("can't set attribute %s to %s" % (name, value))
    # end def __setattr__

    def __setstate__ (self, attr) :
        self.__dict__ ["_attr"] = attr
    # end def __setstate__

# end class _Status_

class _Status_C_ (_Status_) :

    @classmethod
    def load (cls, filename) :
        try :
            with open (filename, "rb") as f :
                try :
                    cls._Table = pyk.pickle.load (f)
                except EOFError :
                    pass
        except IOError :
            pass
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
        with open (filename, "wb") as f :
            pyk.pickle.dump (cls._Table, f, pyk.pickle_protocol)
    # end def save

# end class _Status_C_

class _Status_I_ (_Status_) :

    def load (self, filename) :
        try :
            with open (filename, "rb") as f :
                try :
                    attrs = pyk.pickle.load (f)
                except EOFError :
                    pass
                else :
                    self._set_attr (** attrs)
        except IOError :
            pass
    # end def load

    def save (self, filename) :
        with open (filename, "wb") as f :
            pyk.pickle.dump (self._attr, f, pyk.pickle_protocol)
    # end def save

# end class _Status_I_

if __name__ != "__main__" :
    PMA._Export ("_Status_", "_Status_C_", "_Status_I_")
### __END__ PMA._Status_
