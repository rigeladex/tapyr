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
#    PMA.SCM.__init__
#
# Purpose
#    PMA change tracker`
#
# Revision Dates
#    15-Jan-2006 (MG) Creation
#    ««revision-date»»···
#--

from   _TFL.Package_Namespace import Package_Namespace
from   _PMA                   import PMA

SCM = Package_Namespace ()
PMA._Export ("SCM")

del Package_Namespace

### __END__ PMA.SCM.__init__
