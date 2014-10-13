# -*- coding: utf-8 -*-
# Copyright (C) 2008 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    DJO.NAV.Video
#
# Purpose
#    Model navigation for embedded video
#
# Revision Dates
#    10-Dec-2008 (CT) Creation
#    ««revision-date»»···
#--

from   _DJO                     import DJO
from   _TFL                     import TFL
import _DJO._NAV.Base

class Video (DJO.NAV.Page) :
    """Model a page containing an embedded video"""

    template = "video.html"

# end class Video

if __name__ != "__main__":
    DJO.NAV._Export ("*")
### __END__ Video


