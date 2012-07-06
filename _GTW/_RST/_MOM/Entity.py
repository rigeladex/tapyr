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
#    GTW.RST.MOM.Entity
#
# Purpose
#    Provide RESTful resource for a MOM entity instance
#
# Revision Dates
#    22-Jun-2012 (CT) Creation
#     3-Jul-2012 (CT) Factored from _GTW/_RST/MOM.py
#     4-Jul-2012 (CT) Use `pid_query` for `long`, `basestring` pids, too
#     5-Jul-2012 (CT) Add support for `closure`, factor `_response_obj_attrs`
#     6-Jul-2012 (CT) Change `Entity.GET` to use `seen` to show each entity
#                     once only
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._RST.Resource
import _GTW._RST.HTTP_Method
import _GTW._RST._MOM.Mixin

from   _MOM.import_MOM          import MOM, Q

from   _TFL._Meta.Once_Property import Once_Property
import _TFL._Meta.Object

_Ancestor = GTW.RST.Leaf

class RST_Entity (GTW.RST.MOM.RST_Mixin, _Ancestor) :
    """RESTful node for a specific instance of an essential type."""

    _real_name                 = "Entity"

    implicit                   = True

    class RST_Entity_DELETE (GTW.RST.DELETE) :

        _real_name             = "DELETE"

        def _response_body (self, resource, request, response) :
            result = resource.GET ()._response_body \
                (resource, request, response)
            if resource._check_cid (request, response, result) :
                obj = resource.obj
                pid = obj.pid
                obj.destroy ()
                result ["status"] = \
                    ("Object with pid %s successfully deleted" % pid)
            return result
        # end def _response_body

    DELETE = RST_Entity_DELETE # end class

    class RST_Entity_GET (_Ancestor.GET) :

        _real_name             = "GET"

        def _response_attr \
                (self, resource, request, response, obj, attr, seen) :
            k = attr.name
            if attr.E_Type and issubclass (attr.E_Type, MOM.Id_Entity) :
                v = attr.get_value (obj)
                if v is not None :
                    if request.has_option ("closure") and v.pid not in seen :
                        v = self._response_obj \
                            (resource, request, response, v, v.primary, seen)
                    else :
                        v = int (v.pid)
            else :
                v = attr.get_raw (obj)
            return k, v
        # end def _response_attr

        def _response_body (self, resource, request, response) :
            attrs = resource.attributes
            obj   = resource.obj
            seen  = set ()
            return self._response_obj \
                ( resource, request, response, obj, attrs, seen
                , url = resource.abs_href
                )
        # end def _response

        def _response_obj \
                (self, resource, request, response, obj, attrs, seen, ** kw) :
            seen.add (obj.pid)
            return dict \
                ( attributes = self._response_obj_attrs
                    (resource, request, response, obj, attrs, seen)
                , cid        = obj.last_cid
                , pid        = obj.pid
                , type_name  = obj.type_name
                , ** kw
                )
        # end def _response_obj

        def _response_obj_attrs \
                (self, resource, request, response, obj, attrs, seen) :
            return dict \
                (   self._response_attr
                        (resource, request, response, obj, a, seen)
                for a in attrs
                if  a.to_save (obj)
                )
        # end def _response_obj_attrs

    GET = RST_Entity_GET # end class

    class RST_Entity_PUT (GTW.RST.MOM._PUT_POST_Mixin_, GTW.RST.PUT) :

        _real_name                 = "PUT"

        success_code               = 200

        def _apply_attrs (self, resource, request, response, attrs) :
            obj  = resource.obj
            body = {}
            if resource._check_cid (request, response, body) :
                obj.set_raw (** attrs)
            else :
                self.failure_code = response.status_code
                raise ValueError (body ["error"])
            return obj
        # end def _apply_attrs

    PUT = RST_Entity_PUT # end class

    def __init__ (self, ** kw) :
        assert "name" not in kw
        self.pop_to_self (kw, "ETM", prefix = "_")
        obj = kw.pop ("obj")
        if isinstance (obj, (int, long, basestring)) :
            obj   = self.ETM.pid_query (obj)
        self.obj  = obj
        self.name = str (obj.pid)
        self.pop_to_self (kw, "attributes")
        self.__super.__init__ (** kw)
    # end def __init__

    @Once_Property
    def E_Type (self) :
        return self.obj.__class__
    # end def E_Type

    @property
    def change_query_filters (self) :
        return (Q.pid == self.obj.pid, )
    # end def change_query_filters

    def _check_cid (self, request, response, result) :
        cid_c  = request.req_data.get ("cid")
        if cid_c is None :
            cid_c = request.json.get ("cid")
        cid_s  = self.change_info and self.change_info.cid
        error  = None
        if cid_c is None :
            code  = 400 ### Bad request
            error = "You need to send the object's `cid` with the request"
        elif int (cid_c) != cid_s :
            code  = 409 ### Conflict
            error = \
                ( "Cid mismatch: requested cid = %s, current cid = %s"
                % (cid_c, cid_s)
                )
        if error is not None :
            result ["error"] = error
            response.status_code = code
        return not error
    # end def _check_cid

Entity = RST_Entity # end class

if __name__ != "__main__" :
    GTW.RST.MOM._Export ("*")
### __END__ GTW.RST.MOM.Entity
