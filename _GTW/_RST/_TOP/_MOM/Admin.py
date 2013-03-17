# -*- coding: iso-8859-15 -*-
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
#    GTW.RST.TOP.MOM.Admin
#
# Purpose
#    Directories and pages for managing instances of MOM E-types
#
# Revision Dates
#    19-Jul-2012 (CT) Creation
#    25-Jul-2012 (CT) Fix `Alias`: delegate `ETM` to `target`
#     2-Aug-2012 (CT) Use `response.renderer`, not `request.renderer`
#     6-Aug-2012 (CT) Replace `_do_change_info_skip` by `skip_etag`
#     6-Aug-2012 (MG) Consider `hidden`in  `is_current_dir`
#     9-Aug-2012 (CT) Fix `is_current_dir` (test for "/" after `startswith`)
#     9-Aug-2012 (CT) Redefine `E_Type.entries` to avoid version from mixin
#    10-Aug-2012 (CT) Use `logging.exception` instead of `print`
#    13-Aug-2012 (CT) Guard access to `Form` in `changer_injected_templates`
#    10-Oct-2012 (CT) Pass `error` positionally to `Status` classes
#    23-Oct-2012 (CT) Fix `E_Type_Alias.short_title`: `.target.ETM.type_name`
#     6-Nov-2012 (CT) Remove obsolete code
#    13-Nov-2012 (CT) Add `scope.rollback` to `_Changer_._rendered_post`
#    21-Nov-2012 (CT) Fix indentation of `scope.rollback` call
#     7-Dec-2012 (CT) Consider `dont_et_map`
#     7-Dec-2012 (CT) Convert `form_parameters` to `property` to allow
#                     redefinition
#    11-Dec-2012 (CT) Change default for `form.referrer` to `parent.abs_href`
#    12-Dec-2012 (CT) Fix call to `QR.from_request` in `QX_Completer`
#    13-Dec-2012 (CT) Handle `MOM.An_Entity` in `._rendered_post` of
#                     `Completer` and `Completed`
#    13-Dec-2012 (CT) Add argument `AQ` to `_rendered_completions`
#    14-Dec-2012 (CT) Use `child_permission_map` in `_new_child_x`
#    17-Dec-2012 (CT) Redefine `et_map_name`, remove init-code for `ET_Map`
#    17-Mar-2013 (CT) Add `_login_required` to `E_Type, `Group`, `Site``
#    17-Mar-2013 (CT) Add guard `response.renderer` to `E_Type.rendered`
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _CAL                     import CAL
from   _GTW                     import GTW
from   _TFL                     import TFL

import _CAL.Delta

from   _GTW._AFS._MOM.Element   import Form  as AFS_Form
from   _GTW._AFS.Value          import Value as AFS_Value

from   _GTW._RST._TOP._MOM.Query_Restriction import  \
     ( Query_Restriction      as QR
     , Query_Restriction_Spec as QRS
     )

import _GTW._RST._TOP._MOM.Mixin
import _GTW._RST._TOP.Dir
import _GTW._RST._TOP.Page
import _GTW.FO
import _GTW.jQuery

from   _MOM.import_MOM          import MOM, Q

import _TFL._Meta.Object

from   _TFL._Meta.Once_Property import Once_Property
from   _TFL.Decorator           import getattr_safe
from   _TFL.I18N                import _, _T, _Tn
from   _TFL.predicate           import uniq

from   itertools                import chain as iter_chain
from   posixpath                import join  as pp_join

import logging

_Ancestor = GTW.RST.TOP.Page

class _Action_ (_Ancestor) :

    args              = (None, )
    implicit          = True

    _exclude_robots   = True

    class _Action_POST_ (GTW.RST.POST) :

        _real_name             = "POST"

        def _response_body (self, resource, request, response) :
            result = resource._rendered_post (request, response)
            if result is None :
                raise resource.Status.Not_Found ()
            return result
        # end def _response_body

    POST = _Action_POST_ # end class

    @property
    @getattr_safe
    def obj (self) :
        ETM = self.ETM
        pid = self.args [0] if self.args else None
        if pid is not None :
            return ETM.pid_query (pid)
    # end def obj

    def field_element (self, form, fid) :
        try :
            return form  [fid]
        except KeyError :
            error = _T ("Form corrupted, unknown element id %s" % (fid, ))
            raise self.top.Status.Bad_Request (error)
    # end def field_element

    def form_element (self, fid) :
        try :
            form = AFS_Form   [fid]
            return form, form [fid]
        except KeyError :
            error = _T ("Form corrupted, unknown element id %s" % (fid, ))
            raise self.top.Status.Bad_Request (error)
    # end def form_element

    def instantiated (self, elem, fid, ETM, obj, kw) :
        ikw = dict (self._nested_form_parameters (elem), ** kw)
        return elem.instantiated (fid, ETM, obj, ** ikw)
    # end def instantiated

    def session_secret (self, request, sid) :
        try :
            return request.session.edit_session (sid)
        except request.session.Expired as exc :
            ### XXX re-authorization form (password only)
            raise self.top.Status.Request_Timeout (expired = "%s" % (exc, ))
        except LookupError as exc :
            raise self.top.Status.Bad_Request ("Session expired: %s" % (exc, ))
    # end def session_secret

    def _check_readonly (self, request) :
        if self.top.scope.readonly : ### XXX might be out-of-date !!!
            error = \
                (_T ( "At the moment, the database is set to "
                      "readonly to allow maintenance."
                    )
                )
            raise self.top.Status.Service_Unavailable \
                ( error
                , retry_after = CAL.Date_Time_Delta (minutes = 15)
                )
    # end def _check_readonly

    def _nested_form_parameters (self, elem) :
        result = {}
        fkw    = self.form_parameters.get ("form_kw")
        if fkw :
            for name in elem.names  :
                try :
                    fkw = fkw [name]
                except KeyError :
                    break
            else :
                result = dict (form_kw = {elem.name : fkw})
        return result
    # end def _nested_form_parameters

    def _raise_401 (self, request) :
        error = _T ("Not logged in or login-session is expired")
        raise self.top.Status.Unauthorized (error)
    # end def _raise_401

    def _raise_403 (self, request) :
        error = _T ("Not authorized for this page")
        raise self.top.Status.Forbidden (error)
    # end def _raise_403

    def _ui_displayed (self, ETM, names, matches) :
        def _gen () :
            for n in names :
                try :
                    attr = ETM.get_etype_attribute (n)
                except AttributeError :
                    disp = lambda v : getattr (v, "ui_display", v)
                else :
                    disp = lambda v, attr = attr : attr.ac_ui_display (v)
                yield disp
        attr_displayers = list (_gen ())
        for match in matches :
            yield tuple \
                (d (v) for d, v in zip (attr_displayers, match))
    # end def _ui_displayed

