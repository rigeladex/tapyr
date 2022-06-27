# -*- coding: utf-8 -*-
# Copyright (C) 2004 Christian Tanzer. All rights reserved
# tanzer@gg32.com                                      https://www.gg32.com
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <https://www.gg32.com/license/bsd_3c.html>.
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
