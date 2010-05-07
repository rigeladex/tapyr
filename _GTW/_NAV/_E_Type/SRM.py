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
#    GTW.NAV.E_Type.SRM
#
# Purpose
#    Navigation directory and pages for instances of SRM
#
# Revision Dates
#    30-Apr-2010 (CT) Creation
#     5-May-2010 (CT) Creation continued
#     7-May-2010 (CT) `Regatta_Event._get_objects` and `._get_pages` changed
#                     to set `ETM` and `E_Type` properly
#    ««revision-date»»···
#--

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW.FO
import _GTW._NAV.Base
import _GTW._NAV._E_Type.Manager
import _GTW._NAV._E_Type.Mixin

import _TFL._Meta.Object
from   _TFL._Meta.Once_Property import Once_Property

from   _TFL.I18N                import _, _T, _Tn
from   _TFL.predicate           import first
from   posixpath                import join  as pjoin

class Regatta (GTW.NAV.E_Type.Instance_Mixin, GTW.NAV.Dir) :
    """Navigation directory for a single regatta."""

    def __init__ (self, manager, obj, ** kw) :
        kw ["src_dir"] = kw ["sub_dir"] = obj.perma_name
        self.__super.__init__ (manager, obj, ** kw)
        self.name = obj.perma_name
    # end def __init__

    def _get_child (self, child, * grandchildren) :
        entries = self._entries
        try :
            result = first (e for e in entries if e.name == child)
        except IndexError :
            pass
        else :
            if grandchildren :
                result = result._get_child (* grandchildren)
            return result
    # end def _get_child

    def _get_objects (self) :
        obj    = self.obj
        result = []
        sk     = TFL.Sorted_By ("left.nation", "left.sail_number")
        boats  = obj.boats = self.scope.SRM.Boat_in_Regatta.r_query \
            (right = obj).order_by (sk).all ()
        if boats :
            ### XXX results
            n = _T (u"Participants")
            result.append \
                ( GTW.NAV.Page
                    ( self
                    , name        = u"%s.html" % (n.lower (), )
                    , title       = n
                    , desc        = u"%s %s" %
                        ( _T (u"List of participants for"), self.title)
                    , template    = u"regatta_registration.html"
                    , regatta     = obj
                    )
                )
        return result
    # end def _get_objects

# end class Regatta

class Regatta_Event (GTW.NAV.E_Type.Instance_Mixin, GTW.NAV.Dir) :
    """Navigation directory for a single regatta event."""

    def __init__ (self, manager, obj, ** kw) :
        kw ["src_dir"] = kw ["sub_dir"] = obj.perma_name
        self.__super.__init__ (manager, obj, ** kw)
    # end def __init__

    def _get_child (self, child, * grandchildren) :
        entries = self._entries
        try :
            result = first (e for e in entries if e.name == child)
        except IndexError :
            pass
        else :
            if grandchildren :
                result = result._get_child (* grandchildren)
            return result
    # end def _get_child

    def _get_objects (self) :
        pkw    = self.page_args
        result = self._get_pages ()
        scope  = self.obj.home_scope
        for r in sorted (self.obj.regattas, key = TFL.Sorted_By ("name")) :
            kw  = dict \
                ( pkw
                , ETM       = scope [r.type_name]
                , E_Type    = r.__class__
                )
            result.append (Regatta (self, r, page_args = pkw, ** kw))
        return result
    # end def _get_objects

    def _get_pages (self) :
        T     = GTW.NAV.E_Type.Instance
        ETM   = self.scope.SRM.Page
        pkw   = self.page_args
        kw    = dict \
            ( pkw
            , ETM       = ETM
            , E_Type    = ETM._etype
            )
        rev   = self.obj
        query = ETM.query_s (event = rev)
        return [T (self, o, page_args = pkw, ** kw) for o in query]
    # end def _get_pages

# end class Regatta_Event

class SRM (GTW.NAV.E_Type.Manager_T_Archive_Y) :
    """Navigation directory listing regatta events by year."""

    Page            = Regatta_Event

    def __init__ (self, src_dir, ** kw) :
        self.__super.__init__ (src_dir = src_dir, ** kw)
        top   = self.top
        scope = top.scope
        for et in (scope.SRM.Page, scope.SRM.Regatta_C, scope.SRM.Regatta_H) :
            etn = et.type_name
            if etn not in top.E_Types :
                top.E_Types [etn] = self
    # end def __init__

    def href_display (self, obj) :
        scope = self.top.scope
        comps = [self.abs_href, str (obj.year)]
        if isinstance (obj, (scope.SRM.Page._etype, scope.SRM.Regatta._etype)) :
            comps.append (obj.event.perma_name)
        comps.append (obj.perma_name)
        return pjoin (* comps)
    # end def href_display

    def _get_grandchild (self, y, grandchildren) :
        gc0, gcs = grandchildren [0], grandchildren [1:]
        result   = self.__super._get_grandchild (y, (gc0, ))
        if result and gcs :
            result = result._get_child (* gcs)
        return result
    # end def _get_grandchild

# end class SRM

if __name__ != "__main__" :
    GTW.NAV.E_Type._Export ("*")
### __END__ GTW.NAV.E_Type.SRM
