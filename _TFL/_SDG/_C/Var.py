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
#    30-Jul-2004 (CT) `Maybe_Const` factored
#    30-Jul-2004 (CT) `Multiple_Var` added
#     9-Aug-2004 (CT) `Initializer` handling added
#     9-Aug-2004 (CT) `_Var_` factored
#    ««revision-date»»···
#--

from   _TFL              import TFL
import _TFL._SDG._C._Decl_
import _TFL._SDG._C.Expression
import _TFL._SDG._C.Initializer
import _TFL._SDG._C.Type

class _Var_ ( TFL.SDG.C.Maybe_Const
            , TFL.SDG.C.Maybe_Extern
            , TFL.SDG.C.Maybe_Static
            , TFL.SDG.C.Maybe_Volatile
            , TFL.SDG.Leaf
            ) :

    init_arg_defaults    = dict \
        ( type           = ""
        , init           = None
        , new_line_col   = 0
        )

    initializers         = None

    _autoconvert         = dict \
        ( type           = lambda s, k, v : s._convert_type (v)
        )
    _struct              = None

    front_args           = ("type", "name")

    _common_format       = \
        ("""%(::.extern:)s"""
         """%(::.static:)s"""
         """%(::.volatile:)s"""
         """%(::.const:)s"""
         """%(::.struct:)s"""
         """%(::*type:)s %(name)s"""
        )

    def _convert_type (self, v) :
        result = self._convert (v, TFL.SDG.C.Type)
        if result.name in TFL.SDG.C.Struct.extension :
            self._struct = TFL.SDG.C.Struct.extension [result.name]
        return result
    # end def _convert_type

# end class _Var_

class Var (_Var_) :
    """Model C variables"""

    Ancestor             = _Var_

    init_arg_defaults    = dict \
        ( struct         = None
        , init_dict      = {}
        , trailer        = ";"
        )

    _autoconvert         = dict \
        ( init           = lambda s, k, v
              : v not in ("", None) and TFL.SDG.C.Init_Atom (v) or None
        , struct         = lambda s, k, v : v and "struct " or None
        )

    h_format             = "".join \
        ( ( Ancestor._common_format
          , "%(trailer)s"
          )
        )

    c_format             = "".join \
        ( ( Ancestor._common_format
          , """%(:front= = :*initializers:)s"""
          , """%(trailer)s"""
          , """%(:head= :*description:)s"""
          )
        )

    def __init__ (self, type, name, init = "", ** kw) :
        self.__super.__init__ (type, name, init = init, ** kw)
        if self.init_dict :
            if not self._struct :
                raise TFL.SDG.Invalid_Node (self, self.type, self.init_dict)
            self.initializers = self._struct._setup_initializers \
                (self.init_dict)
        if self.init :
            if self.init_dict :
                raise TFL.SDG.Invalid_Node (self, self.init, self.init_dict)
            self.initializers = self.init
    # end def __init__

# end class Var

class Multiple_Var (Var) :
    """Declaration for multiple variables"""

    Ancestor             = Var

    init_arg_defaults    = dict \
        ( var_names      = ""
        )

    h_format             = "".join \
        ( ( Ancestor._common_format
          , """%(:front=, :._var_names:)s"""
          , """%(trailer)s"""
          )
        )

    c_format             = "".join \
        ( ( Ancestor._common_format
          , """%(:front=, :._var_names:)s"""
          , """%(:head= = :*init:)s"""
          , """%(trailer)s"""
          )
        )

    _var_names           = property (lambda s : ", ".join (s.var_names))

    def __init__ (self, type, name, * var_names, ** kw) :
        ### need to jump through hoops to accomodate optional arg `init` of
        ### ancestor vs. `* var_names`
        self.__super.__init__ (type, name, var_names = var_names, ** kw)
    # end def __init__

# end class Multiple_Var

if __name__ != "__main__" :
    TFL.SDG.C._Export ("*", "_Var_")
### __END__ TFL.SDG.C.Var
