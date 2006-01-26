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
#    TGL.TKT.HILD._test_Cmd_Mgr
#
# Purpose
#    Simple test of the hildon wrapper
#
# Revision Dates
#    21-Jan-2006 (MG) Creation
#    ««revision-date»»···
#--

from   _TGL                   import TGL
import _TGL._UI
from   _TGL._UI.App_Context   import App_Context
import _TGL._TKT._HILD.App
import _TGL._TKT._HILD.App_View

HILD = TGL.TKT.HILD

AC   = App_Context   (TGL)
app  = HILD.App      (AC = AC)
view = app.view
app.title          = 'Foo'
view.title         = 'Bar'
app.two_part_title = True
app.show           ()
print app.view.vbox, app.view.menu
#TGL.TKT.GTK.main   ()

### __END__ TGL.TKT.GTK._test_Cmd_Mgr
