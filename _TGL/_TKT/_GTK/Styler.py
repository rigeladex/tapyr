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
#    TGL.TKT.GTK.Styler
#
# Purpose
#    Base styler for GTK
#
# Revision Dates
#     2-Apr-2005 (MG) Creation
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
from   _TFL                   import TFL
import _TFL._TKT.Styler

class _TKT_GTK_Styler_ (TFL.TKT.Styler) :

    _real_name = "Styler"

Styler = _TKT_GTK_Styler_ # end class _TKT_GTK_Styler_

if __name__ != "__main__" :
    GTK._Export ("Styler")
### __END__ TGL.TKT.GTK.Styler
