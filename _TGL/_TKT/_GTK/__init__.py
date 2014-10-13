# -*- coding: utf-8 -*-
# Copyright (C) 2005 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. office@spannberg.com
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    TGL.TKT.GTK.__init__
#
# Purpose
#    Package providing GTK toolkit support for TGL
#
# Revision Dates
#    21-Mar-2005 (MG) Creation
#    25-Mar-2005 (CT) Moved to `TGL`
#    20-May-2005 (MG) `Error` added
#    10-Aug-2005 (CT) Use `set_TNS_name` instead of home-grown code
#    ««revision-date»»···
#--

from   _TFL                   import TFL
from   _TGL                   import TGL
from   _TFL.Package_Namespace import Package_Namespace
import _TGL._TKT

GTK = Package_Namespace ()
TGL.TKT._Export         ("GTK")

GTK.stop_cb_chaining = True
GTK.Error            = Exception

import _TGL._TKT.Mixin
TGL.TKT.Mixin.set_TNS_name ("GTK")

del Package_Namespace

### __END__ TGL.TKT.GTK.__init__
