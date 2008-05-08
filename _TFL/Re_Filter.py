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
#    TFL.Re_Filter
#
# Purpose
#    Provide classes for filtering with regexes
#
# Revision Dates
#     6-May-2008 (CT) Creation
#    ««revision-date»»···
#--

from    _TFL.Regexp import *
import  _TFL.Command_Line
import  _TFL.Filter

class Re_Filter (TFL.Filter) :
    """Return all items of an iterable of strings that match a Regexp.

       >>> f = Re_Filter ("(foo|bar)")
       >>> g = ~ f
       >>> l = ["fool", "abc", "barroom", "fubar", "zoppl", "sucks"]
       >>> f.filter (l)
       ['fool', 'barroom', 'fubar']
       >>> g.filter (l)
       ['abc', 'zoppl', 'sucks']
    """

    def __new__ (cls, * args, ** kw) :
        return super (Re_Filter, cls).__new__ (cls, None)
    # end def __new__

    def __init__ (self, pattern, flags = 0, quote = 0) :
        if isinstance (pattern, Regexp) :
            regexp = pattern
        else :
            regexp = Regexp (pattern, flags, quote)
        self._regexp = regexp
        super (Re_Filter, self).__init__ (self.match)
    # end def __init__

    def match (self, item) :
        return self._regexp.search (item)
    # end def match

# end class Re_Filter

class Re_Filter_OA (Re_Filter) :
    """Return all objects with a specific attributes matching a Regexp."""

    def __init__ (self, attr, pattern, flags = 0, quote = 0) :
        self._attr = attr
        super (Re_Filter_OA, self).__init__ (pattern, flags = 0, quote = 0)
    # end def __init__

    def match (self, obj) :
        return self.__super.match (getattr (obj, self._attr))
    # end def match

# end class Re_Filter_OA

class Re_Filter_Opt (TFL.Opt) :
    """Re_Filter option class for use with TFL.Command_Line."""

    default_type = "T"
    _cooked_     = Re_Filter

    def __init__ (self, name, description = "", ** kw) :
        kw.setdefault ("auto_split", """\n""")
        self.__super.__init__ (name, description = description, ** kw)
    # end def __init__

    def value_1 (self) :
        result = self.__super.value_1 ()
        if result :
            return self._cooked_ (result)
    # end def value_1

    def values (self) :
        result = self.__super.values ()
        if result :
            cooked = self._cooked_
            return TFL.Filter_And (* (cooked (r) for r in result))
    # end def values

# end class Re_Filter_Opt

class Re_Filter_OA_Opt (Re_Filter_Opt) :
    """Re_Filter_OA option class for use with TFL.Command_Line."""

    def _cooked_ (self, v) :
        attr, pattern = v.split (":", 1)
        return Re_Filter_OA (attr, pattern)
    # end def _cooked_

# end class Re_Filter_OA_Opt

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.Re_Filter
