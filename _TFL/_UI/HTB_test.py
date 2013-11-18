# -*- coding: utf-8 -*-
# Copyright (C) 2005 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
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
#     7-Mar-2005 (RSC) Added background color (using "found" style)
#    14-Mar-2005 (RSC) New test for a wrapped line
#    14-Mar-2005 (RSC) Wrapped-line test for non-root node.
#    14-Mar-2005 (RSC) Yet another test that now reproduces problem with
#                      line-wrapping
#    14-Mar-2005 (RSC) `nowrap` tags changed to wrap -- left only one
#                      nowrap for testing.
#    15-Mar-2005 (RSC) Changed one test-case to get an auto-wrap for
#                      testing lmargin1/lmargin2
#    15-Mar-2005 (RSC) Added test for hyper-link in `name` of a node
#    21-Mar-2005 (RSC) Added test for `head_open` parameter
#    29-Mar-2005 (CT)  s/head_open/header_open/g
#    29-Mar-2005 (CT)  `mknode_2` added and used to test empty `header_open`
#    14-Apr-2005 (CT)  `bot_pos`, `eot_pos`, and `current_pos` replaced by
#                      `buffer_head`, `buffer_tail`, and `insert_mark`,
#                      respectively
#    20-Apr-2005 (MZO) update doctest (added necessary imports)
#    20-Apr-2005 (MZO) update test - tail/head_contents
#     5-Sep-2005 (MZO) fixed import
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ««revision-date»»···
#--



from   _TFL                 import TFL
import _TFL._UI
import _TFL._UI.HTB
from   _TFL._UI.App_Context import App_Context

class T :
    name = "test"
    def __init__ (self, name = None) :
        if name :
            self.name = name
# end class T

o = (T (), T ('s2'), T ('ss1'))

class My_Linked (TFL.UI.HTB.Node_Linked) :
    def follow (self, o, event = None) :
        print "clicked: %s" % o.name
        self.__super.follow (o, event)
    # end def follow

    def new_child (self, name, header = "", contents = "", o_links = ()) :
        c = self.__super.new_child (name, header, contents)
        c.o_links = o_links
        return c
    # end def new_child
# end class My_Linked

def mknode (tb, name, * tags) :
    n = My_Linked \
        ( tb
        , name
        , "1. test line\n2. test line\n3. test line"
        , header_open = "4. test Line\n5. test Line\n6. test Line"
        , o_links = o
        )
    n.insert (tb.insert_mark, * tags)
    return n
# end def mknode

def mknode_2 (tb, name, * tags) :
    n = My_Linked \
        ( tb
        , name
        , "1. test line\n2. test line\n3. test line"
        , header_open = ""
        , o_links = o
        )
    n.insert (tb.insert_mark, * tags)
    return n
# end def mknode_2

def mkchild (tn, name, o_links = ()) :
    n = tn.new_child (name, "1. test line\n2. test line", o_links = o_links)
    return n
# end def mkchild

def insert_stuff (tb) :
    tb.insert            (tb.insert_mark, "**           Test me           **\n")
    tn = TFL.UI.HTB.help (tb)
    tn.insert            (tb.insert_mark, "rindent", "found")
    tn = mknode          (tb, "n1", "wrap", "found")
    x = mkchild          (tn, "s1")
    mkchild              (tn, "s2", o)
    nn = mkchild         (tn, "s3")
    mkchild              (nn, "ss1", o)
    nnn = mkchild        (nn, "ss2")
    tn = mknode_2        (tb, "n2", "wrap", "found")
    mkchild              (tn, "s-a")
    c = mkchild \
        ( tn
        , "s-b, this is a very long name which should wrap\n"
          "and display an error in formatting..."
        )
    s = " asii " * 100 + "END"
    c.new_child ("node3_with_line_break_tiii\nmytext_iii_line_asdf" + s, '', s)
    tn.open              ()
    tn = mknode          (tb, "n3", "nowrap", "found")
    mkchild              (tn, "s-x")
    # ignored by save, print, tail/head_contents
    tb.insert            (tb.insert_mark, "Middle **        Test me      **\n")
    mkchild              (tn, "s-y")
    tn = mknode \
        ( tb
        , "n4, this is a very long name which should wrap "
          "and display an error in formatting..."
        , "wrap", "found"
        )
    tb.insert            (tb.insert_mark, "END **           Test me   **\n")
# end def insert_stuff

## TGW test: see _TOM/_TKT/_TGW/HTB_test.py

"""
from _TFL import TFL
import _TFL._UI
import _TFL._UI.Command_Mgr
from _TOM import TOM
import _TFL._TKT
import _TFL._TKT._Tk.Command_Interfacer
import _TOM._UI
import _TOM._UI.Change_Counter
TFL.UI.Change_Counter = TOM.UI.Change_Counter
from _TFL._UI.HTB_test import *
import _TFL._TKT._Tk.Text
import _TFL._TKT._Tk.Butcon
AC = TFL.UI.App_Context (TFL)
AC.ui_state.gauge = None
tb = TFL.UI.HTB.Browser (AC, name = "Foo")
tb.exposed_widget.pack  ()
insert_stuff (tb)
tb.head_contents ()
tb.tail_contents ()
"""