# end class _Action_

_Ancestor = _Action_

class _HTML_Action_ (_Ancestor) :

    argn                 = None

    class _HTML_Action_POST_ (_Ancestor.POST) :

        _real_name             = "POST"
        _renderers             = \
            _Ancestor.GET._renderers + (GTW.RST.Mime_Type.JSON, )

    POST = _HTML_Action_POST_ # end class

    def form (self, obj = None, ** kw) :
        if obj is None :
            obj = self.obj
        return self.parent.Form \
            (self.ETM, obj, ** dict (self.form_parameters, ** kw))
    # end def form

    def form_value (self, json_cargo) :
        try :
            return AFS_Value.from_json (json_cargo)
        except Exception as exc :
            raise self.top.Status.Bad_Request ("%s" % (exc, ))
    # end def form_value

    def form_value_apply (self, fv, scope, sid, session_secret) :
        try :
            return fv.apply \
                (scope, _sid = sid, _session_secret = session_secret)
        except GTW.AFS.Error.Conflict :
            raise self.top.Status.Conflict (conflicts = fv.as_json_cargo)
        except Exception as exc :
            if __debug__ :
                logging.exception ("form_value_apply: %s", fv)
            raise self.top.Status.Bad_Request ("%s" % (exc, ))
    # end def form_value_apply

# end class _HTML_Action_

_Ancestor = _Action_

class _JSON_Action_ (_Ancestor) :

    argn                 = 0

    class _JSON_Action_Method_ (GTW.RST.HTTP_Method) :

        _renderers             = (GTW.RST.Mime_Type.JSON, )

    # end class _JSON_Action_Method_

    class _JSON_Action_GET_ (_JSON_Action_Method_, _Ancestor.GET) :

        _real_name             = "GET"

    GET  = _JSON_Action_GET_ # end class

    class _JSON_Action_POST_ (_JSON_Action_Method_, _Ancestor.POST) :

        _real_name             = "POST"

    POST = _JSON_Action_POST_ # end class

    def _get_attr_filter (self, json) :
        ET  = self.E_Type
        etn = None
        if "key" in json :
            key = json.key
        else :
            form, elem = self.form_element   (json.fid)
            field      = self.field_element  (form, json.trigger)
            etn        = elem.type_name
            key        = field.name
        if "etn" in json :
            etn = json.etn
        if etn is not None :
            ET  = self.scope [etn].E_Type
        return QR.Filter (ET, key)
    # end def _get_attr_filter

    def _rendered_completions (self, ETM, query, names, entity_p, json, AQ = None) :
        if entity_p :
            fct = self._rendered_completions_e
        else :
            fct = self._rendered_completions_a
        return fct (ETM, query, names, json, AQ)
    # end def _rendered_completions

    def _rendered_completions_a (self, ETM, query, names, json, AQ = None) :
        if AQ is None :
            AQ   = ETM.E_Type.AQ
        result   = dict (matches = [], partial = False)
        max_n    = self.max_completions + 1
        fs       = tuple (getattr (AQ, n).QR for n in names)
        matches  = query.attrs (* fs).limit (max_n).all ()
        n        = result ["completions"] = len (matches)
        finished = result ["finished"]    = n == 1
        if n :
            if n < max_n :
                result ["fields"]  = len    (names)
                result ["matches"] = sorted \
                    (self._ui_displayed (ETM, names, matches))
            else :
                if json.trigger == json.trigger_n :
                    s_matches = query.attrs (fs [0]).limit (max_n).all ()
                    m = len (s_matches)
                    if m < max_n :
                        s_matches = \
                            ( [m [0], "..."] for m in self._ui_displayed
                                (ETM, names [:1], s_matches)
                            )
                        result ["fields"]  = 1
                        result ["matches"] = sorted (s_matches)
                        result ["partial"] = True
                    else :
                        ### XXX find fewer partial matches !!!
                        result ["fields"]  = 0
        return result
    # end def _rendered_completions_a

    def _rendered_completions_e (self, ETM, query, names, json, AQ = None) :
        result   = dict (partial = False)
        max_n    = self.max_completions + 1
        matches  = query.limit (max_n).all ()
        n        = result ["completions"] = len (matches)
        finished = result ["finished"]    = n == 1
        if n :
            if n < max_n :
                result ["fields"]  = 2
                result ["matches"] = list \
                    ((m.ui_display, m.pid) for m in matches)
            else :
                result = dict \
                    ( self._rendered_completions_a
                        (ETM, query, names [:1], json)
                    , ** result
                    )
                result ["partial"] = True
        return result
    # end def _rendered_completions_e

    def _rendered_esf (self, af, filters, ** kw) :
        template = self.top.Templateer.get_template ("e_type")
        result   = dict \
            ( callbacks = [] ### XXX
            , html      = template.call_macro
                ("entity_selector_form", self, af, filters)
            , ** kw
            )
        return result
    # end def _rendered_esf

