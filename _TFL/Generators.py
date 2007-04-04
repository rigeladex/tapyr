# -*- coding: iso-8859-1 -*-
# Copyright (C) 2002-2007 Mag. Christian Tanzer. All rights reserved
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
#    TFL.Generators
#
# Purpose
#    Provide useful generators
#
# Revision Dates
#    18-Apr-2002 (CT) Creation
#    19-Apr-2002 (CT) `Lazy_List` added
#    29-Jul-2002 (CT) s/paired/paired_zip/
#     6-Oct-2003 (CT) s/paired/paired_zip/ in doc-string, too
#     9-Mar-2004 (CT) `_doc_test` changed to not use `import`
#    30-Jul-2004 (CT) `Look_Ahead_Gen` added
#    30-Jul-2004 (CT) `pairwise` changed to use `Look_Ahead_Gen`
#    12-Aug-2004 (CT) Additional doctest for `Look_Ahead_Gen` added to show
#                     behavior for single element sequence
#    21-Sep-2004 (CT) `Look_Ahead_Gen` changed to call `.next` lazily instead
#                     of (over)-eagerly
#    26-Oct-2004 (CT) `alt_iter` added
#     9-Feb-2005 (CED) `Lazy_List` fixed to handle step`ed slices and doctest
#                      added
#     9-Feb-2005 (CED) `Fibonacci`, `Primes` added (moved from _YAGNI to here)
#    15-Feb-2005 (CED) `Faculties` added (moved from _YAGNI to here)
#    24-Mar-2005 (CT)  Cruft removed (recent additions by CED and Python
#                      legacies)
#     1-Jul-2005 (CT)  `pairwise_circle` defined here
#     8-Dec-2006 (CT)  `window_wise` added
#    16-Feb-2007 (CT)  `enumerate_slice` added
#     1-Mar-2007 (CT)  Adapted to signature change of `DL_Ring`
#    ««revision-date»»···
#--

from _TFL import TFL

def alt_iter (* iterables) :
    """Alternating iterator

       >>> s1 = range (4)
       >>> s2 = [chr (i + 65) for i in range (3)]
       >>> s3 = range (42, 55, 3)
       >>> list (alt_iter ())
       []
       >>> list (alt_iter (s1))
       [0, 1, 2, 3]
       >>> list (alt_iter (s1, s2))
       [0, 'A', 1, 'B', 2, 'C', 3]
       >>> list (alt_iter (s2, s1))
       ['A', 0, 'B', 1, 'C', 2, 3]
       >>> list (alt_iter (s1, s2, s3))
       [0, 'A', 42, 1, 'B', 45, 2, 'C', 48, 3, 51, 54]
    """
    iters = [iter (x) for x in iterables]
    while iters :
        i = 0
        while i < len (iters) :
            try :
                yield iters [i].next ()
            except StopIteration :
                del iters [i]
            else :
                i += 1
# end def alt_iter

class Look_Ahead_Gen (object) :
    """Wrap a generator/iterator to provide look ahead

       >>> for i in Look_Ahead_Gen (range (3)) :
       ...   print i
       ...
       0
       1
       2
       >>> lag = Look_Ahead_Gen (range (1))
       >>> for i in lag :
       ...   print i, lag.is_finished
       ...
       0 True
       >>> lag = Look_Ahead_Gen (range (3))
       >>> for i in lag :
       ...   print i, lag.is_finished
       ...
       0 False
       1 False
       2 True
    """

    is_finished        = property (lambda s : not s)

    def __init__ (self, source) :
        self.source    = source    = iter (source)
        self._sentinel = self.succ = object ()
    # end def __init__

    def __nonzero__ (self) :
        try :
            if self.succ is self._sentinel :
                self.succ = self.source.next ()
        except StopIteration :
            return False
        return True
    # end def __nonzero__

    def __iter__ (self) :
        source    = self.source
        _sentinel = self._sentinel
        while True :
            if self.succ is _sentinel :
                next      = source.next ()
            else :
                next      = self.succ
                self.succ = _sentinel
            yield next
    # end def __iter__

# end class Look_Ahead_Gen

