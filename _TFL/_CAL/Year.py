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
#    TFL.CAL.Year
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
#     5-Jan-2004 (CT) `Week.__int__` added
#     8-Jan-2004 (CT) `Week.__nonzero__` and `Day.__nonzero__` added
#     8-Jan-2004 (CT) Doctest added to `Year`
#     6-Feb-2004 (CT) Made `Week` lazy and central to `Year`s working
#     6-Feb-2004 (CT) Made `Day` shared between weeks of different years in
#                     same calendar (concerns weeks 0, 1, 52, 53)
#     9-Feb-2004 (CT) Made `Month` and `Year` lazy, too
#    11-Feb-2004 (MG) `_day_names` added
#    15-Oct-2004 (CT) Adapted to use `TFL.CAL.Date` instead of
#                     `lib/python/Date_Time`
#    ««revision-date»»···
#--

from   _TFL      import TFL
from   _TFL._CAL import CAL
import _TFL._Meta.Object
import _TFL._CAL.Appointment
import _TFL._CAL.Date
import _TFL._CAL.Holiday
import _TFL.d_dict

from   predicate import *
import sos

class _Cal_ (TFL.Meta.Object) :
    _days  = {}
    _weeks = {}
    _years = {}
# end class _Cal_

class Day (TFL.Meta.Object) :
    """Model a single day in a calendar"""

    is_holiday = ""

    id         = property (lambda s : s.date.tuple [:3])
    number     = property (lambda s : s.date.day)

    def __new__ (cls, cal, date) :
        Table = cal._days
        if isinstance (date, (str, unicode)) :
            date = TFL.CAL.Date (* [int (x) for x in date.split ("/")]) ### XXX
        id = date.ordinal
        if id in Table :
            return Table [id]
        self = Table [id] = TFL.Meta.Object.__new__ (cls)
        self._init_ (id, date)
        return self
    # end def __new__

    def _init_ (self, id, date) :
        self.date         = date
        self.appointments = []
        self._utilization = []
    # end def __init__

    def add_appointments (self, * apps) :
        self.appointments.extend (apps) ### XXX use dict_from_list
    # end def add_appointments

    def as_plan (self) :
        self.sort_appointments ()
        d = self.date
        l = TFL.CAL.Date (d.year, 12, 31)
        holi = self.is_holiday
        if holi :
            holi = "%26s" % ("=%s=" % (holi, ), )
        return "\n".join \
            ( [ "# %s      %s#%2.2d, %s, day %d/-%d %s"
              % ( self
                , d.formatted ("%a")
                , d.week
                , d.formatted ("%d-%b-%Y")
                , d.rjd
                , l.rjd - d.rjd + 1
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
        return getattr (self.date, name)
    # end def __getattr__

# end class Day

class Week (TFL.Meta.Object) :
    """Model a single week in a calendar"""

    tue = property (lambda s : s.days [1])
    wed = property (lambda s : s.days [2])
    thu = property (lambda s : s.days [3])
    fri = property (lambda s : s.days [4])
    sat = property (lambda s : s.days [5])
    sun = property (lambda s : s.days [6])

    _day_names = ("Mo", "Tu", "We", "Th", "Fr", "Sa", "So")

    def __init__ (self, year, number, mon) :
        self.year   = year
        self.number = number
        self.mon    = mon
        if number == 1 and int (year) != int (self.thu.year) :
            self.number = 53
        elif number == 53 and int (year) != int (self.thu.year) :
            self.number = 0
    # end def _init_

    def as_cal (self) :
        line = " ".join ([("%2d" % d.day) for d in self.days])
        return "%2.2d %s" % (self.number, line)
    # end def as_cal

    def populate (self) :
        if "days" not in self.__dict__ :
            d         = self.mon
            cal       = self.year.cal
            self.days = days = [d]
            days.extend ([Day (cal, d.date + i) for i in range (1, 7)])
    # end def populate

    def __getattr__ (self, name) :
        if name == "days" :
            self.populate ()
            return self.days
        raise AttributeError, name
    # end def __getattr__

    def __str__ (self) :
        return "week %2.2d" % (self.number, )
    # end def __str__

    def __repr__ (self) :
        return "week %2.2d <%s to %s>" % (self.number, self.mon, self.sun)
    # end def __repr__

    def __int__ (self) :
        return self.number
    # end def __int__

    def __nonzero__ (self) :
        n = self.number
        return (   (n > 0)
               and (  (n < 53)
                   or (int (self.year) == int (self.thu.year))
                   )
               )
    # end def __nonzero__

# end class Week

class Month (TFL.Meta.Object) :
    """Model a single month in a calendar"""

    head   = property (lambda s : s.days [0])
    number = property (lambda s : s.month)
    tail   = property (lambda s : s.days [-1])

    def __init__ (self, year, month) :
        self.year  = year
        self.month = month
    # end def __init__

    def populate (self) :
        if "days" not in self.__dict__ :
            Y = self.year
            n = self.month
            d = Y.dmap [(Y.number, n, 1)]
            i = d.rjd - 1
            self.days = days = []
            while d.month == n :
                days.append (d)
                i += 1
                try :
                    d = Y.days [i]
                except IndexError :
                    break
    # end def populate

    def __getattr__ (self, name) :
        if name == "days" :
            self.populate ()
            return self.days
        raise AttributeError, name
    # end def __getattr__

    def __len__ (self) :
        return len (self.days)
    # end def __len__

    def __str__ (self) :
        return self.head.formatted ("%Y/%m")
    # end def __str__

    def __repr__ (self) :
        return "%s (%s, %s)" % \
            (self.__class__.__name__, self.year.number, self.month)
    # end def __repr__

# end class Month

class Year (TFL.Meta.Object) :
    """Model a single year in a calendar.

       >>> for d in Year (2004).weeks [0].days :
       ...   print d, d.year == 2004
       ...
       2003/12/29 False
       2003/12/30 False
       2003/12/31 False
       2004/01/01 True
       2004/01/02 True
       2004/01/03 True
       2004/01/04 True
       >>> for d in Year (2004).weeks [-1].days :
       ...   print d, d.year == 2004
       ...
       2004/12/27 True
       2004/12/28 True
       2004/12/29 True
       2004/12/30 True
       2004/12/31 True
       2005/01/01 False
       2005/01/02 False
       >>> for y in range (2003, 2006) :
       ...   Y  = Year (y)
       ...   w0, w1 = Y.weeks [0], Y.weeks [-1]
       ...   print "%4.4d: %r %s, %r %s" % (y, w0, bool (w0), w1, bool (w1))
       ...
       2003: week 01 <2002/12/30 to 2003/01/05> True, week 53 <2003/12/29 to 2004/01/04> False
       2004: week 01 <2003/12/29 to 2004/01/04> True, week 53 <2004/12/27 to 2005/01/02> True
       2005: week 00 <2004/12/27 to 2005/01/02> False, week 52 <2005/12/26 to 2006/01/01> True
    """

    ### you can run the doctest with
    ###     /swing/python/run_doctest.py -path ~/lib/python/_TFL/_CAL Year

    number          = property (lambda s : s.year)

    def __init__ (self, year = None, cal = _Cal_, populate = False) :
        D           = TFL.CAL.Date
        self.year   = year or D ().year
        self.cal    = cal
        self.months = months = []
        self.weeks  = weeks  = []
        self.mmap   = mmap   = {}
        self.wmap   = wmap   = {}
        for m in range (1, 13) :
            month   = mmap [m] = Month (self, m)
            months.append (month)
        self.head   = h = Day (cal, D (year = year, month = 1,  day = 1))
        self.tail   = t = Day (cal, D (year = year, month = 12, day = 31))
        if h.weekday == 0 :
            d = h
        else :
            d = Day (cal, h.date - h.weekday)
        w_head = w = wmap [h.week] = Week (self, h.week, d)
        weeks.append (w_head)
        d = Day (cal, d.date + 7)
        while d.year == year :
            w = Week (self, d.week, d)
            wmap [w.number] = w
            weeks.append (w)
            d = Day (cal, d.date + 7)
        self.holidays = CAL.holidays (self)
        if populate :
            self.populate ()
    # end def __init__

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

    def populate (self) :
        self.days = days \
                  =  [d for d in self.weeks  [0].days [self.head.weekday:]]
        for w in self.weeks [1:-1] :
            days.extend (w.days)
        days.extend \
            ([d for d in self.weeks [-1].days [:self.tail.weekday + 1]])
        self.dmap = dmap = {}
        for d in days :
            dmap [d.id] = d
        dmap = self.cal._days
        for ord, name in self.holidays.iteritems () :
            dmap [ord].is_holiday = name
    # end def populate

    def sort_appointments (self) :
        for d in self.days :
            d.sort_appointments ()
    # end def sort_appointments

    def __getattr__ (self, name) :
        if name in ("days", "dmap") :
            self.populate ()
            return getattr (self, name)
        raise AttributeError, name
    # end def __getattr__

    def __int__ (self) :
        return self.year
    # end def __int__

    def __len__ (self) :
        return len (self.days)
    # end def __len__

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
        f = open (file_name, "w")
        f.write  (Yf ())
        f.close  ()
# end def write_year

def _command_spec (arg_array = None) :
    from Command_Line import Command_Line
    today    = TFL.CAL.Date ()
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
### __END__ TFL.CAL.Year
