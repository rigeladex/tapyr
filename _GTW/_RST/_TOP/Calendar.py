# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.RST.TOP.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.RST.TOP.Calendar
#
# Purpose
#    Page displaying a calendar
#
# Revision Dates
#     2-Aug-2012 (CT) Creation (based on GTW.NAV.Calendar)
#     2-Aug-2012 (CT) Redefine `Calendar.Day.rendered` to handle `qx`
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _CAL                     import CAL
from   _GTW                     import GTW
from   _TFL                     import TFL

import _CAL.Calendar
import _CAL.Delta

import _GTW._RST.HTTP_Method
import _GTW._RST._TOP.Dir
import _GTW._RST._TOP.Page

from   _TFL.defaultdict         import defaultdict_kd
from   _TFL.I18N                import _, _T, _Tn
from   _TFL.Regexp              import Regexp, re
from   _TFL._Meta.Once_Property import Once_Property

import datetime
from   posixpath                import join  as pp_join

class _Cal_Method_ (GTW.RST.HTTP_Method) :

    _do_change_info        = GTW.RST.HTTP_Method._do_change_info_skip

# end class _Cal_Method_

class _Mixin_ (GTW.RST.TOP._Base_) :

    @property
    def weeks (self) :
        n = self.week_roller_size
        w = self.anchor.wk_ordinal
        return [self._cal.week [i] for i in range (w - 1, w + n - 1)]
    # end def weeks

# end class _Mixin_

_Ancestor = GTW.RST.TOP.Page

class _Cal_Page_ (_Ancestor) :

    args               = (None, )
    implicit           = True

    _exclude_robots    = True

    class _Cal_Page_GET_ (_Cal_Method_, _Ancestor.GET) :

        _real_name             = "GET"

    GET = _Cal_Page_GET_ # end class

# end class _Cal_Page_

class _Day_ (_Cal_Page_) :
    """Page displaying calendary events for a specific day."""

    page_template_name = "calendar_day"
    template_qx_name   = "calendar_day_qx"

    def rendered (self, context, template = None) :
        if self.qx_p :
            T          = self.top.Templateer
            template   = T.get_template (self.template_qx_name)
            call_macro = template.call_macro
            result     = call_macro ("day", self, self.day)
        else :
            result = self.__super.rendered (context, template)
        return result
    # end def rendered

# end class _Day_

_Ancestor = GTW.RST.TOP.Dir_V

class _Year_ (_Cal_Page_) :
    """Page displaying calendar for a specific year."""

    @property
    def anchor (self) :
        return self._cal.day [datetime.date (self.year, 1, 1).toordinal ()]
    # end def anchor

# end class _Year_

_Ancestor = GTW.RST.TOP.Dir_V

class Calendar (_Mixin_, _Ancestor) :
    """Page displaying a calendar."""

    Day                = _Day_
    Year               = _Year_

    dir_template_name  = "calendar"
    event_manager_name = "GTW.OMP.EVT.Event_occurs"
    page_template_name = "calendar"
    pid                = "Cal"
    week_roller_size   = 6
    year_window_size   = 3

    _cal               = None
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

    anchor             = property (TFL.Getter.today)

    class _Calender_GET_ (_Cal_Method_, _Ancestor.GET) :

        _real_name             = "GET"

    GET = _Calender_GET_ # end class

    def __init__ (self, ** kw) :
        self.__super.__init__ (** kw)
        if self._cal is None :
            self.__class__._cal   = CAL.Calendar   ()
            self.__class__.events = defaultdict_kd (self._get_events)
            def _day_get_events (this) :
                return self.events [this.date.date]
            _CAL.Year.Day.events = property (_day_get_events)
    # end def __init__

    def day_href (self, day) :
        return pp_join (self.abs_href, day.formatted ("%Y/%m/%d"))
    # end def day_href

    @Once_Property
    def event_manager (self) :
        scope = self.top.scope
        if scope and self.event_manager_name :
            return scope [self.event_manager_name]
    # end def event_manager

    @property
    def max_year (self) :
        return self.anchor.year + self.year_window_size
    # end def max_year

    @property
    def min_year (self) :
        return self.anchor.year - self.year_window_size
    # end def min_year

    @property
    def today (self) :
        return self._cal.day [datetime.date.today ().toordinal ()]
    # end def today

    @property
    def year (self) :
        return self._cal.year [self.anchor.year]
    # end def year

    def _get_child (self, child, * grandchildren) :
        if child in (self.q_prefix, self.qx_prefix) and not grandchildren :
            result = getattr (self, child.upper ()) (parent = self)
        else :
            result = None
            qx_p   = child == self.qx_prefix
            if qx_p :
                child, grandchildren = grandchildren [0], grandchildren [1:]
            try :
                y = int (child)
            except ValueError :
                pass
            else :
                if self.min_year <= y <= self.max_year :
                    year = self._cal.year [y]
                    if not grandchildren :
                        if not qx_p :
                            result = self.Year (parent = self, year = year)
                    elif len (grandchildren) == 2 :
                        try :
                            m, d = [int (c) for c in grandchildren]
                            day  = year.dmap [y, m, d]
                        except (ValueError, LookupError) :
                            pass
                        else :
                            Day = self.Day
                            return Day \
                                ( day    = day
                                , name   = str (day)
                                , parent = self
                                , qx_p   = qx_p
                                , year   = year
                                )
        return result
    # end def _get_child

    def _get_events (self, date) :
        evm = self.event_manager
        return evm.query_s (date = date).all ()
    # end def _get_events

# end class Calendar

if __name__ != "__main__" :
    GTW.RST.TOP._Export ("*")
### __END__ GTW.RST.TOP.Calendar
