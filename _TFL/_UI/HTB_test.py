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
#    TFL.UI.HTB_test
#
# Purpose
#    Test for TFL.UI.HTB
#
# Revision Dates
#    25-Feb-2005 (RSC) Creation from TFL.TKT.Tk.HTB_test
#    ««revision-date»»···
#--

from   _TFL                 import TFL
import _TFL._UI
import _TFL._UI.HTB
from   _TFL._UI.App_Context import App_Context

class T :
    name = "test"
# end class T

o = T ()

class My_Linked (TFL.UI.HTB.Node_Linked) :
    def follow (self, o, event = None) :
        print "clicked: %s" % o.name
        self.__super.follow (o, event)
    # end def follow
# end class My_Linked

def mknode (tb, name) :
    n = My_Linked \
        ( tb
        , name
        , "1. test line\n2. test line\n3. test line"
        , o_links = (o,)
        )
    n.insert (tb.current_pos, "nowrap")
    return n
# end def mknode

def mkchild (tn, name) :
    n = tn.new_child (name, "1. test line\n2. test line")
    return n
# end def mkchild

def insert_stuff (tb) :
    tb.insert            (tb.current_pos, "**           Test me           **\n")
    tn = TFL.UI.HTB.help (tb)
    tn.insert            (tb.current_pos, "rindent")
    tn = mknode          (tb, "n1")
    x = mkchild          (tn, "s1")
    mkchild              (tn, "s2")
    nn = mkchild         (tn, "s3")
    mkchild              (nn, "ss1")
    nnn = mkchild        (nn, "ss2")
    tn = mknode          (tb, "n2")
    mkchild              (tn, "s-a")
    mkchild              (tn, "s-b")
    tn.open              ()
    tn = mknode          (tb, "n3")
    mkchild              (tn, "s-x")
    mkchild              (tn, "s-y")
    tn = mknode          (tb, "n4")
# end def insert_stuff

"""
from _TFL._UI.HTB_test import *
import _TFL._TKT._Tk.Text
import _TFL._TKT._Tk.Butcon
tb = TFL.UI.HTB.Browser (TFL.UI.App_Context (TFL), name = "Foo")
tb.exposed_widget.pack  ()
insert_stuff (tb)

"""
