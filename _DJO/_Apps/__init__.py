# -*- coding: utf-8 -*-
# Copyright (C) 2009 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    DJO.Apps.__init__
#
# Purpose
#    Package with Django applications
#
# Revision Dates
#    14-May-2009 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL.Package_Namespace import Package_Namespace
from   _DJO                   import DJO

Apps = Package_Namespace ()
DJO._Export ("Apps")

del Package_Namespace

### __END__ DJO.Apps.__init__
