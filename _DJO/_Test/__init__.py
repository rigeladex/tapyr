# -*- coding: utf-8 -*-
# Copyright (C) 2008 Martin Gl<FC>ck All rights reserved
# Langstrasse 4, 2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    DJO.Test.__init__
#
# Purpose
#    Package for extening the standard django test capabilites
#
# Revision Dates
#     7-Oct-2008 (MG) Creation
#    ««revision-date»»···
#--

from   _TFL.Package_Namespace import Package_Namespace
from   _DJO                   import DJO

Test = Package_Namespace ()

DJO._Export ("Test")

del Package_Namespace

### __END__ DJI.Test.__init__
