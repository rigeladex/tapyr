# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.NAV.E_Type.
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
#    GTW.NAV.E_Type.SRM
#
# Purpose
#    Navigation directory and pages for instances of SRM
#
# Revision Dates
#    30-Apr-2010 (CT) Creation
#     5-May-2010 (CT) Creation continued
#     7-May-2010 (CT) `Regatta_Event._get_objects` and `._get_pages` changed
#                     to set `ETM` and `E_Type` properly
#    10-May-2010 (CT) `Regatta._get_objects` changed to include `Results`
#    12-May-2010 (CT) `Results._get_objects` changed to sort by `skipper`
#    23-Jun-2010 (MG) `SRM.__init__` changed to use app-type instead of scope
#    17-Aug-2010 (CT) `template` corrected
#    17-Aug-2010 (CT) Switch from `title/desc` to `short_title/title`
#    20-Sep-2010 (CT) `Results._get_objects` changed to support team races, too
#    23-Nov-2010 (CT) `_SRM_Year_` redefined to display `regatta_calendar`
#    14-Dec-2010 (CT) `_SRM_Year_.template` removed (otherwise `entries`
#                     inherit the wrong template)
#    14-Dec-2010 (CT) `SRM` derived from `Manager_T_Archive` instead of
#                     `Manager_T_Archive_Y`
#    16-Dec-2010 (CT) Redefine `delegate_view_p` instead of bypassing
#                     `__super.rendered`
#    22-Dec-2010 (CT) `top.E_Types` replaced by `ET_Map`
#     3-Jan-2011 (CT) `delegate_view_p` replaced by `dir_template_name`
#     5-Jan-2011 (CT) `Registration`, `Result`, and `Result_Teamrace` factored
#     9-Sep-2011 (CT) Use `.E_Type` instead of `._etype`
#     9-Nov-2011 (CT) Fix `head_line` for `Registration`
#     2-Feb-2012 (CT) Add `href_register` and `bir_admin`
#     2-Feb-2012 (CT) Add `Regatta_Event.Page` with template `regatta_page`
#    15-Feb-2012 (CT) Add `Crew_Member.max_links` to `form_kw`
#    24-Apr-2012 (CT) Change `Regatta_Event._get_objects` to determine
#                     sequence according to `today > date.start`
#    30-Apr-2012 (CT) Add and use `_register_submit_callback`
#     7-May-2012 (CT) Change `Regatta._get_objects` to DRY
#     7-May-2012 (CT) Add attribute `bir_admin` to `Regatta`
#    30-May-2012 (CT) Change `href_register` to honor `is_cancelled`
#    18-Jun-2012 (CT) Rename `email` to `email_from`
#    13-May-2013 (CT) Use `query`, not `r_query`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW.FO
import _GTW._NAV.Base
import _GTW._NAV._E_Type.Manager
import _GTW._NAV._E_Type.Mixin

import _TFL._Meta.Object
from   _TFL._Meta.Once_Property import Once_Property

from   _TFL                     import pyk
from   _TFL.I18N                import _, _T, _Tn
from   _TFL.predicate           import first
from   posixpath                import join  as pjoin

import datetime

