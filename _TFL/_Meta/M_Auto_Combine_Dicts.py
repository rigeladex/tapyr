# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 Mag. Christian Tanzer. All rights reserved
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
#    TFL.Meta.M_Auto_Combine_Dicts
#
# Purpose
#    Metaclass autocombining dictionaries of newly defined class with those
#    of its ancestors
#
# Revision Dates
#    23-Jul-2004 (CT) Creation (factored from TOM.Meta.M_Auto_Combine)
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ««revision-date»»···
#--



"""
Meta class for auto-combining the dict-attributes mentioned in
`_dicts_to_combine` between a class and it's ancestors.

>>> from predicate import sorted
>>> class A (object) :
...     __metaclass__     = M_Auto_Combine_Dicts
...     _dicts_to_combine = ("foo", "bar")
...     bar               = TFL.d_dict (x = 1, y = 2)
...
>>> class B (A) :
...     _dicts_to_combine = A._dicts_to_combine + ("baz", )
...     foo               = TFL.d_dict (u = 1)
...     bar               = TFL.d_dict (y = 3, z = 42)
...
>>> sorted (A.foo.iteritems ())
[]
>>> sorted (B.foo.iteritems ())
[('u', 1)]
>>> sorted (A.bar.iteritems ())
[('x', 1), ('y', 2)]
>>> sorted (B.bar.iteritems ())
[('x', 1), ('y', 3), ('z', 42)]
>>> B.baz
{}
"""

from   _TFL                import TFL

import _TFL.d_dict
import _TFL._Meta.M_Class

class M_Auto_Combine_Dicts (TFL.Meta._M_Type_) :
    """Meta class for auto-combining the dict-attributes mentioned in
       `_dicts_to_combine` between a class and it's ancestors.
    """

    _dicts_to_combine = ()

    def __init__ (cls, name, bases, dict) :
        cls._m_combine_dicts (bases, dict)
        super (M_Auto_Combine_Dicts, cls).__init__ (name, bases, dict)
    # end def __init__

    def _m_combine_dicts (cls, bases, dict) :
        for name in cls._dicts_to_combine :
            c_dict  = getattr (cls, name, {})
            b_dicts = [getattr (b, name, {}) for b in bases]
            setattr (cls, name, TFL.d_dict (c_dict, * b_dicts))
    # end def _m_combine_dicts

# end class M_Auto_Combine_Dicts

if __name__ != "__main__" :
    TFL.Meta._Export ("*")
### __END__ TFL.Meta.M_Auto_Combine_Dicts
