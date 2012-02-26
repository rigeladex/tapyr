# -*- coding: iso-8859-15 -*-
# Copyright (C) 2004-2011 TTTech Computertechnik AG. All rights reserved
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
#    10-Aug-2004 (MG)  Creation
#    11-Aug-2004 (MG)  Creation continued
#    12-Aug-2004 (MG)  Backward compatibility added
#    24-May-2005 (CED) Import of `Enum` added
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    26-Feb-2012 (MG) `__future__` imports added
#    ««revision-date»»···
#--



from   __future__  import absolute_import, division, print_function, unicode_literals
from   _TFL._SDG._C                     import C
import _TFL._SDG._C.Array
import _TFL._SDG._C.Block
import _TFL._SDG._C.Comment
import _TFL._SDG._C.Enum
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

### __END__ TFL.SDG.C.import_C