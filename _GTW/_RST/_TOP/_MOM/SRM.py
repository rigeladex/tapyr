# -*- coding: utf-8 -*-
# Copyright (C) 2012-2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.RST.TOP.MOM.
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
#    GTW.RST.TOP.MOM.SRM
#
# Purpose
#    Archive of pages displaying regattas
#
# Revision Dates
#    18-Jul-2012 (CT) Creation
#    26-Jul-2012 (CT) Add `Archive.Year.regattas`
#     6-Aug-2012 (CT) Replace `_do_change_info_skip` by `skip_etag`
#    10-Aug-2012 (CT) Add missing `SRM.` to `change_query_filters`
#    10-Aug-2012 (CT) Add `skip_etag` to various classes
#    17-Sep-2012 (CT) Add `is_cancelled` to `Regatta_Event.sort_key`
#     6-Nov-2012 (CT) Add `href_regatta` to `Archive`
#    12-Nov-2012 (CT) Redefine `Regatta._get_child` to return `admin`
#                     factor `_get_bir_admin` for use by `_get_child`
#     5-Dec-2012 (CT) Add `Regatta_Event.regattas`
#     5-Dec-2012 (CT) Fix typo in `Archive.Year.regattas`
#     5-Dec-2012 (CT) Redefine `Archive.Year.sort_key`
#     7-Dec-2012 (CT) Rename `query_filters` to `query_filters_d`
#    17-Mar-2013 (CT) Add `_login_required = False` to `_get_bir_admin`
#     3-May-2013 (CT) Rename `login_required` to `auth_required`
#     4-May-2013 (CT) Add `submit_error_callback`,
#                     factor methods from `_register_submit_callback`
#    23-May-2013 (CT) Add `_regatta_registration_changed_msg`, call it in
#                     `_register_submit_error_callback`
#    14-Jun-2013 (CT) Add CSV-rendering for `Regatta.Registration`
#    15-Jun-2013 (CT) Add guard to CSV-rendering against empty `boats`
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._RST._TOP._MOM.Mixin
import _GTW._RST._TOP.Dir
import _GTW._RST._TOP.Page

from   _MOM.import_MOM          import MOM, Q

from   _TFL._Meta.Property      import Alias_Property
from   _TFL._Meta.Once_Property import Once_Property
from   _TFL.Decorator           import getattr_safe
from   _TFL.I18N                import _, _T, _Tn
from   _TFL.predicate           import first, uniq

import _TFL.defaultdict

from   posixpath                import join as pp_join

import datetime
import itertools

class _Regatta_Page_ (GTW.RST.TOP.MOM.Entity_Mixin_Base, GTW.RST.TOP.Page) :

    skip_etag           = True

# end class _Regatta_Page_

_Ancestor = GTW.RST.TOP.Dir

