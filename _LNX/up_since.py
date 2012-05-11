# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package LNX.
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
#    up_since
#
# Purpose
#    Provide the date/time at which the kernel was booted
#
# Revision Dates
#    10-Nov-2010 (CT) Creation
#    ««revision-date»»···
#--

import datetime

def up_since () :
    now = datetime.datetime.now ()
    with open ("/proc/uptime") as f :
        since = float (f.readline ().split () [0])
    return now - datetime.timedelta (seconds = since)
# end def up_since

if __name__ != "__main__" :
    from _LNX import LNX
    LNX._Export ("up_since")
else :
    print up_since ().strftime ("%Y/%m/%d %H:%M")
### __END__ up_since
