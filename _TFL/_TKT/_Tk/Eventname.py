# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004-2005 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.cluster
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
#    TFL.TKT.Tk.Eventname
#
# Purpose
#    Provide symbolic names for Tkinter events (keys, mouse clicks, ...)
#
# Revision Dates
#    13-Jan-2005 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL                 import TFL
import _TFL._TKT._Tk
import _TFL._TKT.Eventname

Eventname = _Eventname \
    ( click_1        = "<ButtonRelease-1>"
    , click_2        = "<ButtonRelease-2>"
    , click_3        = "<ButtonRelease-3>"
    , copy           = "<Control-Key-c>"
    , cut            = "<Control-Key-x>"
    , paste          = "<Control-Key-v>"
    )

if __name__ != "__main__" :
    TFL.TKT.Tk._Export ("Eventname")
### __END__ TFL.TKT.Tk.Eventname
