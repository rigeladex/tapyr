# -*- coding: iso-8859-1 -*-
# Copyright (C) 1998-2005 Mag. Christian Tanzer. All rights reserved
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
#    TFL.predicate
#
# Purpose
#    Provide predicate-functions for iterables
#
# Revision Dates
#    19-Mar-1998 (CT) Creation
#     4-Apr-1998 (CT) `paired' renamed to `pairwise'
#                     `paired' added
#    26-Apr-1998 (CT) `paired'   implemented via `map' instead of `for'-loop
#    26-May-1998 (CT) `pairwise' implemented via `map' instead of `for'-loop
#    26-May-1998 (CT) `cartesian' added
#     3-Jun-1998 (CT) `xored_string' added
#    10-Jul-1998 (CT) `reversed'     added
#    28-Jan-1999 (CT) `split_by_key' added
#    28-Jan-1999 (CT) `intersection' defined here (was in `Math_Func.py')
#    19-Feb-1999 (CT) `matches'      added
#    22-Feb-1999 (CT) `common_head'  added
#    26-Feb-1999 (CT) `matches' renamed to `re_matches', `matches' added
#    13-Aug-1999 (CT) `bit_size_cmp' added
#    29-Oct-1999 (CT) `identity' and `cross_sum' added
#    23-Nov-1999 (CT) `random_string' added
#    27-Jan-2000 (CT) `extender' added and `flattened' optimized by map-ping it
#    10-Mar-2000 (CT) `relax' added
#    14-Mar-2000 (CT) `un_nested' added
#    24-Mar-2000 (CT) `flattened' uses `un_nested'
#    27-Mar-2000 (CT) `cartesian' changed to call `flattened' directly
#                     (using `apply' fails if a one-element list is passed
#                     into `flattened' -- `un_nested' then does too much of a
#                     good thing)
#     5-Apr-2000 (CT) Optional parameter `min_result_size' added to
#                     `split_by_key'
#    11-Apr-2000 (CT) `split_by_key' corrected (handle empty `seq' gracefully)
#     9-May-2000 (CT) `head_slices' added
#    30-May-2000 (CT) `byte_alignment' added
#    30-May-2000 (CT) `bit_size_cmp' tentatively changed to cmp regarding
#                     `byte_alignment'
#     8-Nov-2000 (CT) `has_substr' added
#     9-Jan-2001 (CT) Use `operator.add' instead of hone grown lambda
#     9-Jan-2001 (CT) `Indices' and `IV_Pairs' added
#     7-Mar-2001 (CT) Comment added to `relax'
#    20-Sep-2001 (AGO) `union' added
#    17-Dec-2001 (CT)  `extender` changed to apply `list`
#    11-Mar-2002 (CT)  `list_difference` added
#     4-Jul-2002 (CT)  `bit_alignment` added
#    29-Jul-2002 (CT)  `dsu_ed` added
#    29-Jul-2002 (CT)  `_predicate_22` and `_predicate_21` factored to be able
#                      to use generators where available
#     1-Aug-2002 (CT)  s/dsu_ed/dusort/g
#    29-Aug-2002 (CT)  `bit_size_decorator` added
#    06-Sep-2002 (RMA) Moved pairwise from '_predicate_21' because change
#                      change from 29-Jul does not work for pairwise.
#    13-Dec-2002 (CT)  `intersection_n` and `intersection_ns` added
#    14-Jan-2003 (CT)  `first` added
#     4-Feb-2003 (CT)  `sorted` argument added to `split_by_key`
#     4-Feb-2003 (CT)  `dusplit_by_key` added
#     5-Feb-2003 (CED) `dusplit_by_key` removed
#    11-Mar-2003 (CT)  `second` added
#    19-Mar-2003 (CED) `lists_equal` added
#     9-Apr-2003 (CT)  `dict_from_list` used
#    13-May-2003 (CED) `tupelize` added
#     5-Jun-2003 (CT)  `third` added
#     6-Jun-2003 (CT)  `sum` added if not there already (2.3 adds a builtin
#                      for this)
#    17-Jun-2003 (CED) `gcd`, `gcd_n`, `lcm`, `lcm_n` added
#     1-Jul-2003 (CED) `lcm_n` fixed
#     1-Aug-2003 (CT)  `rounded_up` and `rounded_down` added
#    13-Aug-2003 (CED) 'rounded_up` fixed
#    18-Aug-2003 (CT)  `pairwise` changed to use `zip` instead of `map`
#    29-Aug-2003 (CT)  Optional argument `sorted` removed from `split_by_key`
#    29-Aug-2003 (CT)  `dusplit` added
#    26-Oct-2003 (CT)  `all_true` and `any_true` added
#    26-Oct-2003 (CT)  `all_true_p` and `any_true_p` added
#    26-Oct-2003 (CT)  Ancient and obsolete `number_q`, `forall_q`, and
#                      `exists_q`
#    21-Nov-2003 (CT)  Stupid typo in `any_true` fixed
#    12-Dec-2003 (CT)  References to modules `string` and `types` removed
#    19-Feb-2004 (CED) `rotate_l/r` added
#     1-Apr-2004 (CT)  `apply` removed
#     1-Apr-2004 (CT)  `split_by_key`, `dusplit` and `common_head` changed to
#                      work with generators, too
#     1-Apr-2004 (CT)  Some doc-tests added
#     1-Apr-2004 (CT)  `flatten` added (didn't dare to remove `flattened`
#                      although that one dies if called with a single flat
#                      sequence as argument)
#     1-Apr-2004 (CT)  `cartesian` simplified by using list comprehension
#                      instead of `map`
#     2-Apr-2004 (CT)  Yesterday's `apply` removal reverted
#                      (sorry for the stupid breakage!)
#     2-Apr-2004 (CT)  `cartesian` changed to use `flattened` again
#    10-May-2004 (CED) `tripplewise`, `tripplewise_circle`,
#                      `pairwise_circle` added
#    11-May-2004 (CED) `is_contiguous` added
#    25-May-2004 (CED) Some doctests added
#    30-Jun-2004 (CT)  `list_difference` fixed to do what the doc-string
#                      claims it does
#    20-Oct-2004 (CED) Some doctests added, some `map` calls replaced by
#                      list comprehension
#    20-Oct-2004 (CED) `list` used where possible
#    15-Nov-2004 (CED) Second parameter of `dusort`, `dusplit` made optional
#    17-Nov-2004 (CED) `min_element`, `max_element` added
#    17-Nov-2004 (CED) Last changes reverted
#     1-Dec-2004 (CED) `fit_to_ceil_in_cycle` added
#    24-Mar-2005 (CT)  Moved into package `TFL` and removed
#                      various cruft
#    31-Mar-2005 (CED) `fit_to_ceil_in_cycle` re-added
#    ��revision-date�����
#--

