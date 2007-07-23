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
#    TFL.SDG.C.Expression
#
# Purpose
#    Model C expressions
#
# Revision Dates
#    28-Jul-2004 (CT) Creation
#    25-Aug-2004 (CT) Add `H` to scope (otherwise `ifdef.condition` doesn't
#                     work in header files)
#    20-Oct-2004 (CT) `H` removed from scope (not all expressions should
#                     appear in headerfile by default)
#    23-Jul-2007 (CED) Activated absolute_import
#    ««revision-date»»···
#--
from __future__ import absolute_import


from   _TFL              import TFL
import _TFL._SDG._C.Node

class Expression (TFL.SDG.C.Node) :
    """Model C expressions"""

    scope               = TFL.SDG.C.C

    init_arg_defaults   = dict \
        ( code          = ""
        )

    front_args          = ("code", )

    h_format = c_format = "%(code)s"

# end class Expression

if __name__ != "__main__" :
    TFL.SDG.C._Export ("*")
### __END__ TFL.SDG.C.Expression
