# -*- coding: iso-8859-1 -*-
# Copyright (C) 2002-2005 Mag. Christian Tanzer. All rights reserved
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
#    ««revision-date»»···
#--

from __future__ import generators

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
       [('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'e'), ('e', 'f')]
       >>> list (pairwise (range (4)))
       [(0, 1), (1, 2), (2, 3)]
    """
    lag = Look_Ahead_Gen (seq)
    for h in lag :
        if lag :
            yield h, lag.succ
# end def pairwise

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

def _faculty () :
    """Generator used to create a lazy evaluating list
       of Faculties

       >>> Faculties [3]
       6
       >>> Faculties [5]
       120
    """
    yield 0
    x, y = 1, 2
    while True :
        yield x
        x, y = x * y, y + 1
# end def _faculty

def _fib () :
    """Generator used to create a lazy evaluating list
       of Fibonacci numbers

       >>> Fibonacci [0:7]
       [0, 1, 1, 2, 3, 5, 8]
       >>> Fibonacci [25]
       75025
    """
    x, y = 0, 1
    while True :
        yield x
        x, y = y, x + y
# end def _fib

def _prime () :
    """Generator used to create a lazy evaluating list
       of Primes

       >>> Primes [0:7]
       [2, 3, 5, 7, 11, 13, 17]
       >>> Primes [100]
       547
    """
    yield 2
    primes = [2, 3]
    while True :
        yield primes [-1]
        candidate = primes [-1] + 2
        while True :
            is_prime = True
            for p in primes :
                if (candidate % p) == 0 :
                    is_prime = False
                    break
                if (p*p > candidate) :
                    break
            if is_prime :
                primes.append (candidate)
                break
            candidate += 2
# end def _prime

### Lazy evaluating list of Fibonacci numbers
Fibonacci = Lazy_List (_fib   ())
### Lazy evaluating list of Primes
Primes    = Lazy_List (_prime ())
### Lazy evaluating list of Faculties
Faculties = Lazy_List (_faculty ())
### unit-test code ############################################################

if __debug__ :
    import U_Test

    def _doc_test () :
        return U_Test.run_module_doc_tests ("_TFL.Generators")
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
### __END__ TFL.Generators
