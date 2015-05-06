# -*- coding: utf-8 -*-
# Copyright (C) 2015 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package _CAL.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    CAL.Quarter
#
# Purpose
#    Class modelling a calendar quarter
#
# Revision Dates
#    28-Jan-2015 (CT) Creation
#     6-May-2015 (CT) Add tests for `jsonified`
#    ««revision-date»»···
#--

from   __future__ import division, print_function
from   __future__ import absolute_import, unicode_literals

from   _CAL                       import CAL
from   _TFL                       import TFL

import _CAL.Date
import _CAL.Delta
from   _CAL.Year                  import _Ordinal_


from   _TFL.pyk                   import pyk
from   _TFL.Regexp                import *

import _TFL._Meta.Object
import _TFL._Meta.Once_Property

@pyk.adapt__str__
class Quarter (_Ordinal_) :
    """Model a calendary quarter.

    >>> from _TFL.json_dump import to_string as jsonified
    >>> q = Quarter (2000, 1)
    >>> print (q, q.days, q.start, q.finis)
    2000/Q1 91 2000-01-01 2000-03-31

    >>> print (jsonified ([q]))
    ["2000/Q1"]

    >>> for i in range (8) :
    ...     r = q + i
    ...     print (r, r.days, r.start, r.finis)
    ...
    2000/Q1 91 2000-01-01 2000-03-31
    2000/Q2 91 2000-04-01 2000-06-30
    2000/Q3 92 2000-07-01 2000-09-30
    2000/Q4 92 2000-10-01 2000-12-31
    2001/Q1 90 2001-01-01 2001-03-31
    2001/Q2 91 2001-04-01 2001-06-30
    2001/Q3 92 2001-07-01 2001-09-30
    2001/Q4 92 2001-10-01 2001-12-31

    >>> q > r
    False
    >>> q < r
    True
    >>> q == r
    False
    >>> q == q
    True

    >>> Quarter.from_string ("2014/Q1")
    Quarter (2014, 1)

    >>> Quarter.from_string ("2015/01/28")
    Quarter (2015, 1)

    >>> Quarter.from_string ("2015/01")
    Traceback (most recent call last):
      ...
    ValueError: 2015/01

    """

    quarter_pattern  = Regexp \
        ( r"(?P<year>     \d{4,4})"
          r"([-/]?)"
          r"Q(?P<quarter> \d{1,1})"
          r"$"
        , flags      = re.VERBOSE | re.IGNORECASE
        )
    _delta           = CAL.Month_Delta (3)

    def __init__ (self, year, quarter) :
        self.year    = year
        self.quarter = quarter
    # end def __init__

    @classmethod
    def from_string (cls, s) :
        Date  = CAL.Date
        match = cls.quarter_pattern.match (s)
        if match :
            return cls (** Date._from_string_match_kw (s, match))
        else :
            date = Date.from_string (s)
            return cls (date.year, date.quarter)
    # end def from_string

    @TFL.Meta.Once_Property
    def days (self) :
        return (self.finis - self.start).days + 1
    # end def days

    @TFL.Meta.Once_Property
    def finis (self) :
        return self.start + self._delta - 1
    # end def finis

    @TFL.Meta.Once_Property
    def ordinal (self) :
        return self.start.ordinal
    # end def ordinal

    @TFL.Meta.Once_Property
    def start (self) :
        quarter = self.quarter
        month   = 1 + 3 * (quarter - 1)
        return CAL.Date (self.year, month, 1)
    # end def start

    def __add__ (self, rhs) :
        d = self.start + CAL.Month_Delta (3 * rhs)
        return self.__class__ (d.year, d.quarter)
    # end def __add__

    def __sub__ (self, rhs) :
        d = self.start - CAL.Month_Delta (3 * rhs)
        return self.__class__ (d.year, d.quarter)
    # end def __sub__

    def __repr__ (self) :
        return "%s (%s, %s)" % \
            (self.__class__.__name__, self.year, self.quarter)
    # end def __repr__

    def __str__ (self) :
        return "%4.4d/Q%d" % (self.year, self.quarter)
    # end def __str__

# end class Quarter

if __name__ != "__main__" :
    CAL._Export ("*")
### __END__ CAL.Quarter
