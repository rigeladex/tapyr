# -*- coding: iso-8859-15 -*-
# Copyright (C) 2004-2011 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
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
#    TFL.SDG.C.Statement
#
# Purpose
#    Model simple statements in the code in a C file
#
# Revision Dates
#    27-Jul-2004 (MG) Creation
#    28-Jul-2004 (CT) Creation continued
#     9-Aug-2004 (CT) `children_group_names` redefined in `_Statement_` to
#                     `Node.Body`, only
#     9-Aug-2004 (CT) `Stmt_Group` changed to inherit from `_Statement_`
#                     first, `_Scope_` second (instead of vice versa)
#                     to get redefined `_Statement_.children_group_names`
#    12-Aug-2004 (MG) Formats of `Stmt_Group` changed
#    13-Aug-2004 (CT) Formats of `Stmt_Group` corrected (removed undefined
#                     children_groups)
#    24-Aug-2004 (MG) `Stmt_Group.default_cgi` changed
#    25-Aug-2004 (MG) `Decl` added to `Stmt_Group`
#    20-Oct-2004 (CT) Import for `_Scope_` added
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    31-Oct-2011 (MG)  imports corrected
#    26-Feb-2012 (MG) `__future__` imports added
#    ««revision-date»»···
#--



from   __future__  import absolute_import, division, print_function, unicode_literals
from   _TFL              import TFL
import _TFL._SDG._C.Node
import _TFL._SDG._C._Scope_

from   _TFL.Regexp       import *

class _Statement_ (TFL.SDG.C.Node) :
    """Model simple statement"""

    cgi                  = TFL.SDG.C.Node.Body
    trailing_semicol_pat = Regexp (r"""; *$""")
    scope                = TFL.SDG.C.C

    children_group_names = \
        ( TFL.SDG.C.Node.Body
        ,
        )

# end class _Statement_

class Statement (TFL.SDG.Leaf, _Statement_) :
    """Generic C statement"""

    init_arg_defaults    = dict \
        ( code           = ""
        )

    _autoconvert         = dict \
        ( code           =
            lambda s, k, v : s.trailing_semicol_pat.sub ("", v)
        )

    front_args           = ("code", )

    h_format = c_format  = """%(code)s; """

# end class Statement

Stmt = Statement

class Stmt_Group (_Statement_, TFL.SDG.C._Scope_) :
    """Group of C statements not enclosed in a block."""

    Ancestor             = TFL.SDG.C._Scope_
    default_cgi          = Ancestor.Body
    star_level           = 2
    _common_format       = """
        %(::*decl_children:)s
        %(::*body_children:)s
    """
    h_format = c_format  = _common_format

    children_group_names = (Ancestor.Body, Ancestor.Decl)
# end class Stmt_Group

if __name__ != "__main__" :
    TFL.SDG.C._Export ("*", "_Statement_", "Stmt")
### __END__ TFL.SDG.C.Statement