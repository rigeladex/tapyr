# -*- coding: utf-8 -*-
# Copyright (C) 2014 Mag. Christian Tanzer All rights reserved
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
#    GTW.RST.TOP.MOM.MF3
#
# Purpose
#    Resources dealing with MF3 forms
#
# Revision Dates
#    29-Apr-2014 (CT) Creation
#     3-May-2014 (CT) Factor `form_attr_spec_d`
#     4-May-2014 (CT) Factor `_commit_scope_fv`
#     6-May-2014 (CT) Use `Show_in_UI_Selector` in `_get_esf_filter`
#     7-May-2014 (CT) Guard access to `default_child` in `_get_esf_filter`
#     9-May-2014 (CT) Factor `form_instance` from `_HTML_Action_` to `_Action_`
#     9-May-2014 (CT) Implement `Completer._rendered_post`,
#                     fix `_rendered_completions`
#    11-May-2014 (CT) Implement `Completed._rendered_post`,
#                     factor `_get_form_field` from `Completer._rendered_post`
#    ««revision-date»»···
#--

from   __future__ import division, print_function
from   __future__ import absolute_import, unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

from   _GTW._MF3                             import Element as MF3
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

import _MOM.formatted

import _TFL._Meta.Object

from   _TFL._Meta.Once_Property import Once_Property
from   _TFL.Decorator           import getattr_safe
from   _TFL.Formatter           import formatted
from   _TFL.I18N                import _, _T, _Tn
from   _TFL.predicate           import uniq

from   itertools                import chain as iter_chain
from   posixpath                import join  as pp_join

import logging

_Ancestor = GTW.RST.TOP.Page

class _Action_ (_Ancestor) :

    args                  = (None, )
    implicit              = True
    skip_etag             = True

    _exclude_robots       = True

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

    def form_instance (self, obj = None, ** kw) :
        if obj is None :
            obj = self.obj
        attr_spec = dict (self.form_attr_spec, ** kw.pop ("form_attr_spec", {}))
        kw.setdefault ("_hash_fct", kw.pop ("hash_fct", self.top.hash_fct))
        result = self.parent.Form \
            (self.scope, obj, attr_spec = attr_spec, ** kw)
        return result
    # end def form_instance

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

    def _raise_401 (self, request) :
        error = _T ("Not logged in or login-session is expired")
        raise self.top.Status.Unauthorized (error)
    # end def _raise_401

    def _raise_403 (self, request) :
        error = _T ("Not authorized for this page")
        raise self.top.Status.Forbidden (error)
    # end def _raise_403

# end class _Action_

_Ancestor = _Action_

