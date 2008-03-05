# -*- coding: iso-8859-1 -*-
# Copyright (C) 2002-2008 Mag. Christian Tanzer. All rights reserved
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
#    TFL.Meta.Object
#
# Purpose
#    Base class using TFL.Meta.Class as metaclass
#
# Revision Dates
#    13-May-2002 (CT) Creation
#    17-Jan-2003 (CT) `M_` prefixes added
#    24-Mar-2003 (CT) Delegation for `__init__` added
#     5-Mar-2008 (CT) `_TFL_Meta_Object_Root_` added to accomodate Python 2.6
#                     (http://bugs.python.org/issue1683368)
#    ««revision-date»»···
#--

from   _TFL import TFL
import _TFL._Meta.M_Class

class _TFL_Meta_Object_Root_ (object) :
    ### Root class to fix `__init__` and `__new__`.
    ###     As of Python 2.6, `object.__init__` doesn't accept parameters
    ### Don't inherit from this (unless you really know what you're doing)

    def __new__ (cls, * args, ** kw) :
        return object.__new__ (cls)
    # end def __new__

    def __init__ (self, * args, ** kw) :
        object.__init__ (self)
    # end def __init__

# end class _TFL_Meta_Object_Root_

class _TFL_Meta_Object_ (_TFL_Meta_Object_Root_) :
    """Base class using TFL.Meta.Class as metaclass."""

    __metaclass__ = TFL.Meta.M_Class
    """TFL.Meta.Class is used as metaclass for this class and all its
       dependents (which don't override the metaclass)
       """

    _real_name    = "Object"
    """This class will be known and used as `Object` although the class
       statement contains a different (mangled) name. This allows the use of
       the generic class name `Object` in different packages without messing
       up Python's name mangling. The renaming is done by `TFL.Meta.Class`.
       """

    __properties  = []
    """`TFL.Meta.Class` will add and initialize all elements of
       `__properties` automatically. These should be instances of
       `TFL.Meta.Property` or one of its descendents (or signature compatible
       with it).
       """

    def __init__ (self, * args, ** kw) :
        ### delegate to `__super` to accomodate multiple inheritance
        self.__super.__init__ (* args, ** kw)
    # end def __init__

# end class _TFL_Meta_Object_

Object = _TFL_Meta_Object_

if __name__ != "__main__" :
    TFL.Meta._Export ("Object")
### __END__ TFL.Meta.Object
