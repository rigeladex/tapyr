# -*- coding: iso-8859-1 -*-
# Copyright (C) 1998-2004 Mag. Christian Tanzer. All rights reserved
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
#    TFL.B64
#
# Purpose
#    Provide conversion to/from strings in Base64 number system
#
# Revision Dates
#    27-Nov-1998 (CT) Creation
#    12-Sep-2004 (CT) Factored from B64.py in lib/python
#    12-Sep-2004 (CT) `_ord_map` changed (sequence of characters in sorted
#                     order, `.` replaced by `_`)
#    12-Sep-2004 (CT) Optional parameters added to `atoi` and `itoa`
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ««revision-date»»···
#--



_base    = 64
_chars   = "0123456789=ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz"
_ord_map = {}
for i, c in enumerate (_chars) :
    _ord_map [i] = c
    _ord_map [c] = i

def atoi (string, _ord_map = _ord_map) :
    """Convert `string' in B64 representation to integer. If the result is
       too large to fit a normal integer, Pythons long integer type is used.
    """
    result = 0
    for c in string :
        result = (result << 6) + _ord_map [c]
    return result
# end def atoi

def itoa (number, _base = _base, _ord_map = _ord_map) :
    """Convert `number' to string in B64 representation."""
    result = []
    if number == 0 :
        result.append ("0")
    elif number > 0 :
        while number > 0 :
            number, r = divmod (number, _base)
            result.append (_ord_map [r])
        result.reverse ()
    else :
        raise ValueError, "Cannot handle negative number %s." % (number, )
    return "".join (result)
# end def itoa

if __name__ != "__main__" :
    from _TFL import TFL
    TFL._Export_Module ()
### __END__ B64
