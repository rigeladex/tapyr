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
#    TGL.TKT.GTK.Day_Column
#
# Purpose
#    Colum with a special header widget
#
# Revision Dates
#    18-Dec-2005 (MG) Creation
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Tree_View_Column

class Day_Column (GTK.Tree_View_Column) :
    """Colum with a special header widget"""

    def __init__ (self, * args, ** kw) :
        self.__super.__init__ (* args, ** kw)
        #self._label = self.TNS.Label (self.title)
        #self._label.show             ()
        #self.widget = self._label
    # end def __init__

# end class Day_Column

if __name__ != "__main__" :
    GTK._Export ("Day_Column")
### __END__ TGL.TKT.GTK.Day_Column