from   _TFL             import TFL
import _TFL.Generators

### legacy aliases
IV_Pairs       = enumerate
dict_from_list = dict.fromkeys

def all_true (seq) :
    """Returns True if all elements of `seq` are true,
       otherwise returns first non-true element.
    """
    for e in seq :
        if not e :
            return e
    else :
        return True
# end def all_true

def all_true_p (seq, pred) :
    """Returns True if `pred` returns true for all elements of `seq`,
       otherwise returns first non-true element.
    """
    for e in seq :
        if not pred (e) :
            return e
    else :
        return True
# end def all_true

def any_true (seq) :
    """Returns first true element of `seq`, otherwise returns False."""
    for e in seq :
        if e :
            return e
    else :
        return False
# end def any_true

def any_true_p (seq, pred) :
    """Returns first element of `seq` for which `pred` returns True,
       otherwise returns False.
    """
    for e in seq :
        if pred (e) :
            return e
    else :
        return False
# end def any_true

def bit_alignment (bits) :
    """Returns alignment in powers of two of data with length `bits'

       >>> [(i, bit_alignment (i)) for i in range (0, 9)]
       [(0, 0), (1, 0), (2, 0), (3, 0), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1)]
       >>> [(i, bit_alignment (i)) for i in range (8, 33, 4)]
       [(8, 1), (12, 2), (16, 2), (20, 1), (24, 1), (28, 4), (32, 4)]
    """
    return byte_alignment ((bits + 4) >> 3)
# end def bit_alignment