class Regatta (GTW.NAV.E_Type.Instance_Mixin, GTW.NAV.Dir) :
    """Navigation directory for a single regatta."""

    bir_admin               = None
    register_email_template = "regatta_register_email"

    class Registration (GTW.NAV.Page) :

        template_name = u"regatta_registration"

    # end class Registration

    class Result (GTW.NAV.Page) :

        template_name = u"regatta_result"

    # end class Result

    class Result_Teamrace (GTW.NAV.Page) :

        template_name = u"regatta_result_teamrace"

    # end class Result_Teamrace

    def __init__ (self, manager, obj, ** kw) :
        kw ["src_dir"] = kw ["sub_dir"] = obj.perma_name
        self.__super.__init__ (manager, obj, ** kw)
        self.name = obj.perma_name
    # end def __init__

    def href_register (self) :
        if not self.obj.is_cancelled :
            if not self.obj.is_team_race :
                start = self.obj.event.date.start
                now   = self.obj.event.__class__.date.start.now ()
                if now < start :
                    return pjoin (self.abs_href, "admin", "create")
            ### XXX implement registration for team race, too
    # end def href_register

    def _get_child (self, child, * grandchildren) :
        entries = self._entries or self._get_objects ()
        try :
            result = first (e for e in entries if e.name == child)
        except IndexError :
            if child == "index.html" and not grandchildren :
                return self
        else :
            if grandchildren :
                result = result._get_child (* grandchildren)
            return result
    # end def _get_child

    def _get_objects (self) :
        np     = _T (u"Participants")
        nr     = _T (u"Results")
        obj    = self.obj
        result = []
        scope  = self.scope
        sk     = TFL.Sorted_By \
            ("skipper.person.last_name", "skipper.person.first_name")
        Result_Type = None
        if obj.is_team_race :
            if first (obj.teams).place :
                Result_Type = self.Result_Teamrace
        else :
            obj.boats = scope.SRM.Boat_in_Regatta.query \
                (right = obj).order_by (sk).all ()
            if obj.races :
                Result_Type = self.Result
        if Result_Type :
            result.append \
                ( Result_Type
                    ( self
                    , name        = u"%s.html" % (nr.lower (), )
                    , short_title = nr
                    , title       = u"%s %s" %
                        ( _T (u"Results for"), self.short_title)
                    , regatta     = obj
                    )
                )
        head = _T (u"List of participants for")
        result.append \
            ( self.Registration
                ( self
                , head_line   = u"%s %s<br />%s, %s" %
                    ( _T (u"Registration list"), obj.name
                    , obj.event.FO.short_title, obj.event.ui_date
                    )
                , name        = u"%s.html" % (np.lower (), )
                , short_title = np
                , title       = u"%s %s"   % (head, self.short_title)
                , regatta     = obj
                )
            )
        bir = self.top.ET_Map ["GTW.OMP.SRM.Boat_in_Regatta"]
        if bir and bir.admin :
            form_kw   = dict \
                ( right = dict
                    ( prefilled   = True
                    , init        = obj
                    )
                )
            if isinstance (obj, scope.SRM.Regatta_C.E_Type) :
                form_kw.update \
                    ( left = dict
                        ( left = dict
                            ( prefilled   = True
                            , init        = obj.boat_class
                            )
                        )
                    , Crew_Member = dict
                        ( max_links   = obj.boat_class.max_crew - 1
                        )
                    )
            bir.admin = bir.admin
            kw = dict \
                ( bir.admin._orig_kw
                , default_qr_kw   = dict (right___EQ = obj.pid)
                , form_id         = "AF_BiR"
                , form_parameters = dict (form_kw = form_kw)
                , implicit        = True
                , name            = "admin"
                , parent          = self
                , submit_callback = self._register_submit_callback
                )
            self.bir_admin = ba = bir.admin.__class__ (** kw)
            result.append (ba)
        return result
    # end def _get_objects

    def _register_submit_callback (self, handler, scope, fv, result) :
        def _gen (scope, results) :
            from _MOM._Attr import Selector as S
            AQ = S.List (S.primary, S.user)
            SRM = scope.SRM
            for k, x in sorted (results.iteritems ()) :
                if isinstance (x, (SRM.Boat.E_Type, SRM.Sailor.E_Type)) :
                    yield x.type_name, tuple \
                        ( "%s = '%s'" % (a.name, getattr (x.FO, a.name))
                        for a in AQ (x)
                        if  a.has_substance (x)
                        )
        message = "\n".join \
            (   "%s (%s)" % (t, ", ".join (a))
            for t, a in _gen (scope, fv.results)
            )
        try :
            email = self.email_from
            self.send_email \
                ( self.register_email_template
                , email_from    = email
                , email_to      = email
                , email_subject =
                    _T ("%s: regatta registration") % (self.obj.ui_display, )
                , message       = message
                , NAV           = self.top
                , page          = self
                , request       = handler.request
                )
        except Exception as exc :
            pyk.fprint \
                ( "Sending regatta registration email to %r failed "
                  "with exception %s"
                % (email, exc)
                )
            pyk.fprint (message)
    # end def _register_submit_callback