# end class _JSON_Action_

class _JSON_Action_PO_ (_JSON_Action_) :

    GET = None

# end class _JSON_Action_PO_

class _Changer_ (_HTML_Action_) :

    page_template_name   = "e_type_afs"

    @property
    @getattr_safe
    def injected_templates (self) :
        return self.parent.changer_injected_templates
    # end def injected_templates

    def rendered (self, context, template = None) :
        Status   = self.top.Status
        obj      = context ["instance"] = None
        request  = context ["request"]
        req_data = request.req_data
        pid      = req_data.get ("pid") or \
            (self.args [0] if self.args else None)
        scope    = self.top.scope
        self._check_readonly (request)
        if pid == "null" :
            pid = None
        if pid is not None :
            obj = context ["instance"] = self.pid_query_request (pid)
        sid, session_secret = self._new_edit_session (request)
        form = self.form \
            ( obj
            , referrer        = "%s%s" %
                ( request.referrer or self.parent.abs_href
                , "#pk-%s" % (obj.pid, ) if obj else ""
                )
            , _sid            = sid
            , _session_secret = session_secret
            )
        self.Media = self._get_media (head = getattr (form, "Media", None))
        context.update (form = form)
        try :
            self.last_changed = obj.FO.last_changed
        except AttributeError :
            pass
        return self.__super.rendered (context, template)
    # end def rendered

    def _rendered_post (self, request, response) :
        json   = request.json
        scope  = self.top.scope
        result = {}
        if json.get ("cancel") :
            ### the user has clicked on the cancel button and not on
            ### the submit button
            scope.rollback ()
        else :
            fv             = self.form_value (json ["cargo"])
            get_template   = self.top.Templateer.get_template
            session_secret = self.session_secret (request, fv.sid)
            self.form_value_apply (fv, scope, fv.sid, session_secret)
            if not fv.errors :
                try :
                    scope.commit ()
                except Exception as exc :
                    for e in fv.entities () :
                        if e.entity :
                            e.errors = tuple (e.entity.errors)
                            fv.record_errors (e)
            if fv.errors :
                result ["errors"] = fv.errors
            else :
                ikw = dict \
                    ( collapsed       = bool (json.get ("collapsed"))
                    , _sid            = fv.sid
                    , _session_secret = session_secret
                    )
                if "allow_new" in json :
                    ikw ["allow_new"] = bool (json.get ("allow_new"))
                result ["$child_ids"] = rids = []
                for e in fv.entities () :
                    if e.entity :
                        obj = e.entity
                        fi  = self.instantiated \
                            (e.elem, e.id, obj.ETM, obj, ikw)
                        result [e.id] = dict \
                            ( html = get_template
                                (e.elem.renderer).call_macro
                                    (fi.widget, fi, fi, fi.renderer)
                            , json = fi.as_json_cargo
                            )
                        rids.append (e.id)
                if TFL.callable (self.submit_callback) :
                    try :
                        self.submit_callback \
                            (request, response, scope, fv, result)
                    except Exception as exc :
                        logging.exception \
                            ( "%s._rendered_post: %s -> %s"
                            , self.__call__, json ["cargo"], result
                            )
            if fv.errors :
                scope.rollback ()
        return result
    # end def _rendered_post

# end class _Changer_

class Changer (_Changer_) :
    """Page displaying form for changing a specific instance
       of a etype with an AFS form.
    """

    argn            = 1
    name            = "change"
    _login_required = True

# end class Changer

