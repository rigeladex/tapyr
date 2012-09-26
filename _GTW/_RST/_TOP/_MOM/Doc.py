
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
#    25-Sep-2012 (CT) Add support for `graph.svg` to `PNS`
#    25-Sep-2012 (CT) Split `PNS_svg` and `PNS_svg_doc`
#    26-Sep-2012 (CT) Add `App_Type.GET` to handle `?E_Type` queries
#    26-Sep-2012 (CT) Set `hidden` dependent on `is_relevant`
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
from   _TFL.Decorator           import getattr_safe

from   posixpath                import join as pp_join

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
            kw ["short_title"] = self.E_Type.type_base_name
        self.__super.__init__ (** kw)
        if not self.title :
            self.title = self.E_Type.__doc__
    # end def __init__

E_Type = _RST_TOP_MOM_Doc_E_Type_ # end class

_Ancestor = GTW.RST.TOP.Dir

class _RST_TOP_MOM_Doc_PNS_ (GTW.RST.MOM.Doc.Dir_Mixin, _Ancestor) :
    """Directory of pages displaying documentation for E_Types of a specific
       Package Namespace
    """

    _real_name                 = "PNS"

    dir_template_name          = "pns_e_type_doc"
    E_Type                     = E_Type

    class Grapher (GTW.RST.TOP.Page) :

        class Grapher_GET (GTW.RST.TOP.Page.GET) :

            _real_name             = "GET"
            _renderers             = (GTW.RST.Mime_Type.SVG, )

            def _response_body (self, resource, request, response) :
                return resource.PNS_svg_doc
            # end def _response_body

        GET = Grapher_GET # end class

    # end class Grapher

    def __init__ (self, ** kw) :
        self.pop_to_self (kw, "PNS", prefix = "_")
        self.__super.__init__ (** kw)
        if not self.short_title :
            self.short_title = self.PNS._._bname
        if not self.title :
            self.title = \
                (  self.PNS.__doc__
                or _T ("Documentation for package namespace %s")
                     % (self.short_title, )
                )
    # end def __init__

    @Once_Property
    @getattr_safe
    def PNS (self) :
        result = self._PNS
        if isinstance (result, basestring) :
            result = self._PNS = self.top.App_Type.PNS_Map [result]
        return result
    # end def PNS

    @Once_Property
    @getattr_safe
    def PNS_graph (self) :
        PNS = self.PNS
        if PNS :
            try :
                return PNS._Import_Module ("graph")
            except ImportError as exc :
                pass
    # end def PNS_graph

    @Once_Property
    @getattr_safe
    def PNS_svg (self) :
        return self._get_svg (want_document = False)
    # end def PNS_svg

    @Once_Property
    @getattr_safe
    def PNS_svg_doc (self) :
        return self._get_svg (want_document = True)
    # end def PNS_svg_doc

    @property
    @getattr_safe
    def dir_template (self) :
        if self.PNS_graph :
            return self.__super.dir_template
    # end def dir_template

    dir_template.setter (_Ancestor.dir_template.fset)

    @Once_Property
    @getattr_safe
    def href_svg (self) :
        if self.PNS_svg_doc is not None :
            return pp_join (self.abs_href, "graph.svg")
    # end def href_svg

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
                yield self.E_Type \
                    ( ETM    = str (ET.type_name)
                    , hidden = not ET.is_relevant
                    , parent = self
                    )
    # end def _gen_entries

    def _get_child (self, child, * grandchildren) :
        if child == "graph" and not grandchildren :
            result = self.Grapher (name = child, parent = self)
        else :
            result = self.__super._get_child (child, * grandchildren)
        return result
    # end def _get_child

    def _get_svg (self, want_document) :
        PNS_graph = self.PNS_graph
        if PNS_graph is not None :
            from _MOM._Graph.SVG import Renderer as SVG_Renderer
            from StringIO import StringIO
            g = PNS_graph.graph (self.top.App_Type)
            r = SVG_Renderer (g, want_document = want_document)
            f = StringIO ()
            r.render ()
            r.canvas.write_to_xml_stream (f)
            return f.getvalue ()
    # end def _get_svg

PNS = _RST_TOP_MOM_Doc_PNS_ # end class

_Ancestor = GTW.RST.TOP.Dir

class _RST_TOP_MOM_Doc_App_Type_ (GTW.RST.MOM.Doc.Dir_Mixin, _Ancestor) :
    """Directory of PNS directories of E_Types for a specific App_Type."""

    _real_name                 = "App_Type"

    PNS                        = PNS

    class _RST_TOP_MOM_Doc_App_Type_GET (_Ancestor.GET) :

        _real_name             = "GET"

        def __call__ (self, resource, request, response) :
            req_data = request.req_data
            if "E_Type" in req_data :
                name = req_data ["E_Type"]
                etr  = resource.resource_from_e_type (name)
                if etr is not None :
                    return etr.top._http_response (etr, request, response)
                else :
                    raise resource.top.Status.Not_Found ()
            else :
                if resource.dir_template is None :
                    eff = resource._effective_entry
                    return eff.top._http_response (eff, request, response)
                else :
                    return self.__super.__call__ (resource, request, response)
        # end def __call__

    GET = _RST_TOP_MOM_Doc_App_Type_GET # end class

    def resource_from_e_type (self, e_type) :
        if isinstance (e_type, basestring) :
            e_type = self.App_Type.entity_type (e_type)
        names  = e_type.type_name.split (".")
        result = self._get_child (* names)
        return result
    # end def resource_from_e_type

    @property
    def _effective (self) :
        return self
    # end def _effective

    def _gen_entries (self) :
        app_type = self.top.App_Type
        for k, pns in sorted (app_type.PNS_Map.iteritems ()) :
            k      = app_type.PNS_Aliases_R.get (k, k)
            parent = self
            if "." in k :
                names  = k.split (".")
                parent = self._get_child (* names [:-1])
            entry = self.PNS (PNS = pns, name = pns._._bname, parent = parent)
            if entry.entries :
                entry.hidden = all (e.hidden for e in entry.entries)
                if parent is self :
                    yield entry
                else :
                    parent.add_entries (entry)
    # end def _gen_entries

App_Type = _RST_TOP_MOM_Doc_App_Type_ # end class

if __name__ != "__main__" :
    GTW.RST.TOP.MOM._Export_Module ()
### __END__ GTW.RST.TOP.MOM.Doc