# end class Regatta

class Regatta_Event (GTW.NAV.E_Type.Instance_Mixin, GTW.NAV.Dir) :
    """Navigation directory for a single regatta event."""

    dir_template_name = None

    class Page (GTW.NAV.E_Type.Instance) :

        template_name = "regatta_page"

    # end class Page

    def __init__ (self, manager, obj, ** kw) :
        kw ["src_dir"] = kw ["sub_dir"] = obj.perma_name
        self.__super.__init__ (manager, obj, ** kw)
    # end def __init__

    def _get_child (self, child, * grandchildren) :
        entries = self._entries
        try :
            result = first (e for e in entries if e.name == child)
        except IndexError :
            if child == "index.html" and not grandchildren :
                return self
        else :
            if grandchildren :
                result = result._get_child (* grandchildren)
            return result
    # end def _get_child

    def _get_objects (self) :
        pkw    = self.page_args
        result = []
        scope  = self.obj.home_scope
        today  = datetime.date.today ()
        for r in sorted (self.obj.regattas, key = TFL.Sorted_By ("name")) :
            kw  = dict \
                ( pkw
                , ETM       = scope [r.type_name]
                , E_Type    = r.__class__
                )
            result.append (Regatta (self, r, page_args = pkw, ** kw))
        pages = self._get_pages ()
        if today >= self.obj.date.start :
            result.extend (pages)
        else :
            result = pages + result
        return result
    # end def _get_objects

    def _get_pages (self) :
        T     = self.Page
        ETM   = self.scope.SRM.Page
        pkw   = self.page_args
        kw    = dict \
            ( pkw
            , ETM       = ETM
            , E_Type    = ETM.E_Type
            )
        rev   = self.obj
        query = ETM.query_s (event = rev)
        return [T (self, o, page_args = pkw, ** kw) for o in query]
    # end def _get_pages

# end class Regatta_Event

_Ancestor = GTW.NAV.E_Type.Manager_T_Archive

class SRM (_Ancestor) :
    """Navigation directory listing regatta events by year."""

    Page              = Regatta_Event

    class _SRM_Year_ (_Ancestor.Year) :

        dir_template_name = "regatta_calendar"

    Year = _SRM_Year_ # end class

    def __init__ (self, src_dir, ** kw) :
        self.__super.__init__ (src_dir = src_dir, ** kw)
        top   = self.top
        app   = top.App_Type
        for et in ( app ["GTW.OMP.SRM.Page"]
                  , app ["GTW.OMP.SRM.Regatta_C"]
                  , app ["GTW.OMP.SRM.Regatta_H"]
                  ) :
            top.ET_Map [et.type_name].manager = self
    # end def __init__

    def href_display (self, obj) :
        scope = self.top.scope
        comps = [self.abs_href, str (obj.year)]
        if isinstance (obj, (scope.SRM.Page.E_Type, scope.SRM.Regatta.E_Type)) :
            comps.append (obj.event.perma_name)
        comps.append (obj.perma_name)
        return pjoin (* comps)
    # end def href_display

    def _get_grandchild (self, y, grandchildren) :
        gc0, gcs = grandchildren [0], grandchildren [1:]
        result   = self.__super._get_grandchild (y, (gc0, ))
        if result and gcs :
            result = result._get_child (* gcs)
        return result
    # end def _get_grandchild

# end class SRM

if __name__ != "__main__" :
    GTW.NAV.E_Type._Export ("*")
### __END__ GTW.NAV.E_Type.SRM
