# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.RST.MOM.
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
#    GTW.RST.MOM.Doc
#
# Purpose
#    Provide RESTful resources for the documentation of a MOM object model
#
# Revision Dates
#     7-Aug-2012 (CT) Creation
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._RST.Resource
import _GTW._RST.HTTP_Method
import _GTW._RST.Mime_Type
import _GTW._RST._MOM.Mixin

from   _MOM.import_MOM          import MOM

from   _TFL._Meta.Once_Property import Once_Property
import _TFL._Meta.Object
import _TFL.Record

class _RST_MOM_Doc_Mixin_ (TFL.Meta.Object) :
    """Mixin for MOM documentation resources"""

    _real_name                 = "Mixin"

    @Once_Property
    def change_info (self) :
        return TFL.Record (etag = self.top.App_Type.db_version_hash)
    # end def change_info

Mixin = _RST_MOM_Doc_Mixin_ # end class

_Ancestor = GTW.RST.Leaf

class _RST_MOM_Doc_E_Type_ (Mixin, GTW.RST.MOM.Base_Mixin, _Ancestor) :
    """RESTful node documenting a specific essential type."""

    _real_name                 = "E_Type"
    _ETM                       = None

    class _RST_MOM_Doc_E_Type_GET_ (_Ancestor.GET) :

        _real_name             = "GET"

        def _response_attr (self, resource, request, response, attr) :
            result = dict \
                ( default_value = attr.raw_default
                , description   = attr.description
                , is_required   = attr.is_required
                , kind          = attr.kind
                , name          = attr.name
                , p_type        = attr.P_Type.__name__
                , type          = attr.typ
                )
            for k in \
                    ( "example", "explanation", "group", "max_length"
                    , "role_name", "syntax"
                    ) :
                v = getattr (attr, k, None)
                if v :
                    result [k] = v
            if not attr.is_changeable :
                result ["is_changeable"] = False
            if attr.ui_name_T != attr.name :
                result ["ui_name"] = attr.ui_name_T
            if attr.E_Type :
                result ["type_name"] = tn = attr.E_Type.type_name
                if isinstance (attr.E_Type, MOM.An_Entity) :
                    result ["attributes"] = list \
                        (   self._response_attr (resource, request, response, a)
                        for a in attr.E_Type.edit_attr
                        )
                else :
                    result ["url"] = resource.e_type_href (tn)
            return result
        # end def _response_attr

        def _response_body (self, resource, request, response) :
            E_Type   = resource.E_Type
            attrs    = resource.attributes
            children = E_Type.children
            parents  = E_Type.parents
            result   = dict \
                ( description = E_Type.__doc__
                , type_name   = E_Type.type_name
                , url         = resource.abs_href
                )
            if attrs :
                result ["attributes"] = list \
                    (   self._response_attr (resource, request, response, a)
                    for a in attrs
                    )
            if children :
                result ["children"] = self._response_children \
                    (resource, request, response, children)
            if parents :
                result ["parents"] = self._response_parents \
                    (resource, request, response, parents)
            resource.scope.rollback () ### Remove example objects, if any
            return result
        # end def _response_body

        def _response_children (self, resource, request, response, children) :
            return list \
                (   dict
                        ( type_name = k
                        , url       = resource.e_type_href (c)
                        )
                for k, c in sorted (children.iteritems ())
                if  issubclass (c, MOM.Id_Entity)

                )
        # end def _response_children

        def _response_parents (self, resource, request, response, parents) :
            return list \
                (   dict
                        ( type_name = p.type_name
                        , url       = resource.e_type_href (p)
                        )
                for p in sorted (parents) if issubclass (p, MOM.Id_Entity)
                )
        # end def _response_parents

    GET = _RST_MOM_Doc_E_Type_GET_ # end class

    def __init__ (self, ** kw) :
        self.pop_to_self (kw, "ETM", prefix = "_")
        etn = self.type_name
        if "name" not in kw :
            kw ["name"] = etn.replace (".", "-")
        if "short_title" not in kw :
            kw ["short_title"] = etn
        self.__super.__init__ (** kw)
    # end def __init__

E_Type = _RST_MOM_Doc_E_Type_ # end class

_Ancestor = GTW.RST.Dir

class _RST_MOM_Doc_App_Type_ (Mixin, _Ancestor) :
    """RESTful node documenting the essential types of a specific App_Type."""

    _real_name                 = "App_Type"

    E_Type                     = E_Type

    def __init__ (self, ** kw) :
        if "entries" not in kw :
            etf = self.e_type_filter
            kw ["entries"] = tuple \
                (   self.E_Type (ETM = str (et.type_name))
                for et in self.top.App_Type._T_Extension if  etf (et)
                )
        self.__super.__init__ (** kw)
    # end def __init__

    def e_type_filter (self, e_type) :
        return issubclass (e_type, MOM.Id_Entity) and not e_type.is_locked ()
            ### ??? and (et.children or not et.is_partial)
    # end def e_type_filter

    def e_type_href (self, e_type) :
        resource = self.resource_from_e_type (e_type)
        if resource is not None :
            return resource.abs_href
    # end def e_type_href

    def resource_from_e_type (self, e_type) :
        if not isinstance (e_type, basestring) :
            e_type = getattr (e_type, "type_name")
        result = self._entry_map.get (e_type.replace (".", "-"))
        return result
    # end def resource_from_e_type

App_Type = _RST_MOM_Doc_App_Type_ # end class

if __name__ != "__main__" :
    GTW.RST.MOM._Export_Module ()
### __END__ GTW.RST.MOM.Doc
