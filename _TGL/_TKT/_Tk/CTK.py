# -*- coding: utf-8 -*-
# Copyright (C) 1998-2007 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
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