def bit_size_cmp (l, r) :
    """Return comparison of two bit-sizes `l' and `r'.

       Integral byte sizes compare before sub-byte sizes, even sizes compare
       before odd sizes, larger values compare before smaller values.
    """
    return (  cmp (byte_alignment ((r+4) >> 3), byte_alignment ((l+4) >> 3))
           or cmp (r, l)
           )
# end def bit_size_cmp

def bit_size_decorator (bs) :
    """Return a decorator for dusorting' by bit-size `bs`.

       Integral byte sizes compare before sub-byte sizes, even sizes compare
       before odd sizes, larger values compare before smaller values.
    """
    return - byte_alignment ((bs + 4) >> 3), - bs
# end def bit_size_decorator

def byte_alignment (bytes) :
    """Returns alignment in powers of two of data with length `bytes'

       >>> [(i, byte_alignment (i)) for i in range (-3, 3)]
       [(-3, 1), (-2, 2), (-1, 1), (0, 0), (1, 1), (2, 2)]
       >>> [(i, byte_alignment (i)) for i in range (3, 10)]
       [(3, 1), (4, 4), (5, 1), (6, 2), (7, 1), (8, 8), (9, 1)]
    """
    return (bytes ^ (bytes - 1)) & bytes
# end def byte_alignment

def cartesian (s1, s2, combiner = None) :
    """Returns the cartesian product of the sequences `s1' and `s2'.

       >>> l = (3, 1, 7)
       >>> cartesian (l, l)
       [(3, 3), (3, 1), (3, 7), (1, 3), (1, 1), (1, 7), (7, 3), (7, 1), (7, 7)]
    """
    if combiner is None :
        combiner = paired
    result = [combiner ((x, ) * len (s2), s2) for x in s1]
    return flattened (result)
# end def cartesian

def cartesian_n (s1, s2, * si) :
    """Returns the cartesian product of all the sequences given.

       >>> l = (3, 1, 7)
       >>> cartesian_n (l, l)
       [(3, 3), (3, 1), (3, 7), (1, 3), (1, 1), (1, 7), (7, 3), (7, 1), (7, 7)]
       >>> l = (3, 1)
       >>> cartesian_n (l, l, l)
       [(3, 3, 3), (3, 3, 1), (3, 1, 3), (3, 1, 1), (1, 3, 3), (1, 3, 1), (1, 1, 3), (1, 1, 1)]
    """
    result = cartesian (s1, s2)
    for s in si :
        result = cartesian \
            ( result, s
            , lambda a, b : map (lambda l, r : l + (r, ), a, b)
            )
    return result
# end def cartesian_n

def common_head (list) :
    """Return common head of all strings in `list'.
       >>> common_head ([])
       ''
       >>> common_head (["a"])
       'a'
       >>> common_head (["a", "b"])
       ''
       >>> common_head (["ab", "ac", "b"])
       ''
       >>> common_head (["ab", "ac", "ab"])
       'a'
       >>> common_head (["abc", "abcde", "abcdxy"])
       'abc'
    """
    result = ""
    list   = sorted (list)
    if list :
        match = [(l == r and r) or "\0"
                for (l, r) in zip (list [0], list [-1])
                ]
        try :
            last = match.index ("\0")
        except ValueError :
            last = len (match)
        result = "".join (match [:last])
    return result
# end def common_head

def cross_sum (seq, fct = None) :
    """Returns the sum over all elements of `seq' passed trough `fct'.

       `fct' must be a function taking one argument and returning something
       that can be added.
    """
    if fct is None :
        fct = identity
    return sum ([fct (x) for x in seq])
# end def cross_sum

def dusort (seq, decorator) :
    """Returns a sorted copy of `seq`. The sorting is done over a decoration
       of the form `decorator (p), i, p for (i, p) in enumerate (seq)`.

       >>> dusort ([1, 3, 5, 2, 4], lambda e : -e)
       [5, 4, 3, 2, 1]
    """
    temp = [(decorator (p), i, p) for (i, p) in enumerate (seq)]
    temp.sort ()
    return [p [-1] for p in temp]
# end def dusort

