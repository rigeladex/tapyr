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
#    TFL.SDG.C.Initializer
#
# Purpose
#    Model initializers for C data types
#
# Revision Dates
#     9-Aug-2004 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL              import TFL
import _TFL._SDG._C.Node

class Init_Atom (TFL.SDG.C.Node) :
    """Initializer for atomic variables/fields"""

    init_arg_defaults    = dict \
        ( init           = ""
        )
    front_args           = ("init", )

    c_format             = """%(init)s%(:head= :*description:)s"""

# end class Init_Atom

class Init_Comp (TFL.SDG.C.Node) :
    """Initializer for composite variables/fields"""

    c_format             = """
        { %(:rear=%(NL)s}¡sep=, :>*body_children:)s%(:head= :*description:)s
    """

# end class Init_Comp

if __name__ != "__main__" :
    TFL.SDG.C._Export ("*")
### __END__ TFL.SDG.C.Initializer
