# -*- coding: utf-8 -*-
# Copyright (C) 2007-2010 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This package is part of the package GTW.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    GTW.NAV.__init__
#
# Purpose
#    Model navigation on websites
#
# Revision Dates
#    18-Oct-2008 (CT) Creation (factored from DJO.Navigation)
#     8-Jan-2010 (CT) Moved from DJO to GTW
#    ««revision-date»»···
#--

from   _TFL.Package_Namespace import Package_Namespace
from   _GTW                   import GTW

NAV = Package_Namespace ()
GTW._Export ("NAV")

del Package_Namespace

### __END__ GTW.NAV.__init__
