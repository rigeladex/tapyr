# -*- coding: utf-8 -*-
# Copyright (C) 2010-2022 Mag. Christian Tanzer All rights reserved
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
#    LNX.up_since
#
# Purpose
#    Provide the date/time at which the kernel was booted
#
# Revision Dates
#    10-Nov-2010 (CT) Creation
#    22-Mar-2018 (CT) Make Python-3 compatible
#    26-Jan-2022 (CT) Add support for parsing output of `uptime` command
#                     - in case `/proc/uptime` isn't available
#    ««revision-date»»···
#--

from   _TFL           import sos
import datetime

if sos.path.exists ("/proc/uptime") :
    def uptime_seconds () :
        with open ("/proc/uptime") as f :
            return float (f.readline ().split () [0])
else :
    from   _TFL.Regexp import Regexp, re
    import subprocess
    spu = dict \
        ( days         = 86400
        , hours        =  3600
        , minutes      =    60
        , seconds      =     1
        )
    uptime_pat = Regexp \
        ( r"\s+ [0-9:]+ \s+ up \s+"
          r"(?P<days>  \d+) \s+ days \s+"
          r"(?P<hours> \d+):(?P<minutes> \d+)(?: :(?P<seconds> \d+))?"
        , re.VERBOSE
        )
    def uptime_seconds () :
        uptime_res = subprocess.run \
            ( ["uptime"]
            , capture_output = True
            , text           = True
            )
        if uptime_pat.match (uptime_res.stdout) :
            result = sum \
                (   float (v) * spu [u]
                for u, v in uptime_pat.groupdict ().items () if v
                )
            return result

def up_since () :
    now   = datetime.datetime.now ()
    delta = uptime_seconds ()
    return now - datetime.timedelta (seconds = delta)
# end def up_since

if __name__ != "__main__" :
    from _LNX import LNX
    LNX._Export ("up_since")
else :
    print (up_since ().strftime ("%Y/%m/%d %H:%M"))
### __END__ LNX.up_since
