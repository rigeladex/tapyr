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
#    TFL.TKT.Tk.HTB_test
#
# Purpose
#    Test for TFL.UI.HTB
#
# Revision Dates
#    25-Feb-2005 (RSC) Refactored into TFL.UI.HTB_test
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ««revision-date»»···
#--



from   CT_TK                import root, YES, BOTH
from   _TFL                 import TFL
import _TFL._UI.HTB
from   _TFL._UI.HTB_test    import insert_stuff
from   _TFL._UI.App_Context import App_Context

import _TFL._TKT._Tk
import _TFL._TKT._Tk.Text
import _TFL._TKT._Tk.Butcon

if __name__ == "__main__" :
    AC = App_Context (TFL)

    tb  = TFL.UI.HTB.Browser (AC, name = 'huhu')
    tb.text.exposed_widget.pack  (expand = YES, fill = BOTH)
    insert_stuff (tb)
    tb.text.exposed_widget.mainloop ()
