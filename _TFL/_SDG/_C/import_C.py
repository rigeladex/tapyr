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
#    TFL.SDG.C.import_C
#
# Purpose
#    Provide all imports needed to create a C-document.
#
#    Usage:
#        from _TFL._SDG._C.import_C import C
#
#        module = C.Module (...)
#        module.add (C.If (...))
#        [...]
#
# Revision Dates
#    10-Aug-2004 (MG) Creation
#    11-Aug-2004 (MG) Creation continued
#    12-Aug-2004 (MG) Backward compatibility added
#    ««revision-date»»···
#--

from   _TFL._SDG._C                     import C
import _TFL._SDG._C.Array
import _TFL._SDG._C.Block
import _TFL._SDG._C.Comment
import _TFL._SDG._C.For_Stmt
import _TFL._SDG._C.Function
import _TFL._SDG._C.If_Stmt
import _TFL._SDG._C.Include
import _TFL._SDG._C.Macro
import _TFL._SDG._C.Macro_If
import _TFL._SDG._C.Module
import _TFL._SDG._C.New_Line
import _TFL._SDG._C.Statement
import _TFL._SDG._C.Struct
import _TFL._SDG._C.Switch
import _TFL._SDG._C.Typedef
import _TFL._SDG._C.Var
import _TFL._SDG._C.While

### backward compatibility
from Formatted_Stream import Formatted_C_Stream, Formatted_Stream
C.Formatted_Stream   = Formatted_Stream
C.Formatted_C_Stream = Formatted_C_Stream
### __END__ TFL.SDG.C.import_C
