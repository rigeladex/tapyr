
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
#    GTW.RST.TOP.MOM.Doc
#
# Purpose
#    Directories and pages for documenting MOM E-types
#
# Revision Dates
#     8-Aug-2012 (CT) Creation
#    10-Aug-2012 (CT) Continue creation
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._RST._MOM.Doc
import _GTW._RST._TOP.Dir
import _GTW._RST._TOP.Page

from   _MOM.import_MOM          import MOM

from   _TFL._Meta.Once_Property import Once_Property
from   _TFL.I18N                import _, _T, _Tn

_Ancestor = GTW.RST.TOP.Page

class _RST_TOP_MOM_Doc_E_Type_ (_Ancestor, GTW.RST.MOM.Doc.E_Type) :
    """Page displaying documentation for a specific E_Type."""

    _real_name                 = "E_Type"

    document_class             = "E-Type-Doc"
    page_template_name         = "e_type_doc"

    class _RST_TOP_MOM_Doc_E_Type_GET_ (_Ancestor.GET) :

        _real_name             = "GET"

        def _render_context (self, resource, request, response, ** kw) :
            get    = GTW.RST.MOM.Doc.E_Type.GET ()
            cargo  = get._response_body (resource, request, response)
            result = self.__super._render_context \
                ( resource, request, response
                , rst_cargo = cargo
                , ** kw
                )
            result ["resource"] = resource
            return result
        # end def _render_context

    GET = _RST_TOP_MOM_Doc_E_Type_GET_ # end class

    def __init__ (self, ** kw) :
        self.pop_to_self (kw, "ETM", prefix = "_")
        if "name" not in kw :
            kw ["name"] = self.E_Type.type_base_name
        if "short_title" not in kw :
            kw ["short_title"] = _T (self.E_Type.type_base_name)
        self.__super.__init__ (** kw)
    # end def __init__

E_Type = _RST_TOP_MOM_Doc_E_Type_ # end class

_Ancestor = GTW.RST.TOP.Dir

class _RST_TOP_MOM_Doc_PNS_ (GTW.RST.MOM.Doc.Dir_Mixin, _Ancestor) :
    """Directory of pages displaying documentation for E_Types of a specific
       Package Namespace
    """

    _real_name                 = "PNS"

    E_Type                     = E_Type

    def __init__ (self, ** kw) :
        self.pop_to_self (kw, "PNS", prefix = "_")
        self.__super.__init__ (** kw)
        if not self.short_title :
            self.short_title = self.PNS._._bname
        if not self.title:
            self.title = self.PNS.__doc__
    # end def __init__

    @Once_Property
    def PNS (self) :
        result = self._PNS
        if isinstance (result, basestring) :
            result = self._PNS = self.top.App_Type.PNS_Map [result]
        return result
    # end def PNS

    def _add_index (self, l) :
        self._entries.sort (key = TFL.Getter.short_title)
        self.__super._add_index (0)
    # end def _add_index

    def _gen_entries (self) :
        PNS      = self.PNS
        app_type = self.top.App_Type
        etf      = self.e_type_filter
        for ET in app_type.etypes_by_pns [PNS.__name__] :
            if etf (ET) :
                yield self.E_Type (ETM = str (ET.type_name), parent = self)
    # end def _gen_entries

PNS = _RST_TOP_MOM_Doc_PNS_ # end class

_Ancestor = GTW.RST.TOP.Dir

class _RST_TOP_MOM_Doc_App_Type_ (GTW.RST.MOM.Doc.Dir_Mixin, _Ancestor) :
    """Directory of PNS directories of E_Types for a specific App_Type."""

    _real_name                 = "App_Type"

    PNS                        = PNS

    def resource_from_e_type (self, e_type) :
        if isinstance (e_type, basestring) :
            e_type = self.App_Type.entity_type (e_type)
        names  = e_type.type_name.split (".")
        result = self._get_child (* names)
        return result
    # end def resource_from_e_type

    def _gen_entries (self, ) :
        app_type = self.top.App_Type
        for k, pns in sorted (app_type.PNS_Map.iteritems ()) :
            k      = app_type.PNS_Aliases_R.get (k, k)
            parent = self
            if "." in k :
                names  = k.split (".")
                parent = self._get_child (* names [:-1])
            entry = self.PNS (PNS = pns, name = pns._._bname, parent = parent)
            if entry.entries :
                if parent is self :
                    yield entry
                else :
                    parent.add_entries (entry)
    # end def _gen_entries

App_Type = _RST_TOP_MOM_Doc_App_Type_ # end class

if __name__ != "__main__" :
    GTW.RST.TOP.MOM._Export_Module ()
### __END__ GTW.RST.TOP.MOM.Doc
