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
#    TFL.SDG.C.While
#
# Purpose
#    Model while statements in the code of a C file
#
# Revision Dates
#     9-Aug-2004 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL              import TFL
import _TFL._SDG._C.Block
import _TFL._SDG._C.Conditional

class While (TFL.SDG.C.Conditional, TFL.SDG.C.Block) :
    """While statement"""

    Ancestor             = TFL.SDG.C.Block

    c_format             = "\n".join \
        ( ( """while (%(::*condition:)s)"""
          , Ancestor._c_format
          )
        )

# end class While

class Do_While (TFL.SDG.C.Conditional, TFL.SDG.C.Block) :
    """A `do` ... `while ()` loop"""

    Ancestor             = TFL.SDG.C.Block

    c_format             = "\n".join \
        ( ( """do"""
          , Ancestor._c_format.strip ()
          , """while (%(::*condition:)s);"""
          )
        )

    trailer              = ""

# end class Do_While

if __name__ != "__main__" :
    TFL.SDG.C._Export ("*")
### __END__ TFL.SDG.C.While
