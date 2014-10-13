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
#    TFL.SDG.__init__
#
# Purpose
#    Package modelling structured document generators
#
# Revision Dates
#    23-Jul-2004 (CT) Creation
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    26-Feb-2012 (MG) `__future__` imports added
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals
from   _TFL                   import TFL
from   _TFL.Package_Namespace import Package_Namespace

SDG = Package_Namespace ()
TFL._Export ("SDG")

del Package_Namespace

### __END__ TFL.SDG.__init__
