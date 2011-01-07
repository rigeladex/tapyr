# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010-2011 Mag. Christian Tanzer All rights reserved
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
#    15-Nov-2010 (CT) `Q.rendered` changed to use separate `input`
#                     elements for `year`, `month`, and `day` of `anchor`
#    15-Nov-2010 (CT) `QX` added
#    16-Nov-2010 (CT) `weeks` changed to use `_cal.week` instead of `year.weeks`
#    16-Nov-2010 (CT) `Q._q_args` factored (and call wrapped in try/except)
#    16-Nov-2010 (CT) `Q._q_delta` added and used
#    17-Nov-2010 (CT) `Day.template_qx` added and used in `Calendar._get_child`
#    17-Nov-2010 (CT) `_q_delta` adapted to use of two input/select elements for
#                     `delta` and `delta_unit`
#    26-Nov-2010 (CT) Adapted to change of name of input-elements of
#                     `week_roller_ctrl`
#    16-Dec-2010 (CT) Redefine `delegate_view_p` instead of bypassing
#                     `__super.rendered`
#     3-Jan-2011 (CT) Introduce `template_name`
#     3-Jan-2011 (CT) `delegate_view_p` replaced by `dir_template_name`
#     7-Jan-2011 (CT) `is_current_dir` redefined
#    ««revision-date»»···
#--

from   _CAL                     import CAL
from   _GTW                     import GTW
from   _TFL                     import TFL

import _CAL.Calendar
import _CAL.Delta
import _GTW._NAV.Base

from   _TFL.defaultdict         import defaultdict_kd
from   _TFL.I18N                import _, _T, _Tn
from   _TFL.Regexp              import Regexp, re
from   _TFL._Meta.Once_Property import Once_Property

import datetime
from   posixpath                import join  as pjoin

class _Mixin_ (GTW.NAV._Site_Entity_) :

    @property
    def weeks (self) :
        n = self.week_roller_size
        w = self.anchor.wk_ordinal
        return [self._cal.week [i] for i in range (w - 1, w + n - 1)]
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
    dir_template_name  = template_name = "calendar"
    pid                = "Cal"
    q_prefix           = "q"
    qx_prefix          = "qx"
    week_roller_size   = 6

    event_manager_name = "GTW.OMP.EVT.Event_occurs"

    year_window_size   = 3

    _cal               = None

    anchor             = property (TFL.Getter.today)

    class _Cmd_ (GTW.NAV.Page) :

        implicit          = True
        template_qx_name  = None
        SUPPORTED_METHODS = set (("GET", ))

        def is_current_dir (self, nav_page) :
            p = self.parent
            return p.prefix.startswith (nav_page.prefix)
        # end def is_current_dir

    # end class _Cmd_

    class Day (_Cmd_) :

        name              = "day"
        qx_p              = False
        template_name     = "calendar_day"
        template_qx_name  = "calendar_day_qx"

        def rendered (self, handler, template = None) :
            result = self.__super.rendered (handler, template)
            if 0 and self.qx_p :
                result = handler.json \
                    ( dict
                        ( html     = result
                        , day      = self.day.day
                        , month    = self.day.month
                        , year     = self.day.year
                        )
                    )
            return result
        # end def rendered

    # end class Day

    class Q (_Mixin_, _Cmd_) :

        def rendered (self, handler, template = None) :
            try :
                q_args = self._q_args (handler)
            except Exception, exc :
                print exc
                raise self.top.HTTP.Error_404 (handler.request.path)
            if q_args.anchor != self.anchor :
                self = handler.context ["page"] = self.__class__ \
                    ( parent = self
                    , anchor = q_args.anchor
                    )
            with self.LET (week_roller_size = q_args.week_roller_size) :
                return self._rendered (handler, template)
        # end def rendered

        def _q_args (self, handler) :
            anchor     = self.anchor
            req_data   = handler.request.req_data
            if req_data.get ("Today") :
                anchor = self.today
            else :
                y      = int (req_data.get ("year")  or anchor.year)
                m      = int (req_data.get ("month") or anchor.month)
                d      = int (req_data.get ("day")   or anchor.day)
                anchor = self._cal.day ["%4.4d/%2.2d/%2.2d" % (y, m, d)]
                if req_data.get ("delta") :
                    delta  = self._q_delta (req_data)
                    anchor = self._cal.day [(anchor.date + delta).ordinal]
            wrs = int (req_data.get ("weeks") or self.week_roller_size)
            return TFL.Record \
                ( anchor           = anchor
                , week_roller_size = wrs
                )
        # end def _q_args

        def _q_delta (self, req_data) :
            number = int (req_data.get ("delta"))
            unit   = req_data.get ("delta_unit", "week").rstrip ("s")
            if unit in ("month", "year") :
                DT = CAL.Month_Delta
                if unit == "year" :
                    number *= 12
            elif unit in ("week", "day") :
                DT = CAL.Date_Delta
                if unit == "week" :
                    number *= 7
            else :
                raise ValueError (unit)
            return DT (number)
        # end def _q_delta

        def _rendered (self, handler, template) :
            return self.__super.rendered (handler, template)
        # end def _rendered

    # end class Q

    class QX (Q) :

        template_name = "calendar_qx"

        def _rendered (self, handler, template) :
            anchor = self.anchor
            result = self.__super._rendered (handler, template)
            return handler.json \
                ( dict
                    ( calendar = result
                    , day      = anchor.day
                    , month    = anchor.month
                    , weeks    = self.week_roller_size
                    , year     = anchor.year
                    )
                )
        # end def _rendered

    # end class QX

    class Year (_Mixin_, _Cmd_) :

        name          = "year"
        template_name = "calendar"

        @property
        def anchor (self) :
            return self._cal.day [datetime.date (self.year, 1, 1).toordinal ()]
        # end def anchor

    # end class Day

    def __init__ (self, * args, ** kw) :
        self.__super.__init__ (* args, ** kw)
        if self._cal is None :
            self.__class__._cal  = CAL.Calendar ()
        self.events = defaultdict_kd (self._get_events)
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
    def max_year (self) :
        return self.anchor.year + self.year_window_size
    # end def max_year

    @property
    def min_year (self) :
        return self.anchor.year - self.year_window_size
    # end def min_year

    @property
    def q_href (self) :
        return pjoin (self.abs_href, self.q_prefix)
    # end def q_href

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
            return getattr (self, child.upper ()) (parent = self)
        else :
            qx_p = child == self.qx_prefix
            if qx_p :
                child, grandchildren = grandchildren [0], grandchildren [1:]
            try :
                y = int (child)
            except ValueError :
                return
            else :
                if not (self.min_year <= y <= self.max_year) :
                    return
                year = self._cal.year [y]
                if not grandchildren :
                    if qx_p :
                        return
                    return self.Year (parent = self, year = year)
                elif len (grandchildren) == 2 :
                    try :
                        m, d = [int (c) for c in grandchildren]
                        day  = year.dmap [y, m, d]
                    except (ValueError, LookupError) :
                        return
                    Day = self.Day
                    return Day \
                        ( parent   = self
                        , year     = year
                        , day      = day
                        , qx_p     = qx_p
                        , template =
                            Day.template_qx_name if qx_p else Day.template_name
                        )
    # end def _get_child

    def _get_events (self, date) :
        evm = self.event_manager
        return evm.query_s (date = date).all ()
    # end def _get_events

# end class Calendar

if __name__ != "__main__" :
    GTW.NAV._Export ("*")
### __END__ GTW.NAV.Calendar
