#! /swing/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2002 Mag. Christian Tanzer. All rights reserved
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
#    Field_Reader
#
# Purpose
#    Read and convert fields from the next line of a file
#
# Revision Dates
#    25-May-2002 (CT) Creation
#    ««revision-date»»···
#--

import sys

class Field_Reader :
    """Read and convert fields from the next line of a file"""

    def __init__ (self, * field_types, ** kw) :
        self.field_types = field_types
        self._file       = kw.get ("file",      sys.stdin)
        splitargs        = kw.get ("splitargs", ())
        if isinstance (splitargs, type ("")) :
            splitargs    = (splitargs, )
        self.splitargs   = splitargs
    # end def __init__

    def __call__ (self) :
        fields = self._file.readline ().split (* self.splitargs)
        return [c (f) for (c,f) in zip (self.field_types, fields)]
    # end def __call__
# end class Field_Reader

from _TFL import TFL
TFL._Export ("Field_Reader")

### __END__ Field_Reader