def dusplit (seq, decorator, min_result_size = 1) :
    """Returns a list of lists each containing the elements of `seq'
       comparing equal under `decorator` (`dusplit` is to `split_by_key` what
       `dusort` is to `sorted`).

       >>> dusplit ([(0,1), (1,1), (0,2), (0,3), (2,3)], lambda x : x [0])
       [[(0, 1), (0, 2), (0, 3)], [(1, 1)], [(2, 3)]]
       >>> dusplit ([(0,1), (1,1), (0,2), (0,3), (2,3)], lambda x : x [1])
       [[(0, 1), (1, 1)], [(0, 2)], [(0, 3), (2, 3)]]
    """
    result = [[]]
    temp   = [(decorator (p), i, p) for (i, p) in enumerate (seq)]
    if temp :
        temp.sort ()
        for (a, b) in TFL.pairwise (temp) :
            result [-1].append (a [-1])
            if a [0] != b [0] :
                result.append ([])
        result [-1].append (temp [-1] [-1])
    if len (result) < min_result_size :
        result = result + ([[]] * (min_result_size - len (result)))
    return result
# end def dusplit

def extender (l, tail) :
    """Return list `l' extended by `tail' (`l' is changed in place!)

       >>> extender ([1, 2, 3], (4, 5))
       [1, 2, 3, 4, 5]
       >>> extender ([], [1])
       [1]
    """

    l [len (l):] = list (tail)
    return l
# end def extender

def first (x, * args, ** kw) :
    """Returns the first argument unchanged"""
    return x
# end def first

### Gimme a better name, please, please
def fit_to_ceil_in_cycle (n, ceil, cycle) :
    """
       >>> fit_to_ceil_in_cycle (3, 5, 10)
       3
       >>> fit_to_ceil_in_cycle (5, 3, 10)
       -5
    """
    while (n > ceil) :
        n -= cycle
    return n
# end def fit_to_ceil_in_cycle

def flatten (* lists) :
    """Returns a list containing all the elements in `lists'.

       >>> flatten (range (3))
       [0, 1, 2]
       >>> flatten (range (3), range (2))
       [0, 1, 2, 0, 1]
       >>> flatten ((range (3), range (2)))
       [[0, 1, 2], [0, 1]]
    """
    result = []
    for l in lists :
        result.extend (un_nested (l))
    return result
# end def flatten

def flattened (* lists) :
    """Returns a list containing all the elements in `lists'.

       >>> flattened (range (3), range (2))
       [0, 1, 2, 0, 1]
       >>> flattened ((range (3), range (2)))
       [0, 1, 2, 0, 1]
    """
    result = []
    map      (lambda l, r = result : extender (r, l), un_nested (lists))
    return   result
# end def flattened

def has_substr (s, subs) :
    """Returns true if `s' contains `subs'"""
    return s.find (subs) >= 0
# end def has_substr

def head_slices (l) :
    """Returns the list of all slices anchored at head of `l'

       >>> head_slices ("abcdef")
       ['a', 'ab', 'abc', 'abcd', 'abcde', 'abcdef']
    """
    return map (lambda i, l = l : l [:i], range (1, len (l) + 1))
# end def head_slices

def identity (x) :
    """Returns its argument unchanged"""
    return x
# end def identity

def intersection (l, r) :
    """Compute intersection of lists `l' and `r'.

       >>> intersection (range (4), range (2,5))
       [2, 3]
    """
    return filter (dict_from_list (l).has_key, r)
# end def intersection

def intersection_n (* lists) :
    """Compute intersection of `lists`."""
    tab = {}
    N   = len (lists)
    for l in lists :
        for x in l :
            tab [x] = tab.get (x, 0) + 1
    result = [x for (x, n) in tab.items () if n == N]
    result.sort ()
    return result
# end def intersection_n

def intersection_ns (lists) :
    return intersection_n (* lists)
# end def intersection_ns

def is_contiguous (seq) :
    """Tells whether the seqence of integers in `seq` is contiguous

       >>> is_contiguous ([1, 2, 3, 4, 5])
       True
       >>> is_contiguous ([10, 8, 9])
       True
       >>> is_contiguous ([42])
       True
       >>> is_contiguous ([])
       True
       >>> is_contiguous ([1, 3, 4])
       False
    """
    for l, r in TFL.pairwise (sorted (seq)) :
        if (r - l) != 1 :
            return False
    return True
# end def is_contiguous

