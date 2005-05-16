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

    def __init__ (self, AC, display_wc = None, outline_wc = None, ** kw) :
        self.__super.__init__ \
            ( AC         = AC
            , display_wc = display_wc
            , outline_wc = outline_wc
            , ** kw
            )
        self._display    = self.ANS.UI.HTD.Root\
            ( AC         = AC
            , wc         = display_wc
            )
        self._outline    = self.ANS.UI.HTD.Root \
            ( AC         = AC
            , wc         = outline_wc
            )
    # end def __init__

    def display (self, msg) :
        """Display `msg` in `self.display` and `self.outline`"""
        display = self._display
        outline = self._outline
        Node    = self.ANS.UI.HTD.Node
        Node_C  = self.ANS.UI.HTD.Node_C
        display.clear ()
        outline.clear ()
        for p in msg.part_iter () :
            body = p.body_lines ()
            if body == () :
                d, o = display, outline
            else :
                d = Node \
                    ( parent   = display
                    , contents = "\n".join (body)
                        ### XXX use type-specific renderer here
                    )
                o = Node_C \
                    ( controlled = d
                    , parent     = outline
                    , contents   = p.summary ()
                    )
            self._add_parts (d, o, p)
    # end def display

    def _add_parts (self, disp, outl, msg) :
        Node    = self.ANS.UI.HTD.Node_B2
        Node_C  = self.ANS.UI.HTD.Node_C
        for p in msg.part_iter () :
            type = p.type
            if type.upper ().startswith ("X-PMA") :
                type = ""
            body = p.body_lines ()
            if body == () :
                d, o = disp, outl
            else :
                d = Node \
                    ( parent   = disp
                    , contents =
                        ### XXX use type-specific renderer here
                        ( ("%s %s %s" % (p.name, type, p.filename), )
                        , (u"\n".join (body), )
                        )
                    )
                o = Node_C \
                    ( controlled = d
                    , parent     = outl
                    , contents   = p.summary ()
                    )
            if type == "text/plain" :
                d.inc_state ()
            self._add_parts (d, o, p)
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
mui._outline.tkt_text.exposed_widget.pack  (expand = YES, fill = BOTH)
msg = PMA.message_from_file ("/swing/private/tanzer/MH/PMA/1")
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
