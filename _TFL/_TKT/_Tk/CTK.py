# -*- coding: utf-8 -*-
# Copyright (C) 1998-2007 Mag. Christian Tanzer. All rights reserved
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
#    CTK
#
# Purpose
#    Provide interface to extended TK functionality
#
# Usage
#    from CTK import *
#       ...
#    CTK.Frame (...)
#
# Revision Dates
#    22-Mar-1998 (CT) Creation
#     7-Nov-2007 (CT) Moved into package _TFL._TKT._Tk
#    ««revision-date»»···
#--

### I wrote this before really understanding how Python modules and packages
### (are supposed to) work. When I found the errors of my ways I was too lazy
### to change all the users of this modules. So it's an unholy mess.

from   _TFL._TKT._Tk import CT_TK as CTK
from   Tkconstants   import *

START  = CTK.START

### __END__ TFL.TKT.Tk.CTK
