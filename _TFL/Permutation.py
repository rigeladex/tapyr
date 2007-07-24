# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 TTTech Computertechnik AG. All rights reserved
# Schönbrunnerstraße 7, A--1040 Wien, Austria. office@tttech.com
#
#++
# Name
#    Permutation
#
# Purpose
#    Models permutations (in algebraic sense)
#    ««text»»···
#
# Revision Dates
#    16-Nov-2004 (CED) Creation
#    17-Nov-2004 (CED) Creation continued .
#    13-Jul-2005 (CED) `__mul__` changed to use sets
#    12-Jul-2007 (CED) `Part_Pos_Translator` and friends added
#    19-Jul-2007 (MZO) [24856] moved Permutation from YAGNI.Permutation to TFL
#                      and Part_Pos_Translator to HWA.Copy_List
#    23-Jul-2007 (CED) Activated absolute_import
#    ««revision-date»»···
#--
#
from __future__ import absolute_import



from   _TFL   import TFL
import _TFL._Meta.Object

from   predicate  import *

class Permutation (TFL.Meta.Object) :
    """Models Permutations (in algebraic sense)

       >>> p1 = Permutation (2, (0, 1))
       >>> p1
       Permutation: ((0, 1),)
       >>> p2 = Permutation (4, (0, 1, 2, 3))
       >>> p3 = Permutation (4, (0, 2), (1, 3))
       >>> p4 = Permutation (4, (3, 1), (2, 0))
       >>> p4
       Permutation: ((0, 2), (1, 3))
       >>> p5 = Permutation (4)
       >>> p5
       Permutation: ()
       >>> p6 = Permutation (4, (0, 2, 1, 3))
       >>> p2 (1)
       2
       >>> p6 (3)
       0
       >>> p5 (2)
       2
       >>> p1 == p2
       False
       >>> p3 == p4
       True
       >>> bool (p1)
       True
       >>> bool (p1 * p1)
       False
       >>> p2 * p4
       Permutation: ((0, 3, 2, 1),)
       >>> p3 * p3 * p3 == p4
       True
       >>> p2 * p2 == p3
       True
       >>> list (p2.generate ())
       [Permutation: ((0, 1, 2, 3),), Permutation: ((0, 2), (1, 3)), Permutation: ((0, 3, 2, 1),), Permutation: ()]
       >>> p4.generated_by (p2)
       True
       >>> p2.generated_by (p4)
       False
       >>> p6.generated_by (p2)
       False
       >>> p4.generates_same_group (p2)
       False
       >>> p2.generates_same_group (p2 * p4)
       True
       >>> p1.sign (), p2.sign (), p3.sign (), p5.sign (), p6.sign ()
       (-1, -1, 1, 1, -1)
       >>> p6 = Permutation (4, (0, 0), (1, 1), (2, 2))
       >>> p6
       Permutation: ()
    """

    def __init__ (self, count, * pl) :
        self.count = count
        self.pl, self._content = self._fixed (pl)
    # end def __init__

    def blown_up (self, count) :
        result = []
        count  = rounded_up (count, self.count)
        for i in xrange (count) :
            mine   = i % self.count
            offset = rounded_down (i, self.count)
            other  = self (mine) + offset
            result.append ((i, other))
        return self.__class__ (count, * tupelize (result))
    # end def blown_up

    def even (self) :
        result = 0
        for (i, j) in self._subset_2 () :
            result += (i < j) != (self (i) < self (j))
        return (result % 2) == 0
    # end def even

    def odd (self) :
        return not self.even ()
    # end def odd

    def sign (self) :
        if self.even () :
            return 1
        else :
            return -1
    # end def sign

    def generated_by (self, other) :
        group = list (other.generate ())
        return self in group
    # end def generated_by

    def generate (self) :
        next = self
        while True :
            yield next
            next = self * next
            if next == self :
                break
    # end def generate

    def generates_same_group (self, other) :
        group1 = list (self.generate ())
        group2 = list (other.generate ())
        return (len (group1) == len (group2)) and (self in group2)
    # end def generates_same_group

    def _build_perm_list (self, i, rhs) :
        result = [i]
        while True :
            j = rhs._permutate_i  (i)
            k = self._permutate_i (j)
            if k == result [0] :
                break
            else :
                result.append (k)
            i = k
        if len (result) > 1 :
            return tuple (result)
        else :
            return ()
    # end def _build_perm_list

    def _fixed (self, pl) :
        result  =[]
        content = {}
        pl      = [p for p in pl if len (set (p)) > 1]
        for p in pl :
            if not isinstance (p, tuple) :
                raise TypeError, "Wrong Arguments: %s" % (pl, )
            if len (p) < 2 :
                raise TypeError, "Illegal Permutation: %s, %s" % (p, pl)
            m = min (p)
            while p [0] != m :
                p = rotate_l (p)
            if p not in result :
                result.append (p)
                for i in p :
                    if i not in content :
                        content [i] = p
        return tuple (sorted (result)), content
    # end def _fixed

    def _permutate_i (self, i) :
        if i not in self._content :
            return i
        l = self._content [i]
        while l [0] != i :
            l = rotate_l (l)
        return l [1]
    # end def _permutate_i

    def _subset_2 (self) :
        for i, j in enumerate (self._content.iterkeys ()) :
            for k in self._content.keys () [i+1 :] :
                yield (j, k)
    # end def _subset_2

    def __repr__ (self) :
        return ( "Permutation: %s"
               % (self.pl, )
               )
    # end def __repr__

    def __call__ (self, i) :
        if not isinstance (i, (int, long)) :
            raise TypeError, "Need integer"
        return self._permutate_i (i)
    # end def __call__

    def __eq__ (self, rhs) :
        return self.pl == rhs.pl
    # end def __eq__

    def __hash__ (self) :
        return hash (self.pl)
    # end def __hash__

    def __mul__ (self, rhs) :
        result = []
        if not isinstance (rhs, Permutation) :
            raise TypeError, "Can only multiply two Permutations"
        content_union = self._content.copy ()
        content_union.update (rhs._content)
        done = set ()
        for i in content_union.iterkeys () :
            if i in done :
                continue
            group = self._build_perm_list (i, rhs)
            done.add (i)
            for j in group :
                done.add (j)
            if group :
                result.append (group)
        return self.__class__ (max (self.count, rhs.count), * result)
    # end def __mul__

    def __nonzero__ (self) :
        return bool (self.pl)
    # end def __nonzero__

# end class Permutation

if __name__ != "__main" :
    TFL._Export ("*")
else :
    import doctest
    doctest.testmod ()
### __END__ _TFL.Permutation


