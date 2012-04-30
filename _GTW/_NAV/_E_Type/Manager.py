# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2012 Mag. Christian Tanzer All rights reserved
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
#    GTW.NAV.E_Type.Manager
#
# Purpose
#    Navigation directory listing the instances of one E_Type
#
# Revision Dates
#    19-Jan-2010 (CT) Creation (ported from DJO.NAV.Model.Manager)
#    20-Jan-2010 (CT) `_Mgr_Base_` factored
#     5-Mar-2010 (CT) `Manager.__init__` corrected
#     5-Mar-2010 (CT) `attr_mapper` and `__getattr__` using it added
#    15-Mar-2010 (CT) `kind_filter` and `kind_name` removed
#    17-Mar-2010 (CT) `_get_child` added
#    18-Mar-2010 (CT) `page_from_obj` added (and used in `_get_child`)
#    18-Mar-2010 (CT) `has_children` added
#    18-Mar-2010 (CT) `Manager_T` begun
#    19-Mar-2010 (CT) `Manager_T_Archive` added
#    23-Mar-2010 (CT) Handling of `sort_key` fixed
#    23-Mar-2010 (CT) `_get_child` rewritten to allow `grandchildren` if
#                     `Page.allows_children`
#     9-Apr-2010 (CT) `Manager_T_Archive._year_filter` factored
#     9-Apr-2010 (CT) `Manager_T_Archive_Y` added
#    12-Apr-2010 (CT) `href_display` changed to use`perma_name` instead of `lid`
#    29-Apr-2010 (CT) `Manager_T_Archive._get_objects` changed to use
#                     `top.copyright_start` instead of `cy - 5` as cutoff
#    29-Apr-2010 (CT) `Manager_T_Archive_Y.href_display` redefined
#    30-Apr-2010 (CT) `_get_objects` changed to pass `page_args` on to each
#                     `Page`
#    30-Apr-2010 (CT) `_get_child` added to `Manager_T` and `Manager_T_Archive`
#    30-Apr-2010 (CT) `_get_grandchild` added to `Manager_T_Archive_Y`
#     5-May-2010 (CT) `Manager_T_Archive._get_objects` changed to not create
#                     empty `Year` instances
#     7-May-2010 (CT) `Manager_T_Archive.Year._get_child` added and used
#     7-May-2010 (CT) `Manager_T_Archive._get_objects` corrected (`manager`
#                     vs. `parent` for `Y._entries`)
#    12-May-2010 (CT) Use `pid`, not `lid`
#    14-Dec-2010 (CT) `Manager_T_Archive._year_filter` changed to use
#                     `Q.date.start.D.YEAR` instead of home-grown code
#    22-Dec-2010 (CT) `top.E_Types` replaced by `ET_Map`
#    22-Dec-2010 (CT) `_admin` added and used
#     9-Apr-2011 (MG) `Manager.href_display` use getattr for `perma_name`
#                     `Link_Manager` started
#    11-May-2011 (MG) `Link_Manager` continued
#    18-Jul-2011 (CT) Use `query_1` instead of home-grown code
#    14-Nov-2011 (CT) Use `__super.query` instead of home-grown code
#     2-Feb-2012 (CT) Robustify `_get_child` (`Manager`, `Manager_T_Archive`)
#    26-Apr-2012 (CT) Redefine `Manager.template_iter` to also yield
#                     `._admin...`
#    ««revision-date»»···
#--

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._NAV.Base
import _GTW._NAV._E_Type._Mgr_Base_
import _GTW._NAV._E_Type.Instance

from   _MOM.import_MOM          import Q

from   _TFL._Meta.Once_Property import Once_Property
from   _TFL.I18N                import _, _T, _Tn
from   _TFL.predicate           import first

from   posixpath                import join  as pjoin

import datetime

