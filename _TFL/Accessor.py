# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005-2007 Mag. Christian Tanzer. All rights reserved
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
#    TFL.Accessor
#
# Purpose
#    Provide syntax-sugared analogons to operator.attrgetter and
#    operator.itemgetter plus an accessor for dynamically-bound methods
#
#    Inspired by a post by "Martin v. Löwis" <martin@v.loewis.de> to
#    python-dev@python.org
#        Subject: Re: [Python-Dev] PEP 309: Partial method application
#        Message-id: <4304E423.9050005@v.loewis.de>
#
# Revision Dates
#    19-Aug-2005 (CT) Creation
#     7-Nov-2007 (CT) `Attribute` and `Item` generalized and refactored into
#                     `Getter`
#    ««revision-date»»···
#--

from   _TFL import TFL
import _TFL._Meta.Object

import operator

class _Getter_ (TFL.Meta.Object) :
    """Generalized (and transitive) accessor to attributes and items.

       *** Beware: this can't be used to refer to magic methods
           (like `__cmp__` or `__str__`)

       >>> from Record import *
       >>> r = Record (a = 1, b = "2", foo = 42, bar = Record (x = 0, y = 137))
       >>> r.bar.z = [1, 42, 137]
       >>> g1 = Getter.foo
       >>> gi = Getter [2]
       >>> gn = Getter.bar.z [-1]
       >>> g1 (r)
       42
       >>> gi (r.bar.z)
       137
       >>> gn (r)
       137
       >>> r.bar.z.append ("howdi")
       >>> gn (r)
       'howdi'

       `Attribute` is a legacy spelling of `Getter`
       >>> r = Record (a = 1, b = "2", foo = 42)
       >>> a = Attribute.foo
       >>> a (r)
       42
       >>> s = Record (x = 0, y = 1)
       >>> a (s)
       Traceback (most recent call last):
         ...
       AttributeError: foo

       `Item` is another legacy spelling of `Getter`
       >>> last = Item [-1]
       >>> last (range (2))
       1
       >>> last (range (5))
       4
       >>> third = Item [3]
       >>> third (range (2))
       Traceback (most recent call last):
         ...
       IndexError: list index out of range
       >>> third (range (5))
       3
     """

    def __init__ (self, getters, doc) :
        self.__getters = getters
        self.__doc__   = doc
    # end def __init__

    def _call_1 (self, o) :
        return self.__getters [0] (o)
    # end def _call_1

    def _call_n (self, o) :
        getters = self.__getters
        result = getters [0] (o)
        for g in getters [1:] :
            result = g (result)
        return result
    # end def _call_n

    def __getattr__ (self, name) :
        return _Getter_n_ \
            ( self.__getters + (operator.attrgetter (name), )
            , "%s.%s`" % (self.__doc__ [:-1], name)
            )
    # end def __getattr__

    def __getitem__ (self, key) :
        return _Getter_n_ \
            (self.__getters + (operator.itemgetter (key), )
            , "%s [%s]`" % (self.__doc__ [:-1], key)
            )
    # end def __getitem__

    def __repr__ (self) :
        return self.__doc__
    # end def __repr__

# end class _Getter_

class _Getter_0_ (TFL.Meta.Object) :
    """Generalized (and transitive) accessor to attributes and items."""

    def __getattr__ (self, name) :
        return _Getter_1_ \
            ( (operator.attrgetter (name), )
            , "Getter function for `.%s`" % name
            )
    # end def __getattr__

    def __getitem__ (self, key) :
        return _Getter_1_ \
            ( (operator.itemgetter (key), )
            ,  "Getter function for `[%s]`" % key
            )
    # end def __getitem__

# end class _Getter_0_

class _Getter_1_ (_Getter_) :
    __call__ = _Getter_._call_1
# end class _Getter_1_

class _Getter_n_ (_Getter_) :
    __call__ = _Getter_._call_n
# end class _Getter_n_

class _Method_ (TFL.Meta.Object) :
    """Accessor to dynamically-bound methods (allows passing such as
        callbacks).

       >>> lower = Method.lower
       >>> lower ("abCDe")
       'abcde'
       >>> lower (u"abCDe")
       u'abcde'
       >>> lower (1)
       Traceback (most recent call last):
         ...
       AttributeError: 'int' object has no attribute 'lower'
    """

    def __getattr__ (self, name) :
        def _ (this, * args, ** kw) :
            return getattr (this, name) (* args, ** kw)
        _.__name__ = name
        return _
    # end def __getattr__

# end class _Method_

Getter = Attribute = Item = _Getter_0_ ()
Method = _Method_ ()

if __name__ != "__main__" :
    TFL._Export ("Attribute", "Getter", "Item", "Method")
### __END__ TFL.Accessor
