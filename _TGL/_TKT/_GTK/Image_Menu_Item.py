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
#    TGL.TKT.GTK.Image_Menu_Item
#
# Purpose
#    Wrapper for the GTK widget ImageMenuItem
#
# Revision Dates
#    12-May-2005 (MG) Automated creation
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Menu_Item
import _TGL._TKT._GTK.Accel_Label
import _TGL._TKT._GTK.Image

class Image_Menu_Item (GTK.Menu_Item) :
    """Wrapper for the GTK widget ImageMenuItem"""

    GTK_Class        = GTK.gtk.ImageMenuItem
    __gtk_properties = \
        ( GTK.SG_Object_Property  ("image")
        ,
        )

    def __init__ (self, label = None, icon = None, name = None, AC = None) :
        self.__super.__init__ (AC = AC, name = name)
        if label :
            label = self.TNS.Accel_Label (label)
            label.show                   ()
            self.add                     (label)
        if icon :
            icon = self.TNS.Image \
                (stock_id = icon, size = GTK.gtk.ICON_SIZE_MENU)
            icon.show ()
            self.image = icon
    # end def __init__

# end class Image_Menu_Item

if __name__ != "__main__" :
    GTK._Export ("Image_Menu_Item")
### __END__ TGL.TKT.GTK.Image_Menu_Item