def list_difference (l, r) :
    """Compute difference of `l` and `r`.

       >>> range (3), range (2,5)
       ([0, 1, 2], [2, 3, 4])
       >>> list_difference (range (3), range (2, 5))
       [0, 1]
       >>> list_difference (range (10), range (3))
       [3, 4, 5, 6, 7, 8, 9]
    """
    tab = dict_from_list (r)
    return [y for y in l if not tab.has_key (y) ]
# end def list_difference

def lists_equal (l, r) :
    """True if set of elements of `l` and `r` is equal.

       >>> l = range (3)
       >>> r = l[::-1]
       >>> l,r
       ([0, 1, 2], [2, 1, 0])
       >>> lists_equal (l, r)
       True
    """
    return dict_from_list (l) == dict_from_list (r)
# end def lists_equal

def matches (list, txt, prefix = "^") :
    """Returns all strings in `list' starting with `txt'.

       If you pass an empty string for `prefix', `matches' returns all
       elements containing `txt'.
    """
    import re
    return re_matches (list, re.compile (prefix + re.escape (txt)))
# end def matches

def paired (s1, s2) :
    """Returns a list of pairs
       `((s1 [0], s2 [0]), ... (s1 [n-1], s2 [n-1]))'.

       >>> paired ([1, 2, 3], [1, 2, 3])
       [(1, 1), (2, 2), (3, 3)]
       >>> paired ([1, 2, 3], [1])
       [(1, 1), (2, None), (3, None)]
       >>> paired ([1], [1, 2, 3])
       [(1, 1), (None, 2), (None, 3)]
       >>> paired ([], [])
       []
    """
    return map (None, s1, s2)
# end def paired

def pairwise_circle (seq) :
    """Returns a list of pairs of a circle of sequence `seq`

       >>> list (pairwise_circle ([1, 2, 3, 4, 5]))
       [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)]
       >>> list (pairwise_circle ([1, 2]))
       [(1, 2), (2, 1)]
       >>> list (pairwise_circle ([1]))
       [(1, 1)]
       >>> list (pairwise_circle ([]))
       []
    """
    return TFL.pairwise (seq + seq [0:1])
# end def pairwise_circle

def random_string (length, char_range = 127, char_offset = 128) :
    """Returns a string of `length' random characters in the interval
       (`char_offset', `char_offset + char_range').
    """
    from random import random
    return "".join \
        ( [   chr (int (random () * char_range + char_offset))
          for c in range (length)
          ]
        )
# end def random_string

def relax (* args, ** kw) :
    """Dismisses its arguments"""
    pass
# end def relax

def reversed (seq) :
    """Returns a reversed copy of `seq'.

       >>> reversed ([1, 2, 3, 4, 5])
       [5, 4, 3, 2, 1]
       >>> reversed ([1])
       [1]
       >>> reversed ([])
       []
    """
    result = list (seq)
    result.reverse ()
    return result
# end def reversed

def re_matches (list, pat) :
    """Returns all strings in `list' matching the regular expression `pat'."""
    if isinstance (pat, (str, unicode)) :
        import re
        pat = re.compile (pat)
    return [ s for s in list
               if  isinstance (s, (str, unicode)) and pat.search (s)
           ]
# end def re_matches

def rotate_l (sequence) :
    """Return a copy of sequence that is rotated left by one element

       >>> rotate_l ([1, 2, 3])
       [2, 3, 1]
       >>> rotate_l ([1])
       [1]
       >>> rotate_l ([])
       []
    """
    return sequence [1:] + sequence [:1]
# end def rotate_l

def rotate_r (sequence) :
    """Return a copy of sequence that is rotated right by one element

       >>> rotate_r ([1, 2, 3])
       [3, 1, 2]
       >>> rotate_r ([1])
       [1]
       >>> rotate_r ([])
       []
    """
    return sequence [-1:] + sequence [:-1]
# end def rotate_r

def rounded_down (value, granularity) :
    """Returns `value` rounded down to nearest multiple of `granularity`.

       >>> rounded_down (3, 5)
       0
       >>> rounded_down (8, 5)
       5
       >>> rounded_down (5, 5)
       5
       >>> rounded_down (-3, 5)
       -5
       >>> rounded_down (-8, 5)
       -10
    """
    return value - (value % granularity)
