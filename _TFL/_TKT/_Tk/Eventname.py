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
#    24-Jan-2005 (CT) Creation continued
#    17-Feb-2005 (MG) `double_click_*` added
#    ««revision-date»»···
#--

from   _TFL                 import TFL
import _TFL._TKT._Tk
import _TFL._TKT.Eventname

Eventname = TFL.TKT._Eventname \
    ( check_everything         = "<F7>"
    , click_1                  = "<ButtonRelease-1>"
    , click_2                  = "<ButtonRelease-2>"
    , click_3                  = "<ButtonRelease-3>"
    , close_window             = "<Control-Key-w>"
    , commit                   = "<Control-Key-Return>"
    , complete                 = "<Alt-i>"
    , continue_scan            = "<B2-Motion>"
    , copy                     = "<Control-Key-c>"
    , cut                      = "<Control-Key-x>"
    , double_click_1           = "<Double-Button-1>"
    , double_click_2           = "<Double-Button-2>"
    , double_click_3           = "<Double-Button-3>"
    , edit_schedule            = "<F4>"
    , exit                     = "<Control-Key-q>"
    , help                     = "<F1>"
    , history_complete         = "<Alt-q>"
    , history_next             = "<Alt-Down>"
    , history_previous         = "<Alt-Up>"
    , make_schedule            = "<F5>"
    , new                      = "<Control-Key-n>"
    , open                     = "<Control-Key-o>"
    , paste                    = "<Control-Key-v>"
    , Print                    = "<Control-Key-p>"
    , redo                     = "<Control-Key-y>"
    , rename                   = "<F2>"
    , save                     = "<Control-Key-s>"
    , save_and_exit            = "<Control-Key-e>"
    , save_as                  = "<Control-Key-S>"
    , search                   = "<Control-Key-f>"
    , search_next              = "<F3>"
    , search_prev              = "<Shift-F3>"
    , select_all               = "<Control-Key-a>"
    , start_scan               = "<ButtonPress-2>"
    , undo                     = "<Control-Key-z>"
    )

if __name__ != "__main__" :
    TFL.TKT.Tk._Export ("Eventname")
### __END__ TFL.TKT.Tk.Eventname
