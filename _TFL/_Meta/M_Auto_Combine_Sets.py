# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2013 Mag. Christian Tanzer. All rights reserved
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
#    TFL.Meta.M_Auto_Combine_Sets
#
# Purpose
#    Metaclass autocombining set-valued attributes of a newly defined class
#    with those of its ancestors
#
# Revision Dates
#     5-Jan-2010 (CT) Creation (new implementation)
#    ««revision-date»»···
#--

"""
Meta class for auto-combining the set-valued attributes mentioned in
`_sets_to_combine` between a class and it's ancestors.

::

    >>> class A (TFL.Meta.BaM (object, metaclass = M_Auto_Combine_Sets)) :
    ...     _sets_to_combine  = ("foo", "bar")
    ...     foo               = set ([1, 2, 3])
    ...
    >>> class B (A) :
    ...     _sets_to_combine  = A._sets_to_combine + ("baz", )
    ...     foo               = set ([5, 4, 3])
    ...     bar               = set ("ab")
    ...
    >>> class C (B) :
    ...     bar               = set ("xyz")
    >>> sorted (A.foo), sorted (A.bar)
    ([1, 2, 3], [])
    >>> sorted (B.foo), sorted (B.bar), sorted (B.baz)
    ([1, 2, 3, 4, 5], ['a', 'b'], [])
    >>> sorted (C.foo), sorted (C.bar), sorted (C.baz)
    ([1, 2, 3, 4, 5], ['a', 'b', 'x', 'y', 'z'], [])
"""

from   _TFL                import TFL
import _TFL._Meta.M_Class

import itertools

class M_Auto_Combine_Sets (TFL.Meta.M_Base) :
    """Meta class for auto-combining the set-valued attributes mentioned in
       `_sets_to_combine` between a class and it's ancestors.
    """

    _sets_to_combine = ()

    def __init__ (cls, name, bases, dict) :
        cls._m_combine_sets    (bases, dict)
        cls.__m_super.__init__ (name, bases, dict)
    # end def __init__

    def _m_combine_sets (cls, bases, dict) :
        for name in cls._sets_to_combine :
            setattr \
                ( cls, name
                , set
                    ( itertools.chain
                        (    getattr (cls, name, set ())
                        , * (getattr (bas, name, set ()) for bas in bases)
                        )
                    )
                )
    # end def _m_combine_sets

# end class M_Auto_Combine_Sets

if __name__ != "__main__" :
    TFL.Meta._Export ("*")
### __END__ TFL.Meta.M_Auto_Combine_Sets
