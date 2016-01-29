# -*- coding: utf-8 -*-
# Copyright (C) 2003-2016 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    CAL.Holiday
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
#    10-Oct-2004 (MG) Use new `CAL.Date_Time` module instead of `Date_Time`
#    15-Oct-2004 (CT) Use `CAL.Date` instead of `CAL.Date_Time`
#    15-Oct-2004 (CT) `_main` and `_command_spec` added
#    17-Oct-2004 (CT) Use `Date_Delta` instead of `Delta`
#    31-Oct-2004 (CT) `_main` changed to display date, too
#     5-Nov-2004 (CT) Use `//` for int division
#    16-Jun-2010 (CT) Use unicode for holiday names
#    16-Jun-2013 (CT) Use `TFL.CAO`, not `TFL.Command_Line`
#    29-Jan-2016 (CT) Modernize, DRY
#    ««revision-date»»···
#--

from   __future__  import absolute_import
from   __future__  import division
from   __future__  import print_function
from   __future__  import unicode_literals

from   _CAL                    import CAL
from   _TFL                    import TFL
from   _TFL.pyk                import pyk

import _CAL.Date
import _CAL.Delta
import _TFL.CAO

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
        raise NotImplementedError \
            ("Only implemented for years between 1583 and 2299")
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
            ### print (d, e, a, (d == 28, e == 6, a > 10))
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
    f    = (b + 8) // 25
    g    = (b - f + 1) // 3
    h    = (19*a + b - d - g + 15) % 30
    i, k = divmod (c, 4)
    l    = (32 + 2*e + 2*i - h - k) % 7
    m    = (a + 11*h + 22*l) // 451
    n, p = divmod (h + l - 7*m + 114, 31)
    return (y, n, p+1)
# end def easter_date

fixed_holidays = \
  { ( 1,  1) : "Neujahr"
  , ( 1,  6) : "Hl. Drei Könige"
  , ( 5,  1) : "Mai-Feiertag"
  , ( 8, 15) : "Mariä Himmelfahrt"
  , (10, 26) : "Nationalfeiertag"
  , (11,  1) : "Allerheiligen"
  , (12,  8) : "Mariä Empfängnis"
  , (12, 25) : "1. Weihnachtstag"
  , (12, 26) : "2. Weihnachtstag"
  }

easter_dependent_holidays = \
  {  0       : "Ostersonntag"
  ,  1       : "Ostermontag"
  , 39       : "Christi Himmelfahrt"
  , 49       : "Pfingstsonntag"
  , 50       : "Pfingstmontag"
  , 60       : "Fronleichnam"
  }

def holidays (Y) :
    result  = {}
    year    = Y.year
    for h, n in pyk.iteritems (fixed_holidays) :
        result [CAL.Date (year, * h).ordinal] = n
    y, m, d = easter_date (year)
    ED      = CAL.Date (y, m, d)
    for d, n in pyk.iteritems (easter_dependent_holidays) :
        D = ED + CAL.Date_Delta (days = d)
        result [D.ordinal] = n
    return result
# end def holidays

def _show (year) :
    """
    >>> _show (2016)
      1 2016/01/01 Neujahr
      6 2016/01/06 Hl. Drei Könige
     87 2016/03/27 Ostersonntag
     88 2016/03/28 Ostermontag
    122 2016/05/01 Mai-Feiertag
    126 2016/05/05 Christi Himmelfahrt
    136 2016/05/15 Pfingstsonntag
    137 2016/05/16 Pfingstmontag
    147 2016/05/26 Fronleichnam
    228 2016/08/15 Mariä Himmelfahrt
    300 2016/10/26 Nationalfeiertag
    306 2016/11/01 Allerheiligen
    343 2016/12/08 Mariä Empfängnis
    360 2016/12/25 1. Weihnachtstag
    361 2016/12/26 2. Weihnachtstag

    """
    import _CAL.Year
    Y = CAL.Year (year)
    O = Y.head.ordinal - 1
    for ordinal, name in sorted (pyk.iteritems (holidays (Y))) :
        print ("%3d %s %s" % (ordinal - O, Y.cal.day [ordinal], name))
# end def _show

def _main (cmd) :
    _show (cmd.year)
# end def _main

today    = CAL.Date ()
year     = today.year
_Command = TFL.CAO.Cmd \
    ( handler       = _main
    , args          =
        ( "year:I=%d?Year for which to show holidays" % (year, )
        ,
        )
    , max_args      = 1
    )

if __name__ != "__main__" :
    CAL._Export ("*")
else :
    _Command ()
### __END__ CAL.Holiday
