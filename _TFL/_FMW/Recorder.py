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
#    TFL.FMW.Recorder
#
# Purpose
#    Model wrapper for functions and methods
#
# Revision Dates
#    22-Sep-2004 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL                   import TFL
import _TFL._FMW
import _TFL._Meta.Object

import sys

class File_Recorder (TFL.Meta.Object) :
    """Record wrapper calls into a file"""

    def __init__ (self, file = None, format = None) :
        self.file   = file
        if format is not None :
            self.format = format
    # end def __init__

    def record (self, ** kw) :
        file = self.file or sys.stdout
        file.write (self.format % kw)
    # end def record

# end class File_Recorder

class Dict_Recorder (TFL.Meta.Object) :
    """Record wrapper calls into a dictionary"""

    def __init__ (self) :
        self.dict = {}
    # end def __init__

    def record (self, ** kw) :
        self.dict.setdefault (kw ["wrapper"].name, []).append (kw)
    # end def record

# end class Dict_Recorder

if __name__ != "__main__" :
    TFL.FMW._Export ("*")
### __END__ TFL.FMW.Recorder



