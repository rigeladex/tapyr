# -*- coding: iso-8859-15 -*-
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
#    TFL.SDG.C.New_Line
#
# Purpose
#    Model empty lines in the code in a C file
#
# Revision Dates
#    26-Jul-2004 (CT) Creation
#    12-Aug-2004 (MG) formats changed
#    12-Aug-2004 (MG) `cgi` added
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ««revision-date»»···
#--



from   _TFL              import TFL
import _TFL._SDG._C.Node

class New_Line (TFL.SDG.Leaf, TFL.SDG.C.Node) :
    """Model an empty line in the code in a C file"""

    cgi                  = None
    init_arg_defaults    = dict \
        ( lines          = 1
        )
    h_format = c_format  = """%('''\\n''' * (lines - 1))s"""

# end class New_Line

class New_Page (TFL.SDG.Leaf, TFL.SDG.C.Node) :
    """Adds a new page character (formfeed)."""

    cgi                  = None
    h_format = c_format  = """%('\f')s"""

# end class New_Page

if __name__ != "__main__" :
    TFL.SDG.C._Export ("*")
### __END__ TFL.SDG.C.New_Line
