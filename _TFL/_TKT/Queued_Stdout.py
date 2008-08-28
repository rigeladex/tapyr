# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005-2008 Mag. Christian Tanzer. All rights reserved
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
#    TFL.TKT.Queued_Stdout
#
# Purpose
#    Provide thread-safe redirection of stdout
#
# Revision Dates
#     7-Feb-2005 (CT) Creation (factored from CTK_Queued_Stdout)
#     3-Jun-2005 (MG) `event` parameter added to `update`
#    27-Aug-2008 (CT) Redirection refactored to `TFL.Output.Redirect_Std`
#    ««revision-date»»···
#--

from   _TFL           import TFL
import _TFL._TKT.Mixin

import Queue
import sys

class _Queued_Stdout_ (TFL.TKT.Mixin) :
    """Provide thread-safe redirection of stdout"""

    _real_name = "_Queued_Stdout_"

    def __init__ (self, out_widget) :
        self._setup_queue ()
        self.out_widget = out_widget
        self._pending   = None
    # end def __init__

    def destroy (self) :
        try :
            if self._pending :
                self._cancel_pending ()
            self.out_widget = None
            self.Queue      = None
        except KeyboardInterrupt :
            raise
        except StandardError, exc :
            print "Queued_Stdout.destroy:", exc
    # end def destroy

    def write (self, text) :
        self.queue.put (text)
        if self._pending is None :
            self._pending = self._schedule_pending ()
    # end def write

    def update (self, event = None) :
        pending = None
        try :
            out_widget = self.out_widget
            queue      = self.queue
            while True :
                try :
                    x = queue.get_nowait ()
                except Queue.Empty :
                    ### Unfortunately, `Queue.Empty` is raised also when the
                    ### queue is locked but not empty <arrrgggh>
                    if not queue.empty () :
                        pending = self._schedule_pending ()
                    break
                else :
                    out_widget.write (x)
        finally :
            self._pending = pending
        return False
    # end def update

    def _cancel_pending (self) :
        pass
    # end def _cancel_pending

    def _schedule_pending (self) :
        pass
    # end def _schedule_pending

    def _setup_queue (self) :
        self.queue = Queue.Queue (maxsize = 0) ### `0` means unlimited
    # end def _setup_queue

Queued_Stdout = _Queued_Stdout_ # end class _Queued_Stdout_

if __name__ != "__main__" :
    TFL.TKT._Export ("*")
### __END__ TFL.TKT.Queued_Stdout