class Regatta (GTW.RST.TOP.MOM.Entity_Mixin_Base, _Ancestor) :
    """Directory displaying a regatta."""

    bir_admin               = None
    register_email_template = "regatta_register_email"
    skip_etag               = True

    class Registration (_Regatta_Page_) :

        page_template_name  = u"regatta_registration"

        class _Regatta_GET_ (_Regatta_Page_.GET) :

            _real_name      = "GET"
            _renderers      = _Regatta_Page_.GET._renderers + \
                (GTW.RST.Mime_Type.CSV, )

            def _response_body (self, resource, request, response) :
                if response.renderer and response.renderer.name == "CSV" :
                    returner = self._response_body_csv
                else :
                    returner = self.__super._response_body
                return returner (resource, request, response)
            # end def _response_body

            def _response_body_csv (self, resource, request, response) :
                def conv (s) :
                    return unicode (s).encode ("utf-8", "replace")
                boats    = resource.obj.boats
                if not boats :
                    return {}
                max_crew = max (len (b.crew) for b in boats)
                b_names  = \
                    [ "registration_date"
                    , "nation"
                    , "sailnumber"
                    , "boat_class"
                    ]
                c_names  = ["first_name", "last_name", "club", "oesv_no"]
                s_names  = list (".".join (["skipper", c]) for c in c_names)
                s_len    = len (s_names)
                w_names  = list \
                    (   ".".join (["crew", str (i), c])
                    for i in range (1, max_crew+1) for c in c_names
                    )
                names    = list (itertools.chain (b_names, s_names, w_names))
                print ("*" * 5, max_crew, names)
                rows     = []
                result   = dict (names = names, rows = rows)
                for b in boats :
                    row  = dict \
                        ( registration_date = b.FO.registration_date
                        , nation            = b.boat.FO.nation
                        , sailnumber        = b.boat.FO.sail_number
                        , boat_class        = b.boat.FO.b_class
                        )
                    row.update (self._crew_attrs (s_names, b.skipper))
                    for i, c in enumerate (b.crew) :
                        off = s_len * i
                        row.update (self._crew_attrs (w_names [off:], c))
                    rows.append \
                        ( TFL.defaultdict
                            (str, ((k, conv (v)) for k, v in row.items ()))
                        )
                return result
            # end def _response_body_csv

            def _crew_attrs (self, names, crew) :
                return dict \
                    ( zip
                        ( names
                        , [ crew.FO.person.first_name
                          , crew.FO.person.last_name
                          , crew.FO.club
                          , crew.FO.mna_number or ""
                          ]
                        )
                    )
            # end def _crew_attrs

        GET = _Regatta_GET_ # end class

    # end class Registration

    class Result (_Regatta_Page_) :

        page_template_name  = u"regatta_result"

    # end class Result

    class Result_Teamrace (_Regatta_Page_) :

        page_template_name  = u"regatta_result_teamrace"

    # end class Result_Teamrace

    @Once_Property
    @getattr_safe
    def change_query_filters (self) :
        pid    = self.obj.pid
        rq     = self.scope.SRM.Boat_in_Regatta.query \
            (Q.right == pid).attr ("pid")
        result = (Q.OR (Q.pid.IN (rq), Q.pid == pid), )
        return result
    # end def change_query_filters

    @property
    @getattr_safe
    def entries (self) :
        cid = self._changed_cid ()
        if cid is not None or not self._entries :
            self._old_cid   = cid
            self._entries   = []
            self._entry_map = {}
            pages = self._get_pages ()
            self.add_entries (* pages)
        return self._entries
    # end def entries

    def href_register (self) :
        obj = self.obj
        if not obj.is_cancelled :
            if not obj.is_team_race :
                event = obj.event
                start = event.date.start
                now   = event.__class__.date.start.now ()
                if now < start :
                    return pp_join (self.abs_href, "admin", "create")
            ### XXX implement registration for team race, too
    # end def href_register

    def _get_bir_admin (self) :
        bir = self.top.ET_Map ["SRM.Boat_in_Regatta"]
        if bir and bir.admin :
            obj     = self.obj
            scope   = self.scope
            form_kw = dict \
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
            kw = dict \
                ( bir.admin._orig_kw
                , default_qr_kw         = dict (right___EQ = obj.pid)
                , form_id               = "AF_BiR"
                , form_parameters       = dict (form_kw = form_kw)
                , implicit              = True
                , name                  = "admin"
                , parent                = self
                , submit_callback       = self._register_submit_callback
                , submit_error_callback = self._register_submit_error_callback
                , _auth_required        = False
                )
            self.bir_admin = result = bir.admin.__class__ (** kw)
            return result
    # end def _get_bir_admin

    def _get_child (self, child, * grandchildren) :
        result = self.__super._get_child (child, * grandchildren)
        if result is None and child == "admin" :
            result = self._get_bir_admin ()
            if result :
                if ((not self._entries) or self._entries [-1] is not result) :
                    self.add_entries (result)
                if grandchildren :
                    result = result._get_child (* grandchildren)
        return result
    # end def _get_child

    def _get_pages (self) :
        np     = _T (u"Participants")
        nr     = _T (u"Results")
        obj    = self.obj
        result = []
        scope  = self.scope
        sk     = TFL.Sorted_By \
            ("skipper.person.last_name", "skipper.person.first_name")
        Result_Type = None
        if obj.is_team_race :
            try :
                place = first (obj.teams).place
            except IndexError :
                pass
            else :
                if place :
                    Result_Type = self.Result_Teamrace
        else :
            if obj.races :
                Result_Type = self.Result
        if Result_Type :
            result.append \
                ( Result_Type
                    ( ETM         = obj.ETM
                    , name        = nr.lower ()
                    , obj         = obj
                    , parent      = self
                    , regatta     = obj
                    , short_title = nr
                    , title       = u"%s %s" %
                        ( _T (u"Results for"), self.short_title)
                    )
                )
        head = _T (u"List of participants for")
        result.append \
            ( self.Registration
                ( ETM         = obj.ETM
                , head_line   = u"%s %s<br />%s, %s" %
                    ( _T (u"Registration list"), obj.name
                    , obj.event.FO.short_title, obj.event.ui_date
                    )
                , name        = np.lower ()
                , obj         = obj
                , parent      = self
                , regatta     = obj
                , short_title = np
                , title       = u"%s %s"   % (head, self.short_title)
                )
            )
        bir_admin = self._get_bir_admin ()
        if bir_admin :
            result.append (bir_admin)
        return result
    # end def _get_pages

    def _regatta_registration_changed_msg (self, scope, fv) :
        def _gen (scope, fv) :
            results = {}
            for ev in fv.entity_values :
                try :
                    cc = ev.elem._changed_children \
                        (ev, results, scope, ev.entity)
                except Exception as exc:
                    pass
                else :
                    if cc :
                        yield "%s\n    %s\n" % \
                            ( ev
                            , "\n    ".join
                                (   "%-25s: %s" % (k, v)
                                for k, v in sorted (cc.iteritems ())
                                )
                            )
                    else :
                        yield str (ev)
        return "\n\n".join (_gen (scope, fv))
    # end def _regatta_registration_changed_msg

    def _regatta_registration_objects_msg (self, scope, fv) :
        def _ents (scope, fv) :
            for ev in fv.entity_values :
                try :
                    e = ev.entity
                except AttributeError :
                    pass
                else :
                    if e is not None :
                        yield e
        def _gen (scope, entities) :
            from _MOM._Attr import Selector as S
            AQ = S.editable
            for x in sorted (uniq (entities), key = TFL.Getter.type_name) :
                yield x.type_name, tuple \
                    ( "%s = '%s'" % (a.name, getattr (x.FO, a.name))
                    for a in AQ (x)
                    if  a.has_substance (x)
                    )
        result = "\n".join \
            (   "%s (%s)" % (t, ", ".join (a))
            for t, a in _gen (scope, _ents (scope, fv))
            )
        return result
    # end def _regatta_registration_objects_msg

    def _register_submit_callback (self, request, response, scope, fv, result) :
        message = self._regatta_registration_objects_msg (scope, fv)
        self._send_registration_email \
            (request, response, scope, fv, result, message)
    # end def _register_submit_callback

    def _register_submit_error_callback (self, request, response, scope, fv, result) :
        from _TFL.Formatter import Formatter
        formatted = Formatter (width = 1024)
        message = "\n\n-----------------\n\n".join \
            (( self._regatta_registration_objects_msg (scope, fv)
             , "\n\n".join
                 ( "%s\n    %s"
                   % (id, "\n    ".join (formatted (e, 2) for e in errors))
                 for id, errors in fv.errors.iteritems ()
                 )
             , self._regatta_registration_changed_msg (scope, fv)
            ))
        self._send_registration_email \
            (request, response, scope, fv, result, message, "*** failed ***")
    # end def _register_submit_error_callback

    def _send_registration_email \
            ( self, request, response, scope, fv, result, message
            , subject_tail = ""
            ):
        try :
            email = self.email_from
            self.send_email \
                ( self.register_email_template
                , email_from    = email
                , email_to      = email
                , email_subject = _T ("%s: regatta registration %s")
                      % (self.obj.ui_display, subject_tail)
                , message       = message
                , NAV           = self.top
                , page          = self
                , request       = request
                )
        except Exception as exc :
            pyk.fprint \
                ( "Sending regatta registration email to %r failed "
                  "with exception %s"
                % (email, exc)
                )
            pyk.fprint (message)
    # end def _send_registration_email