def enumerate_slice (seq, head, tail = None) :
    """Generate `index, value` pairs for slice `seq [head:tail]`.

       >>> tuple (enumerate_slice (range (7), 0))
       ((0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6))
       >>> tuple (enumerate_slice (range (20), 5, 10))
       ((5, 5), (6, 6), (7, 7), (8, 8), (9, 9))
       >>> tuple (enumerate_slice ("abcdefghijklmnopqrstuvwxyz", 20))
       ((20, 'u'), (21, 'v'), (22, 'w'), (23, 'x'), (24, 'y'), (25, 'z'))
    """
    i = head
    for v in seq [head:tail] :
        yield i, v
        i += 1
# end def enumerate_slice

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

def pairwise (seq) :
    """Generates a list of pairs `(seq [0:1], seq [1:2], ..., seq [n-1:n])'.

       >>> list (pairwise ("abcdef"))
       [('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'e'), ('e', 'f')]
       >>> list (pairwise (range (4)))
       [(0, 1), (1, 2), (2, 3)]
       >>> list (pairwise ([1]))
       []
       >>> list (pairwise ([]))
       []
    """
    lag = Look_Ahead_Gen (seq)
    for h in lag :
        if lag :
            yield h, lag.succ
# end def pairwise

def pairwise_circle (seq) :
    """Generates a list of pairs of a circle of iterable `seq`

       >>> list (pairwise_circle ([1, 2, 3, 4, 5]))
       [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)]
       >>> list (pairwise_circle ([1, 2]))
       [(1, 2), (2, 1)]
       >>> list (pairwise_circle ([1]))
       [(1, 1)]
       >>> list (pairwise_circle ([]))
       []
    """
    lag = Look_Ahead_Gen (seq)
    if lag :
        head = lag.succ
        for h in lag :
            if lag :
                yield h, lag.succ
        yield h, head ### close circle
# end def pairwise_circle

def paired_zip (s1, s2) :
    """Generates a list of pairs `((s1 [0], s2 [0]), ... (s1 [-1], s2 [-1]))'.

       >>> list (paired_zip ("abc", range (4)))
       [('a', 0), ('b', 1), ('c', 2)]
    """
    s1 = iter (s1)
    s2 = iter (s2)
    while True :
        yield s1.next (), s2.next ()
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

       >>> def ones () :
       ...     while True :
       ...         yield 1
       ...
       >>> ol = Lazy_List (ones ())
       >>> ol [3]
       1
       >>> ol [0]
       1
       >>> ol [:7]
       [1, 1, 1, 1, 1, 1, 1]
       >>> ol [100:102]
       [1, 1]
       >>> def range_5 () :
       ...     for i in range (5) :
       ...         yield i
       ...
       >>> rl = Lazy_List (range_5 ())
       >>> rl [3]
       3
       >>> try :
       ...     rl [5]
       ... except IndexError :
       ...     print "OK"
       ...
       OK
       >>> rl [::2]
       [0, 2, 4]
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
            return self._data [i.start:i.stop:i.step]
    # end def __getitem__

    def _get (self, last) :
        data = self._data
        next = self._next
        while last > len (data) :
            data.append (next ())
    # end def _get

# end class Lazy_List

def window_wise (seq, size) :
    """Return all windows of `size` elements in `seq`.

       >>> list (window_wise (range (5), 1))
       [(0,), (1,), (2,), (3,), (4,)]
       >>> list (window_wise (range (5), 2))
       [(0, 1), (1, 2), (2, 3), (3, 4)]
       >>> list (window_wise (range (5), 3))
       [(0, 1, 2), (1, 2, 3), (2, 3, 4)]
       >>> list (window_wise (range (5), 4))
       [(0, 1, 2, 3), (1, 2, 3, 4)]
       >>> list (window_wise (range (5), 5))
       [(0, 1, 2, 3, 4)]
       >>> list (window_wise (range (5), 6))
       []
    """
    from _TFL.DL_List import DL_Ring
    s = iter  (seq)
    h = tuple ((s.next () for i in range (size)))
    if len (h) == size :
        w = DL_Ring (h)
        yield tuple (w.values ())
        while True:
            w.pop_front ()
            w.append    (s.next ())
            yield tuple (w.values ())
# end def window_wise

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.Generators
