# -*- coding: iso-8859-1 -*-
# Copyright (C) 2003 Mag. Christian Tanzer. All rights reserved
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
#    Year
#
# Purpose
#    Class modelling a calendar year
#
# Revision Dates
#     5-Apr-2003 (CT) Creation
#    13-Apr-2003 (CT) `Year.as_cal` changed
#    13-Apr-2003 (CT) `Day.as_plan` changed
#    13-Apr-2003 (CT) `create_diary` added
#    13-Apr-2003 (CT) `write_year` factored
#    13-Apr-2003 (CT) `-force` and guard against inadvertent overwriting added
#    19-Apr-2003 (CT) `add_appointments`  added to `Day`
#    19-Apr-2003 (CT) `sort_appointments` added to `Day` and `Year`
#    20-Apr-2003 (CT) `easter_date` added
#    15-Dec-2003 (CT) Computation of `w_head` corrected in `Year.__init__`
#    ««revision-date»»···
#--

from   _TFL      import TFL
from   _TFL._CAL import CAL
from   Date_Time import *
from   predicate import *

import sos
import _TFL._Meta.Object
import _TFL._CAL.Appointment
import _TFL._CAL.Holiday

class Day (TFL.Meta.Object) :
    """Model a single day in a calendar"""

    is_holiday = ""

    def __init__ (self, date, appointments = None) :
        self.date         = Date (date)
        self.number       = self.date.day
        self.appointments = appointments or [] ### XXX use dict_from_list
    # end def __init__

    def add_appointments (self, * apps) :
        self.appointments.extend (apps)
    # end def add_appointments

    def as_plan (self) :
        self.sort_appointments ()
        d = self.date
        l = Date ("%s/12/31" % (d.year, ))
        holi = self.is_holiday
        if holi :
            holi = "%26s" % ("=%s=" % (holi, ), )
        return "\n".join \
            ( [ "# %s      %s#%2.2d, %s, day %d/-%d %s"
              % ( self
                , d.formatted ("%a")
                , d.week
                , d.formatted ("%d-%b-%Y")
                , d.julian_day
                , l.julian_day - d.julian_day + 1
                , holi
                )
              ]
            + (map (str, self.appointments) or [""])
            )
    # end def as_plan

    def sort_appointments (self) :
        self.appointments.sort ()
    # end def sort_appointments

    def __str__ (self) :
        return self.date.formatted ("%Y/%m/%d")
    # end def __str__

    def __repr__ (self) :
        return """%s ("%s")""" % \
               (self.__class__.__name__, self.date.formatted ("%Y/%m/%d"))
    # end def __repr__

    def __getattr__ (self, name) :
        if not (name.startswith ("__") and name.endswith ("__")) :
            return getattr (self.date, name)
        raise AttributeError
    # end def __getattr__

# end class Day

class Week (TFL.Meta.Object) :
    """Model a single week in a calendar"""

    def __init__ (self, number, * days) :
        self.number = number
        ( self.mon
        , self.tue
        , self.wed
        , self.thu
        , self.fri
        , self.sat
        , self.sun
        )           = self.days = days
        self.head   = self.mon
        self.tail   = self.sun
    # end def __init__

    def as_cal (self) :
        line = " ".join ([("%2d" % d.day) for d in self.days])
        return "%2.2d %s" % (self.number, line)
    # end def as_cal

    def __str__ (self) :
        return "week %2.2d" % (self.number, )
    # end def __str__

    def __repr__ (self) :
        return "week %2.2d <%s to %s>" % (self.number, self.mon, self.sun)
    # end def __repr__

# end class Week

class Month (TFL.Meta.Object) :
    """Model a single month in a calendar"""

    def __init__ (self, year, month) :
        self.year  = year
        self.month = self.number = month
        self.head  = Day (Time_Tuple (year = year, month = month, day = 1))
        self.days  = [self.head]
        d          = Date (self.head.date) + 1
        while d.month == month :
            self.days.append (Day (d))
            d.inc ()
        self.tail  = self.days [-1]
    # end def __init__

    def __len__ (self) :
        return len (self.days)
    # end def __len__

    def __str__ (self) :
        return self.head.formatted ("%Y/%m")
    # end def __str__

    def __repr__ (self) :
        return "%s (%s, %s)" % (self.__class__.__name__, self.year, self.month)
    # end def __repr__

