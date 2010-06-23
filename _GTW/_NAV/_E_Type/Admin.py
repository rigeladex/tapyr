# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
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
#    ««revision-date»»···
#--

from   _GTW                     import GTW
from   _TFL                     import TFL
from   _MOM.import_MOM          import Q

import _GTW._Form._MOM.Instance

import _GTW.FO
import _GTW._NAV.Base
import _GTW._NAV._E_Type._Mgr_Base_

import _TFL._Meta.Object
from   _TFL._Meta.Once_Property import Once_Property

from   _TFL.I18N                import _, _T, _Tn

from   itertools                import chain as ichain
from   posixpath                import join  as pjoin

class Admin (GTW.NAV.E_Type._Mgr_Base_, GTW.NAV.Page) :
    """Navigation page for managing the instances of a specific E_Type."""

    template    = "e_type_admin"

    class _Cmd_ (GTW.NAV.E_Type.Mixin, GTW.NAV.Page) :

        implicit          = True
        SUPPORTED_METHODS = set (("GET", "POST"))

    # end class _Cmd_

    class Changer (_Cmd_) :
        """Model an admin page for creating or changing a specific instance
           of a etype.
        """

        Media           = None ### cancel inherited property defined
        name            = "create"
        args            = (None, )
        template        = "e_type_change"
        form_parameters = {}

        def rendered (self, handler, template = None) :
            ETM      = self.ETM
            E_Type   = self.E_Type
            HTTP     = self.top.HTTP
            context  = handler.context
            obj      = context ["instance"] = None
            request  = handler.request
            req_data = request.req_data
            pid      = req_data.get ("pid") or self.args [0]
            if pid is not None :
                try :
                    obj = ETM.pid_query (pid)
                except LookupError :
                    request.Error = \
                        ( _T ("%s `%s` doesn't exist!")
                        % (_T (E_Type.ui_name), pid)
                        )
                    raise HTTP.Error_404 (request.path, request.Error)
            form = self.Form \
                ( self.abs_href, obj, cancel_href = self.parent.abs_href
                , ** self.form_parameters
                )
            if request.method == "POST" :
                if req_data.get ("cancel") :
                    ### the user has clicked on the cancel button and not on
                    ### the submit button
                    self.top.scope.rollback ()
                    raise HTTP.Redirect_302 (req_data ["form-cancel-href"])
                else :
                    err_count = form (req_data)
                    if err_count == 0 :
                        man = self.parent.manager
                        if man :
                            man._old_cid = -1
                        tail = "#pk-%s" % (obj.pid) if obj else ""
                        raise HTTP.Redirect_302 \
                            ("%s%s" % (self.parent.abs_href, tail))
                    else :
                        self._display_errors (form)
                        self.top.scope.rollback ()
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

    # end class Changer

    class Completer (_Cmd_) :
        """Deliver completion information for a AJAX request."""

        Media        = None ### cancel inherited property defined

        def rendered (self, handler, template = None) :
            context = handler.context
            request = handler.request
            result  = None
            if request.method == "GET" :
                form_cls, completer = self.Form.form_and_completer (self.forms)
                if form_cls is not None :
                    if completer.suggestions \
                           (form_cls, handler, request.req_data) :
                        return True ### prevent an 404 Error if we return None
                if __debug__ :
                    print "No completer found"
            raise self.top.HTTP.Error_404 (request.path)
        # end def rendered

    # end class Completer

    class Completed (_Cmd_) :
        """Deliver fields for a model instance selected by completion."""

        Media        = None ### cancel inherited property defined

        def rendered (self, handler, template = None) :
            request = handler.request
            result  = None
            if request.method == "GET" :
                form_cls, completer = self.Form.form_and_completer (self.forms)
                args = request.req_data
                pid  = args.get   ("pid")
                if not any (x is None for x in (form_cls, pid)) :
                    if completer.complete (form_cls, handler, pid) :
                        return True ### prevent an 404 Error if we return None
            raise self.top.HTTP.Error_404 (request.path)
        # end def rendered

    # end class Completed

    class Deleter (_Cmd_) :
        """Model an admin page for deleting a specific instance of a etype."""

        name         = "delete"
        template     = "e_type_delete"

        def _view (self, request) :
            HTTP = self.top.HTTP
            pid  = self.args [0]
            ETM  = self.ETM
            try :
                obj = ETM.pid_query (pid)
            except LookupError :
                request.Error = \
                    (_T ("%s `%s` doesn't exist!") % (_T (E_Type.ui_name), pid))
                raise HTTP.Error_404 (request.path, request.Error)
            obj.destroy ()
            ### XXX ??? Feedback ???
            raise HTTP.Redirect_302 (self.parent.abs_href)
        # end def _view

    # end class Deleter

    class _Inline_ (_Cmd_) :
        """Base class for children with need access to the inline."""

        SUPPORTED_METHODS = set (("GET", ))

        template          = "dynamic_form"

        def inline (self) :
            form   = self.Form (self.abs_href, None)
            prefix = self.forms [0]
            inline = \
                    [ig for ig in form.inline_groups if ig.prefix == prefix]
            if len (inline) == 1 :
                return inline [0]
        # end def inline

        def object (self, inline, pid) :
            form_cls = inline.form_cls
            try :
                return form_cls.et_man.pid_query (pid)
            except LookupError :
                request.Error = \
                    ( _T ("%s `%s` doesn't exist!")
                    % (_T (E_Type.ui_name), pid)
                    )
                raise HTTP.Error_404 (request.path, request.Error)
        # end def object

    # end class _Inline_

    class HTML_Form (_Inline_) :
        """Generate the html code for editing of an inline on request."""

        def rendered (self, handler, template = None) :
            inline = self.inline ()
            if inline :
                handler.context ["form"] = inline.prototype_form
                return self.__super.rendered (handler, template)
        # end def rendered

    # end class HTML_Form

    class Fields (_Inline_) :
        """Return the values of the form fields for an instance."""

        def rendered (self, handler, template = None) :
            request = handler.request
            inline = self.inline ()
            if inline :
                obj  = self.object (inline, request.req_data.get ("pid"))
                data = GTW.Form.MOM.Javascript.Completer.form_as_dict \
                    (inline.form_cls (obj))
                data ["ui_display"] = getattr (obj, "ui_display", u"")
                if request.req_data.get ("edit", u"1") == u"1":
                    title = _T ("Edit")
                else :
                    title = _T ("Copy")
                data ["puf_title"] = "%s %s" % (title, obj.ui_display)
                return handler.json (data)
        # end def rendered

    # end class Fields

    class Test (_Inline_) :
        """Return the values of the form fields for an instance."""

        SUPPORTED_METHODS = set (("POST", ))

        template_string   = """
        {%- import "html/rform.jnj" as RForm %}
        {%- if NEW_FORM -%}
          {{- GTW.render_fofi_widget
              (inline, "link_list_display_row", inline, iform, no, False)
          -}}
        {%- else -%}
          {{- GTW.render_fofi_widget
              (inline, "link_list_display",     inline, iform, no, False)
          -}}
        {%- endif -%}
        """

        def rendered (self, handler, template = None) :
            request  = handler.request
            inline   = self.inline ()
            if inline :
                req_data = request.req_data
                no       = req_data.get ("__FORM_NO__")
                try :
                    form   = inline.test (no, req_data)
                    if form.error_count () :
                        handler.context ["form"] = form
                        result = self.__super.rendered (handler, template)
                    else :
                        handler.context ["inline"]   = inline
                        handler.context ["iform"]    = form
                        handler.context ["no"]       = no
                        handler.context ["NEW_FORM"] = \
                            req_data.get ("__NEW__") == "true"
                        result = self.top.Templateer.render_string \
                            (self.template_string, handler.context).strip ()
                finally :
                    form.et_man.home_scope.rollback ()
                return result
        # end def rendered

    # end class Test

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

    def __init__ (self, parent, ** kw) :
        kw ["Form_Spec"] = dict \
            (args = kw.pop ("Form_args", ()), kw = kw.pop ("Form_kw", {}))
        kw ["_list_display"] = kw.pop ("list_display", None)
        self.__super.__init__ (parent, ** kw)
        self.prefix = pjoin (parent.prefix, self.name)
    # end def __init__

    @Once_Property
    def Form (self) :
        return GTW.Form.MOM.Instance.New \
           (self.ETM, * self.Form_Spec ["args"], ** self.Form_Spec ["kw"])
    # end def Form

    @Once_Property
    def manager (self) :
        return self.etype_manager (self.E_Type)
    # end def manager

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

    def href_delete (self, obj) :
        return pjoin (self.abs_href, "delete", str (obj.pid))
    # end def href_delete

    def href_display (self, obj) :
        man = self.manager
        if man :
            return man.href_display (obj)
    # end def href_display

    @property
    def h_title (self) :
        return u"::".join ((self.name, self.parent.h_title))
    # end def h_title

    @Once_Property
    def list_display (self) :
        if self._list_display is None :
            return self._auto_list_display (self.ETM)
        return tuple \
                (getattr (self.ETM._etype, a, a) for a in self._list_display)
    # end def list_display

    def rendered (self, handler, template = None) :
        objects = self._get_entries ()
        handler.context.update \
            ( fields  = self.list_display
            , objects = objects
            )
        return self.__super.rendered (handler, template)
    # end def rendered

    def _auto_list_display (self, E_Type) :
        return list (ichain (E_Type.primary, E_Type.user_attr))
    # end def _auto_list_display

    _child_name_map = dict \
        ( change    = (Changer,   "args")
        , complete  = (Completer, "forms")
        , completed = (Completed, "forms")
        , fields    = (Fields,    "forms")
        , form      = (HTML_Form, "forms")
        , test      = (Test,      "forms")
        )
    child_attrs     = {}

    def _get_child (self, child, * grandchildren) :
        T  = None
        kw = {}
        if child in self._child_name_map :
            T, attr = self._child_name_map [child]
            name    = pjoin (* grandchildren)
            kw      = \
                {"name"   : "%s/%s" % (child, name)
                , attr    : grandchildren
                }
        if child == "create" and not grandchildren :
            T = self.Changer
        if child == "delete" and len (grandchildren) == 1 :
            T = self.Deleter
            kw ["args"] = grandchildren
        if T :
            kw = dict (self.child_attrs.get (T.__name__, {}), ** kw)
            return T (parent = self, ** kw)
    # end def _get_child

# end class Admin

if __name__ != "__main__" :
    GTW.NAV.E_Type._Export ("*")
### __END__ GTW.NAV.E_Type.Admin
