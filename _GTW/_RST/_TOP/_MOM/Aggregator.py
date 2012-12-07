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
#    GTW.RST.TOP.MOM.Aggregator
#
# Purpose
#    Page aggregating the most recent instances of one or more E_Types
#
# Revision Dates
#    17-Jul-2012 (CT) Creation
#     7-Aug-2012 (CT) Change `GTW.RST.MOM.RST_` to `GTW.RST.MOM.`
#     7-Dec-2012 (CT) Rename `query_filters` to `query_filters_s`
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._RST._TOP._MOM.Mixin
import _GTW._RST._TOP.Dir
import _GTW._RST._TOP.Page

from   _MOM.import_MOM          import MOM, Q

from   _TFL._Meta.Once_Property import Once_Property
from   _TFL.Decorator           import getattr_safe
from   _TFL.I18N                import _, _T, _Tn
from   _TFL.predicate           import first

from   posixpath                import join as pp_join

_Ancestor = GTW.RST.TOP.Page

class Aggregator (GTW.RST.MOM.Mixin, _Ancestor) :
    """Page aggregating the most recent instances of one or more E_Types."""

    css_class             = "news-clip"
    query_limit           = 25
    sort_key              = TFL.Sorted_By ("-date.start", "-prio")
    page_template_name    = "e_type_aggregator"

    _exclude_robots       = False
    _old_objects          = None

    class Aggregator_GET (_Ancestor.GET) :

        _real_name             = "GET"

        def _render_context (self, resource, request, response, ** kw) :
            return self.__super._render_context \
                ( resource, request, response
                , calendar = resource.calendar
                , clips    = resource.clips
                , ** kw
                )
        # end def _render_context

    GET = Aggregator_GET # end class

    class Instance (TFL.Meta.Object) :

        def __init__ (self, obj, parent) :
            self.obj    = obj
            self.parent = parent
            self.top    = parent.top
            self.FO     = GTW.FO (obj, parent.top.encoding)
        # end def __init__

        def __getattr__ (self, name) :
            if name == "link_to" :
                top = self.top
                result = getattr (self.obj, name, None)
                if not result :
                    left = getattr (self.obj, "left", None)
                    if left is not None :
                        result = top.obj_href (left)
            else :
                result = getattr (self.FO, name)
            return result
        # end def __getattr__

    # end class Instance

    def __init__ (self, ** kw) :
        kw ["_ETMS"] = kw.pop ("ETMS")
        self.__super.__init__ (** kw)
    # end def __init__

    @Once_Property
    @getattr_safe
    def calendar (self) :
        return getattr (self.top.SC, "Cal", None)
    # end def calendar

    @Once_Property
    @getattr_safe
    def change_query_filters (self) :
        def _gen (ETMS) :
            for ETM in ETMS :
                E_Type = ETM.E_Type
                if E_Type.is_partial :
                    for c in E_Type.children_np :
                        yield c
                else :
                    yield E_Type.type_name
        result = (Q.type_name.IN (sorted (_gen (self.ETMS))), )
        return result
    # end def change_query_filters

    @property
    @getattr_safe
    def clips (self) :
        objects = self.objects
        if self._old_objects is not objects :
            self._clips = \
                [self.Instance (obj = o, parent = self) for o in objects]
            if objects :
                self._old_objects = objects
        return self._clips
    # end def clips

    @Once_Property
    @getattr_safe
    def ETMS (self) :
        result = []
        for etm in self._kw ["_ETMS"] :
            if isinstance (etm, basestring) :
                etm = self.top.scope [etm]
            result.append (etm)
        return result
    # end def ETMS

    @Once_Property
    @getattr_safe
    def query_filters_s (self) :
        return self.__super.query_filters_s + (Q.date.alive, )
    # end def query_filters_s

    def query (self) :
        qs = []
        for ETM in self.ETMS :
            q = ETM.query (* self.query_filters, sort_key = self.sort_key)
            if self.query_limit :
                q = q.limit (self.query_limit)
            qs.append (q)
        result = TFL.Q_Result_Composite (qs)
        result.order_by (self.sort_key)
        if self.query_limit :
            result.limit (self.query_limit)
        return result
    # end def query

# end class Aggregator

if __name__ != "__main__" :
    GTW.RST.TOP.MOM._Export ("*")
### __END__ GTW.RST.TOP.MOM.Aggregator
