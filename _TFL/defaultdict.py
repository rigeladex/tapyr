# -*- coding: iso-8859-15 -*-
# Copyright (C) 2006-2012 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
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
#    TFL.defaultdict
#
# Purpose
#    dict with default value for missing entries
#
# Revision Dates
#    13-Mar-2006 (CT) Creation (for Python 2.4)
#    20-Jun-2007 (CT) Adapted to Python 2.5
#    20-Jun-2007 (CT) `defaultdict_kd` added
#    29-Aug-2008 (CT) s/super(...)/__super/
#    30-May-2012 (CT) Add `defaultdict_nested`
#    ««revision-date»»···
#--

"""
Python 2.5 provides `collections.defaultdict`.
This module allows the use of `defaultdict` in earlier and later versions of
Python.

>>> zd = defaultdict (int)
>>> zd
defaultdict(<type 'int'>, {})
>>> zd [1] = 42
>>> zd [2] = 137
>>> zd
defaultdict(<type 'int'>, {1: 42, 2: 137})
>>> zd [3]
0
>>> zd
defaultdict(<type 'int'>, {1: 42, 2: 137, 3: 0})
"""

from   _TFL import TFL
import _TFL._Meta.M_Class

import sys

class _defaultdict_ (dict) :

    __metaclass__        = TFL.Meta.M_Class

    if sys.hexversion < 0x02050000 :
        def __getitem__ (self, key) :
            try :
                return self.__super.__getitem__ (key)
            except KeyError :
                return self.__missing__ (key)
        # end def __getitem__

    def __missing__ (self, key) :
        if self.default_factory is None :
            raise KeyError (key)
        result = self [key] = self.default_factory ()
        return result
    # end def __missing__

    def _defaultdict__init__ (self, _default_factory, * args, ** kw) :
        self.default_factory = _default_factory
        self.__super.__init__ (* args, ** kw)
    # end def _defaultdict__init__

    def _defaultdict__repr__ (self) :
        return "%s(%r, %s)" % \
            ( self.__class__.__name__, self.default_factory
            , self.__super.__repr__ ()
            )
    # end def _defaultdict__repr__

# end class _defaultdict_

class _defaultdict_kd_ (_defaultdict_) :

    def __missing__ (self, key) :
        if self.default_factory is None :
            raise KeyError (key)
        result = self [key] = self.default_factory (key)
        return result
    # end def __missing__

# end class _defaultdict_kd_

try :
    from collections import defaultdict
except ImportError :
    class defaultdict (_defaultdict_) :
        """defaultdict(_default_factory) --> dict with default factory

           The default factory is called without arguments to produce
           a new value when a key is not present, in __getitem__ only.
           A defaultdict compares equal to a dict with the same items.
        """

        __init__ = _defaultdict_._defaultdict__init__
        __repr__ = _defaultdict_._defaultdict__repr__

    # end class defaultdict

class defaultdict_kd (_defaultdict_kd_) :
    """defaultdict_kd(_default_factory) --> dict with default factory

       The default factory is called with the `key` argument to produce
       a new value when a key is not present, in __getitem__ only.
       A defaultdict compares equal to a dict with the same items.

       >>> dd = defaultdict_kd (lambda k : k * 2)
       >>> sorted (dd.iteritems ())
       []
       >>> dd [1] = 42
       >>> dd [2]
       4
       >>> dd ["a"]
       'aa'
       >>> sorted (dd.iteritems ())
       [(1, 42), (2, 4), ('a', 'aa')]
    """

    __init__ = _defaultdict_kd_._defaultdict__init__
    __repr__ = _defaultdict_kd_._defaultdict__repr__

# end class defaultdict_kd

def defaultdict_nested (depth = 1, leaf = dict) :
    """Return a `defaultdict` nested to `depth` with leaves of type `leaf`.

    >>> from _TFL.Formatter import formatted
    >>> ddn_1 = defaultdict_nested (1, int)
    >>> ddn_1
    defaultdict(<type 'int'>, {})
    >>> ddn_2 = defaultdict_nested (2, int)
    >>> ddn_1 ["foo"] += 1
    >>> ddn_1 ["foo"] += 1
    >>> ddn_1
    defaultdict(<type 'int'>, {'foo': 2})
    >>> ddn_2 ["foo"] ["bar"] += 42
    >>> print formatted (ddn_1)
    { 'foo' : 2 }
    >>> print formatted (ddn_2)
    { 'foo' :
        { 'bar' : 42 }
    }
    >>> ddn_7 = defaultdict_nested (7, int)
    >>> ddn_7 [1] [2] [3] [4] [5] [6] [7] = "foo"
    >>> print formatted (ddn_7)
    { 1 :
        { 2 :
            { 3 :
                { 4 :
                    { 5 :
                        { 6 :
                            { 7 : 'foo' }
                        }
                    }
                }
            }
        }
    }
    >>> ddn_7 [0] [1] [2] [3] [4] [5] [6] [7] = "bar"
    Traceback (most recent call last):
      ...
    TypeError: 'int' object does not support item assignment
    """
    result = defaultdict (leaf)
    for i in range (depth - 1) :
        result = defaultdict (lambda r = result : r)
    return result
# end def defaultdict_nested

if __name__ != "__main__" :
    TFL._Export \
        ( "defaultdict", "defaultdict_kd", "defaultdict_nested"
        , "_defaultdict_", "_defaultdict_kd_"
        )
### __END__ TFL.defaultdict
