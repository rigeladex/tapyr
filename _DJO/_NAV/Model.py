# -*- coding: iso-8859-1 -*-
# Copyright (C) 2008-2009 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
#++
# Name
#    DJO.NAV.Model
#
# Purpose
#    Navigation for django model instances
#
# Revision Dates
#    19-Oct-2008 (CT) Creation
#    19-Oct-2008 (CT) `Field` changed to re-evaluate `value` and `formatted`
#    20-Oct-2008 (CT) `Field.__init__` changed to cope with `field is None`
#    21-Oct-2008 (CT) `format_kw` added to `Field`
#    21-Oct-2008 (CT) `Changer.process_post` factored
#    21-Oct-2008 (CT) `Instance.changer` added
#     1-Dec-2008 (CT) Bug fixes (`Changer.rendered`: import
#                     HttpResponseRedirect, pass `request` to `process_post`)
#    16-Jan-2009 (CT) `kind_filter` added to `Admin` and `Manager`
#    16-Jan-2009 (CT) `disp_filter` added to `Manager`
#    23-Jan-2009 (CT) `kind_filter` based on `kind_name`
#    23-Jan-2009 (CT) `Manager.__init__` changed to consider `kind_name` for
#                     `name` and `title`
#    23-Jan-2009 (CT) `Admin.model_man` added and used
#    23-Jan-2009 (CT) Use `(Model, kind_name)` as index for `top.Models`
#    26-Feb-2009 (CT) `Changer.process_post` changed to call `_before_save`
#    27-Feb-2009 (CT) `count` changed to use `query_fct`
#    27-Feb-2009 (CT) `_Field` added and used in `kind_filter`
#    15-May-2009 (CT) `Admin.Changer.process_post` changed to return
#                     `result, form` instead of `form` to display validation
#                     errors
#    28-May-2009 (CT) s/_Field/_F/g
#    29-May-2009 (CT) Use `_F` instead of `_meta` to access fields
#    29-May-2009 (MG) Use new `DJO.Model_Form.New` in `_auto_form`
#     1-Jun-2009 (CT) Use `_F` instead of `_F.All`
#     2-Jun-2009 (MG) `_auto_form` changed to support form sets defined in
#                     the models
#     5-Jun-2009 (CT) `additional_context` factored from `Admin.rendered` and
#                     used in `Changer.rendered`, too
#    ««revision-date»»···
#--

from   __future__               import with_statement

from   _DJO                     import DJO
from   _TFL                     import TFL

import _DJO._NAV.Base
import _TFL._Meta.Object

from   _TFL._Meta.Once_Property import Once_Property
from   _TFL.predicate           import filtered_join

from   django.utils.translation import gettext as _

from   posixpath import join as pjoin, normpath as pnorm
import itertools

class Field (TFL.Meta.Object) :

    def __init__ (self, name, field, obj, format_kw = {}) :
        if field is None :
            field = obj._F [name]
        self.name      = name
        self.field     = field
        self.obj       = obj
        self.format_kw = dict (format_kw)
    # end def __init__

    @property
    def formatted (self) :
        try :
            f = self.field.as_string
        except AttributeError :
            if isinstance (self.value, unicode) :
                f = lambda x : x
            else :
                f = str
        value = self.value
        if value is None :
            value = ""
        return f (value, ** self.format_kw)
    # end def formatted

    @property
    def value (self) :
        return getattr (self.obj, self.name)
    # end def value

    def __nonzero__ (self) :
        return bool (self.value)
    # end def __nonzero__

    def __unicode__ (self) :
        return self.formatted ### XXX encoding
    # end def __unicode__

# end class Field

class _Model_Mixin_ (TFL.Meta.Object) :

    @property
    def count (self) :
        return self.query_fct ().count ()
    # end def count

    @Once_Property
    def Group (self) :
        name = getattr (self.Model, "NAV_admin_args", {}).get ("Group_Name")
        if name :
            from django.contrib.auth.models import Group
            return Group.objects.get (name = name)
    # end def Group

# end class _Model_Mixin_