# end class Regatta

_Ancestor = GTW.RST.TOP.Dir

class Regatta_Event \
          ( GTW.RST.TOP.MOM.Entity_Mixin_Base
          , GTW.RST.TOP.MOM.E_Type_Mixin
          , _Ancestor
          ) :
    """Directory displaying a regatta event."""

    Entity              = Regatta

    dir_template_name   = None
    page_template_name  = "regatta_page"
    skip_etag           = True
    sort_key            = TFL.Sorted_By ("is_cancelled", "perma_name")

    _old_date           = None

    class Page (GTW.RST.TOP.MOM.Display.Entity) :

        skip_etag           = True
        page_template_name  = "regatta_page"

    # end class Page

    def __init__ (self, ** kw) :
        kw ["ETM"] = "SRM.Regatta"
        self.__super.__init__ (** kw)
    # end def __init__

    @Once_Property
    @getattr_safe
    def ETM_P (self) :
        return self.top.scope.SRM.Page
    # end def ETM_P

    @Once_Property
    @getattr_safe
    def change_query_filters (self) :
        pid    = self.obj.pid
        pq     = self.ETM_P.query (Q.event == pid).attr ("pid")
        rq     = self.ETM.query   (Q.left  == pid).attr ("pid")
        result = (Q.OR (Q.pid.IN (rq), Q.pid.IN (pq)), )
        return result
    # end def change_query_filters

    @property
    @getattr_safe
    def entries (self) :
        today = datetime.date.today ()
        if today == self._old_date :
            _old_entries    = self._entries
        else :
            _old_entries    = None
            self._entries   = []
            self._entry_map = {}
            self._old_date  = today
        result = self.__super.entries
        if result is not _old_entries or not result :
            pages = self._get_pages ()
            if today >= self.obj.date.start :
                self.add_entries (* pages)
            else :
                result          = pages + result
                self._entries   = []
                self._entry_map = {}
                self.add_entries (* result)
        return self._entries
    # end def entries

    @property
    @getattr_safe
    def query_filters_d (self) :
        return self.__super.query_filters_d + (Q.left == self.obj.pid, )
    # end def query_filters_d

    @property
    @getattr_safe
    def regattas (self) :
        return [e for e in self.entries if isinstance (e, Regatta)]
    # end def regattas

    def _add_href_pat_frag_tail \
            (self, head, getter = TFL.Getter.href_pat_frag) :
        ### reduce memory consumption by not traversing into `entries`
        return head
    # end def _add_href_pat_frag_tail

    def _get_pages (self) :
        T     = self.Page
        ETM   = self.ETM_P
        pkw   = self.page_args
        kw    = dict (pkw, ETM = ETM)
        query = ETM.query_s (event = self.obj.pid)
        return \
            [T (parent = self, obj = o, page_args = pkw, ** kw) for o in query]
    # end def _get_pages

