# -*- coding: iso-8859-15 -*-
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
AC  = App_Context (TGL)

win = GTK.Test_Window ("Test the Command Interfacers", AC = AC)
bo  = GTK.V_Box       ()
bu1 = GTK.Button      (label = "Dummy 1")
bu2 = GTK.Button      (label = "Dummy 2")
bo.pack               (bu2, start = False)
bo.pack               (bu1, start = False)
win.add               (bo)

def _dummy (* args) :
    print "Dummy", args

inter   = dict \
    ( cm = GTK.CI_Menu       (AC = AC, accel_group = win.accel_group)
    , mb = GTK.CI_Menubar    (AC = AC, accel_group = win.accel_group)
    , tb = GTK.CI_Toolbar    (AC = AC)
    , bb = GTK.CI_Button_Box (AC = AC)
    )
bo.pack (inter ["tb"])
bo.pack (inter ["mb"])
bo.pack (inter ["bb"])#, where = GTK.END)
cmd_mgr = TGL.UI.Command_Mgr (AC, 0, inter)
g1      = cmd_mgr.add_group \
    ("File", if_names = ("cm:click_3", "mb", "tb", "bb"))
cmd_mgr.bind_interfacers (bu1)
g2      = cmd_mgr.add_group \
    ("Edit", if_names = ("cm:click_3", "mb", "tb", "bb"))
cmd_mgr.bind_interfacers (bu2)
for g, spec in ( (g1, ( ("Open", "gtk-open", "<Ctrl>O")
                      , ("Save", "gtk-save", "<Ctrl>s")
                      , (None,   "",         None)
                      , ("Exit", "gtk-quit", None)
                      )
                  )
               , (g2, ( ("Copy",       "gtk-copy",  None)
                      , ("Cut",        "gtk-cut",   None)
                      , ("Paste",      "gtk-paste", None)
                      , (None,         "",          None)
                      , ("Select_Foo", "gtk-find", None)
                      )
                 )
               ) :
    prec = lambda * args : False
    prec.evaluate_eagerly = True
    for n, i, a in  spec :
        if not n :
            g.add_separator (if_names = ("cm", "mb", "tb"))
        else :
            if i == "gtk-find" :
                as_check_button = True
                cmd             = None
            else :
                as_check_button = False
                cmd             = _dummy
            g.add_command \
                ( TGL.UI.Command (n, cmd, precondition = prec)
                , if_names        = ("cm", "mb", "tb", "bb")
                , icon            = i
                , as_check_button = as_check_button
                , accelerator     = a
                )
        prec = lambda * args : True
        prec.evaluate_eagerly = True

g3 = g2.add_group ("Submenu", if_names = ("mb", "cm", "tb"), icon = "gtk-apply")
def _dummy (* args) :
    print "Submenu"
# end def _dummy

g3.add_command \
    ( TGL.UI.Command ("Item 1", _dummy, precondition = prec)
    , if_names = ("mb", "cm", "tb")
    )
g3.add_command \
    ( TGL.UI.Command ("Item 2", _dummy, precondition = prec)
    , if_names = ("mb", "cm", "tb")
    )
g3.add_command \
    ( TGL.UI.Command ("Item 4", None, precondition = prec)
    , if_names = ("mb", "cm", "tb")
    , as_check_button = True
    )
cmd_mgr.set_auto_short_cuts ()
cmd_mgr.update_state        ()
win.show_all                ()
GTK.main                    ()
### __END__ TGL.TKT.GTK._test_Cmd_Mgr
