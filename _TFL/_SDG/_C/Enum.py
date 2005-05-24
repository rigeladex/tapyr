# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 Mag. Christian Tanzer. All rights reserved
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
#    TFL.SDG.C.Enum
#
# Purpose
#    C enum declaration
#
# Revision Dates
#    24-May-2005 (CED) Creation
#    ««revision-date»»···
#--
#

from   _TFL              import TFL
import _TFL._SDG._C.Node

class Enum_Item (TFL.SDG.C.Node, TFL.SDG.Leaf) :
    """Model an item of a C enum."""

    init_arg_defaults    = dict \
        ( name           = ""
        , value          = ""
        , comment        = ""
        )

    front_args           = ("name", "value", "comment")

    _autoconvert         = dict \
        ( value          = lambda s, k, v : s._convert_value   (v)
        , comment        = lambda s, k, v : s._convert_comment (v)
        )

    c_format = h_format  = """ \
          %(name)s%(value)s%(:front= :>*comment:)s
       """

    def _convert_comment (self, comment) :
        result = ""
        if comment :
            result = TFL.SDG.C.Comment (comment)
        return result
    # end def _convert_comment

    def _convert_value (self, value) :
        result = ""
        if value :
            result = " = %s" % value
        return result
    # end def _convert_value

# end class Enum_Item

class Enum (TFL.SDG.C.Node, TFL.SDG.Leaf) :
    """Model C enum declarations"""

    init_arg_defaults    = dict \
        ( name           = ""
        , values         = []
        , standalone     = ""
        )

    _autoconvert         = dict \
        ( values         = lambda s, k, v : s._convert_values (v)
        , standalone     = lambda s, k, v : v and ";" or ""
        )

    front_args           = ("name", "values")

    c_format = h_format  = \
        ( """enum _%(name)s """
          """%(:front=%(NL)s%(base_indent)s{ """
          """¡front0={"""
          """¡sep=%(base_indent)s, """
          """¡rear=%(NL)s%(base_indent)s}"""
          """¡rear0=}"""
          """:*values:)s%(standalone)s"""
        )

    def _convert_values (self, values) :
        result = []
        if not values :
            raise ValueError, \
               "Enum declaration need at least one possible value"
        for v in values :
            item, comment = \
               [s.strip () for s in (v.split ("//", 1) + [""]) [:2]]
            name, value   = \
               [s.strip () for s in (item.split ("=", 1) + [""]) [:2]]
            result.append (Enum_Item (name, value, comment))
        return result
    # end def _convert_values

# end class Enum

if __name__ != "__main__" :
    TFL.SDG.C._Export ("*")
### __END__ Enum


