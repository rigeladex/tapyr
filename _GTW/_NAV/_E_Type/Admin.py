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
#    ««revision-date»»···
#--

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._Form._MOM.Instance

import _GTW._NAV.Base
import _GTW._NAV._E_Type._Mgr_Base_

import _GTW._Tornado.Request_Data

import _TFL._Meta.Object
from   _TFL._Meta.Once_Property import Once_Property

from   _TFL.I18N                import _, _T, _Tn

from   itertools                import chain as ichain
from   posixpath                import join  as pjoin

class Admin (GTW.NAV.E_Type._Mgr_Base_, GTW.NAV.Page) :
    """Navigation page for managing the instances of a specific E_Type."""

    std_template    = "e_type_admin"

    class Changer (GTW.NAV._Site_Entity_) :
        """Model an admin page for creating or changing a specific instance
           of a etype.
        """

        implicit     = True
        Media        = None ### cancel inherited property defined
        name         = "create"
        lid          = None
        std_template = "e_type_change"

        def rendered (self, handler, template = None) :
            ETM      = self.ETM
            E_Type   = self.E_Type
            HTTP     = self.top.HTTP
            context  = handler.context
            obj      = context ["instance"] = None
            request  = handler.request
            req_data = GTW.Tornado.Request_Data (request.arguments)
            lid      = req_data.get ("lid") or self.lid
            if lid :
                pid  = ETM.pid_from_lid (lid)
                try :
                    obj = ETM.pid_query (pid)
                except LookupError :
                    request.Error = \
                        ( _T ("%s `%s` doesn't exist!")
                        % (_T (E_Type.ui_name), lid)
                        )
                    raise HTTP.Error_404 (request.path, request.Error)
            form = self.Form (self.abs_href, obj)
            if request.method == "POST" :
                err_count = form (req_data)
                if err_count == 0 :
                    man = self.parent.manager
                    if man :
                        man._old_cid = -1
                    raise HTTP.Redirect_302 \
                        ("%s#pk-%s" % (self.parent.abs_href, result.lid))
            self.Media = self._get_media (head = getattr (form, "Media", None))
            context.update (form = form)
            return self.__super.rendered (handler, template)
        # end def rendered

    # end class Changer

    class Completer (GTW.NAV._Site_Entity_) :
        """Deliver completion information for a AJAX request."""

        implicit     = True
        Media        = None ### cancel inherited property defined

        def rendered (self, handler, template = None) :
            context = handler.context
            request = handler.request
            result  = None
            if request.method == "GET" :
                ### XXX
                bnfg = self.Form.unbound_form_map.get (self.field_name)
                if bnfg is not None :
                    relm = bnfg.related_model
                    qfs  = tuple \
                        (   DJO.QF (** {"%s__startswith" % str (k) : str (v)})
                        for (k, v) in request.GET.iteritems ()
                        )
                    context ["completions"] = \
                        sorted (relm.objects.filter (* qfs).distinct ())
                    result = self.__super.rendered \
                        (handler, bnfg.completer.template)
            if result is None :
                raise self.top.HTTP.Error_404 (request.path)
            return result
        # end def rendered

    # end class Completer

    class Completed (GTW.NAV._Site_Entity_) :
        """Deliver fields for a model instance selected by completion."""

        implicit     = True
        Media        = None ### cancel inherited property defined

        def rendered (self, handler, template = None) :
            import json ### part of python2.6+
            request = handler.request
            result  = None
            if request.method == "GET" :
                ### XXX
                bnfg = self.Form.unbound_form_map.get (self.field_name)
                id   = request.GET.get   ("id")
                no   = request.GET.get   ("no")
                if not any (x is None for x in (bnfg, id, no)) :
                    relm = bnfg.related_model
                    try :
                        obj  = relm.objects.get (id = id)
                    except relm.DoesNotExist, exc :
                        request.Error = \
                            ( "%s `%s` existiert nicht!"
                            % (relm._meta.verbose_name, id)
                            )
                        raise self.top.HTTP.Error_404 \
                            (request.path, request.Error)
                    form_class = bnfg.form_class \
                        ( request  = None
                        , instance = obj
                        , prefix   = "%s-M%s" % (bnfg.Name, no)
                        )
                    ### this works well for the tornado backed
                    return dict ((f.name, str (f)) for f in form_class)
            if result is None :
                raise self.top.HTTP.Error_404 (request.path)
            return result
        # end def rendered

    # end class Completed

    class Deleter (GTW.NAV._Site_Entity_) :
        """Model an admin page for deleting a specific instance of a etype."""

        implicit     = True
        name         = "delete"
        std_template = "e_type_delete"

        def _view (self, request) :
            HTTP = self.top.HTTP
            lid  = self.lid
            pid  = ETM.pid_from_lid (lid)
            try :
                obj = self.ETM.pid_query (pid)
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
            self.FO    = GTW.FO (obj, self.top.encoding)
        # end def __init__

        @Once_Property
        def fields (self) :
            admin = self.admin
            FO    = self.FO
            return [(f, getattr (FO, f.name)) for f in admin.list_display]
        # end def fields

        @Once_Property
        def href_change (self) :
            return self.admin.href_change (self.obj)
        # end def href_change

        @Once_Property
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

    def __init__ (self, ETM, ** kw) :
        if "Form" not in kw :
            kw ["Form"] = GTW.Form.MOM.Instance.New (ETM._etype)
        if "list_display" not in kw :
            kw ["list_display"] = self._auto_list_display (ETM, kw)
        self.__super.__init__ (ETM = ETM, ** kw)
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
        handler.context.update \
            ( fields  = self.list_display
            , objects = self._entries
            )
        return self.__super.rendered (handler, template)
    # end def rendered

    def _auto_list_display (self, E_Type, kw) :
        return list (ichain (E_Type.primary, E_Type.user_attr))
    # end def _auto_list_display

    _child_name_map = dict \
        ( change    = (Changer,   "lid")
        , complete  = (Completer, "field_name")
        , completed = (Completed, "field_name")
        )

    def _get_child (self, child, * grandchildren) :
        if child in self._child_name_map :
            T, attr = self._child_name_map [child]
            return T \
                ( parent = self
                , name   = "%s/%s" % (child, grandchildren [0])
                , ** {attr : grandchildren [0]}
                )
        if child == "create" and not grandchildren :
            return self.Changer (parent = self)
        if child == "delete" and len (grandchildren) == 1 :
            return self.Deleter (parent = self, lid = grandchildren [0])
    # end def _get_child

# end class Admin

if __name__ != "__main__" :
    GTW.NAV.E_Type._Export ("*")
### __END__ GTW.NAV.E_Type.Admin