class _HTML_Action_ (_Ancestor) :

    argn                 = None
    nav_off_canvas       = False

    class _HTML_Action_GET_ (_Ancestor.GET) :

        _real_name             = "GET"
        _renderers             = \
            _Ancestor.GET._renderers + (GTW.RST.Mime_Type.JSON, )

    GET = _HTML_Action_GET_ # end class

    class _HTML_Action_POST_ (_Ancestor.POST) :

        _real_name             = "POST"
        _renderers             = \
            _Ancestor.GET._renderers + (GTW.RST.Mime_Type.JSON, )

    POST = _HTML_Action_POST_ # end class

    @property
    @getattr_safe
    def head_line (self) :
        return "%s %s" % \
            (_T (self.__class__.name.capitalize ()), self.E_Type.ui_name_T)
    # end def head_line

    def form_value (self, request, json_cargo) :
        try :
            sid    = json_cargo.get ("sid")
            secret = self.session_secret (request, sid)
            form   = self.form_instance  (sid = sid, session_secret = secret)
            result = form (self.scope, json_cargo)
        except Exception as exc :
            logging.exception \
                ( "form_value: \n  submitted json:\n    %s"
                , formatted (json_cargo, 4)
                )
            raise self.top.Status.Bad_Request ("%s" % (exc, ))
        if result.conflicts :
            ### XXX needs to be changed ???
            raise self.top.Status.Conflict (conflicts = result.as_json_cargo)
        return result
    # end def form_value

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
            key  = json.key
            if "etn" in json :
                etn = json.etn
        else :
            form = self.Form (self.scope)
            elem = form [json.trigger]
            etn  = elem.Entity.E_Type.type_name
            key  = elem.attr.name
        if etn is not None :
            ET   = self.scope [etn].E_Type
        return self.QR.Filter (ET, key)
    # end def _get_attr_filter

    def _get_esf_filter (self, json) :
        QR        = self.QR
        ET        = self.E_Type
        result    = self._get_attr_filter (json)
        fa_filter = Q.AQ.Show_in_UI_Selector
        result.polymorphic_epk = pepk = result.AQ.E_Type.polymorphic_epk
        if pepk :
            scope = self.scope
            result.filters_np = fnps = []
            result.selected_type = 0
            sc = None
            if "etns" in json :
                sc = json.etns
            sc = sc or getattr (result, "default_child", "")
            for i, cnp in enumerate (result.children_np) :
                cf = QR.Filter (ET, "%s[%s]" % (cnp.full_name, cnp.type_name))
                cf.filters = QR.Filter_Atoms (cf, fa_filter)
                fnps.append (cf)
                if cf.type_name == sc :
                    result ["selected_type"] = i
        else :
            result.selected_type = None
            result.filters = QR.Filter_Atoms (result, fa_filter)
        return result
    # end def _get_esf_filter

    def _get_form_field (self, request, json) :
        sid        = json.get ("sid")
        secret     = self.session_secret (request, sid)
        form       = self.form_instance  (sid = sid, session_secret = secret)
        try :
            field  = form [json ["trigger"]]
        except KeyError :
            raise self.Status.Bad_Request
        form.check_sigs (json)
        return form, field
    # end def _get_form_field

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

    def _rendered_esf (self, af, ** kw) :
        template = self.top.Templateer.get_template ("e_type")
        macro    = "entity_selector_form%s" % \
            ("_p" if af.polymorphic_epk else "")
        result   = dict \
            ( callbacks = [] ### XXX
            , html      = template.call_macro (macro, self, af)
            , ** kw
            )
        if af.selected_type is not None :
            result ["selected_type"] = af.selected_type
        return result
    # end def _rendered_esf

# end class _JSON_Action_

class _JSON_Action_PO_ (_JSON_Action_) :

    GET = None

# end class _JSON_Action_PO_