class Admin (_Model_Mixin_, DJO.NAV.Page) :
    """Model an admin page for a specific Django model class."""

    Field           = Field
    has_children    = True
    kind_name       = None
    template        = "model_admin_list.html"

    class Changer (DJO.NAV._Site_Entity_) :

        implicit     = True
        name         = "create"
        obj_id       = None
        template     = "model_admin_change.html"

        def process_post (self, request, obj) :
            form   = self.Form (request.POST, instance = obj)
            result = None
            if form.is_valid () :
                with form.object_to_save () as result :
                    if hasattr (result, "_before_save") :
                        result._before_save \
                            (request, kind_name = self.kind_name)
                    if hasattr (result, "creator") and not result.creator :
                        if request.user.is_authenticated () :
                            result.creator = request.user
            return result, form
        # end def process_post

        def rendered (self, context, nav_page = None) :
            from django.http import HttpResponseRedirect
            request  = context ["request"]
            obj      = context ["instance"] = None
            obj_id   = self.obj_id
            if obj_id :
                try :
                    obj  = self.Model.objects.get (id = obj_id)
                except self.Model.DoesNotExist, exc :
                    from django.http import Http404
                    request.Error = \
                        ( "%s `%s` existiert nicht!"
                        % (self.Model._meta.verbose_name, obj_id)
                        )
                    raise Http404 (request.path)
            if request.method == "POST":
                result, form = self.process_post (request, obj)
                if result :
                    man = self.top.Models.get ((self.Model, self.kind_name))
                    if man :
                        man._old_count = -1
                    return HttpResponseRedirect \
                        ("%s#pk-%s" % (self.parent.abs_href, result.id))
            else :
                form = self.Form (instance = obj)
            context.update (self.parent.additional_context (form = form))
            return self.__super.rendered (context, nav_page)
        # end def rendered

    # end class Changer

    class Deleter (DJO.NAV._Site_Entity_) :

        implicit    = True
        name        = "delete"
        template    = "model_admin_delete.html"

        def _view (self, request) :
            from django.http import HttpResponseRedirect
            obj_id = self.obj_id
            try :
                obj  = self.Model.objects.get (id = obj_id)
            except self.Model.DoesNotExist, exc :
                from django.http import Http404
                request.Error = \
                    ( "%s `%s` doesn't exist!"
                    % (self.Model._meta.verbose_name, obj_id)
                    )
                raise Http404 (request.path)
            obj.delete ()
            ### XXX ??? Feedback ???
            return HttpResponseRedirect (self.parent.abs_href)
        # end def _view

    # end class Deleter

    class Instance (TFL.Meta.Object) :

        def __init__ (self, admin, obj) :
            self.admin = admin
            self.Model = admin.Model
            self.obj   = obj
        # end def __init__

        @Once_Property
        def fields (self) :
            admin = self.admin
            obj   = self.obj
            field = self.Model._F.get
            return [Field (f, field (f), obj) for f in admin.list_display]
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
            try :
                return getattr (self.obj, name)
            except AttributeError :
                return getattr (self.obj._meta, name)
        # end def __getattr__

        def __iter__ (self) :
            return iter (self.fields)
        # end def __iter__

    # end class Instance

    def __init__ (self, Model, ** kw) :
        if "Form" not in kw :
            kw ["Form"] = self._auto_form (Model, kw)
        if "list_display" not in kw :
            kw ["list_display"] = self._auto_list_display (Model, kw)
        k = kw.get ("kind_name")
        self.__super.__init__ (Model = Model, ** kw)
        self.prefix    = pjoin (self.parent.prefix, self.name)
        self.model_man = man = self.top.Models.get ((Model, k))
        if man and man.kind_filter :
            q = lambda : Model.objects.filter (man.kind_filter)
        else :
            q = Model.objects.all
        self.query_fct = q
    # end def __init__

    def additional_context (self, ** kw) :
        M = self.Model
        if self.model_man :
            name   = _(self.model_man.name)
            name_s = _(self.model_man.title)
        else :
            name   = M._meta.verbose_name
            name_s = M._meta.verbose_name_plural
        result     = dict \
            ( Meta         = M._meta
            , Model        = M
            , Model_Name   = name
            , Model_Name_s = name_s
            )
        result.update (kw)
        return result
    # end def additional_context

    @Once_Property
    def href (self) :
        return pjoin (self.prefix, u"")
    # end def href

    def href_create (self) :
        return pjoin (self.abs_href, "create")
    # end def href_create

    def href_change (self, obj) :
        return pjoin (self.abs_href, "change", str (obj.id))
    # end def href_change

    def href_delete (self, obj) :
        return pjoin (self.abs_href, "delete", str (obj.id))
    # end def href_delete

    def rendered (self, context = None, nav_page = None) :
        Instance = self.Instance
        field    = self.Model._F.get
        q        = self.query_fct
        if context is None :
            context = dict (page = self)
        context.update \
            ( self.additional_context
                ( fields  = [field (f) for f in self.list_display]
                , objects = [Instance (self, o) for o in q ()]
                )
            )
        return self.__super.rendered (context, nav_page)
    # end def rendered

    def _auto_list_display (self, Model, kw) :
        result = [f.name for f in Model._F if f.editable]
        return result
    # end def _auto_list_display

    def _auto_form (self, Model, kw) :
        import _DJO.Forms
        Form_Type             = kw.get ("Form", DJO.Model_Form)
        form_name             = "%s_Form" % Model.__name__
        form_dict             = dict ()
        form_set_descriptions = kw.get ("form_set_descriptions", ())
        if "_djo_clean" in kw :
            form_dict ["_djo_clean"] = kw ["_djo_clean"]
        return Form_Type.New (Model, * form_set_descriptions, ** form_dict)
    # end def _auto_form

    def _get_child (self, child, * grandchildren) :
        if child == "change" and len (grandchildren) == 1 :
            return self.Changer \
                ( parent = self
                , name   = "change/%s" % (grandchildren [0], )
                , obj_id = grandchildren [0]
                )
        if child == "create" and not grandchildren :
            return self.Changer (parent = self)
        if child == "delete" and len (grandchildren) == 1 :
            return self.Deleter (parent = self, obj_id = grandchildren [0])
    # end def _get_child

