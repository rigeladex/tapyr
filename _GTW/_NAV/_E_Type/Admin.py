# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2011 Mag. Christian Tanzer All rights reserved
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
#    GTW.NAV.E_Type.Admin
#
# Purpose
#    Navigation page for managing the instances of a specific E_Type
#
# Revision Dates
#    20-Jan-2010 (CT) Creation
#    25-Jan-2010 (CT) `rendered` changed to take `handler` instead of `context`
#    29-Jan-2010 (CT) Call to `rollback` added to `Changer.rendered`
#    29-Jan-2010 (CT) Support for `Form_args` and `Form_kw` added to
#                     `Admin.__init__`
#     3-Feb-2010 (MG) `Completer` fixed
#     5-Feb-2010 (MG) `Completer` changed again, `_get_child` change to
#                     handle multiple sub levels
#     6-Feb-2010 (MG) Use `HTTP.Request_Data` instead of
#                     `GTW.Tornado.Request_Data`
#     6-Feb-2010 (MG) Made `Completed` working again
#    12-Feb-2010 (CT) `Admin.__init__` changed to convert strings in
#                     `list_display` to attributes
#    19-Feb-2010 (CT) `SUPPORTED_METHODS` added
#    22-Feb-2010 (CT) `Changer.rendered` changed to pass `cancel_href` to `Form`
#    22-Feb-2010 (CT) `Completer.rendered` changed to use `cooked_attrs`
#    22-Feb-2010 (CT) Use `request.req_data` instead of home-grown code
#    24-Feb-2010 (CT) `_Cmd_`: s/GTW.NAV._Site_Entity_/GTW.NAV.Page/
#    24-Feb-2010 (MG) `_get_child` changed to always pass the grandchildren
#                     as tuple,
#                     Parameters of childs renamed (lid -> args)
#    26-Feb-2010 (MG) Completion handling changed
#    15-Mar-2010 (CT) `kind_name` removed
#    17-Mar-2010 (CT) `GTW.NAV.E_Type.Mixin` factored
#    23-Mar-2010 (CT) Sort `_entries`
#    24-Mar-2010 (CT) `Changer.rendered` changed to add `last_changed`, if any
#     3-May-2010 (MG) `Admin.Changer`: support for `calcel` submit added
#     5-May-2010 (MG) `_get_child` support for `child_attrs` added
#    12-May-2010 (CT) Use `pid`, not `lid`
#    15-May-2010 (MG) `Form` started
#    15-May-2010 (MG) `Fields` added
#    15-May-2010 (MG) `Test` added
#    17-May-2010 (MG) `Test` removed again
#    19-May-2010 (MG) `Fields` changed
#    19-May-2010 (MG) `Test` readded
#    20-May-2010 (MG) `Test` finished
#    26-May-2010 (MG) Error handing changed
#    01-Jun-2010 (MG) `Changer.form_parameters` added
#    21-Jun-2010 (MG) `From` and `list_display` once properties added, inline
#                     class `Form` renamed to `HTML_Form`
#    14-Jul-2010 (CT) `Changer.rendered` changed to `Redirect_302`
#                     identically for boith `submit` and `cancel`
#     5-Aug-2010 (CT) Support for `composite.field` added
#     6-Aug-2010 (MG) `Changer.rendered` use a nested change to make it
#                     possible to undo all changes done in this form in one step
#     8-Aug-2010 (MG) `Test` changed
#    17-Aug-2010 (CT) `Changer.rendered` changed to check `scope.readonly`
#    31-Aug-2010 (CT) `Changer.obj` added to simplify debugging from
#                     browser-based `Console`
#    21-Dec-2010 (CT) `h_title` removed
#    22-Dec-2010 (CT) Register `Admin` instances in `top.ET_Map`
#     3-Jan-2011 (CT) Introduce `template_name`
#     7-Jan-2011 (CT) `is_current_dir` redefined
#    11-Jan-2011 (CT) s/handler.json/handler.write_json/
#    11-Jan-2011 (CT) `Media` for `tablesorter` added
#    16-Mar-2011 (CT) `AFS` added
#    16-Mar-2011 (CT) `_get_child` simplified
#    29-Mar-2011 (CT) `AFS.form` factored
#    30-Mar-2011 (CT) `Expander` started
#    31-Mar-2011 (CT) `Expander` continued, `href_expand` added
#     1-Apr-2011 (CT) `Expander` continued..
#     4-Apr-2011 (CT) `Expander` continued... (`collapsed`)
#     5-Apr-2011 (CT) `Expander` continued....
#     6-Apr-2011 (CT) `Expander` continued....., `AFS._post_handler` added
#    13-Apr-2011 (CT) `Expander` continued......
#     2-May-2011 (CT) `Expander` continued......., `AFS._post_handler` bug fixes
#     2-May-2011 (CT) `AFS._raise_401` and `._raise_403` added
#    27-May-2011 (CT) `Deleter.SUPPORTED_METHODS` restricted to `POST`
#     7-Jun-2011 (CT) `Deleter._view` started to change to send back `json`
#     8-Jun-2011 (CT) `AFS` attached to `change` URL, and to `create` URL, too
#    22-Jul-2011 (CT) Use `Redirect_303` instead of `Redirect_302`
#    22-Jul-2011 (CT) `AFS_Completer` started
#    24-Jul-2011 (CT) `AFS_Completer` continued
#    25-Jul-2011 (CT) `href_complete` added
#    26-Jul-2011 (CT) `obj`, `Form`, and `form` factored from `AFS` to `_Cmd_`
#    26-Jul-2011 (CT) `AFS_Completed` started, `href_completed` added
#    24-Jul-2011 (CT) `AFS_Completer` continued..
#    28-Jul-2011 (CT) `JSON_Error` added and used for refactored methods
#    28-Jul-2011 (CT) `AFS_Completed` continued
#     1-Aug-2011 (CT) Use of `JSON_Error` fixed
#                     (`return` added to `exc (handler)`)
#     1-Aug-2011 (CT) `AFS_Completed` continued..
#     7-Sep-2011 (CT) `AFS_Completed` and `AFS_Completer` continued...
#     9-Sep-2011 (CT) Use `.E_Type` instead of `._etype`
#    12-Sep-2011 (CT) `AFS._Media.scripts` changed to load `AFS/Elements.js`
#                     before `jQ/afs.js`
#    13-Sep-2011 (CT) `_ui_displayed` added and used in `AFS_Completer`
#    13-Sep-2011 (CT) `AFS_Completer.rendered` changed to indicate partial match
#    15-Sep-2011 (CT) Move instantiation of `attr.completer` to `MOM.Attr.Spec`
#    21-Sep-2011 (CT) `_ui_displayed` changed to deal properly with `pid`
#    21-Sep-2011 (CT) `AFS_Completer` and `AFS_Completed` changed to use
#                     `pid` for entity completion
#    22-Sep-2011 (CT) s/Class/P_Type/ for _A_Entity_ attributes
#    26-Sep-2011 (MG) `AFS.injected_*` added
#    10-Oct-2011 (CT) Old-style form handling removed
#    13-Oct-2011 (CT) `_check_readonly` factored
#    13-Oct-2011 (CT) `Deleter` changed to support json requests, too
#     8-Nov-2011 (CT) Factor `field_element` and guard it against `KeyError`
#    14-Nov-2011 (CT) Add support for `query_restriction`
#    16-Nov-2011 (CT) Change `rendered` to always `LET` `query_restriction`
#    16-Nov-2011 (CT) Add property `head_line`
#    17-Nov-2011 (CT) Change `head_line` to provide `total_f` and `total_u`
#    22-Nov-2011 (CT) Add guard for `completer` to `Complete[dr].rendered`
#    22-Nov-2011 (CT) Add `qr_spec`
#    24-Nov-2011 (CT) Change `rendered` to support json requests
#    25-Nov-2011 (CT) Add `template_iter`, factor (AFS specific) `Form`,
#                     factor `changer_injected_templates`
#    25-Nov-2011 (CT) Add `limit` and `offset` to result of `rendered` for json
#    26-Nov-2011 (CT) Add `button_types` and `buttons` to `rendered`
#    30-Nov-2011 (CT) Add class variable `Admin.button_types`
#    ««revision-date»»···
#--