class Completed (_JSON_Action_PO_) :
    """Return auto completion values for a AFS page."""

    name            = "completed"

    def _rendered_post (self, request, response) :
        json           = TFL.Record (** request.json)
        result         = {}
        scope          = self.top.scope
        session_secret = self.session_secret (request, json.sid)
        form, elem     = self.form_element   (json.fid)
        field          = self.field_element  (form, json.trigger)
        ETM = ETM_R    = scope [elem.type_name]
        E_Type         = ETM.E_Type
        if json.complete_entity :
            obj = self.pid_query_request (json.pid, E_Type)
            ikw = dict \
                ( collapsed        = True
                , copy             = False
                , _sid             = json.sid
                , _session_secret  = session_secret
                )
            if request.json.get ("allow_new") :
                ikw ["allow_new"] = True
            fi       = self.instantiated (elem, json.fid, ETM, obj, ikw)
            renderer = self.top.Templateer.get_template (fi.renderer)
            html     = renderer.call_macro (fi.widget, fi, fi, fi.renderer)
            result.update \
                ( completions = 1
                , html        = html
                , json        = fi.as_json_cargo
                )
        else :
            attr      = getattr (E_Type, field.name)
            completer = attr.completer
            if completer is not None :
                AQ = None
                if issubclass (E_Type, MOM.An_Entity) :
                    ETM_R = scope [elem.anchor.type_name]
                    AQ    = getattr (ETM_R.E_Type.AQ, elem.name)
                names = completer.names
                fs    = ETM.raw_query_attrs (names, json.values, AQ)
                query = ETM_R.query (* fs)
                result ["completions"] = n = query.count ()
                if n == 1 :
                    af     = ETM.raw_query_attrs (names, AQ)
                    values = query.attrs (* af).one ()
                    result.update \
                        ( fields = len (names)
                        , names  = names
                        , values = values
                        )

        return result
    # end def _rendered_post

# end class Completed

class Completer (_JSON_Action_PO_) :
    """Do auto completion for a AFS page."""

    name                 = "complete"

    def _rendered_post (self, request, response) :
        json        = TFL.Record (** request.json)
        result      = dict (matches = [], partial = False)
        scope       = self.top.scope
        form, elem  = self.form_element  (json.fid)
        field       = self.field_element (form, json.trigger)
        ETM = ETM_R = scope [elem.type_name]
        E_Type      = ETM.E_Type
        attr        = getattr (E_Type, field.name)
        completer   = attr.completer
        if completer is not None :
            AQ = None
            if issubclass (E_Type, MOM.An_Entity) :
                ETM_R = scope [elem.anchor.type_name]
                AQ    = getattr (ETM_R.E_Type.AQ, elem.name)
            names  = completer.names
            query  = completer (scope, json.values, ETM_R, AQ)
            result = self._rendered_completions \
                (ETM, query, names, completer.entity_p, json, AQ)
        return result
    # end def _rendered_post

# end class Completer

class Creator (_Changer_) :
    """Page displaying form for creating a new instance of a etype with an
       AFS form.
    """

    argn                 = 0
    name                 = "create"

# end class Creator

class Deleter (_JSON_Action_PO_) :
    """Delete a specific instance of a etype."""

    argn                 = 1
    name                 = "delete"
    page_template_name   = "e_type_delete"

    _login_required      = True

    def _rendered_post (self, request, response) :
        self._check_readonly (request)
        args = self.args
        if args and args [0] :
            E_Type         = self.E_Type
            sra            = self._set_result_args
            pid            = args [0]
            form, elem     = None, None
        else :
            sra            = self._set_result_json
            json           = request.json
            fid            = json.get ("fid")
            pid            = json.get ("pid")
            sid            = json.get ("sid")
            session_secret = self.session_secret (request, sid)
            form, elem     = self.form_element   (fid)
            scope          = self.top.scope
            ETM            = scope [elem.type_name]
            E_Type         = ETM.E_Type
        if pid is not None and pid != "null" :
            result = {}
            obj    = self.pid_query_request (pid, E_Type)
            sra (obj, request, response, result, form, elem)
            obj.destroy ()
            return result
        else :
            error = _T ("You need to specify a pid!")
            raise self.top.Status.Bad_Request (error)
    # end def _rendered_post

    def _set_result_args (self, obj, request, response, result, form, elem) :
        result ["replacement"] = dict \
            ( html = """<td colspan="6">%s</td>"""
              % (_T ("""Object "%s" deleted""") % (obj.ui_display, ))
              ### XXX use template to render this XXX
            , ### XXX undelete link !!!
            )
    # end def _set_result_args

    def _set_result_json (self, obj, request, response, result, form, elem) :
        result ["html"] = \
            ( """<h2>%s</h2>"""
            % (_T ("""Object "%s" deleted""") % (obj.ui_display, ))
              ### XXX use template to render this XXX
            )
    # end def _set_result_json

# end class Deleter

