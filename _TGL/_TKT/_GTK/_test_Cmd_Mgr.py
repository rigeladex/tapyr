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
#    TGL.TKT.GTK._test_Cmd_Mgr
#
# Purpose
#    Simple command mannager and interfaceres test
#
# Revision Dates
#     7-Apr-2005 (MG) Creation
#    ««revision-date»»···
#--

from   _TGL                   import TGL
import _TGL._UI
import _TGL._UI.Command_Mgr
from   _TGL._UI.App_Context   import App_Context
import _TGL._TKT._GTK.Command_Interfacer
import _TGL._TKT._GTK.Test_Window
import _TGL._TKT._GTK.Button
import _TGL._TKT._GTK.V_Box


GTK = TGL.TKT.GTK

win = GTK.Test_Window ("Test the Command Interfacers")
bo  = GTK.V_Box       ()
bu1 = GTK.Button      (label = "Dummy 1")
bu2 = GTK.Button      (label = "Dummy 2")
bo.pack               (bu2, start = False)
bo.pack               (bu1, start = False)
win.add               (bo)

def _dummy (* args) :
    print args

AC      = App_Context (TGL)
inter   = dict \
    ( cm = GTK.CI_Menu    (AC = AC)
    , mb = GTK.CI_Menubar (AC = AC)
    , tb = GTK.CI_Toolbar (AC = AC)
    )
bo.pack (inter ["tb"])
bo.pack (inter ["mb"])
cmd_mgr = TGL.UI.Command_Mgr (AC, 0, inter)
g1      = cmd_mgr.add_group \
    ("File", if_names = ("cm:click_3", "mb", "tb"))
cmd_mgr.bind_interfacers (bu1)
g2      = cmd_mgr.add_group \
    ("Edit", if_names = ("cm:click_3", "mb", "tb"))
cmd_mgr.bind_interfacers (bu2)
prec = lambda * args : False
prec.evaluate_eagerly = True
for n, i in ("Open", "gtk-open"), ("Save", "gtk-save"), (None, ""), ("Exit", "gtk-quit") :
    if not n :
        g1.add_separator (if_names = ("cm", "mb", "tb"))
    else :
        g1.add_command \
            ( TGL.UI.Command (n, _dummy, precondition = prec)
            , if_names = ("cm", "mb", "tb")
            , icon     = i
            )
    prec = lambda * args : True
    prec.evaluate_eagerly = True
for n, i in ("Copy", "gtk-copy"), ("Cut", "gtk-cut"), ("Paste", "gtk-paste") :
    g2.add_command \
        ( TGL.UI.Command (n, _dummy, precondition = prec)
        , if_names = ("cm", "mb", "tb")
        , icon     = i
        )
    prec = lambda * args : False
    prec.evaluate_eagerly = True

cmd_mgr.update_state     ()
win.show_all             ()
GTK.main    ()
### __END__ TGL.TKT.GTK._test_Cmd_Mgr