# end class Regatta_Event

_Ancestor = GTW.RST.TOP.MOM.Display.E_Type_Archive_DSY

class Archive (_Ancestor) :
    """Archive of pages displaying regatta events, organized by year."""

    class _SRM_Year_ (_Ancestor.Year) :

        _real_name          = "Year"

        dir_template_name   = "regatta_calendar"
        Entity              = Regatta_Event
        skip_etag           = True
        sort_key            = TFL.Sorted_By ("date.start", "perma_name")

        @property
        @getattr_safe
        def regattas (self) :
            result = self.entries
            if result and result [-1] is self._admin :
                result = result [:-1]
            return result
        # end def regattas

    Year = _SRM_Year_ # end class

    def __init__ (self, ** kw) :
        kw.setdefault         ("ETM", "SRM.Regatta_Event")
        self.__super.__init__ (** kw)
        top   = self.top
        apt   = top.App_Type
        map   = top.ET_Map
        for k in ( "SRM.Page", "SRM.Regatta_C", "SRM.Regatta_H") :
            et = apt [k]
            map [et.type_name].manager = self
    # end def __init__

    def href_display (self, obj) :
        scope = self.top.scope
        comps = [self.abs_href, str (obj.year)]
        if isinstance (obj, (scope.SRM.Page.E_Type, scope.SRM.Regatta.E_Type)) :
            comps.append (obj.event.perma_name)
        comps.append (obj.perma_name)
        return pp_join (* comps)
    # end def href_display

    href_regatta = href_display

# end class Archive

if __name__ != "__main__" :
    GTW.RST.TOP.MOM._Export_Module ()
### __END__ GTW.RST.TOP.MOM.SRM
