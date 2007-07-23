# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 Mag. Christian Tanzer. All rights reserved
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
#    TFL.TKT.Batch.Eventname
#
# Purpose
#    Provide symbolic names for UI events (even if none are needed in batch
#    mode)
#
# Revision Dates
#    26-Jan-2005 (CT) Creation
#    17-Feb-2005 (MG) `double_click_*` added
#    22-Feb-2005 (CT) Names `any_(enter|leave)` and `focus_(enter|leave)` added
#    22-Feb-2005 (RSC) mouse_motion, cursor movement and open_ close_ events
#    23-Feb-2005 (CT)  `mouse_enter` and `mouse_leave` reintroduced
#     3-Mar-2005 (RSC) `Print_all` added
#    23-Jul-2007 (CED) Activated absolute_import
#    ««revision-date»»···
#--
from __future__ import absolute_import


from   _TFL                 import TFL
import _TFL._TKT._Batch
import _TFL._TKT.Eventname

Eventname = TFL.TKT._Eventname \
    ( any_enter                = None
    , any_leave                = None
    , check_everything         = None
    , click_1                  = None
    , click_2                  = None
    , click_3                  = None
    , close_node_1             = None
    , close_node_all           = None
    , close_node               = None
    , close_window             = None
    , commit                   = None
    , complete                 = None
    , continue_scan            = None
    , copy                     = None
    , cursor_down              = None
    , cursor_end               = None
    , cursor_home              = None
    , cursor_left              = None
    , cursor_right             = None
    , cursor_up                = None
    , cut                      = None
    , double_click_1           = None
    , double_click_2           = None
    , double_click_3           = None
    , edit_schedule            = None
    , exit                     = None
    , focus_enter              = None
    , focus_leave              = None
    , help                     = None
    , history_complete         = None
    , history_next             = None
    , history_previous         = None
    , make_schedule            = None
    , mouse_enter              = None
    , mouse_leave              = None
    , mouse_motion             = None
    , new                      = None
    , open_node_1              = None
    , open_node_all            = None
    , open_node                = None
    , open                     = None
    , paste                    = None
    , Print                    = None
    , Print_all                = None
    , redo                     = None
    , rename                   = None
    , save                     = None
    , save_and_exit            = None
    , save_as                  = None
    , search                   = None
    , search_next              = None
    , search_prev              = None
    , select_all               = None
    , start_scan               = None
    , undo                     = None
    )

if __name__ != "__main__" :
    TFL.TKT.Batch._Export ("Eventname")
### __END__ TFL.TKT.Batch.Eventname
