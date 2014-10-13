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
#    TGL.TKT.Tk.__init__
#
# Purpose
#    Package providing Tk toolkit support for TGL
#
# Revision Dates
#    22-Mar-2005 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL.Package_Namespace import Derived_Package_Namespace
from   _TFL                   import TFL
from   _TGL                   import TGL
import _TFL._TKT._Tk
import _TGL._TKT

Tk = Derived_Package_Namespace (parent = TFL.TKT.Tk)
TGL.TKT._Export ("Tk")

del Derived_Package_Namespace

### __END__ TGL.TKT.Tk.__init__
