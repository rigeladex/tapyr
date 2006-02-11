# -*- coding: iso-8859-1 -*-
# Copyright (C) 2000-2006 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
#++
# Name
#    TFL.Black_Hole
#
# Purpose
#    Provides class taking all function calls and attribute accesses thrown at
#    it and ignores them
#
# Revision Dates
#    16-Aug-2000 (CT) Creation
#    11-Feb-2006 (CT) Moved into package `TFL`
#    ««revision-date»»···
#--

from   _TFL             import TFL

class _Black_Hole_ :
    """Takes all function calls and attribute accesses thrown at it and
       ignores them.

       Don't try too apply `dir' to `black_hole' -- it will die slowly.

       `__coerce__' is needed to allow comparisons and the use of
       `black_hole' with unary and binary operators.

    """

    def __init__    (s, * args, ** kw) : pass
    def __call__    (s, * args, ** kw) : return s
    def __cmp__     (s, o)             : return 0
    def __coerce__  (s, o)             : return s, s
    def __getattr__ (s, n)             : return s
    def __hash__    (s)                : return 0
    def __len__     (s)                : return 0
    def __nonzero__ (s)                : return 0
    def __repr__    (s)                : return "<_Black_Hole_ at %s>" % id (s)
    def __str__     (s)                : return ""

# end class _Black_Hole_

black_hole = _Black_Hole_ ()

if __name__ != "__main__" :
    TFL._Export ("black_hole", "_Black_Hole_")
### __END__ TFL.Black_Hole
