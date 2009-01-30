# -*- coding: iso-8859-1 -*-
# Copyright (C) 2008 Mag. Christian Tanzer. All rights reserved
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
#    Arbeitszeit
#
# Purpose
#    Zeiterfassung
#
# Revision Dates
#    10-Feb-2008 (CT) Creation (ported from Perl)
#    11-Feb-2008 (CT) `-year` added
#    21-Feb-2008 (CT) `-year` processing changed to consider `after` and
#                     `before` (and display the [corrected] `vacation`)
#    ««revision-date»»···
#--

from   __future__        import with_statement

from   _TFL                     import TFL
from   _CAL                     import CAL

from   _TFL._Meta.Once_Property import Once_Property
from   _TFL.predicate           import *

import _TFL._Meta.Object
import _TFL.Accessor
import _TFL.Environment

import _CAL.Date
import _CAL.Year

class _Entry_ (TFL.Meta.Object) :
    """Base class for entries"""

    free = 0.0
    sick = 0.0
    work = 0.0

    def __init__ (self, date, text = "") :
        if isinstance (date, str) :
            date = CAL.Date.from_string (date)
        self.date = date
        self.text = text
    # end def __init__

    @Once_Property
    def formatted_date (self) :
        return self.date.formatted ("%d-%m-%Y")
    # end def formatted_date

# end class _Entry_

class _Hour_Entry_ (_Entry_) :
    """Entry measuring work hours."""

    default_hours = 5
    granularity   = 0.25

    def __init__ (self, date, hours = None, text = "") :
        self.__super.__init__ (date, text)
        if hours is None :
            hours = self.default_hours
        self.hours = rounded_to (float (hours), self.granularity)
    # end def __init__

    @Once_Property
    def formatted_value (self) :
        return "%7.3f" % (self.hours, )
    # end def formatted_value

    def __float__ (self) :
        return self.hours
    # end def __float__

# end class _Hour_Entry_

class Work (_Hour_Entry_) :
    """Entry describing one unit of work."""

    work        = property (TFL.Getter.hours)

# end class Work

class Sick (_Hour_Entry_) :
    """Entry describing work lost to sickness."""

    sick        = property (TFL.Getter.hours)

# end class Sick

class Free (_Entry_) :
    """Entry describing vacation time."""

    free        = property (TFL.Getter.days)
    granularity = 1.0

    def __init__ (self, date, days, text = "") :
        self.__super.__init__ (date, text)
        self.days = rounded_to (float (days), self.granularity)
    # end def __init__

    @Once_Property
    def formatted_value (self) :
        return "%2.0f" % (self.days, )
    # end def formatted_value

    def __float__ (self) :
        return self.days
    # end def __float__

# end class Free

class Period (TFL.Meta.Object) :
    """Collect entries for a period of work."""

    format = "%-24s | %10s | %10s | %10s | %10s"

    def __init__ (self, entries = ()) :
        self.entries = sorted (entries, key = TFL.Getter.date)
        assert self.entries
    # end def __init__

    @Once_Property
    def date (self) :
        return self.entries [0].date
    # end def date

    @Once_Property
    def formatted_date (self) :
        h, t   = self.entries [0], self.entries [-1]
        hd, td = h.date, t.date
        if hd.week == td.week :
            return "KW %2.2d/%4d" % (hd.week, hd.year)
        elif hd.month == td.month :
            return "%2.2d/%4d"    % (hd.month, hd.year)
        else:
            return "%s .. %s" % (h.formatted_date, t.formatted_date)
    # end def formatted_date

    @Once_Property
    def free (self) :
        return sum (e.free for e in self.entries)
    # end def free

    @Once_Property
    def sick (self) :
        return sum (e.sick for e in self.entries)
    # end def sick

    @Once_Property
    def work (self) :
        return sum (e.work for e in self.entries)
    # end def work

    def _formatted (self, v, format = "%7.2f") :
        if v :
            return format % (v, )
        return ""
    # end def _formatted

    def __nonzero__ (self) :
        return bool (self.entries)
    # end def __nonzero__

    def __str__ (self) :
        return self.format % \
            ( self.formatted_date
            , self._formatted (self.work)
            , self._formatted (self.sick)
            , self._formatted (self.work + self.sick)
            , self._formatted (self.free, "%3.0f    ")
            )
    # end def __str__

