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
#    PMA.TKT.HILD.import_GTK
#
# Purpose
#    Import the classes from the GTK package into the HILD package
#
# Revision Dates
#    22-Jan-2006 (MG) Creation
#    ««revision-date»»···
#--

from   _PMA                      import PMA
import _PMA._TKT._HILD
from _PMA._TKT._GTK.Eventname import Eventname
from _PMA._TKT._GTK.Office    import Office

if __name__ != "__main__" :
    PMA.TKT.HILD._Export ("Office", "Eventname")
### __END__ PMA.TKT.HILD.import_GTK
