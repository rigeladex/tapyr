#! /usr/bin/python
# Copyright (C) 2002 Mag. Christian Tanzer. All rights reserved
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
#    Generators
#
# Purpose
#    Provide useful generators
#
# Revision Dates
#    18-Apr-2002 (CT) Creation
#    19-Apr-2002 (CT) `Lazy_List` added
#    29-Jul-2002 (CT) s/paired/paired_zip/
#    ««revision-date»»···
#--

from __future__ import generators

def Integers (n) :
    """Generates integers from 0 to `n`."""
    i = 0
    while i < n :
        yield i
        i += 1
# end def Integers

def Indices (seq) :
    """Generates indices of sequence `seq`.

       >>> list (Indices ("abcdef"))
       [0, 1, 2, 3, 4, 5]
    """
    return Integers (len (seq))
# end def Indices

def IV_Pairs (seq) :
    """Generates index-value pairs `i, s[i]' for all indices of sequence `seq'.

       >>> list (IV_Pairs ("abcdef"))
       [(0, 'a'), (1, 'b'), (2, 'c'), (3, 'd'), (4, 'e'), (5, 'f')]
    """
    i = 0
    for s in seq :
        yield i, s
        i += 1
# end def IV_Pairs

def pairwise (seq) :
    """Generates a list of pairs `(seq [0:1], seq [1:2], ..., seq [n-1:n])'.

       >>> list (pairwise ("abcdef"))
       ['ab', 'bc', 'cd', 'de', 'ef']
       >>> list (pairwise (range (4)))
       [[0, 1], [1, 2], [2, 3]]
    """
    i, l = 0, len (seq)
    while i < l - 1 :
        yield seq [i:i+2]
        i += 1
# end def pairwise

def paired_zip (s1, s2) :
    """Generates a list of pairs `((s1 [0], s2 [0]), ... (s1 [-1], s2 [-1]))'.

       >>> list (paired ("abc", range (4)))
       [('a', 0), ('b', 1), ('c', 2)]
    """
    i, l = 0, min (len (s1), len (s2))
    while i < l :
        yield s1 [i], s2 [i]
        i += 1
# end def paired_zip

def paired_map (s1, s2) :
    """Generates a list of pairs `((s1 [0], s2 [0]), ... (s1 [-1], s2 [-1]))'.

       >>> list (paired_map ("abc", range (4)))
       [('a', [0]), ('b', [1]), ('c', [2]), (None, [3])]
       >>> list (paired_map ("abc", range (2)))
       [('a', [0]), ('b', [1]), ('c', None)]
    """
    i, l1, l2 = 0, len (s1), len (s2)
    l         = min (l1, l2)
    while i < l :
        yield s1 [i:i+1], s2 [i:i+1]
        i += 1
    while i < l1 :
        yield s1 [i:i+1], None
        i += 1
    while i < l2 :
        yield None, s2 [i:i+1]
        i += 1
# end def paired_map

class Lazy_List :
    """List evalatuing a generator lazily.

       Idea stolen from Lib/test/test_generators.py of Python 2.2
    """

    def __init__ (self, generator) :
        self._data = []
        self._next = generator.next
    # end def __init__

    def __getitem__ (self, i) :
        try :
            last = i.stop
        except AttributeError :
            try :
                self._get (i + 1)
            except StopIteration :
                raise IndexError, i
            return self._data [i]
        else :
            try :
                self._get (last)
            except StopIteration :
                pass
            return self._data [i.start:i.stop]
    # end def __getitem__

    def _get (self, last) :
        data = self._data
        next = self._next
        while last > len (data) :
            data.append (next ())
    # end def _get

# end class Lazy_List

### unit-test code ############################################################

if __debug__ :
    import U_Test

    def _doc_test () :
        import Generators
        return U_Test.run_module_doc_tests (Generators)
    # end def _doc_test

    def _test () :
        _doc_test  ()
    # end def _test

    if __name__ == "__main__" :
        _test ()
# end if __debug__

### end unit-test code ########################################################

if __name__ == "__main__" :
    pass
else :
    from _TFL import TFL
    TFL._Export ("*")
### __END__ Generators
