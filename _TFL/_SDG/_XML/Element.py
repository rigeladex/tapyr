# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.cluster
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
#++
# Name
#    TFL.SDG.XML.Element
#
# Purpose
#    Model an element of a XML document
#
# Revision Dates
#    26-Aug-2004 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL              import TFL
import _TFL._SDG._XML
import _TFL._SDG.Node

from   Regexp            import *

class Element (TFL.SDG.Node) :
    """Model an element of a XML document"""

    attr_names           = ()
    base_indent          = "  "
    front_args           = ("elem_type", )
    init_arg_defaults    = dict \
        ( description    = None
        , elem_type      = None
        )

    _xml_format          = """
        %(::*description:)s
        <%(elem_type)s%(:front= :>@_attr_values:)s>
        >%(::*body_children:)s
        </%(elem_type)s>
    """.strip ()

    xml_format           = _xml_format

    _autoconvert         = dict \
        ( description    = lambda s, k, v : s._convert (v, TFL.SDG.XML.Comment)
        , elem_type      = lambda s, k, v : s._checked_elem_type (v)
        )

    _elem_type_pattern   = Regexp ("[A-Za-z_:][-_:.A-Za-z0-9]*")

    _list_of_formats     = TFL.SDG.Node._list_of_formats + \
        ( "xml_format", )

    _specials_pattern    = Regexp ("[&<>]")

    def _attr_values (self, * args, ** kw) :
        for a in self.attr_names :
            v = getattr (self, a)
            if v is not None :
                v = str (v).replace ("'", "&apos;")
                yield """%s = '%s' """ % (a, v)
    # end def _attr_values

    def _checked_elem_type (self, value) :
        if not self._elem_type_pattern.match (value) :
            raise ValueError, "`%s` doesn not match %s" % \
                (value, self._elem_type_pattern.pattern.pattern)
        return value
    # end def _checked_elem_type

# end class Element

class Empty (TFL.SDG.Leaf, Element) :
    """Model an empty element of a XML document"""

    xml_format           = """
        <%(elem_type)s>%(:sep= ¡rear= :>@_attr_values:)s/>
    """

# end class Empty

class Leaf (TFL.SDG.Leaf, Element) :
    """Model a non-empty leave element of a XML document"""

# end class Leaf

if __name__ != "__main__" :
    TFL.SDG.XML._Export ("*")
### __END__ TFL.SDG.XML.Element
