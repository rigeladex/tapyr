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
#    Plan
#
# Purpose
#    Model a yearly calendar with appointments
#
# Revision Dates
#    13-Apr-2003 (CT) Creation
#    ««revision-date»»···
#--
from   _TFL      import TFL
from   _TFL._CAL import CAL
from   Date_Time import *
from   Filename  import *
from   predicate import *
from   Regexp    import *
from __future__  import generators

import sos
import _TFL._Meta.Object
import _TFL._CAL.Appointment
import _TFL._CAL.Year

day_sep       = Regexp ("^#", re.M)
day_pat       = Regexp (r"^ (?P<day>\d{4}/\d{2}/\d{2}) ")

class PDF_Plan (TFL.Meta.Object) :

    inch = INCH = 72
    cm   = inch / 2.54
    mm   = 0.1 * cm

    xsiz = 21.0 * cm
    ysiz = 29.7 * cm
    xo   = 0.5  * cm
    yo   = 0.5  * cm
    ts   = 30
    lw   = 1.0
    font = "Helvetica"

    def __init__ ( self, Y, filename
                 , first_week = 0, last_week = 53, wpx = 2, wpy = 2
                 , linewidth  = 0.6
                 ) :
        from pdfgen import Canvas
        self.Y          = Y
        self.filename   = filename
        self.first_week = first_week
        self.last_week  = last_week
        self.wpx        = wpx
        self.wpy        = wpy
        self.linewidth  = linewidth
        self.canvas = c = Canvas (filename, pagesize = (self.xsiz, self.ysiz))
        self.pager  = p = self.page_generator (c)
        c.setPageCompression (0)
        c.setLineJoin        (2)
        for w in Y.weeks [first_week : last_week] :
            self.one_week (w, p.next ())
        c.save ()
    # end def __init__

    def page_generator (self, c) :
        xo = self.xo
        yo = self.yo
        xl = (self.xsiz - xo) / self.wpx
        yl = (self.ysiz - yo) / self.wpy
        ds = (yl - self.yo - 1 * self.cm) / 7
        xs = [(xo + i * xl) for i in range (self.wpx)]
        ys = [(yo + i * yl) for i in range (self.wpy)]
        ys.reverse ()
        while 1 :
            for y in ys :
                for x in xs :
                    yield (x, x + xl - xo), (y + 0.3, y + 0.3 + yl - yo), ds
            c.showPage ()
    # end def page_generator

    def one_week (self, w, ((x, xl), (y, yl), ds)) :
        c    = self.canvas
        cm   = self.cm
        mm   = self.mm
        font = self.font
        ts   = self.ts
        c.setLineWidth (self.linewidth)
        c.line (x, y, x, yl - 1 * cm)
        y = y + 7 * ds
        c.line (x, y, xl, y)
        c.setFont (font, ts / 2)
        c.drawString (x  + 0.2 * cm, y + 0.2 * cm, "Week %2.2d" % w.number)
        if w.mon.month == w.sun.month :
            m_head = w.mon.formatted ("%B %Y")
        else :
            if w.mon.year == w.sun.year :
                mon_format = "%b"
            else :
                mon_format = "%b %Y"
            m_head = "%s/%s" % \
                (w.mon.formatted (mon_format), w.sun.formatted ("%b %Y"))
        c.drawRightString (xl - 0.2 * cm, y + 0.2 * cm, m_head)
        for d in w.days :
            y -= ds
            self.one_day (c, d, ds, x, xl, y, yl, font, ts, cm, mm)
    # end def one_week

    def line_generator (self, ds, x, xl, y, ts) :
        def _ () :
            lines = ds / (ts + 2)
            yo    = y + ds - ts - 1
            ys    = [(yo - (l * (ts + 1))) for l in range (lines)]
            for xo in [x, x + xl / 2] :
                for yo in ys :
                    yield xo + 0.1 * self.cm, yo + 1
        return _ ()
    # end def line_generator

    def one_day (self, c, d, ds, x, xl, y, yl, font, ts, cm, mm) :
        xo = xl - 0.2 * cm
        c.line (x, y, xl, y)
        c.setFont (font, ts)
        c.drawRightString (xo, y + ds * 0.95 - ts, d.formatted ("%d"))
        c.setFont (font, ts / 5)
        c.drawRightString (xo, y + mm,             d.formatted ("%A"))
        lg = self.line_generator (ds, x, xo - 0.15 * (xl - x), y, ts / 5)
        for a in getattr (d, "appointments", []) :
            try :
                 xo, yo = lg.next ()
            except StopIteration :
                break
            c.drawString (xo, yo, ("%s %s" % (a.time or ">", a.activity))[:40])
    # end def one_day

# end class PDF_Plan

def read_plan (Y, plan_file_name) :
    """Read information from file named `plan_file_name` and put appointments
       into `Y`
    """
    f = file (plan_file_name)
    try :
        buffer = f.read ()
    finally :
        f.close ()
    for entry in day_sep.split (buffer) :
        if day_pat.match (entry) :
            d = Y.map [day_pat.day]
            head, tail = (entry.split ("\n", 1) + [""]) [:2]
            if tail :
                a = CAL.appointments (tail)
                d.appointments += a
# end def read_plan

def write_plan (Y, plan_file_name, replace = 0) :
    today = Date ()
    tail  = today.formatted ("%d.%m.%Y.%H:%M")
    if replace :
        sos.rename (plan_file_name, "%s-%s" % (plan_file_name, tail))
    else :
        plan_file_name = "%s.%s" % (plan_file_name, tail)
    CAL.write_year (Y.as_plan, plan_file_name, force = replace)
# end def write_plan

def command_spec (arg_array = None) :
    from Command_Line import Command_Line
    today    = Date ()
    year     = today.year
    return Command_Line \
        ( option_spec =
            ( "diary:S=~/diary?Path for calendar file"
            , "filename:S=plan?Filename of plan for `year`"
            , "pdf:S?Generate PDF file with plan"
            , "replace:B?Replace old calendar with new file"
            , "sort:B?Sort calendar and write it back"
            , "year:I=%d?Year for which to process calendar" % (year, )
            )
        , max_args    = 0
        , arg_array   = arg_array
        )
# end def command_spec

def main (cmd) :
    year      = cmd.year
    path      = sos.path.join (sos.expanded_path (cmd.diary), "%4.4d" % year)
    Y         = CAL.Year      (year)
    file_name = sos.path.join (path, cmd.filename)
    read_plan   (Y, file_name)
    if cmd.sort :
        for d in Y.days :
            d.appointments.sort ()
        write_plan (Y, file_name, cmd.replace)
    if cmd.pdf :
        pdf_name = Filename (cmd.pdf, ".pdf").name
        PDF_Plan (Y, pdf_name)
# end def main

if __name__ == "__main__" :
    main (command_spec ())
else :
    TFL.CAL._Export ("*")
### __END__ Plan
