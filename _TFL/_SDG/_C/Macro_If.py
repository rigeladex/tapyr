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
#    TFL.SDG.C.Macro_If
#
# Purpose
#    Defines preprocessor if/else/elseif
#
# Revision Dates
#    11-Aug-2004 (MG) Creation
#    13-Aug-2004 (CT) `Macro_If.c_format` simplified
#                     (`%(if_tag)s` instead of `%(::.if_tag:)s`)
#    20-Oct-2004 (CT) Imports for `Conditional` and `If_Stmt` added
#    23-Jul-2007 (CED) Activated absolute_import
#    ««revision-date»»···
#--
from __future__ import absolute_import


from   _TFL                import TFL
import _TFL._SDG._C.Conditional
import _TFL._SDG._C.If_Stmt
import _TFL._SDG._C.Macro

class Macro_Else (TFL.SDG.C.Macro_Block) :
    """C macro else"""

    cgi                  = TFL.SDG.C.Node.Else
    h_format = c_format  = """
        #else
        >%(::*children:)s
    """

# end class Macro_Else

class Macro_Elseif (TFL.SDG.C.Conditional, TFL.SDG.C.Macro_Block) :
    """A Macro elseif statement"""

    cgi                  = TFL.SDG.C.Node.Elseif
    h_format = c_format  = """
        #elif %(::*condition:)s
        >%(::*children:)s
    """
# end class Macro_Elseif

class Macro_If (TFL.SDG.C._Macro_, TFL.SDG.C.If) :
    """If preprocessor statement (#IF)"""

    then_class          = TFL.SDG.C.Macro_Block
    else_class          = Macro_Else
    elif_class          = Macro_Elseif
    if_tag              = "if"

    h_format = c_format = "\n".join \
        ( ( """#%(if_tag)s %(::*condition:)s"""
          , """>%(::*then_children:)s"""
          , """%(::*elseif_children:)s"""
          , """%(::*else_children:)s"""
          , """#endif /* %(if_tag)s %(::*condition:)s */"""
          )
        )

# end class Macro_If

class Macro_Ifndef (Macro_If) :
    """Ifndef preprocessor statement (#ifndef)"""

    if_tag = "ifndef"

# end class Macro_Ifndef

class Macro_Ifdef (Macro_If) :
    """Ifdef preprocessor statement (#ifdef)"""

    if_tag = "ifdef"

# end class Macro_Ifdef

if __name__ != "__main__" :
    TFL.SDG.C._Export ("*")
### __END__ TFL.SDG.C.Macro_If
