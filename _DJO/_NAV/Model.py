# -*- coding: iso-8859-1 -*-
# Copyright (C) 2008 Mag. Christian Tanzer. All rights reserved
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
#    ««revision-date»»···
#--

from   __future__               import with_statement

from   _DJO                     import DJO
from   _TFL                     import TFL

import _DJO._NAV.Base
import _TFL._Meta.Object

from   _TFL._Meta.Once_Property import Once_Property

from   posixpath import join as pjoin, normpath as pnorm
import itertools

class Field (TFL.Meta.Object) :

    def __init__ (self, name, field, obj) :
        if field is None :
            field = obj.__class__._meta.get_field (name)
        self.name     = name
        self.field    = field
        self.obj      = obj
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
        return f (value)
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
        return self.Model.objects.count ()
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
    template        = "model_admin_list.html"

    class Changer (DJO.NAV._Site_Entity_) :

        implicit     = True
        name         = "create"
        obj_id       = None
        template     = "model_admin_change.html"

        def rendered (self, context, nav_page = None) :
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
                form = self.Form (request.POST, instance = obj)
                if form.is_valid () :
                    from django.http import HttpResponseRedirect
                    with form.object_to_save () as result :
                        if hasattr (result, "creator") and not result.creator :
                            if request.user.is_authenticated () :
                                result.creator = request.user
                    man = self.top.Models.get (self.Model)
                    if man :
                        man._old_count = -1
                    return HttpResponseRedirect \
                        ("%s#pk-%s" % (self.parent.abs_href, result.id))
            else :
                form = self.Form (instance = obj)
            context ["form"] = form
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
            field = self.Model._meta.get_field
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
        if not kw.get ("list_display") :
            kw ["list_display"] = self._auto_list_display (Model, kw)
        self.__super.__init__ (Model = Model, ** kw)
        self.prefix = pjoin (self.parent.prefix, self.name)
    # end def __init__

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
        M        = self.Model
        Instance = self.Instance
        field    = M._meta.get_field
        if context is None :
            context = dict (page = self)
        context.update \
            ( dict
                ( fields       =
                    [field (f) for f in self.list_display]
                , objects      =
                    [Instance (self, o) for o in self.Model.objects.all ()]
                , Meta         = M._meta
                , Model        = M
                , Model_Name   = M._meta.verbose_name
                , Model_Name_s = M._meta.verbose_name_plural
                )
            )
        return self.__super.rendered (context, nav_page)
    # end def rendered

    def _auto_list_display (self, Model, kw) :
        result = [f.name for f in Model._meta.fields if f.editable]
        return result
    # end def _auto_list_display

    def _auto_form (self, Model, kw) :
        import _DJO.Forms
        Form_Type = kw.get ("Form", DJO.Model_Form)
        form_name = "%s_Form" % Model.__name__
        form_dict = dict \
            ( Meta = type
                ( "Meta", (object, )
                , dict
                    ( exclude = kw.get ("exclude")
                    , fields  = kw.get ("fields")
                    , model   = Model
                    )
                )
            )
        if "_djo_clean" in kw :
            form_dict ["_djo_clean"] = kw ["_djo_clean"]
        result = Form_Type.__class__ (form_name, (Form_Type, ), form_dict)
        return result
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

    Page       = Instance
    _admin     = None

    def __init__ (self, src_dir, parent, ** kw) :
        Model  = kw.pop ("Model")
        assert Model not in self.top.Models
        self.top.Models [Model] = self
        Meta   = Model._meta
        kw     = dict    (getattr (Model, "NAV_manager_args", {}), ** kw)
        desc   = kw.pop  ("desc", Model.__doc__)
        name   = unicode (Meta.verbose_name)
        title  = kw.pop  ("title", Meta.verbose_name_plural)
        self.__super.__init__ \
            ( src_dir, parent
            , desc         = desc
            , fields       = dict \
                ((f.name, Meta.get_field (f.name)) for f in Meta.fields)
            , name         = name
            , Meta         = Meta
            , Model        = Model
            , Model_Name   = Meta.verbose_name
            , Model_Name_s = Meta.verbose_name_plural
            , title        = title
            , ** kw
            )
        self._old_count = -1
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
        return [T (o, self) for o in self.Model.objects.all ()]
    # end def _get_objects

# end class Manager

if __name__ != "__main__" :
    DJO.NAV._Export_Module ()
### __END__ DJO.NAV.Model
