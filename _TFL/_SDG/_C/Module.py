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
#    ««revision-date»»···
#--

from   _TFL              import TFL
import _TFL._SDG._C._Scope_
import _TFL._SDG._C.Comment
import time

"""
from   _TFL._SDG._C.Module import *
from   _TFL._SDG._C.Statement import *
from   _TFL._SDG._C.Function import *
m = Module (name = "test", header_comment = "A new comment", author = "FooBar")
m.add ("x = 2;")
m.add (Stmt_Group ("y = 42; ", "z = 0"))
m.add (Function ("int", "bar", "void"))
m.add (Function ("int", "baz", "int x, int y"))
print "\n".join (m.as_c_code ())
print "\n".join (m.as_h_code ())

"""

class Module (TFL.SDG.C._Scope_) :
    """Models a C module."""

    Ancestor             = TFL.SDG.C._Scope_

    children_group_names = \
        ( Ancestor.Incl
        , Ancestor.Decl
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
        %(::*incl_children:)s
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

        """ + _format_children + """
        #endif /* _%(name)s_h_ */
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
