# -*- coding: utf-8 -*-
# Copyright (C) 2024 Christian Tanzer All rights reserved
# tanzer@gg32.com.
# #*** <License> ************************************************************
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.gg32.com/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    RTS
#
# Purpose
#    Repeated task scheduler
#
# Revision Dates
#     1-Mar-2024 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL                     import TFL
from   _CAL                     import CAL
from   _LNX                     import LNX

import _CAL.Date_Time
import _CAL.Relative_Delta

import _TFL.CAO
import _TFL._Meta.Object

import subprocess
import time

class _Repeated_Task_ (TFL.Meta.Object) :

    job_name    = "repeated job"
    max_runs    = 0
    _now        = None
    _runs       = None
    _stop       = False

    def __init__ (self, start, period_delta, verbose = False, ** kwds) :
        self.start          = start
        self.period_delta   = period_delta
        self.verbose        = verbose
        self.__dict__.update  (kwds)
        if isinstance (start, CAL.Date_Time) :
            self.start_time = start
            self.next_time  = start
        else :
            self.start_time = CAL.Date_Time ()
            self.next_time  = self.start_time + start
        self.adjust_next_time ()
    # end def __init__

    @property
    def delay (self) :
        return (self.next_time - CAL.Date_Time ()).total_seconds
    # end def delay

    @property
    def stop (self) :
        r  = self._runs
        mx = self.max_runs
        return self._stop or (mx and (r or 0) > mx)
    # end def stop

    def adjust_next_time (self) :
        now = CAL.Date_Time ()
        pd  = self.period_delta
        nt  = self.next_time
        while nt < now :
            nt += pd
        self.next_time = nt
    # end def adjust_next_time

    def schedule (self, max_runs = 0) :
        self.max_runs   = max_runs
        if self._runs is None :
            self._runs  = 1
        while not self.stop :
            if self.verbose :
                print \
                    ( "Next run of", self.job_name
                    , "scheduled for", self.next_time
                    )
            self.schedule_once ()
            self._runs += 1
    # end def schedule

    def schedule_once (self) :
        delay   = self.delay
        self.next_time += self.period_delta
        if delay > 0 :
            time.sleep (delay)
        else :
            self.adjust_next_time ()
        if self.verbose :
            print ("  start", self.job_name, CAL.Date_Time (), end = ", ")
        self.run ()
        if self.verbose :
            print ("finish", CAL.Date_Time ().formatted ("%X"))
    # end def schedule_once

# end class _Repeated_Task_

class Repeated_Task (_Repeated_Task_) :
    """Repeated task

    >>> DT  = CAL.Date_Time
    >>> RD  = CAL.Relative_Delta
    >>> sd  = RD.from_string ("+1 seconds")
    >>> pd  = RD.from_string ("+5 seconds")
    >>> fun = lambda : print ("Repeated task run at", pd)
    >>> rt  = Repeated_Task  (sd, pd, fun)
    >>> rt.schedule (3)
    Repeated task run at +5 seconds
    Repeated task run at +5 seconds
    Repeated task run at +5 seconds

    """

    def __init__ (self, start, period_delta, fun, ** kwds) :
        self.fun = fun
        super ().__init__ (start, period_delta, ** kwds)
    # end def __init__

    def run (self) :
        self.fun ()
    # end def run

# end class Repeated_Task

class Repeated_Task_Shell (_Repeated_Task_) :
    """Repeated task executing a shell command.

    Usage example::

        python -m _LNX.RTS "+minute=2 second=0" "+15 minutes" -verbose \
          ./frequent_update

    """

    def __init__ (self, start, period_delta, * cmds, ** kwds) :
        if not cmds :
            raise ValueError ("Need at least one argument for `cmds`")
        self.cmd = "; ".join (cmds)
        super ().__init__ (start, period_delta, ** kwds)
    # end def __init__

    def run (self) :
        result  = subprocess.run \
            (self.cmd, shell = True, capture_output = True, text = True)
        if result.returncode != 0 :
            if result.stdout.strip () :
                print (result.stdout)
            if result.stderr.strip () :
                print (result.stderr)
    # end def run

# end class Repeated_Task_Shell

def _main (cmd) :
    start       = cmd.start
    delta       = cmd.period_delta
    shell_cmds  = cmd.argv [2:]
    job_name    = cmd.job_name or shell_cmds [0]
    rts         = Repeated_Task_Shell \
        (start, delta, * shell_cmds, verbose = cmd.verbose, job_name = job_name)
    rts.schedule (cmd.max_runs)
# end def _main

_Command = TFL.CAO.Cmd \
    ( handler       = _main
    , args          =
        ( TFL.CAO.Opt.Date_Time
            ( name          = "start"
            , description   = "Start time or relative delta for repeated job"
            )
        , TFL.CAO.Opt.Relative_Delta
            ( name          = "period_delta"
            , description   =
                "Period between runs of repeated task (relative delta)"
            )
        , "shell_cmd:S?Shell command(s) to run repeatedly"
        )
    , opts          =
        ( "-job_name:S?Name of repeated job (default: `shell_cmd`)"
        , "-max_runs:I?Maximum number to run task"
        , "-verbose:B?Print out information about runs"
        )
    , min_args      = 3
    , description   = "Run a shell command or script repeatedly"
    )

if __name__ != "__main__" :
    LNX._Export ("*")
else :
    _Command ()
### __END__ RTS

"""
Interactive test::

from _LNX.RTS import *
DT  = CAL.Date_Time
RD  = CAL.Relative_Delta
fun = lambda : print ("run at", DT (), end = ", ")
sd  = RD.from_string ("+second=10 ")
pd  = RD.from_string ("+5 seconds")
rt  = Repeated_Task (sd, pd, fun, verbose = True)
print (rt.start, rt.period_delta, rt.start_time, rt.next_time, DT ())
rt.schedule (3)

"""