# end class Period

def command_spec (arg_array = None) :
    from   Command_Line import Command_Line
    from   _CAL.Date    import Date_Opt
    return Command_Line \
        ( arg_spec    = ("zeiterfassung:P?File specifying work time")
        , option_spec =
            ( Date_Opt ("after", "Only display entries after specified date")
            , Date_Opt ("before", "Only display entries before specified date")
            , "-Config:P,?Config file(s)"
            , "-hpd:F=8?Hours per day"
            , "-ptf:F=1.0?Part time factor"
            , "-quiet:B?Show total only"
            , "-vacation:I=25?Days of vacation per year"
            , "-Weekly:B?Show weekly summary (default: monthly)"
            , "-year:I?Show work time for year"
            )
        , description = "Show work time specified by `zeiterfassung`."
        , max_args    = 1
        , min_args    = 0
        , arg_array   = arg_array
        )
# end def command_spec

def main (cmd) :
    from _TGL.load_config_file import load_config_file
    globs = globals ()
    for cf in cmd.Config :
        load_config_file (cf, globs)
    if cmd.year :
        ptf       = cmd.ptf
        year      = cmd.year
        Y         = CAL.Year (year)
        days      = Y.days
        cm_d      = Y.dmap [(year, 12, 24)]
        d_range   = ""
        if cmd.after :
            days  = filter (lambda d : d.date >= cmd.after, days)
            if cm_d.date < cmd.after :
                cm_d = None
            d = cmd.after
            d_range  = "%02d.%02d." % (d.date.day, d.date.month)
            if not cmd.before :
                d_range = "%s-31.12." % (d_range, )
        if cmd.before :
            days  = filter (lambda d : d.date <= cmd.before, days)
            if cm_d and cm_d.date > cmd.before :
                cm_d = None
            if not cmd.after :
                d_range  = "01.01"
            d = cmd.before
            d_range = "%s-%02d.%02d" % (d_range, d.date.day, d.date.month)
        if d_range :
            d_range = " [%s]" % (d_range, )
        holidays  = sum \
            ((d.is_weekday and bool (d.is_holiday)) for d in days) * ptf
        workdays  = sum \
            ((d.is_weekday and not   d.is_holiday)  for d in days) * ptf
        vp        = \
            ( sum (float (d.is_weekday and not d.is_holiday)  for d in days)
            / sum (float (d.is_weekday and not d.is_holiday)  for d in Y.days)
            )
        vacation  = cmd.vacation * vp * ptf
        christmas = 0
        if cm_d :
            christmas = 2 * (cm_d.is_weekday and not cm_d.is_holiday)
        holidays += christmas
        workdays -= christmas
        workdays -= vacation
        form      = \
            ( "%s%s: %.0f Arbeitstage, %.0f Feiertage"
              ", %.0f Urlaubstage, %.0f Soll-Stunden"
            )
        print form % \
            (year, d_range, workdays, holidays, vacation, workdays * cmd.hpd)
    if cmd.zeiterfassung :
        with open (cmd.zeiterfassung) as f :
            entries = eval (f.read ())
        splitter = TFL.Getter.date.month
        if cmd.Weekly :
            splitter = TFL.Getter.date.week
        if cmd.after :
            entries = filter (lambda e : e.date >= cmd.after, entries)
        if cmd.before :
            entries = filter (lambda e : e.date <= cmd.before, entries)
        days  = [Period (d) for d in dusplit (entries, TFL.Getter.date)]
        units = [Period (w) for w in dusplit (days, splitter)]
        P = Period (units)
        tot = str (P)
        print P.format % \
            ("Periode", "Arbeit [h]", "Krank [h]", "Total [h]", "Urlaubstage")
        if not cmd.quiet :
            for d in P.entries :
                print d
            print "=" * len (tot)
        print tot
# end def main

"""
$ for y in $(range 2001 2008)
do python /swing/python/Arbeitszeit.py -y $y -ptf 0.6 -hpd 5 ; done

y=2003; python /swing/python/Arbeitszeit.py -ptf 0.60 -hpd 5 -y $y \
  /swing/private/froelich/work/$y.dat -after 20030815

"""

if __name__ == "__main__":
    main (command_spec ())
### __END__ Arbeitszeit
