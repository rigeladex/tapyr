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
#    ««revision-date»»···
#--

from   _TFL                 import TFL
import _TFL._TKT._Batch
import _TFL._TKT.Eventname

Eventname = TFL.TKT._Eventname \
    ( click_1                  = None
    , click_2                  = None
    , click_3                  = None
    , close                    = None
    , copy                     = None
    , cut                      = None
    , exit_after_save          = None
    , exit_without_save        = None
    , new                      = None
    , open                     = None
    , paste                    = None
    , save                     = None
    , save_as                  = None
    , undo                     = None
    )

if __name__ != "__main__" :
    TFL.TKT.Batch._Export ("Eventname")
### __END__ TFL.TKT.Batch.Eventname
