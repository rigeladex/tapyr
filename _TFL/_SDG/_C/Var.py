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
#    TFL.SDG.C.Var
#
# Purpose
#    Model C variables
#
# Revision Dates
#    28-Jul-2004 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL              import TFL
import _TFL._SDG._C._Decl_
import _TFL._SDG._C.Expression
import _TFL._SDG._C.Type

class Var ( TFL.SDG.C.Maybe_Extern
          , TFL.SDG.C.Maybe_Static
          , TFL.SDG.C.Maybe_Volatile
          , TFL.SDG.Leaf
          ) :
    """Model C variables"""

    init_arg_defaults    = dict \
        ( const          = None
        , struct         = None
        , type           = ""
        , init           = None
        , init_dict      = {}
        , trailer        = ";"
        )

    _autoconvert         = dict \
        ( const          = lambda s, k, v : v and "const "   or None
        , init           = lambda s, k, v
              : self._convert
                    ( isinstance (v, int) and str (v) or v
                    , TFL.SDG.C.Expression
                    )
        , struct         = lambda s, k, v : v and "struct "   or None
        , type           = lambda s, k, v : s._convert (v, TFL.SDG.C.Type)
        )

    front_args           = ("type", "name")
    rest_args            = "init"

    _common_format       = \
        ("""%(::.extern:)s"""
         """%(::.static:)s"""
         """%(::.volatile:)s"""
         """%(::.const:)s"""
         """%(::.struct:)s"""
         """%(::*type:)s %(name)s """
        )
    h_format             = _common_format + "%(trailer)s"
    c_format             = "".join \
        ( ( _common_format
          , """%(:head= = :.init:)s"""
          ### XXX , """%(:head= = :*init_dict:)s"""
          , "%(trailer)s"
          )
        )

# end class Var

if __name__ != "__main__" :
    TFL.SDG.C._Export ("*")
### __END__ TFL.SDG.C.Var
