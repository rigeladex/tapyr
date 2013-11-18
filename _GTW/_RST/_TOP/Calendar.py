# -*- coding: utf-8 -*-
# Copyright (C) 2012-2013 Mag. Christian Tanzer All rights reserved
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
#     3-Aug-2012 (CT) Factor `_render_macro`, add `Calendar.Q`
#     6-Aug-2012 (CT) Replace `_do_change_info_skip` by `skip_etag`
#     6-Aug-2012 (MG) Consider `hidden`in  `is_current_dir`
#     9-Aug-2012 (CT) Fix `is_current_dir` (test for "/" after `startswith`)
#    10-Aug-2012 (CT) Move `_Cal_Page_.is_current_dir` to
#                     `Calendar.is_current_page`
#    22-Jan-2013 (CT) Remove spurious `handler.`
#     6-Apr-2013 (CT) Fix typo
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
from   _TFL.Decorator           import getattr_safe
from   _TFL.I18N                import _, _T, _Tn
from   _TFL.Regexp              import Regexp, re
from   _TFL._Meta.Once_Property import Once_Property

import datetime
from   posixpath                import join  as pp_join

class _Mixin_ (GTW.RST.TOP._Base_) :

    @property
    @getattr_safe
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
    skip_etag          = True

    _exclude_robots    = True

    def _render_macro (self, t_name, m_name, * args) :
        T          = self.top.Templateer
        template   = T.get_template (t_name)
        call_macro = template.call_macro
        result     = call_macro (m_name, self, * args)
        return result
    # end def _render_macro

# end class _Cal_Page_

class _Day_ (_Cal_Page_) :
    """Page displaying calendary events for a specific day."""

    macro_name         = "day"
    page_template_name = "calendar_day"
    template_qx_name   = "calendar_day_qx"

    def rendered (self, context, template = None) :
        if self.qx_p :
            result = self._render_macro \
                (self.template_qx_name, self.macro_name, self.day)
        else :
            result = self.__super.rendered (context, template)
        return result
    # end def rendered

# end class _Day_

class _Q_ (_Mixin_, _Cal_Page_) :
    """Pseudo page handling queries."""

    args               = 0
    macro_name         = "week_roller_body"
    page_template_name = "calendar"
    template_qx_name   = "calendar_qx"

    def rendered (self, context, template = None) :
        anchor   = self.anchor
        method   = context ["http_method"]
        request  = context ["request"]
        response = context ["response"]
        try :
            qa   = self._q_args (anchor, request)
        except Exception, exc :
            raise self.Status.Not_Found (exc)
        if qa.anchor == self.anchor :
            this = self
        else :
            this = context ["page"] = self.__class__ \
                ( parent = self
                , anchor = qa.anchor
                )
        with this.LET (week_roller_size = qa.week_roller_size) :
            if this.qx_p :
                response.renderer = GTW.RST.Mime_Type.JSON (method, this)
                result = dict \
                    ( calendar = this._render_macro
                        (this.template_qx_name, this.macro_name, this.weeks)
                    , day      = anchor.day
                    , month    = anchor.month
                    , weeks    = this.week_roller_size
                    , year     = anchor.year
                    )
            else :
                result = this.__super.rendered (context, template)
        return result
    # end def rendered

    def _q_args (self, anchor, request) :
        req_data   = request.req_data
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

# end class _Q_

_Ancestor = GTW.RST.TOP.Dir_V

class _Year_ (_Cal_Page_) :
    """Page displaying calendar for a specific year."""

    @property
    @getattr_safe
    def anchor (self) :
        return self._cal.day [datetime.date (self.year, 1, 1).toordinal ()]
    # end def anchor

# end class _Year_

_Ancestor = GTW.RST.TOP.Dir_V

class Calendar (_Mixin_, _Ancestor) :
    """Page displaying a calendar."""

    Day                = _Day_
    Q                  = _Q_
    Year               = _Year_

    dir_template_name  = "calendar"
    event_manager_name = "GTW.OMP.EVT.Event_occurs"
    page_template_name = "calendar"
    pid                = "Cal"
    skip_etag          = True
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

    def __init__ (self, ** kw) :
        self.calendar = self
        self.__super.__init__ (** kw)
        if self._cal is None :
            self.__class__._cal   = CAL.Calendar   ()
            self.__class__.events = defaultdict_kd (self._get_events)
            def _day_get_events (this) :
                return self.events [this.date.date]
            _CAL.Year.Day.events = property (_day_get_events)
    # end def __init__

    @Once_Property
    @getattr_safe
    def event_manager (self) :
        scope = self.top.scope
        if scope and self.event_manager_name :
            return scope [self.event_manager_name]
    # end def event_manager

    @property
    @getattr_safe
    def max_year (self) :
        return self.anchor.year + self.year_window_size
    # end def max_year

    @property
    @getattr_safe
    def min_year (self) :
        return self.anchor.year - self.year_window_size
    # end def min_year

    @property
    @getattr_safe
    def today (self) :
        return self._cal.day [datetime.date.today ().toordinal ()]
    # end def today

    @property
    @getattr_safe
    def year (self) :
        return self._cal.year [self.anchor.year]
    # end def year

    def day_href (self, day) :
        return pp_join (self.abs_href, day.formatted ("%Y/%m/%d"))
    # end def day_href

    def is_current_page (self, page) :
        ### don't guard against hidden !!!
        p = page.href
        s = self.calendar.href
        return p == s or (p.startswith (s) and p [len (s)] == "/")
    # end def is_current_dir

    def _get_child (self, child, * grandchildren) :
        qx_p = child == self.qx_prefix
        if child in (self.q_prefix, self.qx_prefix) and not grandchildren :
            result = self.Q (name = child, parent = self, qx_p = qx_p)
        else :
            result = None
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
