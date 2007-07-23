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
#    TFL.TKT.Queued_Stdout
#
# Purpose
#    Provide thread-safe redirection of stdout
#
# Revision Dates
#     7-Feb-2005 (CT) Creation (factored from CTK_Queued_Stdout)
#     3-Jun-2005 (MG) `event` parameter added to `update`
#    23-Jul-2007 (CED) Activated absolute_import
#    ��revision-date�����
#--
from __future__ import absolute_import


from   _TFL           import TFL
import _TFL._TKT.Mixin

import Queue
import sys

class _Queued_Stdout_ (TFL.TKT.Mixin) :
    """Provide thread-safe redirection of stdout"""

    _real_name = "_Queued_Stdout_"

    def __init__ (self, out_widget = None, redirect_stderr = True) :
        self._setup_queue ()
        self.out_widget = out_widget
        self.old_stdout = sys.stdout
        sys.stdout      = self
        self._pending   = None
        if redirect_stderr :
            self.old_stderr = sys.stderr
            sys.stderr      = self
    # end def __init__

    def destroy (self) :
        try :
            if sys.stdout is self :
                sys.stdout  = self.old_stdout
            if sys.stderr is self :
                sys.stderr  = self.old_stderr
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
