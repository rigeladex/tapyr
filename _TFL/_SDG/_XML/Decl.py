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
#    TFL.SDG.XML.Decl
#
# Purpose
#    Model declarations of a XML document
#
# Revision Dates
#    27-Aug-2004 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL                   import TFL
import _TFL._SDG._XML.Element

class _Decl_ (TFL.SDG.XML.Leaf) :

    init_arg_defaults    = dict \
        ( name           = None
        , value          = None
        )

    xml_format           = """<%(elem_type)s %(name)s %(::>.value:)s >"""

    _autoconvert         = dict \
        ( name           = lambda s, k, v : s._checked_xml_name (v)
        )

# end class _Decl_

class Element (_Decl_) :
    """Model an element type declaration of a XML document"""

    elem_type            = "!ELEMENT"
    front_args           = ("name", "value")

# end class Element

class Attlist (_Decl_) :
    """Model an attribute list declaration of a XML document"""

    elem_type            = "!ATTLIST"
    front_args           = ("name", )
    rest_args            = "value"

# end class Attlist

if __name__ != "__main__" :
    TFL.SDG.XML._Export_Module ()
### __END__ TFL.SDG.XML.Decl
