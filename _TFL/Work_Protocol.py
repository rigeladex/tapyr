#! /swing/bin/python
# Copyright (C) 2002 Mag. Christian Tanzer. All rights reserved
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
#    TFL.Work_Protocol
#
# Purpose
#    Classes for processing protocol of work time
#
# Revision Dates
#    15-Dec-2002 (CT) Creation
#    ««revision-date»»···
#--

from Date_Time import *
from predicate import *
from Regexp    import *

ignor_pat       = Regexp ( r"^\s*[«%#]", re.X)
eol_comment_pat = Regexp ( r"\s*[%#].*$", re.X)
time_range_pat  = Regexp ( r"^"
                           r"(?P<h1> \d+ (?: : (?P<m1> \d+) )?)"
                           r"-"
                           r"(?P<h2> \d+ (?: : (?P<m2> \d+) )?)"
                           r"$"
                         , re.X
                         )

««py-statement»»···

def to_hours (spec, round_to = 15) :
    h, m = map (int, spec.split (":"))
    m    = int ((m + int (round_to / 2)) / round_to) * round_to
    return h + (m / 60.)
# end def to_hours

def wp_lines (wp, lines, field_sep = "&", cat_sep = ":") :
    """Add `lines` to work protocol `wp`"""
    fsep    = Regexp (r"\s* %s \s*" % (field_sep, ), re.X)
    csep    = Regexp (r"\s* %s \s*" % (cat_sep, ), re.X)
    entries = []
    for line in lines :
        line = line.strip ()
        if not line : continue
        if ignor_pat.match (line) : continue
        dat, tim, cats, desc = fsep.split_n (line, 4)
        cats                 = [c.strip () for c in csep.split (cats)]
        entries.append ((dat, tim, cats, desc))
    for e, f in pairwise (entries) :
        e_dat, e_tim, e_cats, e_desc = e
        f_dat, f_tim, f_cats, f_desc = f
        d = Date (e_dat)
        if time_range_pat.match (e_tim) :
            head = time_range_pat.h1
            tail = time_range_pat.h2
        else :
            head = e_tim
            tail = f_tim
        hours = to_hours (tail) - to_hours (head) or 0.25
    ««py-statement»»···
# end def wp_lines

««py-statement»»···

««py-test-def»»···
««py-script-code»»
### __END__ Work_Protocol