class Expander (_JSON_Action_) :
    """Expand a sub-form (e.g., Entity_Link)"""

    name            = "expand"

    POST            = None

    def rendered (self, context, template = None) :
        obj            = context ["instance"] = None
        request        = context ["request"]
        req_data       = request.req_data
        fid            = req_data.get ("fid")
        pid            = req_data.get ("pid")
        sid            = req_data.get ("sid")
        scope          = self.top.scope
        form, elem     = self.form_element   (fid)
        session_secret = self.session_secret (request, sid)
        ETM            = scope [elem.type_name]
        if pid is not None and pid != "null" :
            obj = context ["instance"] = self.pid_query_request \
                (pid, ETM.E_Type)
        ikw = dict \
            ( collapsed       = bool (req_data.get ("collapsed"))
            , copy            = req_data.get ("copy")
            , _sid            = sid
            , _session_secret = session_secret
            )
        if "allow_new" in req_data :
            ikw ["allow_new"] = bool (req_data ["allow_new"])
        new_id_suffix = req_data.get ("new_id_suffix")
        if new_id_suffix is not None :
            ikw ["new_id_suffix"] = new_id_suffix
        fi       = self.instantiated (elem, fid, ETM, obj, ikw)
        renderer = self.top.Templateer.get_template (fi.renderer)
        html     = renderer.call_macro (fi.widget, form, fi, fi.renderer)
        json     = fi.as_json_cargo
        return dict (html = html, json = json)
    # end def rendered

# end class Expander

class QX_AF_Html (_JSON_Action_PO_) :
    """Process AJAX query for attr-filter's html"""

    name            = "af_html"

    def _rendered_post (self, request, response) :
        result          = {}
        json            = TFL.Record (** request.json)
        E_Type          = self.E_Type
        af              = QR.Filter (E_Type, json.key)
        template        = self.top.Templateer.get_template ("e_type")
        call_macro      = template.call_macro
        result ["html"] = call_macro ("attr_filter_tr", af)
        return result
    # end def _rendered_post

# end class QX_AF_Html

class QX_Completed (_JSON_Action_PO_) :
    """Process AJAX query for entity auto completions"""

    name            = "esf_completed"

    def _rendered_post (self, request, response) :
        json    = TFL.Record (** request.json)
        af      = self._get_attr_filter (json)
        filters = QR.Filter_Atoms (af)
        ETM     = self.top.scope  [af.attr.E_Type.type_name]
        obj     = self.pid_query_request (json.pid, ETM.E_Type)
        for f in filters :
            f.edit = f.value = f.AQ.QR (obj)
        result  = self._rendered_esf \
            ( af, filters
            , value     = obj.pid
            , display   = str (obj.FO)
            )
        return result
    # end def _rendered_post

# end class QX_Completed

class QX_Completer (_JSON_Action_PO_) :
    """Process AJAX query for entity auto completions"""

    name            = "esf_completer"

    def _rendered_post (self, request, response) :
        json   = TFL.Record (** request.json)
        af     = self._get_attr_filter (json)
        ET     = af.attr.E_Type
        at     = QR.Filter  (ET, json.trigger)
        names  = tuple \
            ( uniq
                ( iter_chain
                    ( (at.AQ._full_name, )
                    , tuple (f._full_name for f in ET.AQ.Atoms)
                    )
                )
            )
        qr     = QR.from_request \
            (ET, request, ** request.json.get ("values", {}))
        ETM    = self.top.scope [ET.type_name]
        query  = qr (ETM.query_s ()).distinct ()
        entity_p = getattr (json, "entity_p", False)
        return self._rendered_completions (ETM, query, names, entity_p, json)
    # end def _rendered_post

# end class QX_Completer

class QX_Entity_Selector_Form (_JSON_Action_PO_) :
    """Process AJAX query for entity-selector form"""

    name            = "esf"

    def _rendered_post (self, request, response) :
        json    = TFL.Record (** request.json)
        af      = self._get_attr_filter (json)
        filters = QR.Filter_Atoms       (af)
        result  = self._rendered_esf    (af, filters)
        return result
    # end def _rendered_post

# end class QX_Entity_Selector_Form

class QX_Order_By_Form (_JSON_Action_PO_) :
    """Process AJAX query for order-by form"""

    name            = "obf"

    def _rendered_post (self, request, response) :
        HTTP            = self.top.HTTP
        result          = {}
        E_Type          = self.E_Type
        template        = self.top.Templateer.get_template ("e_type")
        call_macro      = template.call_macro
        result ["html"] = call_macro ("order_by_form")
        return result
    # end def _rendered_post

# end class QX_Order_By_Form

class QX_Select_Attr_Form (_JSON_Action_PO_) :
    """Process AJAX query for select-attr form"""

    name            = "asf"

    def _rendered_post (self, request, response) :
        HTTP            = self.top.HTTP
        result          = {}
        E_Type          = self.E_Type
        template        = self.top.Templateer.get_template ("e_type")
        call_macro      = template.call_macro
        result ["html"] = call_macro ("select_attr_form")
        return result
    # end def _rendered_post

# end class QX_Select_Attr_Form

class _NC_Mixin_ (TFL.Meta.Object) :

    def _new_child_x (self, T, child, grandchildren) :
        argn = T.argn
        if argn is None or len (grandchildren) == argn :
            name   = pp_join (* grandchildren) if grandchildren else ""
            kw     = dict \
                ( args   = grandchildren
                , kind   = child
                , name   = "%s/%s" % (child, name)
                , parent = self
                )
            if child in self.child_permission_map :
                kw ["permission"] = self.child_permission_map [child]
            result = T (** kw)
            return result
    # end def _new_child_x

# end class _NC_Mixin_

_Ancestor = GTW.RST.TOP.Dir_V

