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
#    TGL.TKT.GTK._test_Bindings
#
# Purpose
#    Simple test of the event-binding
#
# Revision Dates
#    31-Mar-2005 (MG) Creation
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Eventname
import _TGL._TKT._GTK.Test_Window
import _TGL._TKT._GTK.Button
import _TGL._TKT._GTK.V_Box

w  = GTK.Test_Window ("Binding Rest")
bo = GTK.V_Box       ()
b1 = GTK.Button      (label = "Button 1")
b2 = GTK.Button      (label = "Button 2")
bo.add               (b1)
bo.add               (b2)
w .add               (bo)
w.show_all           ()

def cb (event, * args) :
    print event.widget, args
# end def cb

b1.bind_add          (GTK.Eventname.click_1,        cb, "sc1")
b1.bind_add          (GTK.Eventname.triple_click_3, cb, "tc1")
b2.bind_add          (GTK.Eventname.click_3,        cb, "sc3")
b2.bind_add          (GTK.Eventname.double_click_2, cb, "dc2")
b2.bind_add          (GTK.Eventname.cursor_home,    cb, "home")
GTK.main             ()
### __END__ TGL.TKT.GTK._test_Bindings


