# -*- coding: utf-8 -*-
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
#    TFL.SDG.C.Type
#
# Purpose
#    Model C types
#
# Revision Dates
#    27-Jul-2004 (CT) Creation
#    23-Sep-2004 (MG) `vaps_channel_format` and friends added
#    24-Sep-2004 (MG) `vaps_channel_format` simplified
#    23-Feb-2005 (CED) `apidoc_tex_format` defined
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    26-Feb-2012 (MG) `__future__` imports added
#    ««revision-date»»···
#--



from   __future__  import absolute_import, division, print_function, unicode_literals
from   _TFL              import TFL
import _TFL._SDG._C.Node

class Type (TFL.SDG.C.Node) :
    """Model C types"""

    type_dict           = { "sbyte2" : "S"
                          , "sbyte4" : "L"
                          , "float"  : "F"
                          }

    front_args          = ("name", )

    h_format = c_format = apidoc_tex_format = "%(name)s"

    vaps_channel_format = """%(name)s"""


# end class Type

if __name__ != "__main__" :
    TFL.SDG.C._Export ("*")
### __END__ TFL.SDG.C.Type