# -*- coding: utf-8 -*-
# Copyright (C) 2020 Christian Tanzer All rights reserved
# tanzer@gg32.com                                      https://www.gg32.com
# #*** <License> ************************************************************
# This module is licensed under the terms of the BSD 3-Clause License
# <https://www.gg32.com/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    SKY.Tides
#
# Purpose
#    Model tides at a specific location
#
# Revision Dates
#    19-Oct-2020 (CT) Creation
#     8-Nov-2020 (CT) Finish creation
#    ««revision-date»»···
#--

from   _SKY                     import SKY
from   _TFL                     import TFL
from   _TFL.pyk                 import pyk

from   _TFL.predicate           import \
    dusplit, rounded_down, rounded_to, rounded_up
from   _TFL.Q_Exp               import Q
from   _TFL._Meta.Once_Property import Once_Property

import _TFL._Meta.Object

from   itertools                import groupby

class Datum (TFL.Meta.Object) :
    """Tidal height for one specific time and location."""

    def __init__ (self, dt, height) :
        self.dt     = dt
        self.height = height
    # end def __init__

    @Once_Property
    def date (self) :
        return self.dt.as_date ()
    # end def date

    @Once_Property
    def hh_mm (self) :
        return self.dt.formatted ("%H:%M")
    # end def hh_mm

    def __repr__ (self) :
        return ("%s %+5.2f" % (self.dt, self.height))
    # end def __repr__

    def __str__ (self) :
        return "%s %+5.2f" % (self.hh_mm, self.height)
    # end def __str__

# end class Datum

class Day (TFL.Meta.Object) :
    """Model tides for one day at a specific location."""

    def __init__ (self, date, loc, extremes, heights = []) :
        self.date      = date
        self.loc      = loc
        self.extremes = extremes
        self.heights  = heights
    # end def __init__

    def details (self) :
        hours = dusplit (self.heights, Q.dt.hour)
        def _gen_lines (self, hours) :
            yield "%s, %s" % (self.date.formatted ("%a"), self)
            yield "=" * 76
            for h in hours :
                yield "  ".join (str (x) for x in h [::2])
        return "\n".join (_gen_lines (self, hours))
    # end def details

    def predicated_ranges (self, pred) :
        def _gen (heights, pred) :
            for p,  hi in groupby (heights, pred) :
                if p :
                    hs = list (hi)
                    yield "%s–%s" % (hs [0].hh_mm, hs [-1].hh_mm)
        return list (_gen (self.heights, pred))
    # end def predicated_ranges

    def __str__ (self) :
        parts = [self.date.formatted ("%Y-%m-%d")] + \
            [str (x) for x in self.extremes]
        return "  ".join (parts)
    # end def __str__

# end class Day

class Location (TFL.Meta.Object) :
    """Model a location for tidal information."""

    Table = {}

    def __init__ (self, loc, lowest_at, highest_at) :
        self.loc        = loc
        self.lowest_at  = lowest_at  ### lowest  astronomical tide at loc
        self.highest_at = highest_at ### highest astronomical tide at loc
        if loc not in self.Table :
            self.Table [loc.name] = self
    # end def __init__

    @Once_Property
    def name (self) :
        return self.loc.name
    # end def name

    def __str__ (self) :
        return "%s [%+5.2f – %+5.2f]" % \
            (self.name, self.lowest_at, self.highest_at)
    # end def __str__

# end class Location

class Year (TFL.Meta.Object) :
    """Model tides for one year at a specific location."""

    def __init__ (self, year, loc, days) :
        self.year = year
        self.loc  = loc
        self.days = days
    # end def __init__

    @Once_Property
    def dmap (self) :
        result = {d.date : d for d in self.days}
        return result
    # end def dmap

    @Once_Property
    def months (self) :
        return dusplit (self.days, Q.date.month)
    # end def months

    @Once_Property
    def weeks (self) :
        return dusplit (self.days, Q.date.week)
    # end def weeks

    def predicated_ranges (self, pred) :
        def _gen (self) :
            desc = str (pred).replace ("Q.",  "")
            def _gen_days (days) :
                yield from \
                    ( "%s  %s"
                    % ( d.date.formatted ("%Y-%m-%d")
                      , (  "  ".join (d.predicated_ranges (pred))
                        or ("no occurrence of '%s'" % desc)
                        )
                      )
                    for d in days
                    )
            yield from self._gen_header \
                ( "Time ranges for '%s' for %%s at %%s" % (desc, )
                , self.loc.loc.name
                , 75
                )
            yield from self._gen_months (_gen_days)
        return "\n".join (_gen (self))
    # end def predicated_ranges

    def summary (self) :
        def _gen (self) :
            def _gen_days (days) :
                yield from (str (d) for d in days)
            yield from self._gen_header \
                ("Tidal extremes for %s at %s", self.loc, 75)
            yield from self._gen_months (_gen_days)
        return "\n".join (_gen (self))
    # end def summary

    def _gen_header (self, fmt, loc, length = 75) :
        days = self.days
        head = days [ 0].date
        tail = days [-1].date
        span = self.year if len (days) >= 365 else ("[%s – %s]" % (head, tail))
        yield fmt % (span, loc)
        yield "=" * 75
    # end def _gen_header

    def _gen_months (self, _gen_days) :
        for i, m in enumerate (self.months) :
            if i :
                yield "\f"
            yield from _gen_days (m)
    # end def _gen_months

# end class Year

if __name__ != "__main__" :
    SKY._Export_Module ()
### __END__ Tides
