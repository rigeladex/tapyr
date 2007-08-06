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
#    TFL.FMW.Tracer
#
# Purpose
#    Provide tracing wrapper for methods and functions without changing the
#    source code of the traced components
#
# Revision Dates
#    22-Sep-2004 (CT) Creation
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ««revision-date»»···
#--



from   _TFL                   import TFL
import _TFL._FMW.Recorder
import _TFL._FMW.Wrapper

class Trace_Recorder_F (TFL.FMW.File_Recorder) :
    """Record trace information into a file"""

    format = \
        ( "%(indent)s%(wrapper)s"
          "\n%(indent)s    %(args)s, %(kw)s\n"
        )

# end class Trace_Recorder_F

class Traced (TFL.FMW.Wrapped_Recorder) :
    """Tracer of execution of a single function or method without changing the
       source code of the measured component.
    """

    Default_Recorder = Trace_Recorder_F
    level            = 0

    def __call__ (self, * args, ** kw) :
        indent = ". " * self.level
        self.recorder.record \
            ( wrapper   = self
            , args      = args + self.args
            , kw        = dict (kw, ** self.kw)
            , indent    = indent
            )
        self.__class__.level += 1
        try :
            result = self.fct (* args, ** kw)
        finally :
            self.__class__.level -= 1
        return result
    # end def __call__

# end class Traced

class Tracer (TFL.FMW.Wrapper) :
    """Trace execution of functions and methods without changing the
       source code of the measured components."""

    Wrapped_FM = Traced

# end class Tracer

if __name__ != "__main__" :
    TFL.FMW._Export ("*")
### __END__ TFL.FMW.Tracer
