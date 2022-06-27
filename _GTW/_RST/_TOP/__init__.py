# -*- coding: utf-8 -*-
# Copyright (C) 2012 Christian Tanzer. All rights reserved
# tanzer@gg32.com                                      https://www.gg32.com
# ****************************************************************************
# This package is part of the package GTW.RST.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <https://www.gg32.com/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    GTW.RST.TOP.__init__
#
# Purpose
#    Framework for Tree-of-Pages, mostly RESTful
#
# Revision Dates
#     3-Jul-2012 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL.Package_Namespace import Package_Namespace
from   _GTW._RST              import RST

TOP = Package_Namespace ()
RST._Export ("TOP")

del Package_Namespace

### __END__ GTW.RST.TOP.__init__
