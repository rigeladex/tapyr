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

    class _Cmd_ (GTW.NAV.Page) :

        implicit          = True
        SUPPORTED_METHODS = set (("GET", "POST"))

    # end class _Cmd_

    class Changer (_Cmd_) :
        """Model an admin page for creating or changing a specific instance
           of a etype.
        """

        Media        = None ### cancel inherited property defined
        name         = "create"
        args         = (None, )
        template     = "e_type_change"

        def rendered (self, handler, template = None) :
            ETM      = self.ETM
            E_Type   = self.E_Type
            HTTP     = self.top.HTTP
            context  = handler.context
            obj      = context ["instance"] = None
            request  = handler.request
            req_data = request.req_data
            lid      = req_data.get ("lid") or self.args [0]
            if lid is not None :
                pid  = ETM.pid_from_lid (lid)
                try :
                    obj = ETM.pid_query (pid)
                except LookupError :
                    request.Error = \
                        ( _T ("%s `%s` doesn't exist!")
                        % (_T (E_Type.ui_name), lid)
                        )
                    raise HTTP.Error_404 (request.path, request.Error)
            form = self.Form \
                (self.abs_href, obj, cancel_href = self.parent.abs_href)
            if request.method == "POST" :
                err_count = form (req_data)
                if err_count == 0 :
                    man = self.parent.manager
                    if man :
                        man._old_cid = -1
                    tail = "#pk-%s" % (obj.lid) if obj else ""
                    raise HTTP.Redirect_302 \
                        ("%s%s" % (self.parent.abs_href, tail))
                else :
                    self._display_errors (form)
                    self.top.scope.rollback ()
            self.Media = self._get_media (head = getattr (form, "Media", None))
            context.update (form = form)
            return self.__super.rendered (handler, template)
        # end def rendered

        def _display_errors (self, form) :
            print form.prefix
            print form.errors, form.field_errors.items ()
            for ig in form.inline_groups :
                for f in ig.forms :
                    self._display_errors (f)
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
                form_cls = self.Form
                for sf in self.forms :
                    form_cls = getattr (form_cls, "sub_forms", {}).get (sf)
                if form_cls is not None :
                    args     = request.req_data
                    et_man   = form_cls.et_man
                    trigger  = getattr \
                        (et_man._etype, args.pop ("TRIGGER_FIELD"))
                    filter   = tuple \
                        (    getattr (Q, k).STARTSWITH (v)
                        for (k, v) in et_man.cooked_attrs (args).iteritems ()
                        )
                    print trigger
                    return handler.json \
                        ( [   dict
                                ( lid   = c.lid
                                , value = trigger.get_raw (c)
                                , label = c.ui_display
                                )
                          for c in et_man.query ().filter (* filter).distinct ()
                          ]
                        )
            if result is None :
                raise self.top.HTTP.Error_404 (request.path)
            return result
        # end def rendered

    # end class Completer

    class Completed (_Cmd_) :
        """Deliver fields for a model instance selected by completion."""

        Media        = None ### cancel inherited property defined

        def rendered (self, handler, template = None) :
            request = handler.request
            result  = None
            if request.method == "GET" :
                HTTP     = self.top.HTTP
                form_cls = self.Form
                for sf in self.forms :
                    form_cls = getattr (form_cls, "sub_forms", {}).get (sf)
                args = request.req_data
                lid  = args.get   ("lid")
                if not any (x is None for x in (form_cls, lid)) :
                    et_man   = form_cls.et_man
                    try :
                        obj  = et_man.pid_query (et_man.pid_from_lid (lid))
                    except IndexError, exc :
                        error = \
                            ( _T("%s `%s` existiert nicht!")
                            % (_T(comp_etm.ui_name), id)
                            )
                        raise self.top.HTTP.Error_404 (request.path, error)
                    form = form_cls (obj)
                    return HTTP.as_json \
                        (    (f, form.get_raw (f))
                        for f in ichain ( form_cls.completer.fields
                                        , ("_lid_a_state_", "instance_state")
                                        )
                        )
            if result is None :
                raise self.top.HTTP.Error_404 (request.path)
            return result
        # end def rendered

    # end class Completed

    class Deleter (_Cmd_) :
        """Model an admin page for deleting a specific instance of a etype."""

        name         = "delete"
        template     = "e_type_delete"

        def _view (self, request) :
            HTTP = self.top.HTTP
            lid  = self.args [0]
            ETM  = self.ETM
            pid  = ETM.pid_from_lid (lid)
            try :
                obj = ETM.pid_query (pid)
            except LookupError :
                request.Error = \
                    (_T ("%s `%s` doesn't exist!") % (_T (E_Type.ui_name), lid))
                raise HTTP.Error_404 (request.path, request.Error)
            obj.destroy ()
            ### XXX ??? Feedback ???
            raise HTTP.Redirect_302 (self.parent.abs_href)
        # end def _view

    # end class Deleter

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
        ETM = kw ["ETM"]
        if isinstance (ETM, basestring) :
            ETM = kw ["ETM"] = parent.scope [ETM]
        if "Form" not in kw :
            kw ["Form"] = GTW.Form.MOM.Instance.New \
                (ETM, * kw.pop ("Form_args", ()), ** kw.pop ("Form_kw", {}))
        if "list_display" not in kw :
            kw ["list_display"] = self._auto_list_display (ETM, kw)
        else :
            kw ["list_display"] = tuple \
                (getattr (ETM._etype, a, a) for a in kw ["list_display"])
        self.__super.__init__ (parent, ** kw)
        self.prefix = pjoin (self.parent.prefix, self.name)
    # end def __init__

    @Once_Property
    def manager (self) :
        return self.top.E_Types.get ((self.E_Type.type_name, self.kind_name))
    # end def manager

    @Once_Property
    def href (self) :
        return pjoin (self.prefix, u"")
    # end def href

    def href_create (self) :
        return pjoin (self.abs_href, "create")
    # end def href_create

    def href_change (self, obj) :
        return pjoin (self.abs_href, "change", obj.lid)
    # end def href_change

    def href_delete (self, obj) :
        return pjoin (self.abs_href, "delete", obj.lid)
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

    def rendered (self, handler, template = None) :
        objects = self._get_entries ()
        handler.context.update \
            ( fields  = self.list_display
            , objects = objects
            )
        return self.__super.rendered (handler, template)
    # end def rendered

    def _auto_list_display (self, E_Type, kw) :
        return list (ichain (E_Type.primary, E_Type.user_attr))
    # end def _auto_list_display

    _child_name_map = dict \
        ( change    = (Changer,   "args")
        , complete  = (Completer, "forms")
        , completed = (Completed, "forms")
        )

    def _get_child (self, child, * grandchildren) :
        if child in self._child_name_map :
            T, attr = self._child_name_map [child]
            name    = pjoin (* grandchildren)
            return T \
                ( parent = self
                , name   = "%s/%s" % (child, name)
                , ** {attr : grandchildren}
                )
        if child == "create" and not grandchildren :
            return self.Changer (parent = self)
        if child == "delete" and len (grandchildren) == 1 :
            return self.Deleter (parent = self, args = grandchildren)
    # end def _get_child

# end class Admin

if __name__ != "__main__" :
    GTW.NAV.E_Type._Export ("*")
### __END__ GTW.NAV.E_Type.Admin
