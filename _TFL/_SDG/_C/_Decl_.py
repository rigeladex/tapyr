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
#    TFL.SDG.C._Decl_
#
# Purpose
#    Model C declarations
#
# Revision Dates
#    28-Jul-2004 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL              import TFL
import _TFL._SDG._C.Node

class _Decl_ (TFL.SDG.C.Node) :
    """Root class for C declaration nodes"""

    cgi                  = TFL.SDG.C.Node.Decl

# end class _Decl_

class Maybe_Extern (_Decl_) :
    """Mixin for node types that may be declared extern"""

    init_arg_defaults    = dict (extern = None)
    _autoconvert         = dict \
        ( extern         = lambda s, k, v : v and "extern "   or None
        )

# end class Maybe_Extern

class Maybe_Static (_Decl_) :
    """Mixin for node types that may be declared static"""

    init_arg_defaults    = dict (static = None)
    _autoconvert         = dict \
        ( static         = lambda s, k, v : v and "static "   or None
        )

# end class Maybe_Static

class Maybe_Volatile (_Decl_) :
    """Mixin for node types that may be declared volatile"""

    init_arg_defaults    = dict (volatile = None)
    _autoconvert         = dict \
        ( volatile       = lambda s, k, v : v and "volatile "   or None
        )

# end class Maybe_Volatile

if __name__ != "__main__" :
    TFL.SDG.C._Export ("*", "_Decl_")
### __END__ TFL.SDG.C._Decl_
