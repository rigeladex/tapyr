# -*- coding: utf-8 -*-
# Copyright (C) 2006-2009 Mag. Christian Tanzer. All rights reserved
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
#    PMA.Thread
#
# Purpose
#    Implement base classes for threads used by PMA
#
# Revision Dates
#     5-Jan-2006 (CT) Creation
#    26-Jan-2006 (MG) Timeout handling implemented using a socket with timeout
#    28-Mar-2008 (CT) Explicit call to `threading.Thread.__init__` added
#                     (due to change of _TFL_Meta_Object_Root_ from 5-Mar-2008)
#    17-Jul-2009 (CT) `_check_MRO` added to avoid error from new check in
#                     _TFL_Meta_Object_Root_
#    ««revision-date»»···
#--

from   _TFL                    import TFL
from   _PMA                    import PMA

import _TFL._Meta.Object

import atexit
import sys
import threading
import socket

class _Thread_ (TFL.Meta.Object, threading.Thread) :
    """Base class for PMA threads"""

    _real_name      = "Thread"

    def __init__ (self, auto_start = False, ** kw) :
        self.__super.__init__     (** kw)
        threading.Thread.__init__ (self, ** kw)
        if auto_start :
            self.start ()
    # end def __init__

    @classmethod
    def _check_MRO (cls, args, kw) :
        """We know what we're doing and explicitly call
           `threading.Thread.__init__`.
        """
    # end def _check_MRO

# end class _Thread_

Thread = _Thread_

class Polling_Thread (_Thread_) :
    """Base class for PMA polling threads"""

    def __init__ (self, poll_interval = 10, ** kw) :
        self.finish         = False
        self.poll_interval  = poll_interval
        atexit.register       (self.quit)
        self.setup_sockets    ()
        self.__super.__init__ (** kw)
    # end def __init__

    def run (self) :
        while not self.finish :
            self._poll       ()
            try :
                self.client.recv (4) # returns after the timeout or when data
                                     # has beed written into the socket
            except socket.timeout :
                pass # we want a timeout to occure
    # end def run

    def setup_sockets (self) :
        self.server         = socket.socket \
            (socket.AF_INET, socket.SOCK_STREAM)
        self.client         = socket.socket \
            (socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind                  (("", 0)) # let the system choose
                                                    # the port
        _, port = self.server.getsockname ()  # result is ip address, port
        self.server.listen                (1) # accept owe client
        self.client.connect               (("", port)) # client connects
        self.sock, _ = self.server.accept () # get `connection socket`
        # now we are almost down, we need to set the timeout value
        self.client.settimeout            (self.poll_interval)
    # end def setup_sockets

    def quit (self) :
        self.finish = True
        self.sock.send ("Stop")
    # end def quit

    def _poll (self) :
        raise NotImplemented, "%s must implement _poll" % self.__class__
    # end def _poll

# end class Polling_Thread

if __name__ != "__main__" :
    PMA._Export ("*")
### __END__ PMA.Thread
