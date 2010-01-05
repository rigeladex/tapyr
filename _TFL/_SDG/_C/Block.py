# -*- coding: iso-8859-1 -*-
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
#    TFL.SDG.C.Block
#
# Purpose
#    Model C blocks
#
# Revision Dates
#    30-Jul-2004 (CT) Creation
#    24-Aug-2004 (CT) `trailer` added
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ««revision-date»»···
#--



from   _TFL              import TFL
import _TFL._SDG._C._Scope_

class Block (TFL.SDG.C._Scope_) :
    """C block of statements"""

    cgi                  = TFL.SDG.C.Node.Body
    star_level           = 3
    trailer              = ";"

    h_format             = ""
    _c_format = c_format = "".join \
        ( ( """ >{
                >>%(::*decl_children:)s
                >>%(::*head_children:)s
                >>%(::*body_children:)s
                >>%(::*tail_children:)s
                >}%(trailer)s
            """
          )
        )

# end class Block

if __name__ != "__main__" :
    TFL.SDG.C._Export ("*")
### __END__ TFL.SDG.C.Block
