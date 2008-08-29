# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005-2008 DI Christian Eder. All rights reserved
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
#    M_Auto_Combine_Sets
#
# Purpose
#    Metaclass autocombining sets of newly defined class with those
#    of its ancestors
#
# Revision Dates
#    13-Jul-2005 (CED) Creation (stolen from M_Auto_Combine_Dicts)
#    13-Jul-2005 (CED) Export added
#    29-Aug-2008 (CT)  s/super(...)/__m_super/
#    ««revision-date»»···
#--
#

"""
Meta class for auto-combining the set-attributes mentioned in
`_sets_to_combine` between a class and it's ancestors.

>>> class A (object) :
...     __metaclass__     = M_Auto_Combine_Sets
...     _sets_to_combine  = ("foo",)
...     foo               = set ([1, 2, 3])
...
>>> class B (A) :
...     foo               = set ([5, 4, 3])
...
>>> sorted (A.foo)
[1, 2, 3]
>>> sorted (B.foo)
[1, 2, 3, 4, 5]
"""

from   _TFL                import TFL
import _TFL._Meta.M_Class

class M_Auto_Combine_Sets (TFL.Meta._M_Type_) :
    """Meta class for auto-combining the set-attributes mentioned in
       `_sets_to_combine` between a class and it's ancestors.
    """

    _sets_to_combine = ()

    def __init__ (cls, name, bases, dict) :
        cls._m_combine_sets    (bases, dict)
        cls.__m_super.__init__ (name, bases, dict)
    # end def __init__

    def _m_combine_sets (cls, bases, dict) :
        for name in cls._sets_to_combine :
            sets   = [getattr (b, name, set ()) for b in bases + (cls, )]
            setattr (cls, name, reduce (set.union, sets, set ()))
    # end def _m_combine_sets

# end class M_Auto_Combine_Sets

if __name__ != "__main__" :
    TFL.Meta._Export ("*")
### __END__ M_Auto_Combine_Sets


