# -*- coding: utf-8 -*-
# Copyright (C) 2006 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    TGL.DRA.__init__
#
# Purpose
#    Package for data reduction and analysis
#
# Revision Dates
#    15-Nov-2006 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL.Package_Namespace import Package_Namespace
from   _TGL                   import TGL

DRA = Package_Namespace ()

TGL._Export ("DRA")

del Package_Namespace

### __END__ TGL.DRA.__init__
