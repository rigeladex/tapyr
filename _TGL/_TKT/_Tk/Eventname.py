# -*- coding: iso-8859-15 -*-
# Copyright (C) 2005 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
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
#    TGL.TKT.Tk.Eventname
#
# Purpose
#    Provide symbolic names for Tkinter events (keys, mouse clicks, ...)
#
# Revision Dates
#    31-Mar-2005 (CT) Creation
#     1-Apr-2005 (CT) Bindings changed to use `Alt-<letter>` instead of
#                     `Alt-Cursor` keys
#    ««revision-date»»···
#--

"""
Consistency check:

>>> from   _TGL                       import TGL
>>> import _TGL._TKT
>>> import _TGL._TKT.Eventname
>>> import _TGL._TKT._Batch.Eventname
>>> import _TGL._TKT._Tk.Eventname
>>> TGL.TKT._Eventname.check_names (TGL.TKT.Batch.Eventname, TGL.TKT.Tk.Eventname)
_TGL._TKT._Tk.Eventname defines all names that _TGL._TKT._Batch.Eventname defines
_TGL._TKT._Batch.Eventname defines all names that _TGL._TKT._Tk.Eventname defines

"""

from   _TFL                 import TFL
from   _TGL                 import TGL
import _TFL._TKT._Tk.Eventname
import _TGL._TKT._Tk

Eventname = TFL.TKT._Eventname \
    (  ** dict \
        ( TFL.TKT.Tk.Eventname._map
        , node_down            = "<Alt-n>"
        , node_end             = "<Alt-e>"
        , node_home            = "<Alt-a>"
        , node_left            = "<Alt-b>"
        , node_right           = "<Alt-f>"
        , node_up              = "<Alt-p>"
        , triple_click_1       = "<Triple-Button-1>"
        , triple_click_2       = "<Triple-Button-2>"
        , triple_click_3       = "<Triple-Button-3>"
        )
    )

if __name__ != "__main__" :
    TGL.TKT.Tk._Export ("Eventname")
### __END__ TGL.TKT.Tk.Eventname
