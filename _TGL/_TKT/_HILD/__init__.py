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
#    TGL.TKT.HILD.__init__
#
# Purpose
#    Package providing hildon toolkit support for TGL
#
# Revision Dates
#    21-Jan-2006 (MG) Creation
#    ««revision-date»»···
#--

from   _TFL                   import TFL
from   _TGL                   import TGL
from   _TFL.Package_Namespace import Derived_Package_Namespace
import _TGL._TKT
import _TGL._TKT._GTK

HILD = Derived_Package_Namespace (parent = TGL.TKT.GTK)
TGL.TKT._Export         ("HILD")

import _TGL._TKT.Mixin
TGL.TKT.Mixin.set_TNS_name ("HILD", override = "GTK")

del Derived_Package_Namespace

import hildon
HILD.hildon = hildon

### __END__ TGL.TKT.HILD.__init__
