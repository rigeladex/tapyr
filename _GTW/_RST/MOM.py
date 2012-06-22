# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.RST.
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
#    GTW.RST.MOM
#
# Purpose
#    RESTful resource for essential types and objects of MOM meta object model
#
# Revision Dates
#    22-Jun-2012 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._RST.Resource
import _GTW._RST.HTTP_Method

from   _TFL._Meta.Once_Property import Once_Property

class RST_E_Type_Mixin (TFL.Meta.Object) :
    """Mixin for classes of E_Type classes."""

    query_restriction          = None
    sort_key                   = None

    _change_info               = None
    _last_change               = None
    _objects                   = []
    _old_cid_e                 = -1
    _old_cid_o                 = -1
    _sort_key_cid_r            = TFL.Sorted_By ("-cid")

    objects                    = property (lambda s : s._get_objects ())
    _entries                   = property \
        ( lambda s    : s._get_entries ()
        , lambda s, v : True
        )

    def __init__ (self, ** kw) :
        self.pop_to_self (kw, "ETM", prefix = "_")
        if "name" not in kw :
            kw ["name"] = self.E_Type.type_name
        self.__super.__init__ (** kw)
    # end def __init__

    @property
    def count (self) :
        if self.query_filters :
            result = self.query ().count_transitive ()
        else :
            result = self.ETM.count_transitive
        return result
    # end def count

    @Once_Property
    def E_Type (self) :
        ETM = self._ETM
        if isinstance (ETM, basestring) :
            result = self.top.App_Type [ETM]
        else :
            result = ETM.E_Type
        return result
    # end def E_Type

    @Once_Property
    def ETM (self) :
        result = self._ETM
        if isinstance (result, basestring) :
            result = self.top.scope [result]
        return result
    # end def ETM

    @property
    def change_info (self) :
        return self._change_info
    # end def change_info

    @Once_Property
    def query_filters (self) :
        return tuple ()
    # end def query_filters

    def query (self, sort_key = None) :
        result = self.ETM.query \
            (* self.query_filters, sort_key = sort_key or self.sort_key)
        if self.query_restriction is not None :
            result = self.query_restriction (result)
        return result
    # end def query

    def _get_entries (self) :
        cid   = self.change_info.cid
        if self._old_cid_e != cid :
            self._old_cid_e = cid
            self.__entries  = list \
                (self._new_entry (o) for o in self.objects)
        return self.__entries
    # end def _get_entries

    def _get_objects (self) :
        cid = self.change_info.cid
        if self._old_cid_o != cid :
            self._old_cid_o = cid
            self.__objects  = self.query ().all ()
        return self.__objects
    # end def _get_objects

    def _prepare_handle_method (self, method, request) :
        scope = self.top.scope
        etn   = self.E_Type.type_name
        lc    = scope.query_changes \
            (type_name = etn).order_by (self._sort_key_cid_r).first ()
        if lc is not None :
            self._change_info   = TFL.Record \
                ( cid           = lc.cid
                , etag          = "ET-%s-%s" % (lc.time, lc.cid)
                , last_modified = lc.time
                )
    # end def _prepare_handle_method

# end class RST_E_Type_Mixin

_Ancestor = GTW.RST.Node

class RST_E_Type (RST_E_Type_Mixin, _Ancestor) :
    """RESTful node for a specific essential type."""

    _real_name                 = "E_Type"

    _ETM                       = None

    class RST_E_Type_GET (_Ancestor.GET) :

        _real_name             = "GET"

        ### XXX redefine _response_dict_top and _response_entry to regard
        ###     query parameters (full vs. bare bone answer...)

        def _response_entry (self, resource, request, entry) :
            return entry.pid
        # end def _response_entry

        def _resource_entries (self, resource, request) :
            return resource.objects
        # end def _resource_entries

    GET = RST_E_Type_GET # end class

    def _new_entry (self, instance) :
        return Entity (instance = o, parent = self)
    # end def _new_entry

E_Type = RST_E_Type # end class

if __name__ != "__main__" :
    GTW.RST._Export_Module ()
### __END__ GTW.RST.MOM
