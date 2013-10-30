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
#    GTW.RST.TOP.MOM.Mixin
#
# Purpose
#    Define mixin classes for GTW.RST.TOP.MOM
#
# Revision Dates
#    15-Jul-2012 (CT) Creation
#    18-Jul-2012 (CT) Factor `Entity_Mixin_Base`, `E_Type_Mixin_Base`
#    18-Jul-2012 (CT) Factor from `Display._E_Type_` to `E_Type_Mixin`
#    23-Jul-2012 (CT) Remove `has_children`
#    30-Jul-2012 (CT) Redefine `E_Type_Mixin_Base.QR`
#     7-Aug-2012 (CT) Change `GTW.RST.MOM.RST_` to `GTW.RST.MOM.`
#     7-Aug-2012 (CT) Fix typo (`.admin`, not `._admin`)
#     9-Nov-2012 (CT) Redefine `E_Type_Mixin._get_child_page`
#     7-Dec-2012 (CT) Rename `query_filters` to `query_filters_d`
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._RST._MOM.Mixin
import _GTW._RST._TOP._MOM.Query_Restriction

from   _MOM.import_MOM          import Q

from   _TFL._Meta.Once_Property import Once_Property
from   _TFL.Decorator           import getattr_safe
from   _TFL.I18N                import _, _T, _Tn

import _TFL.Ascii
import _TFL.Attr_Mapper

from   posixpath                import join as pp_join

class TOP_MOM_Entity_Mixin_Base (GTW.RST.MOM.Entity_Mixin) :
    """Base mixin for RST.TOP classes displaying MOM instances."""

    _real_name      = "Entity_Mixin_Base"

    attr_mapper     = TFL.Attr_Mapper ()

    _exclude_robots = False

    def __init__ (self, ** kw) :
        obj = kw ["obj"]
        if "name" not in kw :
            name = unicode (getattr (obj, "perma_name", None))
            if name is None :
                name = getattr (obj, "name", obj.pid)
            kw ["name"] = TFL.Ascii.sanitized_filename (name)
        self.__super.__init__ (** kw)
        ### Get `short_title` and `title` from `obj`
        if "short_title" not in kw :
            self.short_title = self.__getattr__ ("short_title")
        if "title" not in kw :
            self.title       = self.__getattr__ ("title")
    # end def __init__

    @Once_Property
    @getattr_safe
    def FO (self) :
        return GTW.FO (self.obj, self.top.encoding)
    # end def FO

    def __getattr__ (self, name) :
        if self.attr_mapper :
            try :
                return self.attr_mapper (self.obj.FO, name)
            except AttributeError :
                pass
        return self.__super.__getattr__  (name)
    # end def __getattr__

Entity_Mixin_Base = TOP_MOM_Entity_Mixin_Base # end class

class TOP_MOM_Entity_Mixin (Entity_Mixin_Base) :
    """Mixin for RST.TOP classes displaying MOM instances."""

    _real_name      = "Entity_Mixin"

    def __init__ (self, ** kw) :
        obj = kw ["obj"]
        kw.setdefault ("manager", self.parent)
        kw.setdefault ("hidden",  getattr (obj, "hidden", False))
        self.__super.__init__ (** kw)
    # end def __init__

    @Once_Property
    @getattr_safe
    def E_Type (self) :
        return self.obj.__class__
    # end def E_Type

    @property
    @getattr_safe
    def admin (self) :
        return self.manager.admin
    # end def admin

    @Once_Property
    @getattr_safe
    def permalink (self) :
        return self.manager.href_display (self.obj)
    # end def permalink

Entity_Mixin = TOP_MOM_Entity_Mixin # end class

class TOP_MOM_E_Type_Mixin_Base (GTW.RST.MOM.E_Type_Mixin) :

    _real_name      = "E_Type_Mixin_Base"

    QR              = GTW.RST.TOP.MOM.Query_Restriction

    attr_mapper     = None
    page_args       = {}

    _exclude_robots = False

    def __init__ (self, ** kw) :
        ### Set `self.top` early because it's needed before initialized properly
        self.top = self.parent.top
        self.pop_to_self (kw, "ETM", prefix = "_")
        E_Type      = self.E_Type
        name        = kw.pop  ("name", E_Type.ui_name)
        title       = kw.pop  ("title", _T (E_Type.__doc__))
        a           = "a" ### Fool Babel extract
        short_title = kw.pop  \
            ( "short_title"
            , _T (name.capitalize () if name [0] >= a else name)
            )
        self.__super.__init__ \
            ( name          = TFL.Ascii.sanitized_filename (unicode (name))
            , short_title   = short_title
            , title         = title
            , ** kw
            )
    # end def __init__

    def __getattr__ (self, name) :
        if self.attr_mapper :
            try :
                return self.attr_mapper (self.obj, name)
            except AttributeError :
                pass
        return self.__super.__getattr__  (name)
    # end def __getattr__

E_Type_Mixin_Base = TOP_MOM_E_Type_Mixin_Base # end class

class TOP_MOM_E_Type_Mixin (E_Type_Mixin_Base) :

    _real_name      = "E_Type_Mixin"

    disp_filter     = None

    _old_objects    = None

    @Once_Property
    @getattr_safe
    def admin (self) :
        return self.top.ET_Map [self.type_name].admin
    # end def admin

    @property
    @getattr_safe
    def entries (self) :
        objects = self.objects
        if self._old_objects is not objects :
            self._entry_map = {}
            self._entries   = []
            entries         = tuple (self._new_entry (o) for o in objects)
            self.add_entries (* entries)
            admin = self.admin
            if admin and admin is not self :
                self.add_entries (admin)
            if objects :
                self._old_objects = objects
        return self._entries
    # end def entries

    @property
    @getattr_safe
    def query_filters_d (self) :
        result = list (self.__super.query_filters_d)
        if self.disp_filter is not None :
            result.append (self.disp_filter)
        return tuple (result)
    # end def query_filters_d

    def href_create (self) :
        admin = self.admin
        if admin :
            return admin.href_create ()
    # end def href_create

    def href_display (self, obj) :
        return pp_join \
            (self.abs_href, getattr (obj, "perma_name", str (obj.pid)))
    # end def href_display

    def page_from_obj (self, obj) :
        href   = self.href_display  (obj)
        result = self.top.Table.get (href.strip ("/"))
        if result is None :
            result = self._new_entry (obj)
        return result
    # end def page_from_obj

    def template_iter (self) :
        for t in self.__super.template_iter () :
            yield t
        if self.admin :
            for t in self.admin.template_iter () :
                yield t
    # end def template_iter

    def _get_child_page (self, obj) :
        return self.page_from_obj (obj)
    # end def _get_child_page

    def _get_child_query (self, child) :
        try :
            n, result = self.ETM.query_1 \
                (perma_name = child, * self.query_filters)
        except Exception :
            result = None
        if result is None :
            result = self.__super._get_child_query (child)
        return result
    # end def _get_child_query

    def _new_entry (self, instance, ** kw) :
        kw.setdefault ("ETM", instance.ETM)
        return self.__super._new_entry \
            (instance, ** dict (self.page_args, ** kw))
    # end def _new_entry

E_Type_Mixin = TOP_MOM_E_Type_Mixin # end class

if __name__ != "__main__" :
    GTW.RST.TOP.MOM._Export ("*")
### __END__ GTW.RST.TOP.MOM.Mixin
