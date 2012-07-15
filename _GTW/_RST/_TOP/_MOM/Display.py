# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
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
#    GTW.RST.TOP.MOM.Display
#
# Purpose
#    Display instances of MOM E-types
#
# Revision Dates
#    15-Jul-2012 (CT) Creation
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._RST._TOP._MOM.Mixin
import _GTW._RST._TOP.Dir
import _GTW._RST._TOP.Page

from   _TFL._Meta.Once_Property import Once_Property
from   _TFL.I18N                import _, _T, _Tn

import datetime

_Ancestor = GTW.RST.TOP.Page

class TOP_MOM_Entity (GTW.RST.TOP.MOM.Entity_Mixin, _Ancestor) :
    """Display page for one instance of a E_Type."""

    _real_name      = "Entity"

    @property
    def contents (self) :
        return self.obj.contents
    # end def contents

    @property
    def changer (self) :
        admin = self.admin
        if admin :
            return admin._get_child ("change", self.obj.pid)
    # end def changer

    def href_change (self) :
        admin = self.admin
        if admin :
            return admin.href_change (self.obj)
    # end def href_change

    def href_delete (self) :
        admin = self.admin
        if admin :
            return admin.href_delete (self.obj)
    # end def href

Entity = TOP_MOM_Entity # end class

_Ancestor = GTW.RST.TOP.Dir

class _TOP_MOM_E_Type_ (GTW.RST.TOP.MOM.E_Type_Mixin, _Ancestor) :
    """Directory displaying the instances of one E_Type."""

    _real_name      = "_E_Type_"

    Entity          = Entity

    disp_filter     = None

    _old_objects    = None

    @Once_Property
    def admin (self) :
        return self.top.ET_Map [self.type_name].admin
    # end def admin

    @property
    def entries (self) :
        objects = self.objects
        if self._old_objects is not objects :
            self._entry_map = {}
            self._entries   = []
            self.add_entries (* (self._new_entry (o) for o in objects))
            if self._admin :
                self.add_entries (self._admin)
            self._old_objects = objects
        return self._entries
    # end def entries

    @property
    def has_children (self) :
        return self.count > 0
    # end def has_children

    @Once_Property
    def query_filters (self) :
        result = list (self.__super.query_filters)
        if self.disp_filter is not None :
            result.append (self.disp_filter)
        return tuple (result)
    # end def query_filters

    def href_create (self) :
        admin = self.admin
        if admin :
            return admin.href_create ()
    # end def href_change

    def href_display (self, obj) :
        return pjoin \
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
        if self._admin :
            for t in self._admin.template_iter () :
                yield t
    # end def template_iter

    def _get_child_query (self, child) :
        n, result = self.ETM.query_1 (perma_name = child)
        if result is None :
            result = self.__super._get_child_query (child)
        return result
    # end def _get_child_query

    def _new_entry (self, instance, ** kw) :
        return self.__super._new_entry \
            (instance, ** dict (self.page_args, ** kw))
    # end def _new_entry

_E_Type_ = _TOP_MOM_E_Type_ # end class

class TOP_MOM_E_Type (_E_Type_) :
    """Directory displaying the instances of one E_Type."""

    _real_name      = "E_Type"

    admin_args      = {}
    sort_key        = TFL.Sorted_By ("-date.start", "perma_name")

    _admin          = None

    def __init__ (self, ** kw) :
        self.__super.__init__ (** kw)
        self.top.ET_Map [self.type_name].manager = self
        if self.admin_args :
            if "sort_key" in self.admin_args :
                self.sort_key = self.admin_args ["sort_key"]
            self._admin = self._admin_page (self.admin_args)
    # end def __init__

    def _admin_page (self, admin_args, parent = None) :
        m_kw = admin_args.copy ()
        if parent is None :
            parent = self
        if parent is self :
            short_title = _T ("Admin")
        else :
            short_title = m_kw.pop ("short_title", self.short_title)
        title = m_kw.pop \
            ( "title"
            , "%s: %s" % (self.title.rstrip ("."), _T ("Administration"))
            )
        ETM   = m_kw.pop ("ETM", self.ETM)
        Type  = m_kw.pop ("Type", GTW.RST.TOP.MOM.Admin.E_Type)
        return Type \
            ( parent      = parent
            , name        = self.name
            , short_title = short_title
            , title       = title
            , ETM         = ETM
            , ** m_kw
            )
    # end def _admin_page

E_Type = TOP_MOM_E_Type # end class

class _TOP_MOM_E_Type_Archive_ (E_Type) :
    """Directory displaying the instances of one E_Type organized by year."""

    _real_name      = "_E_Type_Archive_"

    _old_year       = None

    class Year (_E_Type_) :
        """Display instances of a specific year."""

        @Once_Property
        def query_filters (self) :
            return \
                ( (self.parent._year_filter (self.year), )
                + self.__super.query_filters
                )
        # end def query_filters

        def _get_child (self, child, * grandchildren) :
            result = self.__super._get_child (child, * grandchildren)
            if result is None and child == "index.html" and not grandchildren :
                return self
        # end def _get_child

    # end class Year

    @property
    def entries (self) :
        if self._old_year != self.year :
            self._entry_map = {}
            self._entries   = []
            self.add_entries \
                ( * ( self.Year
                        ( name       = str (y)
                        , parent     = self
                        , year       = y
                        )
                    for y in xrange
                        (self.year + 1, self.top.copyright_start - 1, -1)
                    )
                )
            if self._admin :
                self.add_entries (self._admin)
            self._old_year = self.year
        return self._entries
    # end def entries

    @property
    def year (self) :
        return datetime.date.today ().year
    # end def year

_E_Type_Archive_ = _TOP_MOM_E_Type_Archive_ # end class

class TOP_MOM_E_Type_Archive_DSY (_E_Type_Archive_) :
    """Directory displaying the instances of one E_Type organized by
       `date.start.year`.
    """

    _real_name = "E_Type_Archive_DSY"

    def _year_filter (self, y) :
        return (Q.date.start.D.YEAR (y), )
    # end def _year_filter

E_Type_Archive_DSY = TOP_MOM_E_Type_Archive_DSY # end class

class TOP_MOM_E_Type_Archive_Y (_E_Type_Archive_) :
    """Directory displaying the instances of one E_Type organized by `year`."""

    _real_name = "E_Type_Archive_Y"

    def href_display (self, obj) :
        return pjoin (self.abs_href, str (obj.year), obj.perma_name)
    # end def href_display

    def _year_filter (self, y) :
        return (Q.year == y, )
    # end def _year_filter

E_Type_Archive_Y = TOP_MOM_E_Type_Archive_Y # end class

if __name__ != "__main__" :
    GTW.RST.TOP.MOM._Export_Module ()
### __END__ GTW.RST.TOP.MOM.Display
