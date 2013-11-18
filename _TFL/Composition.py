# -*- coding: utf-8 -*-
# Copyright (C) 2000-2009 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
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
#    TFL.Composition
#
# Purpose
#    Function composition
#
# Revision Dates
#    19-Apr-2000 (CT)  Creation
#    25-May-2004 (CED) Doctest added
#    30-Oct-2006 (CED) Moved to TFL
#    ««revision-date»»···
#--

from _TFL        import TFL

class Composition :
    """Functor for composing two functions:

       >>> c = Composition (outer = lambda x : x * 2, inner = lambda x : x + 5)
       >>> c (1)
       12
    """

    def __init__ (self, outer, inner) :
        self.outer = outer
        self.inner = inner
    # end def __init__

    def __call__ (self, * args, ** kw) :
        return self.outer (self.inner (* args, ** kw))
    # end def __call__

# end class Composition

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.Composition
