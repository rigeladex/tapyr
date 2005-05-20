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
#    TGL.TKT.GTK.Toplevel
#
# Purpose
#    A Toplevel window for applications.
#
# Revision Dates
#    20-May-2005 (MG) Creation
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Window
import _TGL._TKT._GTK.Signal

class Toplevel (GTK.Window) :
    """A toplevel window for applications."""

    def __init__ (self, * args, ** kw) :
        self.__super.__init__ (* args, ** kw)
        #self.bind_add (GTK.Signal.Destroy, GTK.quit)
    # end def __init__

# end class Toplevel

if __name__ != "__main__" :
    GTK._Export ("Toplevel")
### __END__ Toplevel