class _Changer_ (_HTML_Action_) :

    page_template_name   = "e_type_mf3"

    @property
    @getattr_safe
    def head_line (self) :
        return _T (self.ETM.E_Type.ui_name)
    # end def head_line

    @property
    @getattr_safe
    def injected_templates (self) :
        return self.parent.form_injected_templates
    # end def injected_templates

    def rendered (self, context, template = None) :
        Status   = self.top.Status
        args     = self.args
        obj      = context ["instance"] = None
        request  = context ["request"]
        response = context ["response"]
        req_data = request.req_data
        parent   = self.parent
        pid      = req_data.get ("pid") or (args [0] if args else None)
        scope    = self.top.scope
        self._check_readonly (request)
        if pid == "null" :
            pid = None
        if pid is not None :
            obj = context ["instance"] = self.pid_query_request (pid)
        sid, session_secret = self._new_edit_session (response)
        referrer = "%s%s" % \
                ( request.referrer or parent.abs_href
                , parent.href_anchor_pid (obj)
                )
        form = self.form_instance \
            (obj, sid = sid, session_secret = session_secret)
        context.update (form = form, referrer = referrer)
        try :
            self.last_changed = obj.FO.last_changed
        except AttributeError :
            pass
        with self.LET (form = form, referrer = referrer) :
            if response.renderer.name == "JSON" :
                t      = self.top.Templateer.get_template \
                    (form.template_module)
                result = dict \
                    (form = t.call_macro ("main", self, form))
            else :
                result = self.__super.rendered (context, template)
        return result
    # end def rendered

    def _call_submit_callback (self, cb, request, response, scope, fv, result) :
        ### XXX does this need to be changed ???
        if TFL.callable (cb) :
            try :
                cb (self, request, response, scope, fv, result)
            except Exception as exc :
                logging.exception \
                    ( "%s._rendered_post: %s -> %s"
                    , self.__class__, request.json ["cargo"], result
                    )
    # end def _call_submit_callback

    def _commit_scope_fv (self, scope, fv, request, response) :
        self.commit_scope (request, response)
    # end def _commit_scope_fv

    def _formatted_submit_entities (self, scope, fv, skip_attrs = {}) :
        result = []
        for c in fv.entities () :
            e = c.entity
            if e is not None :
                result.append (MOM.formatted (e, skip_attrs = skip_attrs))
        return "\n\n".join (result)
    # end def _formatted_submit_entities

    def _rendered_post (self, request, response) :
        json   = request.json
        scope  = self.top.scope
        result = {}
        if json.get ("cancel") :
            ### the user has clicked on the cancel button and not on
            ### the submit button
            scope.rollback ()
        else :
            fv = self.form_value (request, json ["cargo"])
            if not fv.submission_errors :
                try :
                    self._commit_scope_fv (scope, fv, request, response)
                except Exception as exc :
                    for e in fv.entity_elements :
                        if e.essence :
                            e._commit_errors = tuple (e.entity.errors)
            result.update (fv.as_json_cargo)
            result ["html"] = reh = {}
            get_template    = self.top.Templateer.get_template
            if 0 : ### XXX ???
                for e in fv.entity_elements [1:] :
                    tm          = e.template_module or e.parent.template_module
                    t           = get_template (tm)
                    reh [e.id]  = t.call_macro (e.template_macro, self, fv, e, tm)
            if fv.errors :
                self._call_submit_callback \
                    ( self.submit_error_callback
                    , request, response, scope, fv, result
                    )
                scope.rollback ()
            else :
                self._call_submit_callback \
                    ( self.submit_callback
                    , request, response, scope, fv, result
                    )
        return result
    # end def _rendered_post

# end class _Changer_

class Instance (_Changer_) :
    """Page displaying form for changing a specific instance
       of a etype with an MF3 form.
    """

    argn            = 1
    name            = "change"
    _auth_required  = True

    class _MF3_Delete_ (GTW.RST.DELETE) :

        _real_name             = "DELETE"

        def _response_body (self, resource, request, response) :
            resource._check_readonly (request)
            obj    = resource.obj
            result = {}
            if obj is None :
                raise resource.Status.Not_Found ()
            ### XXX confirm deleting links to `obj`
            result ["replacement"] = _T \
                ("""Object "%s" deleted""") % (obj.ui_display, )
            obj.destroy ()
            return result
        # end def _response_body

    DELETE = _MF3_Delete_ # end class

# end class Instance

class Completed (_JSON_Action_PO_) :
    """Return auto completion values for a AFS page."""

    name                 = "completed"

    def _rendered_post (self, request, response) :
        json         = request.json
        form, field  = self._get_form_field (request, json)
        result       = {}
        scope        = self.top.scope
        completer    = field.completer
        if completer is not None :
            eor    = self.eligible_object_restriction (completer.etn)
            result = completer.choose (scope, json, eor, self.pid_query_request)
        return result
    # end def _rendered_post

# end class Completed

class Completer (_JSON_Action_PO_) :
    """Do auto completion for a AFS page."""

    name                 = "complete"

    def _rendered_post (self, request, response) :
        json         = request.json
        form, field  = self._get_form_field (request, json)
        result       = dict (matches = [], partial = False)
        scope        = self.top.scope
        completer    = field.completer
        if completer is not None :
            eor    = self.eligible_object_restriction (completer.etn)
            result = completer.choices (scope, json, eor, self.max_completions)
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


