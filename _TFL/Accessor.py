# -*- coding: utf-8 -*-
# Copyright (C) 2005-2013 Mag. Christian Tanzer. All rights reserved
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
#    18-Sep-2009 (CT) `_call_1` and `_call_n` changed to call callable results
#    18-Sep-2009 (CT) `_Getter_0_.__getattr__` changed to deal properly with
#                     composite names (e.g., `.x.y.z`)
#    18-Sep-2009 (CT) `_call_1` and `_call_n` changed back to *not* call
#                     callable results (breaks too many users)
#    16-Aug-2012 (CT) Simplify `_Getter_`: get rid of `_Getter_[01n]_`
#    22-Feb-2013 (CT) Remove legacy spellings `Attribute` and `Item`
#    ««revision-date»»···
#--

from   _TFL import TFL
import _TFL._Meta.Object

import operator

class _Getter_ (TFL.Meta.Object) :
    """Generalized (and transitive) accessor to attributes and items.

       .. note::
           Beware!

           This can't be used to refer to magic methods
           (like `__cmp__` or `__str__`)

       >>> from _TFL.Record import Record
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

       >>> s = Record (x = 0, y = 1)
       >>> g1 (s)
       Traceback (most recent call last):
         ...
       AttributeError: foo

       >>> last = Getter [-1]
       >>> last (range (2))
       1
       >>> last (range (5))
       4
       >>> third = Getter [3]
       >>> third (range (2))# doctest:+ELLIPSIS
       Traceback (most recent call last):
         ...
       IndexError: ... index out of range
       >>> third (range (5))
       3
    """

    def __init__ (self, getters = None, doc = None) :
        self.__getters = getters or ()
        self.__doc__   = doc
    # end def __init__

    def __call__ (self, o) :
        getters = self.__getters
        if getters :
            result = o
            for g in getters :
                result = g (result)
            return result
        else :
            raise TypeError ("Getter isn't directly callable")
    # end def _call_n

    def __getattr__ (self, name) :
        if self.__doc__ :
            doc = "%s.%s`" % (self.__doc__ [:-1], name)
        else :
            doc = "Getter function for `.%s`" % name
        return self.__class__ \
            (self.__getters + (operator.attrgetter (name), ), doc)
    # end def __getattr__

    def __getitem__ (self, key) :
        if self.__doc__ :
            doc = "%s [%s]`" % (self.__doc__ [:-1], key)
        else :
            doc = "Getter function for `[%s]`" % key
        return self.__class__ \
            (self.__getters + (operator.itemgetter (key), ), doc)
    # end def __getitem__

    def __repr__ (self) :
        return self.__doc__
    # end def __repr__

# end class _Getter_

class _Method_ (TFL.Meta.Object) :
    """Accessor to dynamically-bound methods (allows passing such as
        callbacks).

       >>> lower = Method.lower
       >>> lower ("abCDe")
       'abcde'
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

Getter = _Getter_ ()
Method = _Method_ ()

__doc__ = """
Module `Accessor`
==========================

.. moduleauthor:: Christian Tanzer <tanzer@swing.co.at>

"""

if __name__ != "__main__" :
    TFL._Export ("Getter", "Method")
### __END__ TFL.Accessor