class Manager (GTW.NAV.E_Type._Mgr_Base_, GTW.NAV.Dir) :
    """Navigation directory listing the instances of one E_Type."""

    Page            = GTW.NAV.E_Type.Instance

    admin_args      = {}
    attr_mapper     = None
    disp_filter     = None
    sort_key        = TFL.Sorted_By ("-date.start", "perma_name")

    _admin          = None

    def __init__ (self, src_dir, ** kw) :
        self.__super.__init__ (src_dir = src_dir, ** kw)
        if "sort_key" in self.admin_args :
            self.sort_key = self.admin_args ["sort_key"]
        self.top.ET_Map [self.type_name].manager = self
        if self.admin_args :
            self._admin = self._admin_page (self.admin_args)
    # end def __init__

    @Once_Property
    def admin (self) :
        return self.top.ET_Map [self.type_name].admin
    # end def admin

    @property
    def has_children (self) :
        return self.count > 0
    # end def has_children

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
        result = self.top.Table.get (href)
        if result is None :
            result = self.Page (self, obj, ** self.page_args)
        return result
    # end def page_from_obj

    @Once_Property
    def query_filters (self) :
        result = list (self.__super.query_filters)
        if self.disp_filter is not None :
            result.append (self.disp_filter)
        return tuple (result)
    # end def query_filters

    def template_iter (self) :
        for t in self.__super.template_iter () :
            yield t
        if self._admin :
            for t in self._admin.template_iter () :
                yield t
    # end def template_iter

    @Once_Property
    def type_name (self) :
        return self.E_Type.type_name
    # end def type_name

    def _admin_page (self, admin_args, parent = None) :
        m_kw = admin_args.copy ()
        if parent is None :
            parent = self
        if parent is self :
            short_title = _T ("Admin")
        else :
            short_title = m_kw.pop ("short_title", self.short_title)
        title = m_kw.pop ("title", "%s: Verwaltung" % (self.title.rstrip (".")))
        ETM   = m_kw.pop ("ETM", self._ETM)
        Type  = m_kw.pop ("Type", GTW.NAV.E_Type.Admin)
        return Type \
            ( parent      = parent
            , name        = self.name
            , short_title = short_title
            , title       = title
            , ETM         = ETM
            , ** m_kw
            )
    # end def _admin_page

    def _get_child (self, child, * grandchildren) :
        result = None
        n, obj = self.ETM.query_1 (perma_name = child)
        if obj is None :
            try :
                obj = self.ETM.pid_query (child)
            except (LookupError, ValueError) :
                pass
        if obj is not None :
            result = self.page_from_obj (obj)
            if grandchildren :
                if self.Page.allows_children :
                    result = result._get_child (* grandchildren)
                else :
                    result = None
        if result is None :
            return self.__super._get_child (child, * grandchildren)
        return result
    # end def _get_child

    def _get_entries (self) :
        result = self.__super._get_entries ()
        if self._admin :
            result = result + [self._admin]
        return result
    # end def _get_entries

    def __getattr__ (self, name) :
        if self.attr_mapper :
            try :
                return self.attr_mapper (self.obj, name)
            except AttributeError :
                pass
        return self.__super.__getattr__  (name)
    # end def __getattr__

# end class Manager

class Manager_T (Manager) :
    """Navigation directory listing the recent instances of one E_Type, plus
       an archive.
    """

    archive_name      = "Archive"
    query_limit       = 7

    def query (self) :
        result = self.__super.query ()
        if self.query_limit :
            result = result.limit (self.query_limit)
        return result
    # end def query

    @Once_Property
    def query_filters (self) :
        result = list (self.__super.query_filters)
        result.append (Q.date.alive)
        return tuple  (result)
    # end def query_filters

    def _get_child (self, child, * grandchildren) :
        if child == self.archive_name :
            archive = self._entries [-1]
            if not grandchildren :
                return archive
            else :
                return archive._get_child (* grandchildren)
        return self.__super._get_child (child, * grandchildren)
    # end def _get_child

    def _get_objects (self) :
        T      = self.Page
        kw     = self.page_args
        name   = self.archive_name
        result = [T (self, o, ** kw) for o in self.query ()]
        arch   = Manager_T_Archive \
            ( ETM       = self.ETM
            , name        = name
            , Page        = T
            , page_args   = kw
            , parent      = self
            , sort_key    = self.sort_key
            , src_dir     = pjoin (self.src_dir, name)
            , sub_dir     = name
            , short_title = name
            )
        result.append (arch)
        return result
    # end def _get_objects

