# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 Mag. Christian Tanzer. All rights reserved
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
#    Execution_Timer
#
# Purpose
#    Measure execution time of functions and methods without changing the
#    source code of the measured components
#
# Revision Dates
#     5-Jul-2004 (CT) Creation
#    15-Jul-2004 (CT) `Execution_Timer.add_method` changed to use
#                     `new.instancemethod` instead of an ad-hoc function
#    15-Jul-2004 (CT) `Execution_Timer._measurer` factored from `add_method`
#                     and `add_function`
#    ««revision-date»»···
#--

from   _TFL import TFL
import _TFL._Meta.Object

import new
import sys
import time

class Execution_Time_Recorder_F (TFL.Meta.Object) :
    """Record execution time measurements into a file"""

    format = "%-40s : cpu = %s, elapsed = %s\n"

    def __init__ (self, file = None, format = None) :
        self.file   = file
        if format is not None :
            self.format = format
    # end def __init__

    def record (self, measurer, cpu, elapsed) :
        file = self.file or sys.stdout
        file.write (self.format % (measurer.name, cpu, elapsed))
    # end def record

# end class Execution_Time_Recorder_F

class Execution_Time_Recorder_D (TFL.Meta.Object) :
    """Record execution time measurements into a dictionary"""

    def __init__ (self) :
        self.dict = {}
    # end def __init__

    def record (self, measurer, cpu, elapsed) :
        self.dict.setdefault (measurer.name, []).append ((cpu, elapsed))
    # end def record

# end class Execution_Time_Recorder_D

class Execution_Time_Measurer (TFL.Meta.Object) :
    """Measurer of execution time of a single function or method"""

    def __init__ (self, __name__, name, fct, recorder) :
        self.__name__ = __name__
        self.__doc__  = getattr (fct, "__doc__", None)
        self.name     = name
        self.fct      = fct
        self.recorder = recorder
    # end def __init__

    def __call__ (self, * args, ** kw) :
        start_clock = time.clock ()
        start_time  = time.time  ()
        result      = self.fct   (* args, ** kw)
        end_clock   = time.clock ()
        end_time    = time.time  ()
        self.recorder.record \
            (self, end_clock - start_clock, end_time - start_time)
        return result
    # end def __call__

# end class Execution_Time_Measurer

class Execution_Timer (TFL.Meta.Object) :
    """Measure execution time of functions and methods without changing the
       source code of the measured components.
    """

    def __init__ (self, recorder = None) :
        if recorder is None :
            recorder = Execution_Time_Recorder_F ()
        self.recorder = recorder
    # end def __init__

    def add_function (self, module, name) :
        """Add measurer for function with `name` of module od package-namespace
           `module`.
        """
        setattr (module, name, self._measurer (module, name))
    # end def add_function

    def add_method (self, cls, name) :
        """Add measurer for method with `name` of class `cls`"""
        measurer = self._measurer (cls, name)
        setattr (cls, name, new.instancemethod (measurer, None, cls))
    # end def add_method

    def _measurer (self, cm, name) :
        qname  = "%s.%s" % (cm.__name__, name)
        fct    = getattr (cm, name)
        return Execution_Time_Measurer (name, qname, fct, self.recorder)
    # end def _measurer

# end class Execution_Timer

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ Execution_Timer