class Expander (_JSON_Action_) :
    """Expand a sub-form (e.g., Entity_Link)"""

    name            = "expand"

    POST            = None

    ### XXX

# end class Expander

class QX_Completed (_JSON_Action_PO_) :
    """Process AJAX query for accepting completion of entity auto completion"""

    name            = "esf_completed"

    def _rendered_post (self, request, response) :
        json   = TFL.Record (** request.json)
        af     = self._get_esf_filter (json)
        ETM    = self.top.scope  [af.type_name]
        obj    = self.pid_query_request (json.pid, ETM.E_Type)
        for f in af.filters :
            f.edit = f.value = f.AQ.QR (obj)
        result = self._rendered_esf \
            ( af
            , value     = obj.pid
            , display   = str (obj.FO)
            )
        return result
    # end def _rendered_post

# end class QX_Completed

class QX_Completer (_JSON_Action_PO_) :
    """Process AJAX query for querying completions for entity auto completions"""

    name            = "esf_completer"

    def _rendered_post (self, request, response) :
        json   = TFL.Record (** request.json)
        af     = self._get_attr_filter (json)
        ET     = af.AQ.E_Type
        at     = QR.Filter  (ET, json.trigger)
        names  = tuple \
            ( uniq
                ( iter_chain
                    ( (at.AQ._full_name, )
                    , tuple (f._full_name for f in ET.AQ.Atoms)
                    )
                )
            )
        scope  = self.top.scope
        qr     = QR.from_request \
            (scope, ET, request, ** request.json.get ("values", {}))
        ETM    = scope [ET.type_name]
        bq     = ETM.query_s ()
        if 0 : ### XXX TBD
            ### For some attributes, `eligible_object_restriction` is too
            ### restrictive here. For instance, an attribute referring to a
            ### person should normally not be restricted even if the user is
            ### only allowed to change his own `PAP.Person` instance
            ###
            ### `eligible_object_restriction` is used in two conflicting
            ### ways:
            ### - to restrict `objects` in `Admin_Restricted`
            ### - to restrict the completions offered in an entity selector
            ###   form: we might want some restrictions here, but not
            ###   necessarily the same ones as for `Admin_Restricted`
            eor    = self.eligible_object_restriction (ET.type_name)
            if eor is not None :
                bq = bq.filter (eor)
        query  = qr (bq).distinct ()
        entity_p = getattr (json, "entity_p", False)
        return self._rendered_completions (ETM, query, names, entity_p, json)
    # end def _rendered_post

# end class QX_Completer

class QX_Entity_Selector_Form (_JSON_Action_PO_) :
    """Process AJAX query for entity-selector form"""

    name            = "esf"

    def _rendered_post (self, request, response) :
        json   = TFL.Record (** request.json)
        af     = self._get_esf_filter (json)
        result = self._rendered_esf   (af)
        return result
    # end def _rendered_post

# end class QX_Entity_Selector_Form

_Ancestor = GTW.RST.TOP.Dir_V
_Mixin    = GTW.RST.TOP.MOM.Admin._NC_Mixin_
class _QX_Dispatcher_ (_Mixin, _Ancestor) :

    name                  = "qx"

    _v_entry_type_list    = \
        (QX_Completed, QX_Completer, QX_Entity_Selector_Form)

# end class _QX_Dispatcher_

