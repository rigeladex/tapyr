# -*- coding: iso-8859-15 -*-
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
#    Pack_Mixin
#
# Purpose
#    A mixin providing the `pack` function used by boxes and tree view cells
#
# Revision Dates
#    27-Mar-2005 (MG) Creation
#    18-May-2005 (MG) Use `child.exposed_widget`
#    ««revision-date»»···
#--

from _TGL._TKT._GTK import GTK

class Pack_Mixin (object) :
    """Mixin providing the `pack` function"""
    def pack (self, child, start = True, expand = True, fill = True) :
        if start :
            fct = self.wtk_object.pack_start
        else :
            fct = self.wtk_object.pack_end
        return fct \
            (child.exposed_widget.wtk_object, expand = expand, fill = fill)
    # end def pack

# end class Pack_Mixin

if __name__ != "__main__" :
    GTK._Export ("Pack_Mixin")
### __END__ Pack_Mixin


