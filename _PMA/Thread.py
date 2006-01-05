# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006 Mag. Christian Tanzer. All rights reserved
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
#    PMA.Thread
#
# Purpose
#    Implement base classes for threads used by PMA
#
# Revision Dates
#     5-Jan-2006 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL                    import TFL
from   _PMA                    import PMA

import _TFL._Meta.Object

import atexit
import sys
import threading
import time

class _Thread_ (TFL.Meta.Object, threading.Thread) :
    """Base class for PMA threads"""

    _real_name = "Thread"

    def __init__ (self, auto_start = False, ** kw) :
        self.__super.__init__ (** kw)
        if auto_start :
            self.start ()
    # end def __init__

# end class _Thread_

Thread = _Thread_

class Polling_Thread (_Thread_) :
    """Base class for PMA polling threads"""

    def __init__ (self, poll_interval = 10, ** kw) :
        self.finish         = False
        self.poll_interval  = poll_interval
        atexit.register       (setattr, self, "finish", True)
        self.__super.__init__ (** kw)
    # end def __init__

    def run (self) :
        while not self.finish :
            ### print >> sys.__stdout__, self, "run poll", time.strftime ("%H:%M:%S", time.localtime ())
            self._poll  ()
            ### print >> sys.__stdout__, "  goto sleep", time.strftime ("%H:%M:%S", time.localtime ())
            self._sleep ()
    # end def run

    def _sleep (self) :
        time.sleep (self.poll_interval)
    # end def _sleep

    def _poll (self) :
        raise NotImplemented, "%s must implement _poll" % self.__class__
    # end def _poll

# end class Polling_Thread

if __name__ != "__main__" :
    PMA._Export ("*")
### __END__ PMA.Thread
