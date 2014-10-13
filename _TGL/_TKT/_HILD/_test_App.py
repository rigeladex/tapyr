# -*- coding: utf-8 -*-
# Copyright (C) 2005 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. office@spannberg.com
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
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