# end class Admin

class Instance (DJO.NAV.Page) :
    """Model a page showing on model instance"""

    def __init__ (self, obj, manager) :
        for f in "name", "slug" :
            name = getattr (obj, f, None)
            if name :
                break
        else :
            name = str (obj.id)
        self.__super.__init__ \
            ( manager = manager
            , name    = name
            , obj     = obj
            , parent  = manager
            )
        for k in itertools.chain (manager.attr_map, manager.fields) :
            setattr (self, k, self._get_field (k))
    # end def __init__

    @property
    def contents (self) :
        return self.obj.contents
    # end def contents

    @property
    def changer (self) :
        admin = self.manager.admin
        if admin :
            return admin._get_child ("change", self.obj.id)
    # end def changer

    @property
    def href_change (self) :
        admin = self.manager.admin
        if admin :
            return admin.href_change (self.obj)
    # end def href_change

    @property
    def href_delete (self) :
        admin = self.manager.admin
        if admin :
            return admin.href_delete (self.obj)
    # end def href

    def _get_field (self, name) :
        man = self.manager
        k   = man.attr_map.get (name, name)
        if k in man.fields :
            return Field (k, man.fields [k], self.obj)
        return "%s: `%s/%s` is not defined" % (self.Model.name, name, k)
    # end def _get_field

# end class Instance

class Manager (_Model_Mixin_, DJO.NAV.Dir) :
    """Model a directory showing one Django model"""

    Page            = Instance
    _admin          = None

    kind_name       = None
    disp_filter     = None

    def __init__ (self, src_dir, parent, ** kw) :
        Model  = kw.pop ("Model")
        kn     = unicode (kw.get ("kind_name"))
        assert (Model, kn) not in self.top.Models
        self.top.Models [(Model, kn)] = self
        Meta   = Model._meta
        kw     = dict    (getattr (Model, "NAV_manager_args", {}), ** kw)
        desc   = kw.pop  ("desc", Model.__doc__)
        name   = filtered_join ("-", (unicode (Meta.verbose_name), kn))
        title  = kw.pop  \
            ( "title"
            , filtered_join ("-", (unicode (Meta.verbose_name_plural), kn))
            )
        self.__super.__init__ \
            ( src_dir, parent
            , desc         = desc
            , fields       = dict ((f.name, f) for f in Model._F)
            , name         = name
            , Meta         = Meta
            , Model        = Model
            , Model_Name   = name
            , Model_Name_s = title
            , title        = title
            , _F           = Model._F
            , ** kw
            )
        self._old_count = -1
        qf = None
        if self.kind_filter :
            qf = self.kind_filter
            if self.disp_filter :
                qf = self.disp_filter | qf
        elif self.disp_filter :
            qf = self.disp_filter
        if qf :
            query_fct = lambda : Model.objects.filter (qf)
        else :
            query_fct = Model.objects.all
        self.query_fct = query_fct
    # end def __init__

    @property
    def admin (self) :
        if self._admin is None :
            Admin = self.top.Admin
            if Admin :
                self._admin = Admin._get_child (self.name)
        return self._admin
    # end def admin

    @property
    def href_create (self) :
        admin = self.admin
        if admin :
            return admin.href_create ()
    # end def href_change

    @Once_Property
    def kind_filter (self) :
        if self.kind_name :
            import _DJO.QF
            cind = self._F.kind.choice_to_code (self.kind_name)
            return DJO.QF (kind__exact = cind)
    # end def kind_filter

    def _get_entries (self) :
        count = self.count
        if self._old_count != count :
            ### XXX Doesn't catch changes to fields of objects
            self._objects   = self._get_objects ()
            self._old_count = count
        return self._objects
    # end def _get_entries

    _entries = property (_get_entries, lambda s, v : True)

    def _get_objects (self) :
        T = self.Page
        return [T (o, self) for o in self.query_fct ()]
    # end def _get_objects

# end class Manager

if __name__ != "__main__" :
    DJO.NAV._Export_Module ()
### __END__ DJO.NAV.Model
