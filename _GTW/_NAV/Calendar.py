# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.NAV.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    GTW.NAV.Calendar
#
# Purpose
#    Navigation directory for providing a calendar
#
# Revision Dates
#     9-Mar-2010 (CT) Creation
#    ««revision-date»»···
#--

from   _CAL                     import CAL
from   _GTW                     import GTW
from   _TFL                     import TFL

import _CAL.Calendar
import _GTW._NAV.Base

import datetime
from   posixpath                import join  as pjoin

class Calendar (GTW.NAV.Dir) :
    """Navigation directory for providing a calendar."""

    day_names        = \
        ( "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"
        , "Saturday", "Sunday"
        )
    pid              = "Cal"
    template         = "calendar"
    week_roller_size = 6

    def __init__ (self, * args, ** kw) :
        self.__super.__init__ (* args, ** kw)
        self._cal  = CAL.Calendar ()
        self._year = None
    # end def __init__

    def day_href (self, day) :
        return pjoin (self.abs_href, day.formatted ("%Y%m%d"))
    # end def day_href

    ### if we want to display a site-admin specific page (and not
    ### just the page of the first child [a E_Type_Admin]), we'll
    ### need to bypass `_Dir_.rendered`
    def rendered (self, handler, template = None) :
        return GTW.NAV._Site_Entity_.rendered (self, handler, template)
    # end def rendered

    @property
    def today (self) :
        return self._cal.day [datetime.date.today ().toordinal ()]
    # end def today

    def week_href (self, week) :
        return pjoin (self.abs_href, "%s-wk-%s" % (week.year, week.number))
    # end def week_href

    @property
    def weeks (self) :
        n     = self.week_roller_size
        today = self.today
        w     = today.week
        return self.year.weeks [w - 1 : w + n - 1]
    # end def weeks

    @property
    def year (self) :
        result = self._year
        if result is None or result.number != self.today.year :
            result = self._year = self._cal.year [datetime.date.today ().year]
            result.populate ()
        return result
    # end def year

# end class Calendar

if __name__ != "__main__" :
    GTW.NAV._Export ("*")
### __END__ GTW.NAV.Calendar
