# -*- coding: iso-8859-1 -*-
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
#    TGL.TKT.GTL._test_HTD
#
# Purpose
#    Test TGL.UI.HTD used with Tk toolkit
#
# Revision Dates
#     3-Apr-2005 (CT) Creation
#    ««revision-date»»···
#--

import _TGL._TKT._GTK
import _TGL._TKT._GTK.Butcon
import _TGL._TKT._GTK.Eventname
import _TGL._TKT._GTK.Text

from _TGL._TKT._test_HTD import *

__test__ = dict (interface_test = HTD_interface_test)

""""""
from   _TGL._UI.HTD import *
from   _TFL._UI.App_Context import App_Context
import _TGL._TKT._GTK
import _TGL._TKT._GTK.Butcon
import _TGL._TKT._GTK.Test_Window
import _TGL._TKT._GTK.Eventname
import _TGL._TKT._GTK.Text

def show (t) :
    x = t.get    ()
    y = x.rstrip ()
    print y
    print "%s characters with %s trailing whitespace" % \
          (len (x), len (x) - len (y))

nl  = chr (10)
AC  = App_Context (TGL)
r   = Root (AC, nl.join (("R.line 1", "R.line 2")))
t   = r.tkt_text
#t.exposed_widget.pack (expand = "yes", fill = "both")

n1 = Node ( r
          , ( r.Style.T ("n1.line 1 ", "yellow")
            , nl, "n1 line 2"
            , Styled ("continued", r.Style.blue)
            ))

n2 = Node_B  (r, nl.join (("n2 line 1", "n2 line 2")))
n3 = Node_B2 ( r
             , ( ["n3 closed line 1"]
               , ["n3 open line 1", nl, "n3 open line 2"])
             , r.Style.light_gray)
n3.inc_state ()

m1 = Node_B2 ( n3
             , (["m1 closed line 1"], ["m1 open line 1\nm1 open line 2"]))
m2 = Node    ( n3, ("m2 line 1", nl, "m2 line 2"))
n4 = Node_B2 ( r, ( ["n4 closed line 1"]
                  , ["n4 open line 1", nl, "n4 open line 2"])
             , r.Style.light_blue)
win = TGL.TKT.GTK.Test_Window (AC = AC)
win.add                       (r.tkt_text)
win.show_all                  ()
TGL.TKT.GTK.main              ()
""""""

### __END__ TGL.TKT.GTK._test_HTD
