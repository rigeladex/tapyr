# -*- coding: utf-8 -*-
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
#    TGL.TKT.GTK.Test_Window
#
# Purpose
#    A toplevel window which has a proper destroy callback
#
# Revision Dates
#    27-Mar-2005 (MG) Creation
#    20-May-2005 (MG) Widget memory support added
#     4-Jun-2005 (MG) `_quit`: dump widget memory only if `AC.memory` is nt
#                     None
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Window
import _TGL._TKT._GTK.Signal

class Test_Window (GTK.Window) :
    """Toplevel window with a proper destroy callback"""

    def __init__ (self, * args, ** kw) :
        self.__super.__init__ (* args, ** kw)
        self.bind_add (GTK.Signal.Delete, self._quit)
        self.bind_add (GTK.Signal.Destroy, GTK.quit)
    # end def __init__

    def _quit (self, event) :
        if self.AC and getattr (self.AC, "memory", None) :
            self.save_widget_memory (True)
            self.AC.memory.dump     ()
    # end def _quit

# end class Test_Window

if __name__ != "__main__" :
    GTK._Export ("Test_Window")
### __END__ TGL.TKT.GTK.Test_Window
