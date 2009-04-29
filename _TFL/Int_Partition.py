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
#    TFL.Int_Partition
#
# Purpose
#    Compute partition of (positive) integers
#
#    http://en.wikipedia.org/wiki/Partition_(number_theory)
#
# Revision Dates
#    29-Apr-2009 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL import TFL
import _TFL._Meta.Object

def int_partitions (n, l) :
    """Generate all partitions of length `l` for the positive integer
       `n`, i.e., all sums of `l + 1` positive integers adding up to `n`.

       >>> list (int_partitions (8, 0))
       [(8,)]
       >>> list (int_partitions (8, 1))
       [(7, 1), (6, 2), (5, 3), (4, 4)]
       >>> list (int_partitions (8, 2))
       [(6, 1, 1), (5, 2, 1), (4, 3, 1)]
       >>> list (int_partitions (8, 3))
       [(5, 1, 1, 1), (4, 2, 1, 1), (3, 3, 1, 1)]
       >>> list (int_partitions (8, 4))
       [(4, 1, 1, 1, 1), (3, 2, 1, 1, 1)]
       >>> list (int_partitions (8, 5))
       [(3, 1, 1, 1, 1, 1), (2, 2, 1, 1, 1, 1)]
       >>> list (int_partitions (8, 6))
       [(2, 1, 1, 1, 1, 1, 1)]
       >>> list (int_partitions (8, 7))
       [(1, 1, 1, 1, 1, 1, 1, 1)]
       >>> list (int_partitions (8, 8))
       []
    """
    assert l >= 0
    if l == 0 :
        yield (n, )
    elif l == 1 :
        for p in range (1, n // 2 + 1) :
            n -= 1
            yield n, p
    else :
        for ps in int_partitions (n, l - 1) :
            if ps [0] > ps [1] :
                yield (ps [0] - 1, ) + ps [1:] + (1, )
# end def int_partitions

class _Int_Partition_N_ (TFL.Meta.Object) :
    """Compute partition of (positive) integers.

       >>> for i in range (6) :
       ...   print i, list (Int_Partition (i))
       ...
       0 []
       1 [(1,)]
       2 [(2,), (1, 1)]
       3 [(3,), (2, 1), (1, 1, 1)]
       4 [(4,), (3, 1), (2, 2), (2, 1, 1), (1, 1, 1, 1)]
       5 [(5,), (4, 1), (3, 2), (3, 1, 1), (2, 2, 1), (2, 1, 1, 1), (1, 1, 1, 1, 1)]

       >>> Int_Partition [2,0]
       ((2,),)
       >>> Int_Partition [2,1]
       ((1, 1),)
       >>> Int_Partition [2,2]
       ()

       >>> for n in range (9) :
       ...   for l in range (n) :
       ...     print n, l, Int_Partition [n, l]
       ...
       1 0 ((1,),)
       2 0 ((2,),)
       2 1 ((1, 1),)
       3 0 ((3,),)
       3 1 ((2, 1),)
       3 2 ((1, 1, 1),)
       4 0 ((4,),)
       4 1 ((3, 1), (2, 2))
       4 2 ((2, 1, 1),)
       4 3 ((1, 1, 1, 1),)
       5 0 ((5,),)
       5 1 ((4, 1), (3, 2))
       5 2 ((3, 1, 1), (2, 2, 1))
       5 3 ((2, 1, 1, 1),)
       5 4 ((1, 1, 1, 1, 1),)
       6 0 ((6,),)
       6 1 ((5, 1), (4, 2), (3, 3))
       6 2 ((4, 1, 1), (3, 2, 1))
       6 3 ((3, 1, 1, 1), (2, 2, 1, 1))
       6 4 ((2, 1, 1, 1, 1),)
       6 5 ((1, 1, 1, 1, 1, 1),)
       7 0 ((7,),)
       7 1 ((6, 1), (5, 2), (4, 3))
       7 2 ((5, 1, 1), (4, 2, 1), (3, 3, 1))
       7 3 ((4, 1, 1, 1), (3, 2, 1, 1))
       7 4 ((3, 1, 1, 1, 1), (2, 2, 1, 1, 1))
       7 5 ((2, 1, 1, 1, 1, 1),)
       7 6 ((1, 1, 1, 1, 1, 1, 1),)
       8 0 ((8,),)
       8 1 ((7, 1), (6, 2), (5, 3), (4, 4))
       8 2 ((6, 1, 1), (5, 2, 1), (4, 3, 1))
       8 3 ((5, 1, 1, 1), (4, 2, 1, 1), (3, 3, 1, 1))
       8 4 ((4, 1, 1, 1, 1), (3, 2, 1, 1, 1))
       8 5 ((3, 1, 1, 1, 1, 1), (2, 2, 1, 1, 1, 1))
       8 6 ((2, 1, 1, 1, 1, 1, 1),)
       8 7 ((1, 1, 1, 1, 1, 1, 1, 1),)
    """

    def __call__ (self, n) :
        """Generate all partitions of the positive integer `n`, i.e., all
           sums of positive integers adding up to `n`.
        """
        for l in range (n) :
            for p in self [(n, l)] :
                yield p
    # end def __call__

    def __getitem__ (self, (n, l)) :
        """Return all partitions of length `l` for the positive integer
           `n`, i.e., all sums of `l + 1` positive integers adding up to `n`.
        """
        return tuple (int_partitions (n, l))
    # end def __getitem__

# end class _Int_Partition_N_

class _Int_Partition_C_ (_Int_Partition_N_) :

    __doc__ = _Int_Partition_N_.__doc__

    _Table  = {}

    def __getitem__ (self, (n, l)) :
        """Return all partitions of length `l` for the positive integer
           `n`, i.e., all sums of `l + 1` positive integers adding up to `n`.
        """
        try :
            result = self._Table [(n, l)]
        except KeyError :
            result = self._Table [(n, l)] = self.__super.__getitem__ ((n, l))
        return result
    # end def __getitem__

# end class _Int_Partition_C_

Int_Partition = _Int_Partition_C_ ()

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ Int_Partition
