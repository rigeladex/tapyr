# -*- coding: utf-8 -*-
# Copyright (C) 2007-2010 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This package is part of the package GTW.NAV.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    GTW.NAV.Test.__init__
#
# Purpose
#    Some test helpers
#
# Revision Dates
#    19-Feb-2010 (MG) Creation
#    ««revision-date»»···
#--

from   _TFL.Package_Namespace import Package_Namespace
from   _GTW                   import GTW

Test = Package_Namespace ()
GTW.NAV._Export ("Test")

del Package_Namespace

### __END__ GTW.NAV.Test.__init__
