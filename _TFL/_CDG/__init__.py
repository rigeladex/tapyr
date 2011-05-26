# -*- coding: iso-8859-15 -*-
# Copyright (C) 2002 Mag. Christian Tanzer. All rights reserved
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
#    TFL.CDG.__init__
#
# Purpose
#    Package C Data structure Generation
#    - provides abstract define of C data structures as paython classes
#    - provides generation of C header files containing the struct/typedef
#      definitions
#    - provides functions to generate a binary buffer to fill the data
#      structures from a python object model
#
#   Examples using this package: table driven FT-Com Layer, table driven
#   Com-Layer, ...
#
# Revision Dates
#    11-Jul-2005 (MG) Creation
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ««revision-date»»···
#--



from   _TFL                   import TFL
from   _TFL.Package_Namespace import Package_Namespace

CDG = Package_Namespace ()
TFL._Export             ("CDG")

del Package_Namespace

### __END__ TFL.CDG.__init__
