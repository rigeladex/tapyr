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
#    TFL.TKT.Tk.Text
#
# Purpose
#    Model simple text widget for Tkinter based GUI
#
# Revision Dates
#    15-Feb-2005 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL                 import TFL
import _TFL._TKT._Tk
import _TFL._TKT.Mixin

from   CTK                  import *

class Text (TFL.TKT.Mixin) :
    """Model simple text widget for Tkinter based GUI"""

    Widget_Type = CTK.C_Text

    current_pos = property (lambda s : s.widget.index (INSERT))

    def __init__ (self, name = None, editable = True) :
        self.widget = self.Widget_Type \
            ( master = None
            , name   = name
            , state  = (DISABLED, NORMAL) [bool (editable)]
            )
    # end def __init__
# end class Text

if __name__ != "__main__" :
    TFL.TKT.Tk._Export ("*")
### __END__ Text
