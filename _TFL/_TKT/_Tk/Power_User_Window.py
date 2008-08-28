# -*- coding: iso-8859-1 -*-
# Copyright (C) 2008 Mag. Christian Tanzer. All rights reserved
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
#    TFL.TKT.Tk.Power_User_Window
#
# Purpose
#    Python interaction window
#
# Revision Dates
#    21-Aug-2008 (CT) Creation (factored from TTA.Power_User_Window)
#    ««revision-date»»···
#--

from   _TFL                     import TFL
from   _TFL._TKT._Tk.CTK        import *
from   _TFL._TKT._Tk.Py_Window  import Py_Window

class Power_User_Window (CTK.C_Toplevel) :

    def __init__ (self, app, globals, locals, name = None) :
        CTK.C_Toplevel.__init__  (self, app.gui, name = "python")
        self.ipreter = Py_Window (self, app.gui, globals, locals, name = name)
        self.ipreter.pack        (expand = YES, fill = BOTH)
        self.minsize             (200, 160)
        self.title \
            ( "%s - %s python interpreter"
            % (app.model.Tool_Supplier, app.model.product_name)
            )
        self.focus_set = self.ipreter.input.focus_set
    # end def __init__

# end class Power_User_Window

if __name__ != "__main__" :
    TFL.TKT.Tk._Export ("Power_User_Window")
### __END__ TFL.TKT.Tk.Power_User_Window
