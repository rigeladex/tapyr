# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 TTTech Computertechnik AG. All rights reserved
# Schönbrunnerstraße 7, A--1040 Wien, Austria. office@tttech.com
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
#    TFL.SDG.C.Include
#
# Purpose
#    C-include statements
#
# Revision Dates
#    11-Aug-2004 (MG) Creation
#    12-Aug-2004 (MG) `cgi` set to `Decl`
#    13-Aug-2004 (CT) `Include.c_format` simplified
#                     (`%(filename)s` instead of `%(::.filename:)s`)
#    ««revision-date»»···
#--

from   _TFL              import TFL
import _TFL._SDG._C.Node

class Include (TFL.SDG.Leaf, TFL.SDG.C.Node) :
    """C-include statements"""

    cgi                    = TFL.SDG.C.Node.Decl
    init_arg_defaults      = dict \
        ( filename         = ""
        )
    front_args             = ("filename", )
    _autoconvert           = dict \
        ( filename         = lambda s, k, v : "<%s>" % (v, )
        )

    h_format = c_format    = """#include %(filename)s"""

# end class Include

Sys_Include = Include

class App_Include (Include) :
    """C-app-include statement"""

    _autoconvert           = dict \
        ( filename         = lambda s, k, v : '"%s"' % (v, )
        )

# end class App_Include

if __name__ != "__main__" :
    TFL.SDG.C._Export ("*", "Sys_Include")
### __END__ TFL.SDG.C.Include
