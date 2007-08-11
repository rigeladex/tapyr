# -*- coding: iso-8859-1 -*-
# Copyright (C) 2003-2007 Mag. Christian Tanzer. All rights reserved
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
#    CAL.pdf
#
# Purpose
#    Create pdf file of calendar with appointments
#
# Revision Dates
#    18-Apr-2003 (CT)  Creation
#    20-Apr-2003 (CT)  `is_holiday` added
#     1-Jan-2004 (CT)  `PDF_Plan_L` and `-landscape` added
#     1-Jan-2004 (CT)  `_cooked` added and used
#    11-Jun-2004 (GKH) deprecation warning removed (issue 10140)
#    19-Dec-2004 (CT)  Small fixes to make it work again
#    25-Dec-2005 (CT)  Default for `pdf_name` computed dynamically (otherwise
#                      it defaults to the current, not the specified `year`)
#    25-Dec-2005 (CT)  Deprecation warnings killed (`/` --> `//`)
#    25-Dec-2005 (CT)  `line_generator` de-obfuscated
#    25-Dec-2005 (CT)  Options `xl` and `yl` added
#     4-Jan-2007 (CT)  Removed stale __future__  import of `generators`
#     4-Jan-2007 (CT)  Pass `default_to_now = True` to `Date`
#     6-Jan-2007 (CT)  Options `xo` and `yo` added
#    11-Aug-2007 (CT) Imports corrected
#    ««revision-date»»···
#--

from   _TFL           import TFL
from   _CAL           import CAL
from   _TFL.Filename  import *
from   _TFL.predicate import *
from   _TFL.Regexp    import *
from   _TFL           import sos

import _TFL._Meta.Object
import _CAL.Plan
import _CAL.Year
import _CAL.Date