from   __future__  import unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL
from   _MOM.import_MOM          import MOM, Q

import _GTW._Form._MOM.Instance
from   _GTW._AFS._MOM.Element   import Form  as AFS_Form
from   _GTW._AFS.Value          import Value as AFS_Value

import _GTW.FO
import _GTW.jQuery

import _GTW._NAV.Base
import _GTW._NAV._E_Type._Mgr_Base_
from   _GTW._NAV._E_Type.Query_Restriction import \
     ( Query_Restriction      as QR
     , Query_Restriction_Spec as QRS
     )

import _TFL._Meta.Object
from   _TFL._Meta.Once_Property import Once_Property

from   _TFL.I18N                import _, _T, _Tn

from   itertools                import chain as ichain
from   posixpath                import join  as pjoin

class JSON_Error (Exception) :

    def __init__ (self, __data = None, ** kw) :
        self.__data = __data
        self.kw     = kw
    # end def __init__

    def __call__ (self, handler) :
        return handler.write_json (self.__data, ** self.kw)
    # end def __call__

# end class JSON_Error

class Admin (GTW.NAV.E_Type._Mgr_Base_, GTW.NAV.Page) :
    """Navigation page for managing the instances of a specific E_Type."""

    css_group           = "Type"
    max_completions     = 20
    template_name       = "e_type_admin"

    button_types        = dict \
        ( ADD           = "button"
        , APPLY         = "submit"
        , CANCEL        = "button"
        , CLEAR         = "button"
        , CLOSE         = "button"
        )

    class _Cmd_ (GTW.NAV.E_Type.Mixin, GTW.NAV.Page) :

        args              = (None, )
        implicit          = True
        SUPPORTED_METHODS = set (("GET", "POST"))

        @property
        def obj (self) :
            ETM = self.ETM
            pid = self.args and self.args [0]
            if pid is not None :
                return ETM.pid_query (pid)
        # end def obj

        def field_element (self, form, fid) :
            try :
                return form  [fid]
            except KeyError :
                error = _T ("Form corrupted, unknown element id %s" % (fid, ))
                raise JSON_Error (error  = error)
        # end def field_element

        def form (self, obj = None, ** kw) :
            if obj is None :
                obj = self.obj
            return self.parent.Form (self.ETM, obj, ** kw)
        # end def form

        def form_element (self, fid) :
            try :
                form = AFS_Form   [fid]
                return form, form [fid]
            except KeyError :
                error = _T ("Form corrupted, unknown element id %s" % (fid, ))
                raise JSON_Error (error  = error)
        # end def form_element

        def form_value (self, json_cargo) :
            try :
                return AFS_Value.from_json (json_cargo)
            except Exception as exc :
                raise JSON_Error (error = "%s" % (exc, ))
        # end def form_value

        def form_value_apply (self, fv, scope, sid, session_secret) :
            try :
                return fv.apply \
                    (scope, _sid = sid, _session_secret = session_secret)
            except GTW.AFS.Error.Conflict :
                raise JSON_Error (conflicts = fv.as_json_cargo)
            except Exception as exc :
                if __debug__ :
                    import traceback; traceback.print_exc ()
                raise JSON_Error (error = "%s" % (exc, ))
        # end def form_value_apply

        def pid_query (self, ETM, pid) :
            try :
                return ETM.pid_query (pid)
            except LookupError :
                error = _T ("%s `%s` doesn't exist!") % \
                    (_T (self.E_Type.ui_name), pid)
                raise JSON_Error (error = error)
        # end def pid_query

        def session_secret (self, handler, sid) :
            try :
                return self._get_edit_session (handler, sid)
            except handler.session.Expired as exc :
                raise JSON_Error \
                    ( expired = "%s" % (exc, )
                    , ### XXX re-authorization form (password only)
                    )
            except LookupError as exc :
                raise JSON_Error (error = "Session expired: %s" % (exc, ))
        # end def session_secret

        def _check_readonly (self, request) :
            if self.top.scope.readonly : ### XXX might be out-of-date !!!
                request.Error = \
                    (_T ( "At the moment, the database is set to "
                          "readonly to allow maintenance."
                        )
                    )
                raise self.top.HTTP.Error_503 (request.path, request.Error)
        # end def _check_readonly

        def _raise_401 (self, handler) :
            if handler.json :
                return handler.write_json \
                    (error = _T ("Not logged in or login-session is expired"))
            else :
                return self.__super._raise_401 (handler)
        # end def _raise_401

        def _raise_403 (self, handler) :
            if handler.json :
                return handler.write_json \
                    (error = _T ("Not authorized for this page"))
            else :
                return self.__super._raise_403 (handler)
        # end def _raise_403

        def _ui_displayed (self, ETM, names, matches) :
            def _gen () :
                for n in names :
                    try :
                        attr = ETM.get_etype_attribute (n)
                    except AttributeError :
                        disp = lambda v : v
                    else :
                        disp = lambda v, attr = attr : attr.ac_ui_display (v)
                    yield disp
            attr_displayers = list (_gen ())
            for match in matches :
                yield tuple \
                    (d (v) for d, v in zip (attr_displayers, match))
        # end def _ui_displayed

    # end class _Cmd_

    class Changer (_Cmd_) :
        """Model an admin page for creating or changing a specific instance
           of a etype with an AFS form.
        """

        name            = "create"
        args            = (None, )
        template_name   = "e_type_afs"
        form_parameters = {}

        @property
        def injected_templates (self) :
            return self.parent.changer_injected_templates
        # end def injected_templates

        def rendered (self, handler, template = None) :
            HTTP     = self.top.HTTP
            context  = handler.context
            obj      = context ["instance"] = None
            request  = handler.request
            req_data = request.req_data
            pid      = req_data.get ("pid") or self.args [0]
            scope    = self.top.scope
            self._check_readonly (request)
            if pid is not None and pid != "null" :
                try :
                    obj = context ["instance"] = self.ETM.pid_query (pid)
                except LookupError :
                    request.Error = \
                        ( _T ("%s `%s` doesn't exist!")
                        % (_T (self.E_Type.ui_name), pid)
                        )
                    raise HTTP.Error_404 (request.path, request.Error)
            if request.method == "POST" :
                return self._post_handler (handler, scope)
            else :
                sid, session_secret = self._new_edit_session (handler)
                form = self.form \
                    (obj, _sid = sid, _session_secret = session_secret)
                self.Media = self._get_media \
                    (head = getattr (form, "Media", None))
                context.update (form = form)
                try :
                    self.last_changed = obj.FO.last_changed
                except AttributeError :
                    pass
                return self.__super.rendered (handler, template)
        # end def rendered

        def _post_handler (self, handler, scope) :
            json       = handler.json
            request    = handler.request
            result     = {}
            if json is None :
                raise NotImplementedError \
                    ("AFS form post requests without content-type json")
            try :
                fv             = self.form_value (json ["cargo"])
                get_template   = self.top.Templateer.get_template
                session_secret = self.session_secret (handler, fv.sid)
                self.form_value_apply (fv, scope, fv.sid, session_secret)
                ikw = dict \
                    ( allow_new       = json.get ("allow_new")
                    , collapsed       = json.get ("collapsed")
                    , _sid            = fv.sid
                    , _session_secret = session_secret
                    )
                result ["$child_ids"] = rids = []
                for e in fv.entities () :
                    if e.entity :
                        obj = e.entity
                        fi  = e.elem.instantiated (e.id, obj.ETM, obj, ** ikw)
                        result [e.id] = dict \
                            ( html = get_template (e.elem.renderer).call_macro
                                (fi.widget, fi, fi, fi.renderer)
                            , json = fi.as_json_cargo
                            )
                        rids.append (e.id)
                return handler.write_json (result)
            except JSON_Error as exc :
                return exc (handler)
        # end def _post_handler

    # end class Changer

    class Completed (_Cmd_) :
        """Return auto completion values for a AFS page."""

        SUPPORTED_METHODS = set (("POST", ))

        def rendered (self, handler, template = None) :
            HTTP      = self.top.HTTP
            request   = handler.request
            if handler.json is None :
                raise HTTP.Error_400 \
                    (_T ("%s only works with content-type json") % request.path)
            json      = TFL.Record (** handler.json)
            result    = {}
            scope     = self.top.scope
            try :
                session_secret = self.session_secret (handler, json.sid)
                form, elem     = self.form_element   (json.fid)
                field          = self.field_element  (form, json.trigger)
                ETM            = scope [elem.type_name]
                E_Type         = ETM.E_Type
                if json.complete_entity :
                    obj = ETM.pid_query (json.pid)
                    result ["completions"] = n = int (obj is not None)
                    if n == 1 :
                        ikw = dict \
                            ( allow_new        = handler.json.get ("allow_new")
                            , collapsed        = False
                            , copy             = False
                            , _sid             = json.sid
                            , _session_secret  = session_secret
                            )
                        fi  = elem.instantiated (json.fid, ETM, obj, ** ikw)
                        renderer = self.top.Templateer.get_template \
                            (fi.renderer)
                        result.update \
                            ( html = renderer.call_macro
                                (fi.widget, fi, fi, fi.renderer)
                            , json = fi.as_json_cargo
                            )
                else :
                    attr      = getattr (E_Type, field.name)
                    completer = attr.completer
                    if completer is not None :
                        names = completer.names
                        fs    = ETM.raw_query_attrs (names, json.values)
                        query = ETM.query (* fs)
                        result ["completions"] = n = query.count ()
                        if n == 1 :
                            af     = ETM.raw_query_attrs (names)
                            values = query.attrs (* af).one ()
                            result ["fields"] = len  (names)
                            result ["names"]  = names
                            result ["values"] = values
                return handler.write_json (result)
            except JSON_Error as exc :
                return exc (handler)
        # end def rendered

    # end class Completed

    class Completer (_Cmd_) :
        """Do auto completion for a AFS page."""

        SUPPORTED_METHODS = set (("POST", ))

        def rendered (self, handler, template = None) :
            HTTP      = self.top.HTTP
            request   = handler.request
            if handler.json is None :
                raise HTTP.Error_400 \
                    (_T ("%s only works with content-type json") % request.path)
            json      = TFL.Record (** handler.json)
            result    = dict (matches = [], partial = False)
            scope     = self.top.scope
            try :
                form, elem   = self.form_element  (json.fid)
                field        = self.field_element (form, json.trigger)
                ETM          = scope [elem.type_name]
                E_Type       = ETM.E_Type
                attr         = getattr (E_Type, field.name)
                completer    = attr.completer
                if completer is not None :
                    max_n        = self.max_completions
                    names        = completer.names
                    query        = completer (self.top.scope, json.values)
                    fs           = tuple (ETM.raw_query_attrs (names))
                    if completer.entity_p :
                        fs      += (Q.pid, )
                        names   += ("pid", )
                    matches      = query.attrs (* fs).limit (max_n + 1).all ()
                    n            = result ["completions"] = len (matches)
                    finished     = result ["finished"]    = n == 1
                    if n :
                        if n <= max_n :
                            result ["fields"]  = len    (names)
                            result ["matches"] = sorted \
                                (self._ui_displayed (ETM, names, matches))
                        else :
                            if json.trigger == json.trigger_n :
                                matches = query.attrs (attr.raw_query).limit \
                                    (max_n + 1).all ()
                                m = len (matches)
                                if m <= max_n :
                                    matches = ([m, "..."] for m in  matches)
                                    result ["fields"]  = 1
                                    result ["matches"] = sorted (matches)
                                    result ["partial"] = True
                                else :
                                    ### XXX find fewer partial matches !!!
                                    result ["fields"]  = 0
                return handler.write_json (result)
            except JSON_Error as exc :
                return exc (handler)
        # end def rendered

    # end class Completer

    class Deleter (_Cmd_) :
        """Model an admin action for deleting a specific instance of a etype."""

        name              = "delete"
        template_name     = "e_type_delete"
        SUPPORTED_METHODS = set (("POST", ))

        def _post_handler_args (self, handler) :
            ETM        = self.ETM
            pid        = self.args and self.args [0]
            request    = handler.request
            result     = {}
            if pid :
                obj    = self.pid_query (ETM, pid)
                result ["replacement"] = dict \
                    ( html = """<td colspan="6">%s</td>"""
                      % (_T ("""Object "%s" deleted""") % (obj.ui_display, ))
                      ### XXX use template to render this XXX
                    , ### XXX undelete link !!!
                    )
                obj.destroy ()
            else :
                request.Error = \
                    ( _T ("You need to specify a pid!"))
                raise self.HTTP.Error_400 (request.path, request.Error)
            return result
        # end def _post_handler_args

        def _post_handler_json (self, handler) :
            json           = handler.json
            request        = handler.request
            fid            = json.get ("fid")
            pid            = json.get ("pid")
            sid            = json.get ("sid")
            result         = {}
            scope          = self.top.scope
            session_secret = self.session_secret (handler, sid)
            form, elem     = self.form_element   (fid)
            ETM            = scope [elem.type_name]
            if pid is not None and pid != "null" :
                obj = self.pid_query (ETM, pid)
                result ["html"] = \
                    ( """<h2>%s</h2>"""
                      % ( _T ("""Object "%s" deleted""")
                        % (obj.ui_display, )
                        )
                      ### XXX use template to render this XXX
                    )
                obj.destroy ()
            else :
                request.Error = \
                    ( _T ("You need to specify a pid!"))
                raise self.HTTP.Error_400 (request.path, request.Error)
            return result
        # end def _post_handler_json

        def _view (self, handler) :
            self._check_readonly (handler.request)
            try :
                if self.args and self.args [0] :
                    ph = self._post_handler_args
                else :
                    ph = self._post_handler_json
                result = ph (handler)
                return handler.write_json (result)
            except JSON_Error as exc :
                return exc (handler)
        # end def _view

    # end class Deleter

    class Expander (_Cmd_) :
        """Expand a sub-form (e.g., Entity_Link)"""

        SUPPORTED_METHODS = set (("GET", ))

        def rendered (self, handler, template = None) :
            context  = handler.context
            obj      = context ["instance"] = None
            request  = handler.request
            req_data = request.req_data
            fid      = req_data.get ("fid")
            pid      = req_data.get ("pid")
            sid      = req_data.get ("sid")
            scope    = self.top.scope
            try :
                form, elem     = self.form_element   (fid)
                session_secret = self.session_secret (handler, sid)
                ETM            = scope [elem.type_name]
                if pid is not None and pid != "null" :
                    obj = context ["instance"] = self.pid_query (ETM, pid)
                ikw = dict \
                    ( allow_new       = req_data.get ("allow_new")
                    , collapsed       = req_data.get ("collapsed")
                    , copy            = req_data.get ("copy")
                    , _sid            = sid
                    , _session_secret = session_secret
                    )
                new_id_suffix = req_data.get ("new_id_suffix")
                if new_id_suffix is not None :
                    ikw ["new_id_suffix"] = new_id_suffix
                fi = elem.instantiated (fid, ETM, obj, ** ikw)
                renderer = self.top.Templateer.get_template (fi.renderer)
                return handler.write_json \
                    ( html = renderer.call_macro
                        (fi.widget, fi, fi, fi.renderer)
                    , json = fi.as_json_cargo
                    )
            except JSON_Error as exc :
                return exc (handler)
        # end def rendered

    # end class Expander

    class Instance (TFL.Meta.Object) :
        """Model a specific instance in the context of an admin page for one
           E_Type, e.g., displayed as one line of a table.
        """

        def __init__ (self, admin, obj) :
            self.admin = admin
            self.obj   = obj
            self.FO    = GTW.FO (obj, admin.top.encoding)
        # end def __init__

        @Once_Property
        def fields (self) :
            admin = self.admin
            FO    = self.FO
            return [(f, getattr (FO, f.name)) for f in admin.list_display]
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

    # end class Instance

    Page = Instance

    @Once_Property
    def __Obsolete_Form (self) :
        try :
            return GTW.Form.MOM.Instance.New \
               (self.ETM, * self.Form_Spec ["args"], ** self.Form_Spec ["kw"])
        except Exception :
            import traceback; traceback.print_exc ()
            raise
    # end def Obsolete_Form

    class __Obsolete_Changer (_Cmd_) :
        ### XXX transfer `nested_change_recorder`, error handling, ...
        ###     to `Changer`

        def rendered (self, handler, template = None) :
            ETM      = self.ETM
            E_Type   = self.E_Type
            HTTP     = self.top.HTTP
            context  = handler.context
            obj      = context ["instance"] = None
            request  = handler.request
            req_data = request.req_data
            pid      = req_data.get ("pid") or  self.args [0]
            if pid is not None and pid != "null" :
                try :
                    obj = ETM.pid_query (pid)
                except LookupError :
                    request.Error = \
                        ( _T ("%s `%s` doesn't exist!")
                        % (_T (E_Type.ui_name), pid)
                        )
                    raise HTTP.Error_404 (request.path, request.Error)
            form  = self.__Obsolete_Form \
                ( self.abs_href, obj, cancel_href = self.parent.abs_href
                , ** self.form_parameters
                )
            scope = self.top.scope
            if scope.readonly : ### XXX might be out-of-date !!!
                request.Error = \
                    (_T ( "At the moment, the database is set to "
                          "readonly to allow maintenance."
                        )
                    )
                raise HTTP.Error_503 (request.path)
            if request.method == "POST" :
                err_count = 0
                if req_data.get ("cancel") :
                    ### the user has clicked on the cancel button and not on
                    ### the submit button
                    scope.rollback ()
                else :
                    with scope.nested_change_recorder \
                        (MOM.SCM.Change.Undoable) :
                            err_count = form (req_data)
                    if err_count == 0 :
                        man = self.parent.manager
                        if man :
                            man._old_cid = -1
                    else :
                        self._display_errors (form)
                        scope.rollback       ()
                if err_count == 0 :
                    tail = "#pk-%s" % (obj.pid) if obj else ""
                    ### http://tumblr.jonthornton.com/post/7902581999/preventing-form-re-submission-with-http-303-redirects
                    raise HTTP.Redirect_303 \
                        ("%s%s" % (self.parent.abs_href, tail))
            self.Media = self._get_media (head = getattr (form, "Media", None))
            context.update (form = form)
            try :
                self.last_changed = obj.FO.last_changed
            except AttributeError :
                pass
            return self.__super.rendered (handler, template)
        # end def rendered

        def _display_errors (self, form, indent = "") :
            print "%s%s" % (indent, form.prefix)
            for e in form.errors.of_form (form) :
                print "%s  %s" % (indent, e)
            for ifi in form.inline_fields :
                ifo = ifi.form
                if form.errors.count (ifo) :
                    self._display_errors (ifo, indent + "  ")
            for ig in form.inline_groups :
                for f in ig.forms :
                    if form.errors.count (f) :
                        self._display_errors (f, indent + "  ")
        # end def _display_errors

    # end class __Obsolete_Changer

    def __init__ (self, parent, ** kw) :
        kw ["Form_Spec"] = dict \
            (args = kw.pop ("Form_args", ()), kw = kw.pop ("Form_kw", {}))
        kw ["_list_display"] = kw.pop ("list_display", None)
        self.__super.__init__ (parent, ** kw)
        self.prefix = pjoin (parent.prefix, self.name)
        self.top.ET_Map [self.E_Type.type_name].admin = self
    # end def __init__

    @Once_Property
    def changer_injected_templates (self) :
        renderers = set (self.Form.renderer_iter ())
        return tuple (self.top.Templateer.get_template (r) for r in renderers)
    # end def changer_injected_templates

    @Once_Property
    def Form (self) :
        return AFS_Form [self.E_Type.GTW.afs_id]
    # end def Form

    @property
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

    @Once_Property
    def href (self) :
        return pjoin (self.prefix, u"")
    # end def href

    def href_create (self) :
        return pjoin (self.abs_href, "create")
    # end def href_create

    def href_change (self, obj) :
        return pjoin (self.abs_href, "change", str (obj.pid))
    # end def href_change

    def href_complete (self) :
        return pjoin (self.abs_href, "complete")
    # end def href_complete

    def href_completed (self) :
        return pjoin (self.abs_href, "completed")
    # end def href_completed

    def href_delete (self, obj = None) :
        result = pjoin (self.abs_href, "delete")
        if obj is not None :
            result = pjoin (result, str (obj.pid))
        return result
    # end def href_delete

    def href_display (self, obj) :
        man = self.manager
        if man :
            return man.href_display (obj)
    # end def href_display

    def href_expand (self) :
        return pjoin (self.abs_href, "expand")
    # end def href_delete

    def is_current_dir (self, nav_page) :
        p = nav_page.href
        return p.startswith (self.href) and p != self.href
    # end def is_current_dir

    @Once_Property
    def list_display (self) :
        if self._list_display is None :
            return self._auto_list_display (self.ETM)
        etype = self.ETM.E_Type
        return tuple \
            (self._attr_kind (etype, a) for a in self._list_display)
    # end def list_display

    @Once_Property
    def manager (self) :
        return self.etype_manager (self.E_Type)
    # end def manager

    @Once_Property
    def qr_spec (self) :
        return QRS (self.E_Type, self.list_display)
    # end def qr_spec

    def rendered (self, handler, template = None) :
        fields = self.list_display
        qr = QR.from_request_data (self.ETM.E_Type, handler.request.req_data)
        with self.LET (query_restriction = qr) :
            objects = self._get_objects () if qr else self._get_entries ()
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
                handler.context.update \
                    ( fields            = fields
                    , objects           = objects
                    , query_restriction = self.query_restriction
                    )
                if handler.wants_json :
                    template   = self.top.Templateer.get_template ("e_type")
                    call_macro = template.call_macro
                    buttons    = dict \
                        ( FIRST = call_macro
                            ("qr_button_first", self, fields, qr)
                        , LAST  = call_macro
                            ("qr_button_last",  self, fields, qr)
                        , NEXT  = call_macro
                            ("qr_button_next",  self, fields, qr)
                        , PREV  = call_macro
                            ("qr_button_prev",  self, fields, qr)
                        )
                    result = handler.write_json \
                        ( dict
                            ( buttons          = buttons
                            , head_line        = self.head_line
                            , limit            = qr.limit
                            , object_container = call_macro
                                ("admin_table", self, fields, objects)
                            , offset           = qr.offset
                            )
                        )
                else :
                    result = self.__super.rendered (handler, template)
            return result
    # end def rendered

    def template_iter (self) :
        T = self.top.Templateer
        yield self.template
        yield T.get_template \
            (self.Changer.template_name, self.changer_injected_templates)
        yield T.get_template (self.Deleter.template_name)
    # end def template_iter

    def _attr_kind (self, etype, name) :
        if "." in name :
            x = etype
            for n in name.split (".") :
                x = getattr (x.E_Type, n)
            return TFL.Record \
                ( name         = name
                , attr         = x.attr
                , ui_name      = x.ui_name
                , description  = x.description
                )
        else :
            return getattr (etype, name)
    # end def _attr_kind

    def _auto_list_display (self, E_Type) :
        return list (ichain (E_Type.primary, E_Type.user_attr))
    # end def _auto_list_display

    _child_name_map      = dict \
        ( change         = (Changer,       "args",  None)
        , complete       = (Completer,     "args",  None)
        , completed      = (Completed,     "args",  None)
        , create         = (Changer,       "args",  0)
        , delete         = (Deleter,       "args",  None)
        , expand         = (Expander,      "args",  0)
        )
    child_attrs          = {}

    def _get_child (self, child, * grandchildren) :
        T  = None
        kw = {}
        if child in self._child_name_map :
            C, attr, n = self._child_name_map [child]
            if n is None or len (grandchildren) == n :
                T      = C
                name   = pjoin (* grandchildren) if grandchildren else ""
                kw     = \
                    {"name"   : "%s/%s" % (child, name)
                    , "kind"  : child
                    , attr    : grandchildren or (None, )
                    }
        if T :
            kw = dict (self.child_attrs.get (T.__name__, {}), ** kw)
            return T (parent = self, ** kw)
    # end def _get_child

    @property
    def children (self) :
        for n, (T, _, _) in self._child_name_map.iteritems () :
            yield T \
                ( parent = self
                , kind   = n
                , ** self.child_attrs.get (T.__name__, {})
                )
    # end def children

# end class Admin

if __name__ != "__main__" :
    GTW.NAV.E_Type._Export ("*")
### __END__ GTW.NAV.E_Type.Admin
