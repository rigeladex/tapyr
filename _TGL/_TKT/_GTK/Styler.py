# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 TTTech Computertechnik AG. All rights reserved
# Schönbrunnerstraße 7, A--1040 Wien, Austria. office@tttech.com
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
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
