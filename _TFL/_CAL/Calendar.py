# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 Mag. Christian Tanzer. All rights reserved
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
#    Calendar
#
# Purpose
#    Model a calendar used by a single person/group/project
#
# Revision Dates
#    10-Nov-2004 (CT) Creation
#    14-Nov-2004 (CT) `_new_week` added
#    15-Nov-2004 (CT) More doctests added
#    10-Dec-2004 (CT) Small fixes
#    ««revision-date»»···
#--

from   _TFL      import TFL
from   _TFL._CAL import CAL
import _TFL._CAL.Date
import _TFL._CAL.Year
import _TFL._Meta.Object
from   predicate import *
import sos

class _Cal_Dict_ (dict) :

    def __init__ (self, cal, creator) :
        dict.__init__ (self)
        self.cal     = cal
        self.creator = creator
    # end def __init__

    def __getitem__ (self, key) :
        try :
            return dict.__getitem__ (self, key)
        except KeyError :
            try :
                result = self [key] = self.creator (key)
            except KeyboardInterrupt :
                raise
            except StandardError, exc :
                print "_Cal_Dict_", self.creator, exc
                raise KeyError, key
            else :
                return result
    # end def __getitem__

# end class _Cal_Dict_

class Calendar (TFL.Meta.Object) :
    """Model a calendar used by a single person/group/project

       >>> from _TFL._CAL.Date  import *
       >>> d = Date (2004, 11, 15)
       >>> C = Calendar ()
       >>> y = C.year [2004]
       >>> y
       Year (2004)
       >>> y is C.year [2004]
       True
       >>> C.week [d.wk_ordinal] is y.weeks [d.week - 1]
       True
       >>> C = Calendar ()
       >>> len (C.week)
       0
       >>> C.week [d.wk_ordinal]
       week 47 <2004/11/15 to 2004/11/21>
       >>> len (C.week)
       53
    """

    day             = property (lambda s : s._days)
    week            = property (lambda s : s._weeks)
    year            = property (lambda s : s._years)

    def __init__ (self, name = None, root_path = None) :
        self.name   = name
        self._days  = _Cal_Dict_ (self, self._new_day)
        self._weeks = _Cal_Dict_ (self, self._new_week)
        self._years = _Cal_Dict_ (self, self._new_year)
    # end def __init__

    def _new_day (self, date) :
        result = TFL.CAL.Day (self, date)
        ### XXX read appointments
        return result
    # end def _new_day

    def _new_week (self, wko) :
        d = self.day  [wko * 7]
        y = self.year [d.year]
        if wko not in self._weeks :
            if d.month == 1 :
                y = self.year [d.year - 1]
            elif d.month == 12 :
                y = self.year [d.year + 1]
        if wko in self._weeks :
            return self._weeks [wko]
        else :
            print "%s._new_week is stymied: %s" % \
                (self.__class__.__name__, wko)
    # end def _new_week

    def _new_year (self, year) :
        return TFL.CAL.Year (year, cal = self, populate = False)
    # end def _new_year

# end class Calendar

if __name__ != "__main__" :
    TFL.CAL._Export ("*")
### __END__ Calendar
