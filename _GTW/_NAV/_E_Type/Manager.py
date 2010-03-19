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

    def __init__ (self, src_dir, ** kw) :
        self.__super.__init__ (src_dir = src_dir, ** kw)
        etn = self.E_Type.type_name
        top = self.top
        if etn not in top.E_Types :
            top.E_Types [etn] = self
    # end def __init__

    @Once_Property
    def admin (self) :
        Admin = self.top.Admin
        if Admin :
            return Admin._get_child (self.name)
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
        return pjoin (self.abs_href, obj.lid)
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
        if self.disp_filter :
            result.append (self.disp_filter)
        return tuple (result)
    # end def query_filters

    def _get_child (self, child, * grandchildren) :
        if not grandchildren :
            try :
                obj = self.ETM.query (perma_name = child).one ()
            except Exception :
                try :
                    obj = self.lid_query (self.ETM, child)
                except LookupError :
                    return
            return self.page_from_obj (obj)
    # end def _get_child

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

    query_limit       = 7

    def query (self) :
        result = self.ETM.query \
            ( * self.query_filters
            , sort_key =  TFL.Sorted_By ("-date.start", "-prio", "perma_name")
            )
        return result.limit (self.query_limit)
    # end def query

    @Once_Property
    def query_filters (self) :
        result = list (self.__super.query_filters)
        result.append (Q.date.alive)
        return tuple  (result)
    # end def query_filters

    def _get_objects (self) :
        T = self.Page
        kw = self.page_args
        sk = TFL.Sorted_By ("-date.start", "-prio", "perma_name")
        qr = self.ETM.query (sort_key = sk)
        cy = datetime.date.today ().year
        result = \
            [   T (self, o, ** kw)
            for o in qr.filter (Q.date.alive).limit (self.query_limit)
            ]
        name = "Archive"
        arch = Manager_T_Archive \
            ( src_dir   = pjoin (self.src_dir, name)
            , parent    = self
            , name      = name
            , sub_dir   = name
            , title     = name
            , ETM       = self.ETM
            , page_args = self.page_args
            )
        result.append (arch)
        return result
    # end def _get_objects

# end class Manager_T

class Manager_T_Archive (Manager_T) :

    class _Cmd_ (GTW.NAV.Dir) :
        pass
    # end class _Cmd_

    class Year (_Cmd_) :
        pass
    # end class Year

    def _get_objects (self) :
        T  = self.Page
        kw = self.page_args
        sk = TFL.Sorted_By  ("-date.start", "-prio", "perma_name")
        qr = self.ETM.query (sort_key = sk)
        cy = datetime.date.today ().year
        result = []
        for y in xrange (cy, cy - 5, -1) :
            qy = qr.filter \
                ( (Q.date.start >= datetime.date (y,  1,  1))
                , (Q.date.start <= datetime.date (y, 12, 31))
                )
            name = str (y)
            Y = self.Year \
                ( src_dir = pjoin (self.src_dir, name)
                , parent  = self
                , year    = y
                , name    = name
                , sub_dir = name
                , title   = name
                )
            _entries = [T (Y, o, ** kw) for o in qy]
            if _entries :
                Y._entries = _entries
                result.append (Y)
                print y, Y.abs_href, len (_entries)
        return result
    # end def _get_objects

# end class Manager_T_Archive

if __name__ != "__main__" :
    GTW.NAV.E_Type._Export ("*")
### __END__ GTW.NAV.E_Type.Manager
