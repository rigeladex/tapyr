# -*- coding: utf-8 -*-
# Copyright (C) 2005 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. office@spannberg.com
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
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
#    15-May-2005 (MG) Accelerator support added
#    15-May-2005 (MG) `label` handling moved into `Menu_Item`
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

    def __init__ ( self
                 , label     = None
                 , icon      = None
                 , name      = None
                 , underline = None
                 , AC        = None
                 ) :
        self.__super.__init__ \
            (label = label, underline = underline, name = name, AC = AC)
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