_non_ascii = Regexp (r"[äöüßÄÖÜ]")
_to_ascii  = \
  { "ä" : "ae"
  , "ö" : "oe"
  , "ü" : "ue"
  , "ß" : "ss"
  , "Ä" : "Ae"
  , "Ö" : "Oe"
  , "Ü" : "Ue"
  }

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
                 , first_week = 0, last_week = -1, wpx = 2, wpy = 2
                 , linewidth  = 0.6, xl = None, yl = None, xo = None, yo = None
                 ) :
        from pdfgen import Canvas
        if last_week < 0 :
            last_week  += len (Y.weeks) + 1
        self.Y          = Y
        self.filename   = filename
        self.first_week = first_week
        self.last_week  = last_week
        self.wpx        = wpx
        self.wpy        = wpy
        self.linewidth  = linewidth
        if xo :
            self.xo     = xo * self.cm
        if yo :
            self.yo     = yo * self.cm
        if xl :
            self.xl     = xl * self.cm
        else :
            self.xl     = (self.xsiz - self.xo) / wpx
        if yl :
            self.yl     = yl * self.cm
        else :
            self.yl     = (self.ysiz - self.yo) / wpy
        self.canvas = c = Canvas (filename, pagesize = (self.xsiz, self.ysiz))
        self.pager  = p = self.page_generator (c)
        c.setPageCompression (0)
        c.setLineJoin        (2)
        wpp = wpx * wpy
        for w in self.seq_generator (first_week, last_week, wpp) :
            page = p.next ()
            if w is not None :
                self.one_week (Y.weeks [w], page)
        c.save ()
    # end def __init__

    def seq_generator (self, first_week, last_week, wpp) :
        s, r   = divmod (last_week - first_week, wpp)
        stride = s + (r > 0)
        for w in range (first_week, first_week + stride) :
            for i in range (wpp) :
                d = i * stride
                if w + d < last_week :
                    yield w + d
                else :
                    yield None
    # end def seq_generator

    def page_generator (self, c) :
        xo = self.xo
        yo = self.yo
        xl = self.xl
        yl = self.yl
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
        c.setFont (font, ts // 2)
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
        lines = int (ds / (ts + 2))
        yo    = y + ds - ts - 1
        ys    = [(yo - (l * (ts + 1))) for l in range (lines)]
        for xo in [x, x + xl // 2] :
            for yo in ys :
                yield xo + 0.1 * self.cm, yo + 1
    # end def line_generator

    def one_day (self, c, d, ds, x, xl, y, yl, font, ts, cm, mm) :
        xo = xl - 0.2 * cm
        c.line            (x, y, xl, y)
        c.setFont         (font, ts)
        c.drawRightString (xo, y + ds * 0.95 - ts, d.formatted ("%d"))
        c.setFont         (font, ts // 5)
        c.drawRightString (xo, y + mm,             d.formatted ("%A"))
        lg = self.line_generator (ds, x, xo - 0.15 * (xl - x), y, ts // 5)
        if d.is_holiday :
            lg.next ()
            xo, yo = lg.next ()
            c.setFont    (font, ts // 2)
            c.drawString (xo, yo, self._cooked (d.is_holiday) [:20])
            c.setFont    (font, ts // 5)
        for a in getattr (d, "appointments", []) :
            try :
                 xo, yo = lg.next ()
            except StopIteration :
                break
            txt = ("%s %s" % (a.time or ">", self._cooked (a.activity))) [:40]
            c.drawString (xo, yo, txt)
    # end def one_day

    def _cooked (self, text) :
        return _non_ascii.sub \
            ( lambda m : _to_ascii.get (m.group (0), "?")
            , text
            )
    # end def _cooked

# end class PDF_Plan

class PDF_Plan_L (PDF_Plan) :

    cm   = PDF_Plan.cm
    xsiz = 29.7 * cm
    ysiz = 21.0 * cm
    xo   = 0.9  * cm

# end class PDF_Plan_L

def _command_spec (arg_array = None) :
    from _TFL.Command_Line import Command_Line
    today    = CAL.Date ()
    year     = today.year
    return Command_Line \
        ( option_spec =
            ( "diary:S=~/diary?Path for calendar file"
            , "filename:S=plan?Filename of plan for `year`"
            , "head_week:I=0?Number of first week to process"
            , "landscape:B?Print in landscape format"
            , "pdf:S=?Generate PDF file with plan"
            , "tail_week:I=-1"
                "?Number of last week to process (negative numbers "
                "counting from the end of the year)"
            , "XL:F?X length of one week (in cm)"
            , "XO:F=0.9?X offset of one week (in cm relative to XL)"
            , "YL:F?Y length of one week"
            , "YO:F=0.5?Y offset of one week (in cm relative to YL)"
            , "year:I=%d?Year for which to process calendar" % (year, )
            )
        , max_args    = 0
        , arg_array   = arg_array
        )
# end def _command_spec

def _main (cmd) :
    year      = cmd.year
    head      = cmd.head_week
    tail      = cmd.tail_week
    path      = sos.path.join (sos.expanded_path (cmd.diary), "%4.4d" % year)
    Y         = CAL.Year  (year)
    wd        = Y.weeks [0].number
    if tail < 0 :
        tail += len (Y.weeks)
    file_name = sos.path.join (path, cmd.filename)
    CAL.read_plan (Y, file_name)
    pdf_name = Filename (cmd.pdf or ("plan_%s.pdf" % year), ".pdf").name
    if cmd.landscape :
        PDF_Plan_L \
            ( Y, pdf_name, head - wd, tail + 1 - wd
            , wpx = 3
            , wpy = 1
            , xl  = cmd.XL
            , yl  = cmd.YL
            , xo  = cmd.XO
            , yo  = cmd.YO
            )
    else :
        PDF_Plan \
            ( Y, pdf_name, head - wd, tail + 1 - wd
            , xl  = cmd.XL
            , yl  = cmd.YL
            , xo  = cmd.XO
            , yo  = cmd.YO
            )
# end def _main

"""
export PYTHONPATH=$PYTHONPATH:/swing/private/tanzer/ttt/lib/old/pdfgen
python pdf.py -year 2007 -landscape -XL 8.95 -YL 16.85 -XO=1.5
"""

if __name__ == "__main__" :
    _main (_command_spec ())
else :
    CAL._Export ("*")
### __END__ CAL.pdf
