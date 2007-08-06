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
#    20-Sep-2004 (CT) `x_attrs` added
#    21-Oct-2004 (CT) Use `"` instead of `'` in output
#     5-Sep-2005 (CT) `XML.Node` factored
#     6-Sep-2005 (CT) `xml_format` changed (`elem_type.rear0` empty instead
#                     of space)
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ««revision-date»»···
#--



from   _TFL              import TFL
import _TFL._SDG._XML.Node

class Element (TFL.SDG.XML.Node) :
    """Model an element of a XML document"""

    front_args           = ("elem_type", )
    init_arg_defaults    = dict \
        ( elem_type      = None
        , x_attrs        = {}
        )

    _xml_format          = """
        %(::*description:)s
        <%(elem_type)s%(:head= ¡rear0=¡rear=%(NL)s:>@_attr_values:)s>
        >%(::*body_children:)s
        </%(elem_type)s>
    """.strip ()

    xml_format           = _xml_format

    _autoconvert         = dict \
        ( elem_type      = lambda s, k, v : s._checked_xml_name (v)
        ,
        )

# end class Element

class Leaf (TFL.SDG.Leaf, Element) :
    """Model a leaf element of a XML document"""

# end class Leaf

class Empty (Leaf) :
    """Model an empty element of a XML document"""

    xml_format           = \
        ( """<%(elem_type)s"""
            """%(:head= ¡rear0=¡rear=%(NL)s:>@_attr_values:)s"""
          """/>"""
        )

# end class Empty

if __name__ != "__main__" :
    TFL.SDG.XML._Export ("*")
### __END__ TFL.SDG.XML.Element
