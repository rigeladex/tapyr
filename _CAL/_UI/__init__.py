# -*- coding: utf-8 -*-
# Copyright (C) 2004 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    CAL.UI.__init__
#
# Purpose
#    Package providing User Interface for CAL
#
# Revision Dates
#    17-Jun-2005 (MG) Creation
#    ««revision-date»»···
#--

from   _TFL.Package_Namespace import Derived_Package_Namespace
from   _CAL                   import CAL
from   _TGL                   import TGL
import _TGL._UI

UI = Derived_Package_Namespace (parent = TGL.UI)

CAL._Export ("UI")

del Derived_Package_Namespace

### __END__ CAL.UI.__init__
