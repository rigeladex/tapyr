# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004-2008 Mag. Christian Tanzer. All rights reserved
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
#    TFL.Meta.M_Auto_Combine_Lists
#
# Purpose
#    Metaclass autocombining lists of newly defined class with those of its
#    ancestors
#
# Revision Dates
#    23-Jul-2004 (CT)  Creation (factored from TOM.Meta.M_Auto_Combine)
#    13-Jul-2005 (CED) Use sets instead of dicts
#     2-Jul-2006 (MG)  Unnecessary imports removed
#    14-Dec-2007 (MG)  Import changed
#    ««revision-date»»···
#--

"""Meta class for auto-combining the list-attributes mentioned in
`_lists_to_combine` between a class and it's ancestors.

>>> class A (object) :
...     __metaclass__     = M_Auto_Combine_Lists
...     _lists_to_combine = ("foo", "bar")
...     bar               = [1, 3]
...
>>> class B (A) :
...     _lists_to_combine = A._lists_to_combine + ("baz", )
...     foo               = [0]
...     bar               = [-1, 1, 2, 42]
...
>>> A.foo
[]
>>> B.foo
[0]
>>> A.bar
[1, 3]
>>> B.bar
[-1, 1, 2, 3, 42]
>>> B.baz
[]
"""

from   _TFL                import TFL
import _TFL._Meta.M_Class
from   _TFL.predicate      import sorted

class M_Auto_Combine_Lists (TFL.Meta._M_Type_) :
    """Meta class for auto-combining the list-attributes mentioned in
       `_lists_to_combine` between a class and it's ancestors.

       Beware:
       - the sequence of elements in the _lists_to_combine is not
         kept!
       - Multiple occurrences of the same element are skipped
       - The elements of the _lists_to_combine must be hashable
    """

    _lists_to_combine = ()

    def __init__ (cls, name, bases, dict) :
        cls._m_combine_lists (bases, dict)
        super (M_Auto_Combine_Lists, cls).__init__ (name, bases, dict)
    # end def __init__

    def _m_combine_lists (cls, bases, dict) :
        for ltc in cls._lists_to_combine :
            n   = "__%s" % ltc
            s   = set ()
            for b in bases :
                ltc_set = getattr (b, n, getattr (b, ltc, []))
                s.update (ltc_set)
            try :
                s.update (dict.get (ltc, []))
            except TypeError :
                print cls, [(x, type (x)) for x in dict.get (ltc, [])]
                raise
            setattr (cls, n,   s)
            setattr (cls, ltc, sorted (s))
    # end def _m_combine_lists

# end class M_Auto_Combine_Lists

if __name__ != "__main__" :
    TFL.Meta._Export ("*")
### __END__ TFL.Meta.M_Auto_Combine_Lists
