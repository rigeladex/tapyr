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
#    ««revision-date»»···
#--

from   _TFL      import TFL
from   Date_Time import *
from   predicate import *

import sos
import _TFL._Meta.Object
import _TFL._CAL

class Day (TFL.Meta.Object) :
    """Model a single day in a calendar"""

    def __init__ (self, date) :
        self.date         = Date (date)
        self.appointments = []
    # end def __init__

    def as_plan (self) :
        d = self.date
        return "\n".join \
            ( [ "# %s      %s#%2.2d"
              % (self, d.formatted ("%a"), d.week)
              ]
            + [a.as_plan for a in self.appointments]
            + [""]
            )
    # end def as_plan

    def __str__ (self) :
        return self.date.formatted ("%Y/%m/%d")
    # end def __str__

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

# end class Month

class Year (TFL.Meta.Object) :
    """Model a single year in a calendar"""

    def __init__ (self, year) :
        self.year   = self.number = year
        self.months = months = []
        self.days   = days   = []
        self.weeks  = weeks  = []
        for m in range (1, 13) :
            month = Month (year, m)
            months.append (month)
            days.extend   (month.days)
        self.head = h = days [0]
        self.tail = t = days [-1]
        w_head = Week \
            ( h.week
            , * ( [h.date - i for i in range (h.day + 1, 0, -1)]
                + days [0 : 6 - h.day]
                )
            )
        weeks.append (w_head)
        i = w_head.sun.julian_day
        for w in range (w_head.number + 1, 53) :
            weeks.append (Week (w, * days [i : i+7]))
            i += 7
        if i < len (days) :
            weeks.append \
                (Week
                     ( weeks [-1].number + 1
                     , * ( days [i : ]
                         + [t.date + j for j in range (1, 8 - (len(days) - i))]
                         )
                     )
                )
    # end def __init__

    def __len__ (self) :
        return len (self.days)
    # end def __len__

    def as_plan (self) :
        return "\n\n".join \
            ( ["###  Plan for %s %s" % (self.year, "#" * 35)]
            + [d.as_plan () for d in self.days]
            + ["### End of plan for %s %s" % (self.year, "#" * 33)]
            )
    # end def as_plan

    def as_cal (self) :
        lines  = [w.as_cal () for w in self.weeks]
        month  = 12
        result = []
        tail   = ""
        for w, l in zip (self.weeks, lines) :
            d  = w.sun
            if d.month != month :
                month = d.month
                tail  = d.formatted ("%b")
                l     = "%s %s %s" % (l, tail [0], d.formatted ("%m"))
            else :
                l     = "%s %s   " % (l, tail [0:1] or ".")
            tail      = tail [1:]
            result.append (l)
        result.append (" ")
        return "\n".join (result)
    # end def as_cal

# end class Year

def command_spec (arg_array = None) :
    from Command_Line import Command_Line
    today    = Date ()
    year     = today.year
    return Command_Line \
        ( option_spec =
            ( "path:S=~/diary?Path for calendar files"
            , "Plan:S=plan?Filename of plan for `year`"
            , "View:S=view?Filename of view for `year`"
            , "write:B?Write files"
            , "year:I=%d?Year for which to process calendar" % (year, )
            )
        , max_args    = 0
        , arg_array   = arg_array
        )
# end def command_spec

def main (cmd) :
    year = cmd.year
    path = sos.path.join (sos.expanded_path (cmd.path), "%4.4d" % year)
    Y    = Year (year)
    pfil = sos.path.join (path, cmd.Plan)
    vfil = sos.path.join (path, cmd.View)
    if cmd.write :
        if cmd.Plan :
            f = file (pfil, "w")
            f.write  (Y.as_plan ())
            f.close  ()
        if cmd.View :
            f = file (vfil, "w")
            f.write  (Y.as_cal ())
            f.close  ()
# end def main

if __name__ == "__main__" :
    main (command_spec ())
else :
    TFL.CAL._Export ("*")
### __END__ Year
