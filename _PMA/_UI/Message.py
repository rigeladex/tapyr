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
#    ««revision-date»»···
#--

from   _TFL                    import TFL
from   _PMA                    import PMA

import _PMA.Message
import _PMA.Mailcap

import _PMA._UI
import _PMA._UI.HTB
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
        self._display    = self.ANS.UI.HTB.Browser \
            ( AC         = AC
            , wc         = display_wc
            )
        self._summary    = self.ANS.UI.HTB.Browser \
            ( AC         = AC
            , wc         = summary_wc
            )
    # end def __init__

    def display (self, msg) :
        """Display `msg` in `self.display` and `self.summary`"""
        display = self._display
        summary = self._summary
        Node    = self.ANS.UI.HTB.Node
        display.clear ()
        summary.clear ()
        for p in msg.part_iter () :
            print p.name, p.body_lines () [0:1]
            d = Node \
                ( browser  = display
                , name     = p.name
                , contents = "\n".join (p.body_lines ())
                             ### XXX use type-specific renderer here
                )
            self._add_parts (d, p)
            d.open ()
    # end def display

    def _add_parts (self, node, msg) :
        for p in msg.part_iter () :
            print p.name, list (p.body_lines ()) [0:1]
            c = node.new_child \
                ( name     = p.name
                , contents = "\n".join (p.body_lines ())
                )
    # end def _add_parts

# end class Message

"""
from   _PMA._UI.Message     import *
from   _TFL._UI.App_Context import App_Context
import _PMA._TKT._Tk
import _PMA._UI.HTB
import _PMA._TKT._Tk.Text

from   CTK import *

ac  = App_Context (PMA)
msg = PMA.message_from_file ("/swing/private/tanzer/MH/PMA/5")
mui = Message (ac)
mui._display.text.exposed_widget.pack  (expand = YES, fill = BOTH)
mui.display (msg)

"""

if __name__ != "__main__" :
    PMA.UI._Export ("*")
### __END__ Message
