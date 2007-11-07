# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004-2007 Mag. Christian Tanzer. All rights reserved
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
#    CTK_Queued_Stdout
#
# Purpose
#    Provide thread-safe redirection of stdout into TK-Widget
#
# Revision Dates
#    15-Sep-2004 (CT) Creation
#    20-Sep-2004 (CT) Use `put` instead of `put_nowait` to await `Queue.Full`
#                     exceptions due to a momentarily locked queue
#    20-Sep-2004 (CT) `update` changed to reschedule itself when catching
#                     `Queue.Empty` for a locked non-empty queue
#     7-Nov-2007 (CT) Moved into package _TFL._TKT._Tk
#    ««revision-date»»···
#--

import Queue
import sys

class CTK_Queued_Stdout :
    """Provide thread-safe redirection of stdout into TK-Widget"""

    def __init__ (self, out_widget, redirect_stderr = True) :
        self.out_widget = out_widget
        self.queue      = Queue.Queue (maxsize = 0) ### `0` means unlimited
        self._pending   = None
        self.old_stdout = sys.stdout
        sys.stdout      = self
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
                self.out_widget.after_cancel (self._pending)
            self.out_widget = None
            self.Queue      = None
        except KeyboardInterrupt :
            raise
        except StandardError, exc :
            print "CTK_Queued_Stdout.destroy:", exc
    # end def destroy

    def write (self, text) :
        self.queue.put (text)
        if self._pending is None :
            self._pending = self.out_widget.after_idle (self.update)
    # end def write

    def update (self) :
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
                        pending = out_widget.after_idle (self.update)
                    break
                else :
                    out_widget.write (x)
        finally :
            self._pending = pending
    # end def update

# end class CTK_Queued_Stdout

### __END__ TFL.TKT.Tk.CTK_Queued_Stdout
