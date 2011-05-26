# -*- coding: iso-8859-15 -*-
# Copyright (C) 2004-2010 Mag. Christian Tanzer. All rights reserved
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
#    TFL.Meta.M_Auto_Combine_Dicts
#
# Purpose
#    Metaclass autocombining dictionaries of newly defined class with those
#    of its ancestors
#
# Revision Dates
#    23-Jul-2004 (CT) Creation (factored from TOM.Meta.M_Auto_Combine)
#    29-Aug-2008 (CT)  s/super(...)/__m_super/
#     2-Feb-2009 (CT) s/_M_Type_/M_Base/
#     3-Feb-2009 (CT) Documentation improved
#     5-Jan-2010 (CT) Use `itertools.chain` instead of `TFL.d_dict`
#    ««revision-date»»···
#--

"""
Meta class for auto-combining the dict-valued attributes mentioned in
`_dicts_to_combine` between a class and it's ancestors.

::

    >>> class A (object) :
    ...     __metaclass__     = M_Auto_Combine_Dicts
    ...     _dicts_to_combine = ("foo", "bar")
    ...     bar               = dict (x = 1, y = 2)
    ...
    >>> class B (object) :
    ...     foo               = dict (u = 1, v = "a")
    ...     bar               = dict (y = 3, z = 42)
    ...
    >>> class BA (B, A) :
    ...     _dicts_to_combine = A._dicts_to_combine + ("baz", )
    ...
    >>> class AB (A, B) :
    ...     foo               = dict (v = "b", w = "a")
    ...     bar               = dict (x = "z", z = -42)
    >>> sorted (A.foo.items ()), sorted (A.bar.items ())
    ([], [('x', 1), ('y', 2)])
    >>> sorted (B.foo.items ()), sorted (B.bar.items ())
    ([('u', 1), ('v', 'a')], [('y', 3), ('z', 42)])
    >>> sorted (BA.foo.items ()), sorted (BA.bar.items ()), sorted (BA.baz.items ())
    ([('u', 1), ('v', 'a')], [('x', 1), ('y', 3), ('z', 42)], [])
    >>> sorted (AB.foo.items ()), sorted (AB.bar.items ())
    ([('u', 1), ('v', 'b'), ('w', 'a')], [('x', 'z'), ('y', 2), ('z', -42)])
"""

from   _TFL                import TFL

import _TFL._Meta.M_Class

import itertools

class M_Auto_Combine_Dicts (TFL.Meta.M_Base) :
    """Meta class for auto-combining the dict-valued attributes mentioned in
       `_dicts_to_combine` between a class and it's ancestors.
    """

    _dicts_to_combine = ()

    def __init__ (cls, name, bases, dct) :
        cls._m_combine_dicts   (bases, dct)
        cls.__m_super.__init__ (name, bases, dct)
    # end def __init__

    def _m_combine_dicts (cls, bases, dct) :
        for name in cls._dicts_to_combine :
            setattr \
                ( cls, name
                , dict
                    ( itertools.chain
                        ( * (   getattr (c, name, {}).iteritems ()
                            for c in reversed ((cls, ) + bases)
                            )
                        )
                    )
                )
    # end def _m_combine_dicts

# end class M_Auto_Combine_Dicts

if __name__ != "__main__" :
    TFL.Meta._Export ("*")
### __END__ TFL.Meta.M_Auto_Combine_Dicts
