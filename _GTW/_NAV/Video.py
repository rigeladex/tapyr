# -*- coding: utf-8 -*-
# Copyright (C) 2008-2011 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.NAV.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    GTW.NAV.Video
#
# Purpose
#    Model navigation for embedded video
#
# Revision Dates
#    10-Dec-2008 (CT) Creation
#     8-Jan-2010 (CT) Moved from DJO to GTW
#     3-Jan-2011 (CT) Introduce `template_name`
#    ««revision-date»»···
#--

from   _GTW                     import GTW
from   _TFL                     import TFL
import _GTW._NAV.Base

class Video (GTW.NAV.Page) :
    """Model a page containing an embedded video"""

    template_name = "video"

# end class Video

if __name__ != "__main__":
    GTW.NAV._Export ("*")
### __END__ GTW.NAV.Video
