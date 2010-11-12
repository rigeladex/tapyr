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
#    12-Mar-2010 (CT) Children `Day`, `Week`, and `Year` added
#    12-Nov-2010 (CT) `_Mixin_` factored, `Q` added and used
#    ««revision-date»»···
#--

from   _CAL                     import CAL
from   _GTW                     import GTW
from   _TFL                     import TFL

import _CAL.Calendar
import _GTW._NAV.Base

from   _TFL.defaultdict         import defaultdict_kd
from   _TFL.I18N                import _, _T, _Tn
from   _TFL._Meta.Once_Property import Once_Property

import datetime
from   posixpath                import join  as pjoin

class _Mixin_ (GTW.NAV._Site_Entity_) :

    @property
    def weeks (self) :
        n = self.week_roller_size
        w = self.anchor.week
        return self.year.weeks [w - 1 : w + n - 1]
    # end def weeks

# end class _Mixin_

class Calendar (_Mixin_, GTW.NAV.Dir) :
    """Navigation directory for providing a calendar."""

    day_abbrs          = \
        ( _("Mon"), _("Tue"), _("Wed"), _("Thu")
        , _("Fri"), _("Sat"), _("Sun")
        )
    day_names          = \
        ( _("Monday"), _("Tuesday"), _("Wednesday"), _("Thursday")
        , _("Friday"), _("Saturday"), _("Sunday")
        )
    month_abbrs        = \
        ( _("Jan"), _("Feb"), _("Mar")
        , _("Apr"), _("May"), _("Jun")
        , _("Jul"), _("Aug"), _("Sep")
        , _("Oct"), _("Nov"), _("Dec")
        )
    month_names        = \
        ( _("January"), _("February"), _("March")
        , _("April"),   _("May"),      _("June")
        , _("July"),    _("August"),   _("September")
        , _("October"), _("November"), _("December")
        )
    pid                = "Cal"
    query_prefix       = "q"
    template           = "calendar"
    week_roller_size   = 6

    event_manager_name = "GTW.OMP.EVT.Event_occurs"

    _y                 = datetime.date.today ().year
    year_range         = (_y - 3, _y + 3)
    del _y

    _cal               = None

    anchor             = property (TFL.Getter.today)

    class _Cmd_ (GTW.NAV.Page) :

        implicit          = True
        SUPPORTED_METHODS = set (("GET", ))

    # end class _Cmd_

    class Day (_Cmd_) :

        name         = "day"
        template     = "calendar_day"

    # end class Day

    class Q (_Mixin_, _Cmd_) :

        def rendered (self, handler, template = None) :
            req_data = handler.request.req_data
            if req_data ["Submit"] == _T ("Today") :
                anchor = self.today
            elif "anchor" in req_data :
                anchor = self._cal.day [req_data ["anchor"]]
            wrs = int (req_data.get ("weeks") or self.week_roller_size)
            if anchor != self.anchor :
                y = anchor.year
                self = handler.context ["page"] = self.Year \
                    ( parent = self
                    , anchor = anchor
                    , year   = self._cal.year [y]
                    )
            with self.LET (week_roller_size = wrs) :
                return self.__super.rendered (handler, template)
        # end def rendered

    # end class Q

    class Week (_Cmd_) :

        name         = "week"
        template     = "calendar_week"

    # end class Week

    class Year (_Mixin_, _Cmd_) :

        name         = "year"
        template     = "calendar"

    # end class Day

    def __init__ (self, * args, ** kw) :
        self.__super.__init__ (* args, ** kw)
        if self._cal is None :
            self.__class__._cal  = CAL.Calendar ()
        self.events = defaultdict_kd (self._get_events)
        self._year  = None
        def _day_get_events (this) :
            return self.events [this.date.date]
        _CAL.Year.Day.events = property (_day_get_events)
    # end def __init__

    def day_href (self, day) :
        return pjoin (self.abs_href, day.formatted ("%Y/%m/%d"))
    # end def day_href

    @Once_Property
    def event_manager (self) :
        scope = self.top.scope
        if scope and self.event_manager_name :
            return scope [self.event_manager_name]
    # end def event_manager

    @property
    def q_href (self) :
        return pjoin (self.abs_href, self.query_prefix)
    # end def q_href

    def rendered (self, handler, template = None) :
        ### if we want to display a site-admin specific page (and not
        ### just the page of the first child [a E_Type_Admin]), we'll
        ### need to bypass `_Dir_.rendered`
        return _Mixin_.rendered (self, handler, template)
    # end def rendered

    @property
    def today (self) :
        return self._cal.day [datetime.date.today ().toordinal ()]
    # end def today

    def week_href (self, week) :
        return pjoin (self.abs_href, "%s/week/%s" % (week.year, week.number))
    # end def week_href

    @property
    def year (self) :
        result = self._year
        if result is None or result.number != self.today.year :
            result = self._year = self._cal.year [datetime.date.today ().year]
        return result
    # end def year

    def _get_child (self, child, * grandchildren) :
        try :
            y = int (child)
        except ValueError :
            if child == self.query_prefix and not grandchildren :
                return self.Q (parent = self)
        else :
            if not (self.year_range [0] <= y <= self.year_range [1]) :
                return
            year = self._cal.year [y]
            if not grandchildren :
                if year == self.year :
                    return self
                else :
                    return self.Year (parent = self, year = year)
            elif grandchildren [0] == "week" and len (grandchildren) == 2 :
                try :
                    week = year.weeks [int (grandchildren [1])]
                except (ValueError, LookupError) :
                    return
                return self.Week (parent = self, year = year, week = week)
            elif len (grandchildren) == 2 :
                try :
                    m, d = [int (c) for c in grandchildren]
                    day  = year.dmap [y, m, d]
                except (ValueError, LookupError) :
                    return
                return self.Day (parent = self, year = year, day = day)
    # end def _get_child

    def _get_events (self, date) :
        evm = self.event_manager
        return evm.query_s (date = date).all ()
    # end def _get_events

# end class Calendar

if __name__ != "__main__" :
    GTW.NAV._Export ("*")
### __END__ GTW.NAV.Calendar
