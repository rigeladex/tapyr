# -*- coding: utf-8 -*-
# Copyright (C) 2008 Mag. Christian Tanzer. All rights reserved
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