# end def rounded_down

def rounded_up (value, granularity) :
    """Returns `value` rounded up to nearest multiple of `granularity`.

       >>> rounded_up (3, 5)
       5
       >>> rounded_up (8, 5)
       10
       >>> rounded_up (-3, 5)
       0
       >>> rounded_up (-8, 5)
       -5
    """
    return value + ((granularity - value) % granularity)
# end def rounded_up

def second (x, y, * args, ** kw) :
    """Returns the second argument unchanged"""
    return y
# end def second

def sorted (seq, pred = cmp) :
    """Returns a sorted copy of `seq'.

       >>> sorted ([1, 3, 5, 2, 4])
       [1, 2, 3, 4, 5]
       >>> sorted ([1, 3, 5, 2, 4], lambda l, r : cmp (-l, -r))
       [5, 4, 3, 2, 1]
       >>> sorted ([1, 2, 2, 1])
       [1, 1, 2, 2]
       >>> sorted ([])
       []
    """
    result = list (seq)
    result.sort (pred)
    return result
# end def sorted

def split_by_key (seq, key_cmp, min_result_size = 1) :
    """Returns a list of lists each containing the elements of `seq' with a
       single key as determined by `key_cmp'.

       The result is sorted by `key_cmp'.
    """
    result = [[]]
    source = sorted (seq, key_cmp)
    if source :
        for (a, b) in TFL.pairwise (source) :
            result [-1].append (a)
            if key_cmp (a, b) != 0 :
                result.append ([])
        result [-1].append (source [-1])
    if len (result) < min_result_size :
        result = result + ([[]] * (min_result_size - len (result)))
    return result
# end def split_by_key

def string_cross_sum (string) :
    return cross_sum (string, ord)
# end def string_cross_sum

def tail_slices (l) :
    """Returns the list of all slices anchored at tail of `l'

       >>> tail_slices ("abcdef")
       ['abcdef', 'bcdef', 'cdef', 'def', 'ef', 'f']
    """
    return map (lambda i, l = l : l [i:], range (len (l)))
# end def tail_slices

def third (x, y, z, * args, ** kw) :
    """Returns the third argument unchanged"""
    return z
# end def third

def tupelize (l) :
    """Converts every occurance of a list to a tuple. Afterwards `l` should
       be hashable.

       >>> tupelize ([1, 2, 3])
       (1, 2, 3)
       >>> tupelize ([])
       ()
       >>> tupelize ([1, 2, [3], [4, [5, 6]]])
       (1, 2, (3,), (4, (5, 6)))
    """
    if isinstance (l, (str, unicode)) :
        return l
    try:
        l = list (l)
        for i, e in enumerate (l) :
            l [i] = tupelize (e)
        return tuple (l)
    except TypeError :
        return l
# end def tupelize

def tupled (* seqs) :
    """Returns a list of tuples of corresponding elements of each of `seqs'.

       >>> tupled ([1, 2, 3], [1], [])
       [(1, 1, None), (2, None, None), (3, None, None)]
       >>> tupled ()
    """
    if seqs :
        return apply (map, (None, ) + seqs)
    else :
        return None
# end def tupled

def union (* lists) :
    """Compute the union of lists.

       >>> union (range (3), range (42, 45))
       [0, 1, 2, 42, 43, 44]
    """
    tab = {}
    for l in lists :
        map (lambda x, tab = tab : tab.update  ({x : 1}), l)
    return tab.keys ()
# end def union

def un_nested (l) :
    """Returns list `l' in un-nested form (i.e., if it is a one-element list
       whose first element is a list, returns l [0]).

       This is handy if you want to support the passing of a list to a `*
       args' argument without using `apply'.

       >>> un_nested (range (3))
       [0, 1, 2]
       >>> un_nested ([range (3)])
       [0, 1, 2]
       >>> un_nested ([range (3), range (2)])
       [[0, 1, 2], [0, 1]]
    """
    if (   l
       and len  (l) == 1
       and isinstance (l [0], (list, tuple))
       ) :
        l = l [0]
    return l
# end def un_nested

def xored_string (source, salt = "�") :
    salt = ord (salt)
    return "".join ([chr (ord (c) ^ salt) for c in source])
# end def xored_string

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.predicate