class _QX_Dispatcher_ (_NC_Mixin_, _Ancestor) :

    name                  = "qx"

    _entry_type_map       = dict \
        (  (c.name, c)
        for c in
           ( QX_AF_Html, QX_Completed, QX_Completer
           , QX_Entity_Selector_Form, QX_Order_By_Form, QX_Select_Attr_Form
           )
        )

# end class _QX_Dispatcher_

_Ancestor = GTW.RST.TOP.Dir_V

class E_Type (_NC_Mixin_, GTW.RST.TOP.MOM.E_Type_Mixin, _Ancestor) :
    """Directory displaying the instances of one E_Type."""

    Changer               = Changer
    Deleter               = Deleter

    button_types          = dict \
        ( ADD             = "button"
        , APPLY           = "submit"
        , CANCEL          = "button"
        , CLEAR           = "button"
        , CLOSE           = "button"
        )

    css_group             = "Type"
    default_qr_kw         = dict \
        ( limit           = 25
        )
    dir_template_name     = "e_type_admin"
    max_completions       = 20
    skip_etag             = True
    submit_callback       = None

    _entry_type_map       = dict \
        ((c.name, c) for c in
            ( Changer, Completed, Completer, Creator, Deleter, Expander
            , _QX_Dispatcher_
            )
        )

    _exclude_robots       = True
    _greet_entry          = None
    _form_id              = None
    _form_parameters      = {}
    _list_display         = None
    _login_required       = True
    _sort_key             = None

    class _E_Type_GET_ (_Ancestor.GET) :

        _renderers             = \
            _Ancestor.GET._renderers + (GTW.RST.Mime_Type.JSON, )

    GET = _E_Type_GET_ # end class

    class Entity (TFL.Meta.Object) :
        """Wrap a specific instance in the context of an admin page for one
           E_Type, e.g., displayed as one line of a table.
        """

        def __init__ (self, obj, parent, ** kw) :
            self.admin = parent
            self.obj   = obj
            self.FO    = GTW.FO (obj, parent.top.encoding)
        # end def __init__

        @Once_Property
        @getattr_safe
        def fields (self) :
            admin = self.admin
            FO    = self.FO
            return tuple ((f, f.value (FO)) for f in admin.fields)
        # end def fields

        def href_change (self) :
            return self.admin.href_change (self.obj)
        # end def href_change

        def href_delete (self) :
            return self.admin.href_delete (self.obj)
        # end def href

        def __getattr__ (self, name) :
            return getattr (self.obj, name)
        # end def __getattr__

        def __iter__ (self) :
            return iter (self.fields)
        # end def __iter__

    # end class Entity

    class Field (TFL.Meta.Object) :
        """Model a field describing an attribute."""

        def __init__ (self, aq) :
            self.aq = aq
        # end def __init__

        @Once_Property
        @getattr_safe
        def attr (self) :
            return self.aq._attr
        # end def attr

        @property ### depends on currently selected language (I18N/L10N)
        @getattr_safe
        def description (self) :
            return _T (self.attr.description)
        # end def description

        @Once_Property
        @getattr_safe
        def name (self) :
            return self.aq._full_name
        # end def name

        @property ### depends on currently selected language (I18N/L10N)
        @getattr_safe
        def ui_name (self) :
            return self.attr.ui_name_T
        # end def ui_name

        def value (self, o) :
            return getattr (o, self.name)
        # end def value

        def __getattr__ (self, name) :
            return getattr (self.attr, name)
        # end def __getattr__

    # end class Field

    def __init__ (self, ** kw) :
        self.pop_to_self (kw, "list_display", prefix = "_")
        self._field_map = {}
        self.__super.__init__ (** kw)
    # end def __init__

    @Once_Property
    @getattr_safe
    def changer_injected_templates (self) :
        try :
            form = self.Form
        except LookupError :
            renderers = set ()
        else :
            renderers = set (self.Form.renderer_iter ())
        return tuple (self.top.Templateer.get_template (r) for r in renderers)
    # end def changer_injected_templates

    @property
    @getattr_safe
    def entries (self) :
        return ()
    # end def entries

    @Once_Property
    def et_map_name (self) :
        if not self.implicit :
            return "admin"
    # end def et_map_name

    @Once_Property
    @getattr_safe
    def Form (self) :
        try :
            result = AFS_Form [self.form_id]
        except Exception as exc :
            logging.exception \
                ( "Getting form failed : %s %s %s"
                , self.href, self.E_Type, self.form_id
                )
            raise
        else :
            return result
    # end def Form

    @property
    @getattr_safe
    def form_id (self) :
        _form_id = self._form_id
        return self.E_Type.GTW.afs_id if (_form_id is None) else _form_id
    # end def form_id

    @form_id.setter
    def form_id (self, value) :
        self._form_id = value
    # end def form_id

    @property
    @getattr_safe
    def form_parameters (self) :
        return self._form_parameters
    # end def form_parameters

    @form_parameters.setter
    def form_parameters (self, value) :
        self._form_parameters = value
    # end def form_parameters

    @property
    @getattr_safe
    def head_line (self) :
        co      = getattr (self, "query_size", None)
        if co is None :
            co  = self.count
        qr      = self.query_restriction
        tail    = "%s" % (co, )
        if qr :
            cf  = qr.total_f
            cu  = qr.total_u
            sep = "/"
            if cf and cf != co :
                tail = "%s%s%s" % (tail, sep, cf)
                sep  = "//"
            if cu and cu != cf :
                tail = "%s%s%s" % (tail, sep, cu)
        return "%s (%s)" % (_T (self.ETM.E_Type.ui_name), tail)
    # end def head_line

    @property
    @getattr_safe
    def sort_key (self) :
        result = self._sort_key
        if result is None :
            result = self.E_Type.sorted_by_epk
        return result
    # end def sort_key

    @sort_key.setter
    def sort_key (self, value) :
        self._sort_key = value
    # end def sort_key

    @Once_Property
    @getattr_safe
    def list_display (self) :
        result = self._list_display
        if result is None :
            result = self._auto_list_display
        return result
    # end def list_display

    @Once_Property
    @getattr_safe
    def manager (self) :
        return self.etype_manager (self.E_Type)
    # end def manager

    @Once_Property
    @getattr_safe
    def qr_spec (self) :
        return QRS (self.E_Type)
    # end def qr_spec

    @Once_Property
    @getattr_safe
    def _auto_list_display (self, ) :
        return tuple (a.name for a in self.E_Type.edit_attr)
    # end def _auto_list_display

    def changer (self, pid = None, ** kw) :
        return self.Changer \
            ( form_parameters = dict (self.form_parameters, ** kw)
            , parent          = self
            , pid             = pid
            )
    # end def changer

    def href_create (self) :
        return pp_join (self.abs_href, "create")
    # end def href_create

    def href_change (self, obj) :
        return pp_join (self.abs_href, "change", str (obj.pid))
    # end def href_change

    def href_complete (self) :
        return pp_join (self.abs_href, "complete")
    # end def href_complete

    def href_completed (self) :
        return pp_join (self.abs_href, "completed")
    # end def href_completed

    def href_delete (self, obj = None) :
        result = pp_join (self.abs_href, "delete")
        if obj is not None :
            result = pp_join (result, str (obj.pid))
        return result
    # end def href_delete

    def href_display (self, obj) :
        man = self.manager
        if man :
            return man.href_display (obj)
    # end def href_display

    def href_expand (self) :
        return pp_join (self.abs_href, "expand")
    # end def href_delete

    def href_qx_af_html (self) :
        return pp_join (self.abs_href, self.qx_prefix, "af_html")
    # end def href_qx_af_html

    def href_qx_asf (self) :
        return pp_join (self.abs_href, self.qx_prefix, "asf")
    # end def href_qx_asf

    def href_qx_esf_completed (self) :
        return pp_join (self.abs_href, self.qx_prefix, "esf_completed")
    # end def href_qx_esf_completed

    def href_qx_esf_completer (self) :
        return pp_join (self.abs_href, self.qx_prefix, "esf_completer")
    # end def href_qx_esf_completer

    def href_qx_esf (self) :
        return pp_join (self.abs_href, self.qx_prefix, "esf")
    # end def href_qx_esf

    def href_qx_obf (self) :
        return pp_join (self.abs_href, self.qx_prefix, "obf")
    # end def href_qx_obf

    def is_current_dir (self, page) :
        if not self.hidden :
            p = page.href
            s = self.href
            return p == s or (p.startswith (s) and p [len (s)] == "/")
    # end def is_current_dir

    def rendered (self, context, template = None) :
        request  = context ["request"]
        response = context ["response"]
        qr = QR.from_request (self.ETM.E_Type, request, ** self.default_qr_kw)
        self._fix_filters (qr.filters)
        fields = self._fields (qr.attributes or self.list_display)
        with self.LET (fields = fields, query_restriction = qr) :
            Entity  = self.Entity
            objects = tuple \
                (Entity (obj = o, parent = self) for o in self.objects)
            next_p  = qr.next_p
            prev_p  = qr.prev_p
            button_types = dict \
                ( self.button_types
                , FIRST  = "submit" if prev_p else "button"
                , LAST   = "submit" if next_p else "button"
                , NEXT   = "submit" if next_p else "button"
                , PREV   = "submit" if prev_p else "button"
                )
            with self.LET \
                     ( query_size   = len (objects)
                     , button_types = button_types
                     ) :
                context.update \
                    ( fields            = fields
                    , objects           = objects
                    , query_restriction = self.query_restriction
                    )
                if response.renderer and response.renderer.name == "JSON" :
                    template   = self.top.Templateer.get_template ("e_type")
                    call_macro = template.call_macro
                    buttons    = dict \
                        ( FIRST = call_macro ("qr_button_first", self, qr)
                        , LAST  = call_macro ("qr_button_last",  self, qr)
                        , NEXT  = call_macro ("qr_button_next",  self, qr)
                        , PREV  = call_macro ("qr_button_prev",  self, qr)
                        )
                    result = dict \
                        ( buttons          = buttons
                        , callbacks        = ["setup_obj_list"]
                        , head_line        = self.head_line
                        , limit            = qr.limit
                        , object_container = call_macro
                            ("admin_table", self, fields, objects)
                        , offset           = qr.offset
                        )
                else :
                    result = self.__super.rendered (context, template)
            return result
    # end def rendered

    def template_iter (self) :
        T = self.top.Templateer
        yield self.template
        yield T.get_template \
            (self.Changer.template_name, self.changer_injected_templates)
        yield T.get_template (self.Deleter.template_name)
    # end def template_iter

    def _fields (self, names) :
        def _gen (E_Type, names, map) :
            AQ    = E_Type.AQ
            Field = self.Field
            for n in names :
                try :
                    f = map [n]
                except KeyError :
                    f = map [n] = Field (getattr (AQ, n))
                yield f
        return tuple (_gen (self.E_Type, names, self._field_map))
    # end def _fields

    def _fix_filters (self, filters) :
        scope = self.top.scope
        for f in filters :
            if isinstance (f.AQ, MOM.Attr.Querier.Id_Entity) and f.value :
                try :
                    o = scope.pid_query (int (f.value))
                except (TypeError, ValueError, LookupError) :
                    pass
                else :
                    f.ui_display = o.ui_display
    # end def _fix_filters

    def _new_child (self, T, child, grandchildren) :
        if child == self.qx_prefix and grandchildren :
            new_child = self.__super._new_child
        else :
            new_child = self._new_child_x
        return new_child (T, child, grandchildren)
    # end def _new_child

