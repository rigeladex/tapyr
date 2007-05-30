# -*- coding: iso-8859-1 -*-
# Copyright (C) 2007 TTTech Computertechnik AG. All rights reserved.
# Schoenbrunnerstrasse 7, 1040 Wien, Austria. office@tttech.com
#
#++
# Name
#    TFL.Bit_Calculation
#
# Purpose
#    various calculations concering bits of integers
#
# Revision Dates
#    30-May-2007 (DAL) Creation
#    ««revision-date»»···
#--

import sys

from  _TFL import TFL

def bit_value (v, bit) :
    """Returns the value of the specified `bit` of the given value `v`.

    >>> [bit_value ( 0,x) for x in range (32)] == [0] * 32
    True
    >>> [bit_value (-1,x) for x in range (32)] == [1] * 32
    True
    >>> [bit_value (13,x) for x in range (4)]
    [1, 0, 1, 1]
    """
    assert isinstance (v, int) or isinstance (v, long), type (v)
    assert bit >= 0, bit
    return int ((v >> bit) & 1)
# end def bit_value

def highest_bit_set (v) :
    """Returns the bit position of the highest bit which is set.

    >>> [highest_bit_set (x) for x in range (1,11)]
    [0, 1, 1, 2, 2, 2, 2, 3, 3, 3]
    >>> highest_bit_set (sys.maxint)
    30
    >>> highest_bit_set (~sys.maxint)
    31
    >>> highest_bit_set (sys.maxint + 1)
    31
    >>> cnt = sys.maxint + 1
    >>> l   = []
    >>> while cnt :
    ...   l.append (highest_bit_set (cnt))
    ...   cnt = int (cnt >> 1)
    >>> l == list (reversed (range (32)))
    True
    >>> highest_bit_set ((1L << 400) - 1)
    399
    >>> highest_bit_set (0)
    Traceback (most recent call last):
      ...
    ValueError: v must not be equal 0
    """
    assert isinstance (v, int) or isinstance (v, long), type (v)
    if v < 0 :
        if isinstance (v, int) :
            v &= sys.maxint * 2 + 1
        else :
            assert False, (type(v), v)
    elif not v :
        raise ValueError ("v must not be equal 0")
    count = 0
    while v :
        v    >>= 1
        count += 1
    return count - 1
# end def highest_bit_set

def lowest_bit_set (v) :
    """Returns the bit position of the lowest bit which is set.

    >>> [lowest_bit_set (x) for x in range (1,11)]
    [0, 1, 0, 2, 0, 1, 0, 3, 0, 1]
    >>> lowest_bit_set (0)
    Traceback (most recent call last):
      ...
    ValueError: v must not be equal 0
    >>> [lowest_bit_set (-x) for x in range (1,11)]
    [0, 1, 0, 2, 0, 1, 0, 3, 0, 1]
    >>> lowest_bit_set (1L << 400)
    400
    >>> lowest_bit_set ((1L << 400) - 1)
    0
    """
    assert isinstance (v, int) or isinstance (v, long), type (v)
    if v :
        bit   = 1L
        count = 0
        while not (v & bit) :
            bit  <<= 1
            count += 1
        return count
    else :
        raise ValueError ("v must not be equal 0")

def no_of_bits_set (v) :
    """Counts the number of set bits of an integer or positive long  value.

    >>> [no_of_bits_set (x) for x in range (10)]
    [0, 1, 1, 2, 1, 2, 2, 3, 1, 2]
    >>> no_of_bits_set (sys.maxint)
    31
    >>> [no_of_bits_set (-x) for x in range(10)]
    [0, 32, 31, 31, 30, 31, 30, 30, 29, 31]
    """
    assert isinstance (v, int) or isinstance (v, long), type (v)
    if v < 0 :
        if isinstance (v, int) :
            v &= sys.maxint * 2 + 1
        else :
            assert False, (type(v), v)
    bit   = 1L
    count = 0
    while bit <= v :
        if bit & v :
            count += 1
        bit <<= 1
    return count
# end def no_of_bits_set

def no_of_bits_unset (v) :
    """Counts the nober of unset bits of an integer value.

    >>> [no_of_bits_unset (x) for x in range (10)]
    [32, 31, 31, 30, 31, 30, 30, 29, 31, 30]
    >>> no_of_bits_unset (sys.maxint)
    1
    >>> no_of_bits_unset (0)
    32
    >>> [no_of_bits_unset (-x) for x in range (10)]
    [32, 0, 1, 1, 2, 1, 2, 2, 3, 1]
    """
    assert isinstance (v,int), type (v)
    return no_of_bits_set (~v)
# end def no_of_bits_unset

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.Bit_Calculation