class _MF3_E_Type_Mixin_ (_Mixin, GTW.RST.TOP._Base_) :
    """Mixin handling MF3 forms for one E_Type."""

    _real_name            = "E_Type_Mixin"

    Instance              = Instance

    form_attr_spec_d      = {}
    max_completions       = 20
    nav_off_canvas        = True
    skip_etag             = True
    submit_callback       = None
    submit_error_callback = None

    _auth_required        = True
    _exclude_robots       = True
    _form_attr_spec       = {}
    _field_type_map       = {}
    _form_id_prefix       = "MF3"
    _greet_entry          = None
    _list_display         = None
    _sort_key             = None

    _v_entry_type_list    = \
        (Completed, Completer, Creator, Expander, _QX_Dispatcher_)

    @Once_Property
    def et_map_name (self) :
        if not self.implicit :
            return "mf3"
    # end def et_map_name

    @Once_Property
    @getattr_safe
    def Form (self) :
        return MF3.Entity.Auto (self.E_Type, id_prefix = self.form_id_prefix)
    # end def Form

    @property
    @getattr_safe
    def form_attr_spec (self) :
        result = self._form_attr_spec
        xtra   = self.form_attr_spec_d
        if xtra :
            result = dict (result, ** xtra)
        return result
    # end def form_attr_spec

    @form_attr_spec.setter
    def form_attr_spec (self, value) :
        self._form_attr_spec = value
    # end def form_attr_spec

    @property
    @getattr_safe
    def form_id_prefix (self) :
        return self._form_id_prefix
    # end def form_id_prefix

    @form_id_prefix.setter
    def form_id_prefix (self, value) :
        self._form_id_prefix = value
    # end def form_id_prefix

    @Once_Property
    @getattr_safe
    def form_injected_templates (self) :
        try :
            form = self.Form
        except LookupError :
            renderers = set ()
        else :
            renderers = set (self.Form.template_module_iter ())
        return tuple (self.top.Templateer.get_template (r) for r in renderers)
    # end def form_injected_templates

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
    def qr_spec (self) :
        return QRS (self.E_Type)
    # end def qr_spec

    def eligible_object_restriction (self, type_name) :
        return None
    # end def eligible_objects

    def href_complete (self) :
        return pp_join (self.abs_href, "complete")
    # end def href_complete

    def href_completed (self) :
        return pp_join (self.abs_href, "completed")
    # end def href_completed

    def href_expand (self) :
        return pp_join (self.abs_href, "expand")
    # end def href_delete

    def href_qx_esf_completed (self) :
        return pp_join (self.abs_href, self.qx_prefix, "esf_completed")
    # end def href_qx_esf_completed

    def href_qx_esf_completer (self) :
        return pp_join (self.abs_href, self.qx_prefix, "esf_completer")
    # end def href_qx_esf_completer

    def href_qx_esf (self) :
        return pp_join (self.abs_href, self.qx_prefix, "esf")
    # end def href_qx_esf

    def is_current_dir (self, page) :
        if not self.hidden :
            p = page.href
            s = self.href
            return p == s or (p.startswith (s) and p [len (s)] == "/")
    # end def is_current_dir

    def page_from_obj (self, obj) :
        result = self._new_child_x (self.Instance, str (obj.pid), ())
        return result
    # end def page_from_obj

    def template_iter (self) :
        T = self.top.Templateer
        yield self.template
        yield T.get_template \
            (self.Instance.template_name, self.form_injected_templates)
    # end def template_iter

    def _get_child (self, child, * grandchildren) :
        result = self.__super._get_child (child, * grandchildren)
        if result is None and not grandchildren :
            try :
                pid = int (child)
            except ValueError :
                pass
            else :
                result = self.Instance \
                    ( args   = (child, )
                    , kind   = child
                    , name   = child
                    , parent = self
                    , ** self._child_kw (child)
                    )
        if result is None and self._entry_type_map :
            try :
                T = self._entry_type_map [child]
            except KeyError :
                pass
            else :
                result = self._new_child (T, child, grandchildren)
        return result
    # end def _get_child

    def _new_child (self, T, child, grandchildren) :
        if child == self.qx_prefix and grandchildren :
            new_child = self.__super._new_child
        else :
            new_child = self._new_child_x
        return new_child (T, child, grandchildren)
    # end def _new_child

E_Type_Mixin = _MF3_E_Type_Mixin_ # end class

if __name__ != "__main__" :
    GTW.RST.TOP.MOM._Export_Module ()
### __END__ GTW.RST.TOP.MOM.MF3
