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
#    TFL.SDG.C.Module
#
# Purpose
#    Model C module (aka file)
#
# Revision Dates
#    28-Jul-2004 (CT) Creation
#    12-Aug-2004 (MG) `Incl` group removed (nice try)
#    ««revision-date»»···
#--

from   _TFL              import TFL
import _TFL._SDG._C._Scope_
import _TFL._SDG._C.Comment
import time

"""
from   _TFL._SDG._C.Module    import *
from   _TFL._SDG._C.Statement import *
from   _TFL._SDG._C.Function  import *
from   _TFL._SDG._C.Var       import *
from   _TFL._SDG._C.Struct    import *
from   _TFL._SDG._C.Array     import *
from   _TFL._SDG._C.Typedef   import *
from   _TFL._SDG._C.Block     import *
from   _TFL._SDG._C.If_Stmt   import *
from   _TFL._SDG._C.Switch    import *
from   _TFL._SDG._C.While     import *
from   _TFL._SDG._C.For_Stmt  import *
m = Module (name = "test", header_comment = "A new comment", author = "FooBar")
m.add ("x = 2;")
m.add (Var ("int", "x", init="0", description = "hansi plapper"))
m.add ( Struct ( "TDFT_Sign_Mask"
               , "unsigned long bit_mask    = 42 // mask for value"
               , "unsigned long extend_mask // mask for sign extension"
               , standalone = True
               )
      )
m.add ( Var ( "TDFT_Sign_Mask"
            , "fubar"
            , init_dict = dict (bit_mask = 57, extend_mask = 137)
            )
      )
m.add (Multiple_Var ("float", "y", "z", "u", init="0.0"))
m.add (Stmt_Group ("y = 42; ", "z = 0", cgi = TFL.SDG.C.Node.Tail))
m.add ( Function ( "int", "bar", "void"
                 , "froppel ()"
                 , Block ("foobar ()", "zoppel ()")
                 , If ( "fizzle==42", "x=2; y = 25"
                      , Elseif ("x==2", "frupple", "badauz()")
                      , Else   ("frupple", "badauz()")
                      )
                 )
      )
f=m.body_children ["bar"]
f.add ( Switch ( "quuux"
               , Case ("1", "a = 0; b = 2")
               , Case ("2", "a = 10; b = 20")
               , Default_Case ("hugo ()")
               )
      )
f.add ( While  ("p", "p++", "q++"))
f.add ( Do_While ("!p", "p++", "q++"))
f.add ( For ("i = 0", "i < l", "i++", "google ()", "giggle ()"))
m.add (Typedef  ("long signed int", "sint32"))
m.add (Function ("int", "baz", "int x, int y"))
m.add (Array ("int", "ar", 2, init = (0, 1), static = True))
m.add (Array ( "TDFT_Sign_Mask", "fubars", 2
             , init = [ dict (bit_mask = 57, extend_mask = 137)
                      , dict (bit_mask = 142, extend_mask = -1)
                      ]
             )
      )
m.write_to_c_stream()
m.write_to_h_stream()
print repr (m)
print str  (m)

"""

class Module (TFL.SDG.C._Scope_) :
    """Models a C module."""

    Ancestor             = TFL.SDG.C._Scope_

    children_group_names = \
        ( Ancestor.Decl
        , Ancestor.Head
        , Ancestor.Body
        , Ancestor.Tail
        )

    init_arg_defaults    = dict \
        ( author         = None
        , header_comment = ""
        )

    _autoconvert         = dict \
        ( header_comment =
              lambda s, k, v : s._convert_c_comment (k, v, eol = False)
        )

    star_level           = 3
    pass_scope           = False
    _format_head         = """
        %(::*signature:)s
        %(::*header_comment:)s
        %(::*description:)s
        %(::*explanation:)s
    """.strip ()
    _format_children     = """
        %(::*decl_children:)s
        %(::*head_children:)s
        %(::*body_children:)s
        %(::*tail_children:)s
    """
    c_format             = _format_head + """
    """ + _format_children

    h_format             = _format_head + """

        #ifndef _%(name)s_h_
        #define _%(name)s_h_ 1

        """ + _format_children + """#endif /* _%(name)s_h_ */
    """

    def __init__ (self, * children, ** kw) :
        self.__super.__init__ (* children, ** kw)
        author = ""
        if self.author :
            author = " by %s" % self.author
        self.signature = self._convert_c_comment \
            ( "signature"
            , "Module %s, written%s on %s"
            % ( self.name, author, time.strftime
                  ("%a %d-%b-%Y %H:%M:%S", time.localtime (time.time ()))
              )
            )
    # end def __init__

# end class Module

if __name__ != "__main__" :
    TFL.SDG.C._Export ("Module")
### __END__ TFL.SDG.C.Module
