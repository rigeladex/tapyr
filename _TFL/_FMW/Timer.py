# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 Mag. Christian Tanzer. All rights reserved
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
#    TFL.FMW.Execution_Timer
#
# Purpose
#    Measure execution time of functions and methods without changing the
#    source code of the measured components
#
# Revision Dates
#    22-Sep-2004 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL                   import TFL
import _TFL._FMW.Recorder
import _TFL._FMW.Wrapper

import time

class Execution_Time_Recorder_F (TFL.FMW.File_Recorder) :
    """Record execution time measurements into a file"""

    format = "%(wrapper)-40s : cpu = %(cpu)s, elapsed = %(elapsed)s\n"

# end class Execution_Time_Recorder_F

class Execution_Time_Recorder_D (TFL.FMW.Dict_Recorder) :
    """Record execution time measurements into a dictionary"""

# end class Execution_Time_Recorder_D

class Execution_Time_Measurer (TFL.FMW.Wrapped_FM) :
    """Measurer of execution time of a single function or method"""

    def __init__ (self, __name__, name, fct, recorder = None) :
        self.__super.__init__ (__name__, name, fct)
        if recorder is None :
            recorder = Execution_Time_Recorder_F ()
        self.recorder = recorder
    # end def __init__

    def __call__ (self, * args, ** kw) :
        start_clock = time.clock ()
        start_time  = time.time  ()
        result      = self.fct   (* args, ** kw)
        end_clock   = time.clock ()
        end_time    = time.time  ()
        self.recorder.record \
            ( wrapper = self
            , cpu     = end_clock - start_clock
            , elapsed = end_time - start_time
            )
        return result
    # end def __call__

# end class Execution_Time_Measurer

class Execution_Timer (TFL.FMW.Wrapper) :
    """Measure execution time of functions and methods without changing the
       source code of the measured components.
    """

    Wrapped_FM = Execution_Time_Measurer

# end class Execution_Timer

if __name__ != "__main__" :
    TFL.FMW._Export ("*")
### __END__ TFL.FMW.Execution_Timer
