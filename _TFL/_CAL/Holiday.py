# -*- coding: iso-8859-1 -*-
# Copyright (C) 2003-2004 Mag. Christian Tanzer. All rights reserved
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
#    TFL.CAL.Holiday
#
# Purpose
#    Provide information about fixed and moving Austrian holidays
#
# Revision Dates
#    20-Apr-2003 (CT) Creation
#     6-Feb-2004 (CT) Use (y, m, d) tuples instead of strings as dictionary
#                     keys
#     9-Feb-2004 (CT) Dependency on `Y.map` removed
#     5-Jun-2004 (CT) `easter_date` implementation using Spencer Jones'
#                     algorithm added
#    10-Oct-2004 (MG) Use new `TFL.CAL.Date_Time` module instead of `Date_Time`
#    15-Oct-2004 (CT) Use `TFL.CAL.Date` instead of `TFL.CAL.Date_Time`
#    15-Oct-2004 (CT) `_main` and `_command_spec` added
#    17-Oct-2004 (CT) Use `Date_Delta` instead of `Delta`
#    ««revision-date»»···
#--

from   _TFL            import TFL
import _TFL._CAL.Date
import _TFL._CAL.Delta

def easter_date_gauss (year) :
    """Returns date of easter sunday computed by Gauß' rule as given by
       H.H.Voigt: `Abriß der Astronomie`.
    """
    if   1583 <= year <= 1699 :
        m, n = 22, 2
    elif 1700 <= year <= 1799 :
        m, n = 23, 3
    elif 1800 <= year <= 1899 :
        m, n = 23, 4
    elif 1900 <= year <= 2099 :
        m, n = 24, 5
    elif 2100 <= year <= 2199 :
        m, n = 24, 6
    elif 2200 <= year <= 2299 :
        m, n = 25, 0
    else :
        raise NotImplementedError, \
              "Only implemented for years between 1583 and 2299"
    a   = year                   % 19
    b   = year                   %  4
    c   = year                   %  7
    d   = (19*a + m)             % 30
    e   = ( 2*b + 4*c + 6*d + n) %  7
    day = 22 + d + e
    if day <= 31 :
        month = 3
    else :
        day   = d + e - 9
        month = 4
        if day in (25, 26) and d == 28 and e == 6 and a > 10 :
            ### print d, e, a, (d == 28, e == 6, a > 10)
            day -= 7
    return (year, month, day)
# end def easter_date_gauss

def easter_date (y) :
    """Returns date of easter sunday computed by Spencer Jones algorithm as
       given by Jean Meeus: Astronomical Algorithms.
    """
    a    = y % 19
    b, c = divmod (y, 100)
    d, e = divmod (b, 4)
    f    = (b + 8) / 25
    g    = (b - f + 1) / 3
    h    = (19*a + b - d - g + 15) % 30
    i, k = divmod (c, 4)
    l    = (32 + 2*e + 2*i - h - k) % 7
    m    = (a + 11*h + 22*l) / 451
    n, p = divmod (h + l - 7*m + 114, 31)
    return (y, n, p+1)
# end def easter_date

fixed_holidays = \
  { ( 1,  1) : "Neujahr"
  , ( 1,  6) : "Hl. Drei Könige"
  , ( 5,  1) : "Mai-Feiertag"
  , ( 8, 15) : "Mariae Himmelfahrt"
  , (10, 26) : "Nationalfeiertag"
  , (11,  1) : "Allerheiligen"
  , (12,  8) : "Mariae Empfaengnis"
  , (12, 25) : "1. Weihnachtstag"
  , (12, 26) : "2. Weihnachtstag"
  }

easter_dependent_holidays = \
  {  0      : "Ostersonntag"
  ,  1      : "Ostermontag"
  , 39      : "Christi Himmelfahrt"
  , 49      : "Pfingstsonntag"
  , 50      : "Pfingstmontag"
  , 60      : "Fronleichnam"
  }

def holidays (Y) :
    result  = {}
    year    = Y.year
    for h, n in fixed_holidays.iteritems () :
        result [TFL.CAL.Date (year, * h).ordinal] = n
    y, m, d = easter_date (year)
    ED      = TFL.CAL.Date (y, m, d)
    for d, n in easter_dependent_holidays.iteritems () :
        D = ED + TFL.CAL.Date_Delta (days = d)
        result [D.ordinal] = n
    return result
# end def holidays

def _command_spec (arg_array = None) :
    from Command_Line import Command_Line
    today    = TFL.CAL.Date ()
    year     = today.year
    return Command_Line \
        ( arg_spec   =
            ( "year:I=%d?Year for which to show holidays" % (year, )
            )
        , arg_array   = arg_array
        )
# end def _command_spec

def _main (cmd) :
    from predicate import sorted
    year = TFL.CAL.Date (cmd.year, 1, 1)
    for ordinal, name in sorted (holidays (year).iteritems ()) :
        print "%3d %s" % (ordinal - year.ordinal + 1, name)
# end def _main

if __name__ == "__main__" :
    _main (_command_spec ())
else :
    TFL.CAL._Export ("*")
### __END__ TFL.CAL.Holiday
