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

GTK = TGL.TKT.GTK

AC  = App_Context     (PMA)
win = GTK.Test_Window ("PMA Test", AC = AC)
b   = GTK.V_Box       ()
win.add               (b)
b.show                ()

mui = PMA.UI.Message (AC)
b.pack (mui._display.tkt_text.exposed_widget)
b.pack (mui._outline.tkt_text.exposed_widget )

msg = PMA.message_from_file ("/home/lucky/PMA_Test/MH/customer/HS/3")
mui.display (msg)
win.show_all              ()
GTK.main              ()
### __END__ _test_PMA