# end class Month

class Year (TFL.Meta.Object) :
    """Model a single year in a calendar"""

    def __init__ (self, year = None) :
        self.year   = self.number = y = year or Date ().year
        self.months = months = []
        self.days   = days   = []
        self.weeks  = weeks  = []
        self.map    = map    = {}
        for m in range (1, 13) :
            month = Month (y, m)
            months.append (month)
            days.extend   (month.days)
        self.head = h = days [0]
        self.tail = t = days [-1]
        w_head = Week \
            ( h.week
            , * ( [h.date - i for i in range (h.weekday, 0, -1)]
                + days [0 : 7 - h.weekday]
                )
            )
        weeks.append (w_head)
        i = w_head.sun.julian_day
        for w in range (w_head.number + 1, 52) :
            weeks.append (Week (w, * days [i : i+7]))
            i += 7
        while i < len (days) :
            weeks.append \
                (Week
                     ( weeks [-1].number + 1
                     , * ( days [i : i+7]
                         + [t.date + j for j in range (1, 8 - (len(days) - i))]
                         ) [:8]
                     )
                )
            i += 7
        for d in days :
            map [str (d)] = d
        self.holidays = holidays = CAL.holidays (self)
        for h, n in holidays.iteritems () :
            map [h].is_holiday = n
    # end def __init__

    def __len__ (self) :
        return len (self.days)
    # end def __len__

    def as_plan (self) :
        return "\n\n".join \
            ( ["###  Plan for %s %s" % (self.year, "#" * 35)]
            + [d.as_plan () for d in self.days]
            + ["### End of plan for %s %s\n" % (self.year, "#" * 35)]
            )
    # end def as_plan

    def as_cal (self) :
        result = [   "%s %s" % (w.as_cal (), w.sun.formatted ("%b"))
                 for w in self.weeks
                 ] + [""]
        return "\n".join (result)
    # end def as_cal

    def sort_appointments (self) :
        for d in self.days :
            d.sort_appointments ()
    # end def sort_appointments

    def __str__ (self) :
        return "%s" % (self.year, )
    # end def __str__

    def __repr__ (self) :
        return "%s (%s)" % (self.__class__.__name__, self.year)
    # end def __repr__

# end class Year

def create_diary (Y, path) :
    for m in Y.months :
        mp = sos.path.join (path, "%2.2d" % (m.number, ))
        if not sos.path.isdir (mp) :
            sos.mkdir (mp)
            for d in m.days :
                f = sos.path.join (mp, "%2.2d.%s" % (d.day, "diary"))
                if not sos.path.isfile (f) :
                    open (f, "w").close ()
# end def create_diary

def write_year (Yf, file_name, force = 0) :
    if sos.path.isfile (file_name) and not force:
        print "%s already exists, not overwritten" %(file_name, )
    else :
        f = file (file_name, "w")
        f.write  (Yf ())
        f.close  ()
# end def write_year

def _command_spec (arg_array = None) :
    from Command_Line import Command_Line
    today    = Date ()
    year     = today.year
    return Command_Line \
        ( option_spec =
            ( "create:B?Write files"
            , "diary:B?Create a diary file per day"
            , "force:B?Overwrite existing files if any"
            , "path:S=~/diary?Path for calendar files"
            , "Plan:S=plan?Filename of plan for `year`"
            , "View:S=view?Filename of view for `year`"
            , "year:I=%d?Year for which to process calendar" % (year, )
            )
        , max_args    = 0
        , arg_array   = arg_array
        )
# end def _command_spec

def _main (cmd) :
    year = cmd.year
    path = sos.path.join (sos.expanded_path (cmd.path), "%4.4d" % year)
    Y    = Year (year)
    pfil = sos.path.join (path, cmd.Plan)
    vfil = sos.path.join (path, cmd.View)
    if cmd.create or cmd.diary :
        if not sos.path.isdir (path) :
            sos.mkdir (path)
        if cmd.diary :
            create_diary (Y, path)
        if cmd.create :
            if cmd.Plan :
                write_year (Y.as_plan, pfil, cmd.force)
            if cmd.View :
                write_year (Y.as_cal,  vfil, cmd.force)
# end def _main

if __name__ == "__main__" :
    _main (_command_spec ())
else :
    TFL.CAL._Export ("*")
### __END__ Year
