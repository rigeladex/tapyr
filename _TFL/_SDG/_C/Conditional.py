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
#    Conditional
#
# Purpose
#    Root class for conditional constructs
#
# Revision Dates
#     9-Aug-2004 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL              import TFL
import _TFL._SDG._C.Expression
import _TFL._SDG._C.Node

class Conditional (TFL.SDG.C.Node) :
    """Root class for conditional constructs"""

    init_arg_defaults    = dict \
        ( condition      = ""
        )

    front_args           = ("condition", )

    _autoconvert         = dict \
        ( condition      = lambda s, k, v
              : s._convert (v, TFL.SDG.C.Expression)
        )

# end class Conditional

if __name__ != "__main__" :
    TFL.SDG.C._Export ("*")
### __END__ Conditional
