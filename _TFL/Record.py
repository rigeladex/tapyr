# -*- coding: iso-8859-1 -*-
# Copyright (C) 2000-2003 Mag. Christian Tanzer. All rights reserved
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
#    TFL.Record
#
# Purpose
#    Class emulating a struct/record (but dynamically)
#
# Revision Dates
#    14-Jun-2000 (CT) Creation
#    11-Sep-2000 (CT) `quote' added to `str'
#    21-Jan-2001 (CT) `__getattr__' uses `try/except' instead of `has_key'
#    16-Apr-2003 (CT) `copy` added
#    21-Jan-2006 (MG)  Moved into `TFL` package
#    ««revision-date»»···
#--

from   _TFL.predicate import sorted

class Record :

    def __init__ (self, ** kw) :
        self.__dict__ ["kw"] = kw.copy ()
    # end def __init__

    def copy (self, ** kw) :
        result = self.__class__ (** self.kw)
        result.kw.update (kw)
        return result
    # end def copy

    def __str__ (self) :
        return "(%s)" % (self._formatted_kw (), )
    # end def __str__

    def _formatted_kw (self, key_quote = "", value_quote = "") :
        return ", ".join \
            ( map ( lambda (k, v), kq = key_quote, vq = value_quote
                  : "%s%s%s = %s%s%s" % (kq, k, kq, vq, v, vq)
                  , sorted (self.kw.items ())
                  )
            )
    # end def _formatted_kw

    def __repr__ (self) :
        return "%s (%s)" % \
            (self.__class__.__name__, self._formatted_kw ('', '"""'))
    # end def __repr__

    def __getattr__ (self, name) :
        try :
            return self.kw [name]
        except KeyError :
            raise AttributeError, name
    # end def __getattr__

    def __setattr__ (self, name, value) :
        self.kw [name] = value
    # end def __setattr__

# end class Record

if __name__ != "__main__" :
    from _TFL import TFL
    TFL._Export ("*")
### __END__ TFL.Record
