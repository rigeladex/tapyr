# -*- coding: iso-8859-15 -*-
# Copyright (C) 2004 Mag. Christian Tanzer. All rights reserved
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
#    TFL.SDG.C.For_Stmt
#
# Purpose
#    Model for statements in the code of a C file
#
# Revision Dates
#    10-Aug-2004 (CT) Creation
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ««revision-date»»···
#--



from   _TFL              import TFL
import _TFL._SDG._C.Block
import _TFL._SDG._C.Conditional

class For (TFL.SDG.C.Conditional, TFL.SDG.C.Block) :
    """For statement"""

    Ancestor             = TFL.SDG.C.Block

    init_arg_defaults    = dict \
        ( init           = ""
        , increase       = ""
        )

    front_args           = ("init", "condition", "increase")

    _autoconvert         = dict \
        ( init           = lambda s, k, v
              : s._convert (v, TFL.SDG.C.Expression)
        , increase       = lambda s, k, v
              : s._convert (v, TFL.SDG.C.Expression)
        )

    c_format             = "\n".join \
        ( ( """for (%(::*init:)s; %(::*condition:)s; %(::*increase:)s)"""
          , Ancestor._c_format
          )
        )
# end class For

if __name__ != "__main__" :
    TFL.SDG.C._Export ("*")
### __END__ TFL.SDG.C.For_Stmt
