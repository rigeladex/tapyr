# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004-2005 Mag. Christian Tanzer. All rights reserved
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
#    TFL.binary_string
#
# Purpose
#    Convert integers to/from string in binary representation
#
# Revision Dates
#    25-Feb-2004 (CT) Creation
#     9-Mar-2004 (CT)  `_doc_test` changed to not use `import`
#    20-Jul-2005 (GKH) `int_to_binary_string` with additional parameter
#                      `min_digits` (RUP 16885)
#    26-Sep-2005 (GKH) `int_to_binary_string` trims leading zeros (RUP 16885)
#    23-Jul-2007 (CED) Activated absolute_import
#    ��revision-date�����
#--
from __future__ import absolute_import


from   _TFL           import TFL

_eight_bit_mask   = 0xFF
_eight_bits_table = \
    ( "00000000", "00000001", "00000010", "00000011"
    , "00000100", "00000101", "00000110", "00000111"
    , "00001000", "00001001", "00001010", "00001011"
    , "00001100", "00001101", "00001110", "00001111"
    , "00010000", "00010001", "00010010", "00010011"
    , "00010100", "00010101", "00010110", "00010111"
    , "00011000", "00011001", "00011010", "00011011"
    , "00011100", "00011101", "00011110", "00011111"
    , "00100000", "00100001", "00100010", "00100011"
    , "00100100", "00100101", "00100110", "00100111"
    , "00101000", "00101001", "00101010", "00101011"
    , "00101100", "00101101", "00101110", "00101111"
    , "00110000", "00110001", "00110010", "00110011"
    , "00110100", "00110101", "00110110", "00110111"
    , "00111000", "00111001", "00111010", "00111011"
    , "00111100", "00111101", "00111110", "00111111"
    , "01000000", "01000001", "01000010", "01000011"
    , "01000100", "01000101", "01000110", "01000111"
    , "01001000", "01001001", "01001010", "01001011"
    , "01001100", "01001101", "01001110", "01001111"
    , "01010000", "01010001", "01010010", "01010011"
    , "01010100", "01010101", "01010110", "01010111"
    , "01011000", "01011001", "01011010", "01011011"
    , "01011100", "01011101", "01011110", "01011111"
    , "01100000", "01100001", "01100010", "01100011"
    , "01100100", "01100101", "01100110", "01100111"
    , "01101000", "01101001", "01101010", "01101011"
    , "01101100", "01101101", "01101110", "01101111"
    , "01110000", "01110001", "01110010", "01110011"
    , "01110100", "01110101", "01110110", "01110111"
    , "01111000", "01111001", "01111010", "01111011"
    , "01111100", "01111101", "01111110", "01111111"
    , "10000000", "10000001", "10000010", "10000011"
    , "10000100", "10000101", "10000110", "10000111"
    , "10001000", "10001001", "10001010", "10001011"
    , "10001100", "10001101", "10001110", "10001111"
    , "10010000", "10010001", "10010010", "10010011"
    , "10010100", "10010101", "10010110", "10010111"
    , "10011000", "10011001", "10011010", "10011011"
    , "10011100", "10011101", "10011110", "10011111"
    , "10100000", "10100001", "10100010", "10100011"
    , "10100100", "10100101", "10100110", "10100111"
    , "10101000", "10101001", "10101010", "10101011"
    , "10101100", "10101101", "10101110", "10101111"
    , "10110000", "10110001", "10110010", "10110011"
    , "10110100", "10110101", "10110110", "10110111"
    , "10111000", "10111001", "10111010", "10111011"
    , "10111100", "10111101", "10111110", "10111111"
    , "11000000", "11000001", "11000010", "11000011"
    , "11000100", "11000101", "11000110", "11000111"
    , "11001000", "11001001", "11001010", "11001011"
    , "11001100", "11001101", "11001110", "11001111"
    , "11010000", "11010001", "11010010", "11010011"
    , "11010100", "11010101", "11010110", "11010111"
    , "11011000", "11011001", "11011010", "11011011"
    , "11011100", "11011101", "11011110", "11011111"
    , "11100000", "11100001", "11100010", "11100011"
    , "11100100", "11100101", "11100110", "11100111"
    , "11101000", "11101001", "11101010", "11101011"
    , "11101100", "11101101", "11101110", "11101111"
    , "11110000", "11110001", "11110010", "11110011"
    , "11110100", "11110101", "11110110", "11110111"
    , "11111000", "11111001", "11111010", "11111011"
    , "11111100", "11111101", "11111110", "11111111"
    )

def int_to_binary_string (i, min_digits = 8) :
    """Returns a string representing the integer `i` in binary.

       >>> int_to_binary_string (0)
       '00000000'
       >>> len (int_to_binary_string (0)) == 8
       True
       >>> int_to_binary_string (1)
       '00000001'
       >>> int_to_binary_string (341)
       '101010101'
       >>> int_to_binary_string (1, 10)
       '0000000001'
       >>> [int_to_binary_string(i) == _eight_bits_table[i] for i in range(8)]
       [True, True, True, True, True, True, True, True]
       >>> [ binary_string_to_int (int_to_binary_string (i)) == i
       ... for i in (0, 1, 42, 255, 256, 1023, 100000, 1000000)]
       [True, True, True, True, True, True, True, True]
    """
    bits = []
    while i > 0 :
        k = i &  _eight_bit_mask
        i = i >> 8
        bits.append (_eight_bits_table [k])
    bits.reverse ()
    result = "".join (bits or _eight_bits_table [0]).lstrip ("0")
    if len (result) < min_digits :
        return "0" * (min_digits - len (result)) + result
    else :
        return result
# end def int_to_binary_string

def binary_string_to_int (s) :
    """Returns the integer represented by string `s` in binary form"""
    return int (s, 2)
# end def binary_string_to_int

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.binary_string
