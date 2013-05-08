# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012-2013 Mag. Christian Tanzer All rights reserved
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
#    GTW.RST.MOM.E_Type
#
# Purpose
#    Provide RESTful resource for a MOM entity type
#
# Revision Dates
#    22-Jun-2012 (CT) Creation
#     3-Jul-2012 (CT) Factored from _GTW/_RST/MOM.py
#     4-Jul-2012 (CT) Run `entry.pid` through `int`
#                     (mySQL gives `long` which messes up the test output)
#    31-Jul-2012 (CT) Use `dw.writerow`, not `dw.writeheader`: 2.6 compatibility
#    31-Jul-2012 (CT) Add `_E_Type_CSV_.mime_type_parameters`
#     7-Aug-2012 (CT) Change `GTW.RST.MOM.RST_` to `GTW.RST.MOM.`
#     7-Aug-2012 (CT) Add prefix and suffix `_` to class names
#     4-Oct-2012 (CT) Add `href_obj`
#     4-Oct-2012 (CT) Add `request.brief` to `E_Type.GET`
#     5-Oct-2012 (CT) Pass `attributes` to `_new_entry`
#    16-Oct-2012 (CT) Use dotted names for `attribute_names`
#    18-Oct-2012 (CT) Register `E_Type` in `top.ET_Map` under `"rest_api"`
#    27-Nov-2012 (CT) Derive `E_Type.POST` from `GTW.RST.MOM._POST_Mixin_`
#                     not `GTW.RST.MOM._PUT_POST_Mixin_`
#     7-Dec-2012 (CT) Consider `dont_et_map`
#    17-Dec-2012 (CT) Redefine `et_map_name`, remove `__init__`
#     2-Mar-2013 (CT) Redefine `_handle_method` to call `add_doc_link_header`
#    15-Apr-2013 (CT) Protect `_resource_entries` against `result` of `None`
#     8-May-2013 (CT) Remove `.pid`, `.url` from `attribute_names`, unless CSV
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._RST.Resource
import _GTW._RST.HTTP_Method
import _GTW._RST.Mime_Type
import _GTW._RST._MOM.Mixin
import _GTW._RST._MOM.Entity

from   _MOM.import_MOM          import MOM, Q

from   _TFL._Meta.Once_Property import Once_Property
import _TFL._Meta.Object
from   _TFL.predicate           import dotted_dict

from   posixpath                import join as pp_join

class _E_Type_CSV_ (GTW.RST.Mime_Type.CSV) :

    _real_name                 = "CSV"
    mime_type_parameters       = ("header=present", )

    def rendered (self, request, response, body) :
        import csv
        from   StringIO import StringIO
        names  = body.get ("attribute_names")
        an     = "attributes_raw" if request.raw else "attributes"
        if names :
            nm = dict ((n, n) for n in names)
            rs = list (dotted_dict (e [an]) for e in body ["entries"])
            f  = StringIO       ()
            dw = csv.DictWriter (f, names)
            dw.writerow         (nm)
            dw.writerows        (rs)
            return f.getvalue   ()
    # end def rendered

# end class _E_Type_CSV_

_Ancestor = GTW.RST.Dir_V

class _RST_MOM_E_Type_ (GTW.RST.MOM.E_Type_Mixin, _Ancestor) :
    """RESTful node for a specific essential type."""

    _real_name                 = "E_Type"

    _ETM                       = None

    Entity                     = GTW.RST.MOM.Entity

    et_map_name                = "rest_api"

    class _RST_MOM_E_Type_GET_ (_Ancestor.GET) :

        _real_name             = "GET"

        _renderers             = _Ancestor.GET._renderers + (_E_Type_CSV_, )

        ### XXX redefine _response_dict and _response_entry to regard
        ###     query parameters (full vs. bare bone answer...)

        def _response_body (self, resource, request, response) :
            if request.has_option ("count") :
                ETM = resource.ETM
                if request.has_option ("strict") :
                    qr = ETM.count_strict
                else :
                    qr = ETM.count
                result = dict (count = qr)
            else :
                result = self.__super._response_body \
                    (resource, request, response)
            return result
        # end def _response_body

        def _response_dict (self, resource, request, response, ** kw) :
            if request.verbose :
                def _gen (attributes) :
                    render_csv = response.renderer.name == "CSV"
                    for a in attributes :
                        n  = a.name
                        ts = []
                        if a.E_Type :
                            if issubclass (a.E_Type, MOM.Id_Entity) :
                                if render_csv and not request.brief :
                                    ts = ["pid", "url"]
                            else :
                                ts = [u.name for u in a.E_Type.user_attr]
                        if ts :
                            for t in ts :
                                yield ".".join ((n, t))
                        else :
                            yield n
                self.attributes = tuple (a.name for a in resource.attributes)
                kw ["attribute_names"] = tuple (_gen (resource.attributes))
            return self.__super._response_dict \
                (resource, request, response, ** kw)
        # end def _response_dict

        def _response_entry (self, resource, request, response, entry) :
            pid = int (entry.pid)
            if request.verbose :
                ### Restrict `attributes` only for identical types
                kw = dict (attributes = self.attributes) \
                    if entry.type_name == resource.E_Type.type_name else {}
                e = resource._new_entry (pid, ** kw)
                result = e.GET ()._response_body (e, request, response)
            elif request.brief :
                result = pid
            else :
                result = resource.href_obj (entry)
            return result
        # end def _response_entry

        def _resource_entries (self, resource, request, response) :
            result = resource.objects or []
            return sorted (result, key = Q.pid)
        # end def _resource_entries

    GET = _RST_MOM_E_Type_GET_ # end class

    class _RST_MOM_E_Type_POST_ (GTW.RST.MOM._POST_Mixin_, GTW.RST.POST) :

        _real_name                 = "POST"

        success_code               = 201

        def _apply_attrs (self, resource, request, response, attrs) :
            return resource.ETM (raw = True, ** attrs)
        # end def _apply_attrs

    POST = _RST_MOM_E_Type_POST_ # end class

    def allow_method (self, method, user) :
        if method.name == "POST" and self.ETM.is_partial :
            return False
        return self.__super.allow_method (method, user)
    # end def allow_method

    def _handle_method (self, method, request, response) :
        self.add_doc_link_header (response)
        return self.__super._handle_method (method, request, response)
    # end def _handle_method

    def href_obj (self, obj) :
        return pp_join (self.abs_href, str (obj.pid))
    # end def href_obj

E_Type = _RST_MOM_E_Type_ # end class

if __name__ != "__main__" :
    GTW.RST.MOM._Export ("*")
### __END__ GTW.RST.MOM.E_Type
