# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. office@spannberg.com
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
#    _test_PMA
#
# Purpose
#    Test the PMA stuff for GTK
#
# Revision Dates
#    18-May-2005 (MG) Creation
#    ««revision-date»»···
#--

from   _TGL                   import TGL
from   _PMA                   import PMA
from   _TFL.Command_Line      import Command_Line
import _PMA._UI
import _PMA._TKT
import _PMA._UI.Message
import _PMA.Mailbox

from   _TGL._UI.App_Context   import App_Context
import _TGL._TKT._GTK.V_Box
import _PMA._UI.HTB
import _PMA._TKT._GTK.Text
import _PMA._TKT._GTK.Butcon
import _PMA._TKT._GTK.Eventname
import _PMA._TKT._GTK.Test_Window
import _PMA._TKT._GTK.Paned
import _PMA._TKT._GTK.Tree
import _PMA._TKT._GTK.Tree_View_Column
import _PMA._TKT._GTK.Cell_Renderer_Text
import _PMA._TKT._GTK.Model
import _PMA._TKT.Tree_Adapter

class Folder_Tree (PMA.TKT.Tree_Adapter) :

    schema = \
        ( PMA.TKT.Column
            ("Folder", PMA.TKT.Text_Cell ("name"))
        ,
        )

    def has_children (self, element) :
        return element.sub_boxes
    # end def has_children

    def children (self, element) :
        return element.sub_boxes
    # end def children

# end class Folder_Tree

class Folder_Summary (PMA.TKT.Tree_Adapter) :

    schema = \
        ( PMA.TKT.Column ("No",      PMA.TKT.Text_Cell ("number"))
        , PMA.TKT.Column ("Sender",  PMA.TKT.Text_Cell ("sender"))
        , PMA.TKT.Column ("Subject", PMA.TKT.Text_Cell ("subject"))
        , PMA.TKT.Column ("Date",    PMA.TKT.Text_Cell ("date"))
        )

    def has_children (self, element) :
        return False
    # end def has_children

    def children (self, element) :
        return element.messages
    # end def children

# end class Folder_Summary

GTK = TGL.TKT.GTK

AC  = App_Context     (PMA)
win = GTK.Test_Window ("PMA Test", AC = AC)
psd = GTK.V_Paned     (AC = AC)
pfo = GTK.V_Paned     (AC = AC)
p_h = GTK.H_Paned     (pfo, psd, AC = AC)
win.add               (p_h)

mui = PMA.UI.Message (AC)
psd.pack_bottom (mui._display.tkt_text.exposed_widget)
pfo.pack_bottom (mui._outline.tkt_text.exposed_widget )

cmd = Command_Line (option_spec = ("mailbox:S=/home/lucky/PMA_Test/Testbox", ))
mb  = PMA.Mailbox  (cmd.mailbox)

ft = Folder_Tree   (mb, AC = AC, lazy = False)
fs = Folder_Summary(mb.sub_boxes [1], AC = AC, lazy = False)
pfo.pack_top (ft.tkt)
psd.pack_top (fs.tkt)


msg = mb.messages [0]
mui.display           (msg)
win.show_all          ()
GTK.main              ()
### __END__ _test_PMA


