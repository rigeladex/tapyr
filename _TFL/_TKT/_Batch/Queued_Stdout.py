# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 Mag. Christian Tanzer. All rights reserved
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
#    TFL.TKT.Batch.Queued_Stdout
#
# Purpose
#    Provide thread-safe redirection of stdout for Batch toolkit
#
# Revision Dates
#     7-Feb-2005 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL           import TFL
import _TFL._TKT.Queued_Stdout
import _TFL._TKT._Batch

class Queued_Stdout (TFL.TKT.Queued_Stdout) :

    def write (self, text) :
        self.old_stdout.write (text)
    # end def write

    def _setup_queue (self) :
        pass ### don't need no queue for batch
    # end def _setup_queue

# end class Queued_Stdout

if __name__ != "__main__" :
    TFL.TKT.Batch._Export ("*")
### __END__ TFL.TKT.Batch.Queued_Stdout
