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
#    TGL.TKT.GTK.Tree
#
# Purpose
#    Tree_View widget contained in a scrolled window.
#
# Revision Dates
#    18-May-2005 (MG) Creation
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Tree_View
import _TGL._TKT._GTK.Scrolled_Window

class Tree (GTK.Tree_View) :
    """A scrollable tree view widget"""

    exposed_widget = None ### required to override the property

    def __init__ (self, * args, ** kw) :
        self.__super.__init__ (* args, ** kw)
        self.exposed_widget = self.TNS.Scrolled_Window ()
        ###cannot use the default add here !!! (will add itself or None)
        self.exposed_widget.wtk_object.add             (self.wtk_object)
        self.exposed_widget.show                       ()
    # end def __init__

# end class Tree

if __name__ != "__main__" :
    GTK._Export ("Tree")
### __END__ TGL.TKT.GTK.Tree
