# -*- coding: utf-8 -*-
# Copyright (C) 2010-2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package LNX.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
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
