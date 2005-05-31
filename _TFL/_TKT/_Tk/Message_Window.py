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
#    TFL.TKT.Tk.Message_Window
#
# Purpose
#    Provide a scrollable window for status messages
#
# Revision Dates
#    31-May-2005 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL                      import TFL
from   CTK                       import *

import _TFL._TKT.Mixin
import _TFL._TKT._Tk.Styler
import _TFL._TKT._Tk.Widget

class Message_Window (TFL.TKT.Tk.Widget) :
    """Provide a scrollable window for status messages"""

    ### XXX this should really inherit from `TFL.TKT.Tk.Scrolled_Text`
    ### instead of `Widget`
    ### - downside: some functionality of CTK.Message_Window would be
    ###   duplicated here
    ### - upside:
    ###   * allows factoring of commonalities of different TKT packages
    ###   * allows move of code from TKT to UI

    widget_class = "Message_Window"
    Widget_Type  = CTK.Message_Window

    class Styler (TFL.TKT.Tk.Styler) :
        Opts    = dict.fromkeys \
            ( ( "background", "font", "foreground", "underline"
              , "justify", "lmargin1", "lmargin2", "rmargin", "wrap", "cursor"
              )
            )
    # end class Styler

    def __init__ (self, AC, wc = None, ** kw) :
        self.__super.__init__ (AC = AC, wc = wc, ** kw)
        self.exposed_widget = w = self.Widget_Type \
            ( master    = wc and getattr (wc, "wtk_widget", wc)
            , ** kw
            )
        self.wtk_widget = w.body
    # end def __init__

    def __getattr__ (self, name) :
        res = getattr (self.exposed_widget, name)
        setattr (self, name, res)
        return res
    # end def __getattr__

# end class Message_Window

if __name__ != "__main__" :
    TFL.TKT.Tk._Export ("*")
### __END__ TFL.TKT.Tk.Message_Window
