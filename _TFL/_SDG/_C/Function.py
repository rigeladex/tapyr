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
#    TFL.SDG.C.Function
#
# Purpose
#    Model C functions
#
# Revision Dates
#    28-Jul-2004 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL              import TFL
import _TFL._SDG._C._Decl_
import _TFL._SDG._C.Type
import _TFL._SDG._C.Arg_List

class _Function_ (TFL.SDG.C.Maybe_Extern, TFL.SDG.C.Maybe_Static) :
    """Root class for C function declarations and function definitions"""

    init_arg_defaults    = dict \
        ( arg_list       = ""
        , return_type    = ""
        )
    _autoconvert         = dict \
        ( arg_list       =
            lambda s, k, v : s._convert_args (v)
        , return_type    =
            lambda s, k, v : s._convert (v, TFL.SDG.C.Type)
        )
    front_args           = ("return_type", "name", "arg_list")
    star_level           = 3

    _h_format = _c_format  = \
        ( """%(::*return_type:)s %(name)s"""
              """%(:front=%('''\\n''')s%(base_indent2)s( """
                """¡rear=%('''\\n''')s%(base_indent2)s)"""
                """¡empty= (void)"""
                """:*arg_list"""
                """:)s"""
        )

    def _convert_args (self, v) :
        if v is None or v == "void" :
            return ""
        else :
            return self._convert (v, TFL.SDG.C.Arg_List)
    # end def _convert_args

# end class _Function_

class Fct_Decl (_Function_) :
    """C function declaration"""

    h_format             = _Function_._h_format + ";"
    c_format             = _Function_._c_format + ";"

# end class Fct_Decl

class Function (_Function_, TFL.SDG.C._Scope_) :
    """C function definition"""

    cgi                  = TFL.SDG.C.Node.Body
    _mod_format          = """%(::.static:)s%(::.extern:)s"""
    h_format             = "".join \
        ( ( _mod_format
          , _Function_._h_format
          , """%(:empty=;"""
              """¡front=;%('''\\n''')s%(base_indent2)s"""
              """¡sep=%(base_indent2)s"""
              """:*description:)s
               >
          """
          )
        )
    c_format             = "".join \
        ( ( _mod_format
          , _Function_._c_format
          , """
                >>%(::*description:)s
                {
                >>%(::*explanation:)s
                >>%(::*decl_children:)s
                >>%(::*head_children:)s
                >>%(::*body_children:)s
                >>%(::*tail_children:)s
                }
                >
            """
          )
        )

    def _update_scope_child (self, child, scope) :
        child._update_scope (TFL.SDG.C.C)
    # end def _update_scope_child

# end class Function

if __name__ != "__main__" :
    TFL.SDG.C._Export ("*", "_Function_")
### __END__ TFL.SDG.C.Function
