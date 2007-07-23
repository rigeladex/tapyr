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
#    23-Jul-2007 (CED) Activated absolute_import
#    ««revision-date»»···
#--
from __future__ import absolute_import


from   _TFL import TFL
import _TFL._Meta.Object

import operator

class _Attribute_ (TFL.Meta.Object) :
    """Accessor to attributes.

       >>> from Record import *
       >>> r = Record (a = 1, b = "2", foo = 42)
       >>> a = Attribute.foo
       >>> a (r)
       42
       >>> s = Record (x = 0, y = 1)
       >>> a (s)
       Traceback (most recent call last):
         ...
       AttributeError: foo
    """

    def __getattr__ (self, name) :
        return operator.attrgetter (name)
    # end def __getattr__

# end class _Attribute_

class _Item_ (TFL.Meta.Object) :
    """Accessor to item

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

    def __getitem__ (self, key) :
        return operator.itemgetter (key)
    # end def __getitem__

# end class _Item_

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

Attribute = _Attribute_ ()
Item      = _Item_      ()
Method    = _Method_    ()

if __name__ != "__main__" :
    TFL._Export ("Attribute", "Item", "Method")
### __END__ TFL.Accessor
