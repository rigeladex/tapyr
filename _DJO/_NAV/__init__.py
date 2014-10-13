# -*- coding: utf-8 -*-
# Copyright (C) 2007-2008 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    DJO.NAV.__init__
#
# Purpose
#    Package with Django specific classes and functions for navigation
#
# Revision Dates
#    18-Oct-2008 (CT) Creation (factored from DJO.Navigation)
#    ««revision-date»»···
#--

from   _TFL.Package_Namespace import Package_Namespace
from   _DJO                   import DJO

NAV = Package_Namespace ()
DJO._Export ("NAV")

del Package_Namespace

### __END__ DJO.NAV.__init__
