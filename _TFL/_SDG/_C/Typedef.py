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
#    TFL.SDG.C.Typedef
#
# Purpose
#    Model C typedef declarations
#
# Revision Dates
#    30-Jul-2004 (CT) Creation
#    12-Aug-2004 (MG) `description` and `eol_desc` added to formats
#    ««revision-date»»···
#--

from   _TFL              import TFL
import _TFL._SDG._C.Node

class Typedef (TFL.SDG.C.Maybe_Const, TFL.SDG.Leaf) :
    """Model C typedef declarations"""

    init_arg_defaults    = dict \
        ( type           = ""
        )

    _autoconvert         = dict \
        ( type           = lambda s, k, v : s._convert (v, TFL.SDG.C.Type)
        )

    _name_or_type        = property (lambda s : s.name or s.type.name)

    h_format = c_format  = "".join \
        ( ( """typedef """
          , """%(::.const:)s"""
          , """%(::*type:)s %(::._name_or_type:)s; %(::*eol_desc:)s
               >%(::*description:)s
            """
          )
        )

    def __init__ (self, type, name = None, ** kw) :
        if isinstance (type, TFL.SDG.C.Struct) and not name :
            name = type.name
        self.__super.__init__ (name = name, type = type, ** kw)
    # end def __init__

# end class Typedef

if __name__ != "__main__" :
    TFL.SDG.C._Export ("*")
### __END__ TFL.SDG.C.Typedef
