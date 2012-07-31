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

class _E_Type_CSV_ (GTW.RST.Mime_Type.CSV) :

    _real_name                 = "CSV"
    mime_type_parameters       = ("header=present", )

    def rendered (self, request, response, body) :
        import csv
        from   StringIO import StringIO
        names = body.get ("attribute_names")
        if names :
            nm = dict           ((n, n) for n in names)
            rs = list           (e ["attributes"] for e in body ["entries"])
            f  = StringIO       ()
            dw = csv.DictWriter (f, names)
            dw.writerow         (nm)
            dw.writerows        (rs)
            return f.getvalue   ()
    # end def rendered

# end class _E_Type_CSV_

_Ancestor = GTW.RST.Dir_V

class RST_E_Type (GTW.RST.MOM.RST_E_Type_Mixin, _Ancestor) :
    """RESTful node for a specific essential type."""

    _real_name                 = "E_Type"

    _ETM                       = None

    Entity                     = GTW.RST.MOM.Entity

    class RST_E_Type_GET (_Ancestor.GET) :

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
                attr_names = tuple (a.name for a in resource.attributes)
                kw ["attribute_names"] = attr_names
            return self.__super._response_dict \
                (resource, request, response, ** kw)
        # end def _response_dict

        def _response_entry (self, resource, request, response, entry) :
            pid = int (entry.pid)
            if request.verbose :
                e = resource._new_entry (pid)
                result = e.GET ()._response_body (e, request, response)
            else :
                result = pid
            return result
        # end def _response_entry

        def _resource_entries (self, resource, request, response) :
            result = resource.objects
            return sorted (result, key = Q.pid)
        # end def _resource_entries

    GET = RST_E_Type_GET # end class

    class RST_E_Type_POST (GTW.RST.MOM._PUT_POST_Mixin_, GTW.RST.POST) :

        _real_name                 = "POST"

        success_code               = 201

        def _apply_attrs (self, resource, request, response, attrs) :
            return resource.ETM (raw = True, ** attrs)
        # end def _apply_attrs

    POST = RST_E_Type_POST # end class

    def allow_method (self, method, user) :
        if method.name == "POST" and self.ETM.is_partial :
            return False
        return self.__super.allow_method (method, user)
    # end def allow_method

E_Type = RST_E_Type # end class

if __name__ != "__main__" :
    GTW.RST.MOM._Export ("*")
### __END__ GTW.RST.MOM.E_Type
