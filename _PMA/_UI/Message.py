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
#    ««revision-date»»···
#--

from   _TGL                    import TGL
from   _PMA                    import PMA

import _PMA.Message
import _PMA.Mailcap

import _PMA._UI
import _PMA._UI.HTD
import _PMA._UI.Mixin

class Message (PMA.UI.Mixin) :
    """Abstract user interface for PMA.Message"""

    def __init__ (self, AC, display_wc = None, summary_wc = None, ** kw) :
        self.__super.__init__ \
            ( AC         = AC
            , display_wc = display_wc
            , summary_wc = summary_wc
            , ** kw
            )
        self._display    = self.ANS.UI.HTD.Root\
            ( AC         = AC
            , wc         = display_wc
            )
        self._summary    = self.ANS.UI.HTD.Root \
            ( AC         = AC
            , wc         = summary_wc
            )
    # end def __init__

    def display (self, msg) :
        """Display `msg` in `self.display` and `self.summary`"""
        display = self._display
        summary = self._summary
        Node    = self.ANS.UI.HTD.Node
        display.clear ()
        summary.clear ()
        for p in msg.part_iter () :
            body = p.body_lines ()
            if body == () :
                d, s = display, summary
            else :
                d = Node \
                    ( parent   = display
                    , contents = "\n".join (body)
                        ### XXX use type-specific renderer here
                    )
                s = Node \
                    ( parent   = summary
                    , contents = p.summary ()
                    )
            self._add_parts (d, s, p)
    # end def display

    def _add_parts (self, disp, summ, msg) :
        Node = self.ANS.UI.HTD.Node_B2
        for p in msg.part_iter () :
            type = p.type
            if type.upper ().startswith ("X-PMA") :
                type = ""
            body = p.body_lines ()
            if body == () :
                d, s = disp, summ
            else :
                d = Node \
                    ( parent   = disp
                    , contents =
                        ### XXX use type-specific renderer here
                        ( ("%s %s %s" % (p.name, type, p.filename), )
                        , (u"\n".join (body), )
                        )
                    )
                s = Node \
                    ( parent   = summ
                    , contents = p.summary ()
                    )
            if type == "text/plain" :
                d.inc_state ()
            self._add_parts (d, s, p)
    # end def _add_parts

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
msg = PMA.message_from_file ("/swing/private/tanzer/MH/PMA/1")
mui.display (msg)

mui._summary.tkt_text.exposed_widget.pack  (expand = YES, fill = BOTH)
msg = PMA.message_from_file ("/swing/private/tanzer/MH/inbox/2")
#msg = PMA.message_from_file ("/swing/private/tanzer/MH/PMA/5")
mui.display (msg)

msg = PMA.message_from_file ("/swing/private/tanzer/MH/A/70")
mui.display (msg)

"""

if __name__ != "__main__" :
    PMA.UI._Export ("*")
### __END__ Message
