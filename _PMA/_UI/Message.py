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
#    PMA.UI.Message
#
# Purpose
#    Abstract user interface for PMA.Message
#
# Revision Dates
#    29-Mar-2005 (CT) Creation
#    31-Mar-2005 (CT) Creation continued
#    16-May-2005 (CT) s/summary/outline/
#    16-May-2005 (CT) Use `Node_C` for `outline`
#    17-May-2005 (CT) `PMA.UI.Msg_Display` factored
#    25-Jul-2005 (CT) `clear` added
#    25-Jul-2005 (CT) `display` changed to call `msg.status.set_read`
#    ««revision-date»»···
#--

from   _TGL                    import TGL
from   _PMA                    import PMA

import _PMA.Message
import _PMA.Mailcap

import _PMA._UI
import _PMA._UI.HTD
import _PMA._UI.Mixin
import _PMA._UI.Msg_Display

class Message (PMA.UI.Mixin) :
    """Abstract user interface for PMA.Message"""

    def __init__ (self, AC, display_wc = None, outline_wc = None, ** kw) :
        self.__super.__init__ \
            ( AC         = AC
            , display_wc = display_wc
            , outline_wc = outline_wc
            , ** kw
            )
        self._display    = self.ANS.UI.MD_Root\
            ( AC         = AC
            , wc         = display_wc
            )
        self._outline    = self.ANS.UI.MO_Root \
            ( controlled = self._display
            , AC         = AC
            , wc         = outline_wc
            )
    # end def __init__

    def clear (self) :
        """Clear `self._display` and `self._outline`"""
        for w in self._display, self._outline :
            w.clear ()
    # end def clear

    def display (self, msg) :
        """Display `msg` in `self._display` and `self._outline`"""
        msg.status.set_read   ()
        self._display.display (msg)
        self._outline.display ()
    # end def display

# end class Message

"""
from   _PMA._UI.Message     import *
from   _TFL._UI.App_Context import App_Context
import _PMA._TKT._Tk
import _PMA._UI.HTB
import _PMA._TKT._Tk.Text
import _PMA._TKT._Tk.Butcon
import _PMA._TKT._Tk.Eventname

from   CTK import *

ac  = App_Context (PMA)
mui = Message (ac)
mui._display.tkt_text.exposed_widget.pack  (expand = YES, fill = BOTH)
mui._outline.tkt_text.exposed_widget.pack  (expand = YES, fill = BOTH)
msg = PMA.message_from_file ("/swing/private/tanzer/MH/PMA/10")
mui.display (msg)

msg = PMA.message_from_file ("/swing/private/tanzer/MH/inbox/2")
#msg = PMA.message_from_file ("/swing/private/tanzer/MH/PMA/5")
mui.display (msg)

msg = PMA.message_from_file ("/swing/private/tanzer/MH/A/70")
mui.display (msg)

"""

if __name__ != "__main__" :
    PMA.UI._Export ("*")
### __END__ Message
