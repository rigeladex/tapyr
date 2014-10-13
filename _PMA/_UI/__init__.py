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
#    PMA.UI.__init__
#
# Purpose
#    Package providing User Interface for PMA
#
# Revision Dates
#    29-Mar-2005 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL.Package_Namespace import Derived_Package_Namespace
from   _PMA                   import PMA
from   _TGL                   import TGL
import _TGL._UI

UI = Derived_Package_Namespace (parent = TGL.UI)

PMA._Export ("UI")

del Derived_Package_Namespace

### __END__ PMA.UI.__init__