# end class E_Type

class E_Type_Alias (GTW.RST.TOP.Alias) :

    ETM                   = property \
        ( lambda s        : s.target.ETM
        , lambda s, v     : None
        )

    short_title           = property \
        ( lambda s        : s.target.ETM.type_name
        , lambda s, v     : None
        )

    title                 = property \
        ( lambda s        : s.target.title
        , lambda s, v     : None
        )

    _exclude_robots       = True

# end class E_Type_Alias

_Ancestor = GTW.RST.TOP.Dir

class Group (_Ancestor) :
    """Directory displaying a group of E_Type admin pages."""

    _etypes               = []
    _PNSs                 = []

    css_group             = "Group"
    dir_template_name     = "site_admin"
    show_aliases          = False

    _exclude_robots       = True
    _login_required       = True


    def __init__ (self, ** kw) :
        self.pop_to_self (kw, "etypes", "PNSs", prefix = "_")
        self.__super.__init__ (** kw)
    # end def __init__

    @property
    @getattr_safe
    def entries (self) :
        if not self._entries :
            entries = self._filter_etype_entries \
                (self._etypes, self._pns_entries (* self._PNSs))
            self.add_entries (* entries)
        return self._entries
    # end def entries

    def template_iter (self) :
        for t in self.__super.template_iter () :
            yield t
        for e in self.entries :
            for t in e.template_iter () :
                yield t
    # end def template_iter

    def _add_index (self, l) :
        self._entries.sort (key = TFL.Getter.short_title)
        self.__super._add_index (0)
    # end def _add_index

    def _filter_etype_entries (self, * args) :
        seen = set ()
        for e in iter_chain (* args) :
            if isinstance (e, tuple) :
                cls, args, kw = e
                e = cls (* args, ** dict (kw, parent = self))
            etn = e.ETM.type_name
            if etn not in seen :
                seen.add (etn)
                yield e
    # end def _filter_etype_entries

    def _pns_entries (self, * pnss) :
        app_type = self.top.App_Type
        ET_Map   = self.top.ET_Map
        for pns in pnss :
            PNS = app_type.PNS_Map [pns]
            Nav = getattr (getattr (PNS, "Nav", None), "Admin", None)
            for ET in app_type.etypes_by_pns [pns] :
                if ET.is_relevant and ET.show_in_ui :
                    admin = ET_Map [ET.type_name].admin
                    if (not admin) or self.show_aliases :
                        aa = dict (getattr (ET, "admin_args", {}))
                        aa.update (getattr (Nav, ET.type_base_name, {}))
                        T = E_Type
                        if admin :
                            T = E_Type_Alias
                            aa ["target"] = admin
                        if aa :
                            yield T (parent = self, ** aa)
    # end def _pns_entries

# end class Group

class Site (Group) :
    """Directory displaying admin Groups."""

    _exclude_robots      = True
    _login_required      = True


    def _auto_entries (self) :
        for et in self.top.ET_Map.itervalues () :
            man = et.manager
            if man is not None and et.admin is None :
                m_kw        = man.admin_args.copy ()
                short_title = m_kw.pop ("short_title", man.short_title)
                title       = m_kw.pop \
                    ("title", "%s: %s" % (self.title, man.name))
                ETM         = m_kw.pop ("ETM", man._ETM)
                Type        = m_kw.pop ("Type", E_Type)
                e           = Type \
                    ( ETM         = ETM
                    , name        = man.name
                    , parent      = self
                    , short_title = short_title
                    , title       = title
                    , ** m_kw
                    )
                yield e
    # end def _auto_entries

    def _filter_etype_entries (self, * args) :
        return self.__super._filter_etype_entries \
            (self._auto_entries (), * args)
    # end def _filter_etype_entries

# end class Site

if __name__ != "__main__" :
    GTW.RST.TOP.MOM._Export_Module ()
### __END__ GTW.RST.TOP.MOM.Admin
