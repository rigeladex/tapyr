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
#    ATAX.fahrtenbuch
#
# Purpose
#    Fahrtenbuch
#
# Revision Dates
#     4-Jan-2008 (CT) Creation (ported from a perl version)
#     5-Jan-2008 (CT) Use `CAL.Date_Time` instead of (obsolete) `TFL.Date_Time`
#    ««revision-date»»···
#--

from   __future__        import with_statement

from   _ATAX             import ATAX
from   _CAL              import CAL
from   _ATAX.accounting  import ignor_pat
from   _TFL.predicate    import *
from   _TFL.Regexp       import *
from   _TFL._Meta.Once_Property import Once_Property

import _CAL.Date_Time
import _TFL._Meta.Object
import _TFL.Environment

class FB_Entry (TFL.Meta.Object) :
    """Model one entry of a Fahrtenbuch"""

    str_format = r"  %-11s & %8d & %6d & %s"
    tex_format = r"  %-10s & %6d & %6d & %4d & %4d & \sf %s"

    def __init__ (self, date, km_start, km_finis, priv, desc, ** kw) :
        self.date     = date
        self.km_start = float (km_start)
        self.km_finis = float (km_finis)
        self.priv     = float (priv or 0)
        self.desc, _, self.comment = split_hst (desc, "%")
        self.__dict__.update (kw)
    # end def __init__

    @Once_Property
    def delta (self) :
        return self.km_finis - self.km_start
    # end def delta

    @Once_Property
    def km_business (self) :
        return self.delta * (1.0 - self.priv / 100.)
    # end def km_business

    @Once_Property
    def km_private (self) :
        return self.delta * (self.priv / 100.)
    # end def km_private

    def tex (self) :
        date    = self.date.formatted ("%d.%m.%Y")
        bus_km  = self.km_business
        priv_km = self.km_private
        desc    = self.desc ### TeX-quote `desc`
        return self.tex_format % \
            (date, self.km_start, self.km_finis, bus_km, priv_km, desc)
    # end def tex

    def __nonzero__ (self) :
        return bool (self.delta)
    # end def __nonzero__

    def __str__ (self) :
        date = self.date.formatted ("%d.%m.%Y")
        return self.str_format % (date, self.km_finis, self.priv, self.desc)
    # end def __str__

# end class FB_Entry

class Fahrtenbuch (TFL.Meta.Object) :
    """Model a Fahrtenbuch"""

    lines_per_page = 50
    Entry          = FB_Entry

    def __init__ (self, user, entries = []) :
        self.user    = user
        self.entries = []
        for e in entries :
            self.add (e)
    # end def __init__

    def add (self, entry) :
        self.entries.append (entry)
    # end def add

    @classmethod
    def from_file (cls, user, file_name) :
        result = cls (user)
        add    = result.add
        last   = None
        with open (file_name) as file :
            for line in result._read_lines (file) :
                try :
                    d, km, priv, desc = [f.strip () for f in line.split ("&", 4)]
                except ValueError :
                    print "Split error `%s`" % line
                else :
                    last = result._new_entry (last, d, km, priv, desc)
                    add (last)
        return result
    # end def from_file

    def tex (self) :
        result  = []
        entries = self.entries
        if entries :
            head    = entries [0]
            tail    = entries [-1]
            h_date  = head.date.formatted ("%m/%Y")
            t_date  = tail.date.formatted ("%m/%Y")
            dates   = h_date
            if h_date != t_date :
                dates = "%s -- %s" % (h_date, t_date)
            add    = result.append
            add ( ( r"\def\fahrtenbuchpageheader"
                    r"{\begin{Larger}\bf "
                    r"\strut\triline{Fahrtenbuch}{%s}{%s}"
                    r"\end{Larger}"
                    r"\par\vspace{0.0cm}"
                    r"}"
                  )
                % (self.user, dates)
                )
            add (r"\begin{fahrtenbuch}")
            i   = 1
            lpp = self.lines_per_page
            for e in entries :
                if e :
                    sep = [r"\\ ", r"\CR"] [(i % 5) == 0]
                    add ("%s %s" % (e.tex (), sep.strip ()))
                    i += 1
                    if i > lpp :
                        add (r"\end{fahrtenbuch}")
                        add (r"\\ \hbox{\strut}\hfill ./..%")
                        add (r"\begin{fahrtenbuch}")
                        i = 1
            add (r"\hline\hline")
            kmb  = sum (e.km_business for e in entries)
            kmp  = sum (e.km_private  for e in entries)
            priv = 0
            if kmp :
                priv = 100.0 / ((kmb + kmp) / kmp)
            add ( FB_Entry.tex_format
                % ( "Total", head.km_start, tail.km_finis, kmb, kmp
                  , r"\hfill Privatanteil = \percent{%5.2f} \CR" % priv
                  )
                )
            add (r"\end{fahrtenbuch}")
        return "\n".join (result)
    # end def tex

    def _new_entry (self, last, d, km_finis, priv, desc) :
        km_start = km_finis
        if last is not None :
            km_start = last.km_finis
        return self.Entry \
            (CAL.Date_Time.from_string (d), km_start, km_finis, priv, desc)
    # end def _new_entry

    def _read_lines (self, file) :
        for line in file.readlines () :
            line = line.strip ()
            if line and not ignor_pat.match (line) :
                yield line
    # end def _read_lines

    def __str__ (self) :
        return "\n".join (str (e) for e in self.entries)
    # end def __str__

# end class Fahrtenbuch

def command_spec (arg_array = None) :
    from   _TFL.Command_Line import Command_Line
    return Command_Line \
        ( option_spec =
            ( "-Config:P,?Config file(s)"
            , "-user:S=%s" % TFL.Environment.username.capitalize ()
            )
        , arg_spec    =
            ( "fahrtenbuch:P?File defining fahrtenbuch"
            )
        , min_args    = 1
        , max_args    = 1
        , arg_array   = arg_array
        )
# end def command_spec

def main (cmd) :
    ATAX.Main.load_config (cmd)
    fb = Fahrtenbuch.from_file (cmd.user, cmd.fahrtenbuch)
    print fb.tex ()
# end def main

if __name__ != "__main__" :
    ATAX._Export ("*")
else :
    main (command_spec ())
### __END__ ATAX.fahrtenbuch
