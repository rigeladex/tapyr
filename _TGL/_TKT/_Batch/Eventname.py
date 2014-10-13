# -*- coding: utf-8 -*-
# Copyright (C) 2005 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    TGL.TKT.Batch.Eventname
#
# Purpose
#    Provide symbolic names for UI events (even if none are needed in batch
#    mode)
#
# Revision Dates
#     1-Apr-2005 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL                 import TFL
from   _TGL                 import TGL
import _TFL._TKT._Batch.Eventname
import _TGL._TKT._Batch

Eventname = TFL.TKT._Eventname \
    (  ** dict \
        ( TFL.TKT.Batch.Eventname._map
        , node_down            = None
        , node_end             = None
        , node_home            = None
        , node_left            = None
        , node_right           = None
        , node_up              = None
        , triple_click_1       = None
        , triple_click_2       = None
        , triple_click_3       = None
        )
    )

if __name__ != "__main__" :
    TGL.TKT.Batch._Export ("Eventname")
### __END__ TGL.TKT.Batch.Eventname

