# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Mag. Christian Tanzer. All rights reserved
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
#    TFL.Meta.Mixin_NS
#
# Purpose
#    Provide mixin namespaces
#
# Revision Dates
#    17-Apr-2009 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL             import TFL
import _TFL._Meta
import _TFL._Meta.M_Class

import _TFL.Caller

class M_Mixin_NS (TFL.Meta.M_Class) :
    """Meta class for Mixin_NS"""

    Copy  = TFL.Meta.M_Class.New
    Table = {}

    def New (cls, * mixins) :
        """Create a new Mixin_NS for `mixins` class(es)"""
        assert mixins
        result = cls.Table.get (mixins)
        if result is None :
            mixin  = mixins [0]
            name   = "MNS_%s" % (mixin.__name__, )
            result = cls.Table [mixins] = type \
                ( name
                , (Mixin_NS, ) + mixins
                , dict
                    ( __module__ = TFL.Caller.globals () ["__name__"]
                    , __doc__    = getattr (mixin, "__doc__", None)
                    )
                )
        return result ()
    # end def New

# end class M_Mixin_NS

class Mixin_NS (object) :
    """Mixin namespace: provides access to mixin functionality via a single
       object.

       Inspired by Michele Simionato's essay `Mixins considered harmful/4`
       (http://www.artima.com/weblogs/viewpost.jsp?thread=254507).

       >>> class M1 (object) :
       ...     def foo (self) :
       ...         ### Use `self._obj` to show class of bound object
       ...         print self._obj.__class__.__name__, "foo", self.a, self.b
       ...
       >>> class M2 (object) :
       ...     def foo (self) :
       ...         print self._obj.__class__.__name__, "foo", self.b, self.c
       ...     def bar (self) :
       ...         print self._obj.__class__.__name__, "bar", self.c
       ...
       >>> class C (object) :
       ...     m1 = Mixin_NS.New (M1)
       ...     m2 = Mixin_NS.New (M2)
       ...     a  = 1
       ...     b  = 2
       ...     c  = 3
       ...
       >>> c = C ()
       >>> c.m1.foo ()
       C foo 1 2
       >>> c.m2.foo ()
       C foo 2 3
       >>> c.m2.bar ()
       C bar 3
       >>>
       >>> c.m1 = 42
       Traceback (most recent call last):
       ...
       AttributeError: Cannot assign value 42 to mixin namespace attribute
       >>> C.m1.a
       Traceback (most recent call last):
         ...
       TypeError: Cannot access attributes of unbound instance of <MNS_M1 unbound>
    """

    __metaclass__ = M_Mixin_NS

    def __init__ (self, obj = None) :
        self._obj = obj
    # end def __init__

    def __get__ (self, obj, cls = None):
        if obj is None:
            return self
        return self.__class__ (obj)
    # end def __get__

    def __getattr__(self, name):
        obj = self._obj
        if obj is None :
            raise TypeError \
                ("Cannot access attributes of unbound instance of %r" % (self))
        return getattr (obj, name)
    # end def __getattr__

    def __repr__(self):
        obj = self._obj
        if obj is None :
            msg = "unbound"
        else :
            msg = "bound to %r" % obj
        return "<%s %s>" % (self.__class__.__name__, msg)
    # end def __repr__

    def __set__ (self, obj, value) :
        raise AttributeError \
            ("Cannot assign value %r to mixin namespace attribute" % (value, ))
    # end def __set__

# end class Mixin_NS

if __name__ != "__main__" :
    TFL.Meta._Export ("*")
### __END__ Mixin_NS


