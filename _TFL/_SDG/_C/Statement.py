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
#    TFL.SDG.C.Statment
#
# Purpose
#    Model simple statments in the code in a C file
#
# Revision Dates
#    27-Jul-2004 (MG) Creation
#    ««revision-date»»···
#--
from   _TFL              import TFL
import _TFL._SDG._C.Node

class _Statment_ (TFL.SDG.C.Node) :
    """Model simple statment"""

    trailing_semicol_pat = re.compile (r"""; *$""")

    init_arg_defaults    = dict \
        ( code           = ""
        , scope          = TFL.SDG.C.C
        )

    _autoconvert         = dict \
        ( code           =
              lambda s, k, v, pat = trailing_semicol_pat : pat.sub ("", v)
        )
    h_format             = c_format = """
       %(code)s
    """

# end class _Statment_

if __name__ != "__main__" :
    TFL.SDG.C._Export ("Statment")
### __END__ TFL.SDG.C.Statment