# end class Manager_T

class Manager_T_Archive (Manager) :

    class _Cmd_ (GTW.NAV.Dir) :
        pass
    # end class _Cmd_

    class Year (_Cmd_) :

        def _get_child (self, child, * grandchildren) :
            try :
                result = first \
                    (e for e in self._entries if e.perma_name == child)
            except IndexError :
                if child == "index.html" and not grandchildren :
                    return self
            else :
                if grandchildren :
                    result = result._get_child (* grandchildren)
                return result
        # end def _get_child

    # end class Year

    def _get_child (self, child, * grandchildren) :
        try :
            y = int (child)
        except ValueError :
            pass
        else :
            entries = self._entries
            try :
                year = first (e for e in entries if e.year == y)
            except (IndexError, AttributeError) :
                pass
            else :
                if not grandchildren :
                    return year
                else :
                    result = year._get_child (* grandchildren)
                    if result is not None :
                        return result
        return self.__super._get_child (child, * grandchildren)
    # end def _get_child

    def _get_grandchild (self, y, grandchildren) :
        if len (grandchildren) == 1 :
            gc = grandchildren [0]
            n, obj = self.ETM.query_1 (perma_name = gc)
            if obj is not None :
                return self.page_from_obj (obj)
    # end def _get_grandchild

    def _get_objects (self) :
        T      = self.Page
        pkw    = self.page_args
        kw     = dict (pkw)
        qr     = self.ETM.query (sort_key = self.sort_key)
        cy     = datetime.date.today ().year + 1
        result = []
        for y in xrange (cy, self.top.copyright_start - 1, -1) :
            os = qr.filter (* self._year_filter (y)).all ()
            if os :
                name = str (y)
                Y    = kw ["parent"] = self.Year \
                    ( src_dir     = pjoin (self.src_dir, name)
                    , parent      = self
                    , year        = y
                    , name        = name
                    , sub_dir     = name
                    , short_title = name
                    )
                Y._entries = [T (self, o, page_args = pkw, ** kw) for o in os]
                result.append (Y)
        return result
    # end def _get_objects

    def _year_filter (self, y) :
        return (Q.date.start.D.YEAR (y), )
    # end def _year_filter

# end class Manager_T_Archive

class Manager_T_Archive_Y (Manager_T_Archive) :

    def href_display (self, obj) :
        return pjoin (self.abs_href, str (obj.year), obj.perma_name)
    # end def href_display

    def _get_grandchild (self, y, grandchildren) :
        if len (grandchildren) == 1 :
            gc = grandchildren [0]
            n, obj = self.ETM.query_1 (year = y, perma_name = gc)
            if obj is not None :
                return self.page_from_obj (obj)
    # end def _get_grandchild

    def _year_filter (self, y) :
        return (Q.year == y, )
    # end def _year_filter

# end class Manager_T_Archive_Y

import _TFL.Caller

class Link_Manager (Manager) :
    """Display the links associated with the passed object"""

    allows_children = True

    def __init__ (self, parent, obj, ** kw) :
        scope = TFL.Caller.Object_Scope (obj)
        for attr, default in ( ("title",       "%(ui_display)s")
                             , ("short_title", "%(ui_display)s")
                             ) :
            value = kw.pop (attr, default)
            if isinstance (value, basestring) :
                value = value % scope
            kw [attr] = value
        self.obj  = obj
        self.role = kw.pop ("role")
        self.__super.__init__ \
            ( obj.type_base_name
            , sub_dir = getattr (obj, "perma_name", str (obj.pid))
            , parent  = parent
            , ** kw
            )
    # end def __init__

    @Once_Property
    def query_filters (self) :
        result = list (self.__super.query_filters)
        result.append (getattr (Q, self.role) == self.obj)
        return tuple  (result)
    # end def query_filters

# end class Link_Manager

if __name__ != "__main__" :
    GTW.NAV.E_Type._Export ("*")
### __END__ GTW.NAV.E_Type.Manager
