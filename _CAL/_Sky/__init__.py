# -*- coding: utf-8 -*-
# Copyright (C) 2007 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    CAL.Sky.__init__
#
# Purpose
#    Package for astronomical calculations
#
# Revision Dates
#    13-Nov-2007 (CT) Creation
#    ««revision-date»»···
#--

from   _CAL                   import CAL
from   _TFL.Package_Namespace import Package_Namespace

Sky = Package_Namespace ()
CAL._Export ("Sky")

del Package_Namespace

### __END__ CAL.Sky.__init__
