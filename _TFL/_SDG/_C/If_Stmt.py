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
#    TFL.SDG.C.If_Stmt
#
# Purpose
#    Model if statements in the code in a C file
#
# Revision Dates
#    30-Jul-2004 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL              import TFL
import _TFL._SDG._C.Block
import _TFL._SDG._C.Expression

class Else (TFL.SDG.C.Block) :
    """Else clause of If statement"""

    Ancestor             = TFL.SDG.C.Block
    name                 = "else"

    c_format             = "\n".join \
        ( ( """else"""
          , Ancestor._c_format
          )
        )

# end class Else

class Elseif (TFL.SDG.C.Block) :
    """Else-If clause of If statement"""

    Ancestor             = TFL.SDG.C.Block

    init_arg_defaults    = dict \
        ( condition      = ""
        )

    front_args           = ("condition", )

    _autoconvert         = dict \
        ( condition      = lambda s, k, v
              : s._convert (v, TFL.SDG.C.Expression)
        )

    c_format             = "\n".join \
        ( ( """else if (%(::*condition:)s)"""
          , Ancestor._c_format
          )
        )
# end class Elseif

class If (TFL.SDG.C._Statement_) :
    """If statement"""

    then_class           = TFL.SDG.C.Block
    else_class           = Else
    elif_class           = Elseif

    init_arg_defaults    = dict \
        ( condition      = ""
        , then           = ""
        )

    front_args           = ("condition", "then")

    _autoconvert         = dict \
        ( condition      = lambda s, k, v
              : s._convert (v, TFL.SDG.C.Expression)
        , then           = lambda s, k, v : s._convert (v, s.then_class)
        )

    c_format             = "\n".join \
        ( ( """if (%(::*condition:)s)"""
          , """%(::*then:)s"""
          , """%(::*else_children:)s"""
          )
        )

    ( Else,
    )                    = range (1)
    then_children        = property (lambda s : s.then)
    else_children        = property (lambda s : s.children_groups [s.Else])

    def __init__ (self, * args, ** kw) :
        self.__super.__init__ (* args, ** kw)
        self.then._update_scope   (self.scope)
    # end def __init__

    def insert (self, child, index = None, delta = 0) :
        """Insert `child' to `self.children' at position `index'
           (None means append).
        """
        if not child :
            return
        children  = self.else_children
        child     = self._convert (child, self.else_class)
        default_p = children and isinstance (children [-1], self.else_class)
        if   isinstance (child, self.else_class) :
            if default_p :
                raise TFL.SDG.Invalid_Node, (self, child)
            index = len (children)
        elif isinstance (child, self.elif_class) :
            if default_p :
                if index is None :
                    index = len (children) - 1
                else :
                    index = max (len (children) - 1, index)
        else :
            raise TFL.SDG.Invalid_Node, (self, child)
        self._insert (child, index, children, delta)
    # end def insert

# end class If

if __name__ != "__main__" :
    TFL.SDG.C._Export ("*")
### __END__ TFL.SDG.C.If_Stmt
