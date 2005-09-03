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
#    TGL.TKT.GTK.Image
#
# Purpose
#    Wrapper for the GTK widget Image
#
# Revision Dates
#    28-Mar-2005 (MG) Automated creation
#     3-Apr-2005 (MG) Creation continued
#     5-Apr-2005 (MG) `pixbuf` property added
#     9-Apr-2005 (MG) Stock icon support added
#    14-Aug-2005 (MG) `load` improved
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
from   _TFL                   import TFL
import _TGL._TKT._GTK.Misc
import _TFL.Filename

class Image (GTK.Misc) :
    """Wrapper for the GTK widget Image"""

    GTK_Class        = GTK.gtk.Image
    __gtk_properties = \
        ( GTK.Property            ("file", get = None)
        , GTK.Property            ("icon_name")
        , GTK.Property            ("icon_set")
        , GTK.Property            ("icon_size")
        , GTK.Property            ("image")
        , GTK.Property            ("mask")
        , GTK.Property            ("pixbuf")
        , GTK.Property            ("pixbuf_animation")
        , GTK.SG_Property         ("pixel_size")
        , GTK.Property            ("pixmap")
        , GTK.Property            ("stock")
        , GTK.SG_Property         ("storage_type", set = None)
        , GTK.SG_Property
            ("pixbuf", set_fct_name = "set_from_pixbuf")
        )

    def __init__ (self, filename = None, stock_id = None, size = 0, ** kw) :
        self.__super.__init__ (** kw)
        if filename :
            self.load (filename)
        elif stock_id :
            self.wtk_object.set_from_stock (stock_id, size)
    # end def __init__

    def load (self, filename, width = None, height = None, fit = False) :
        assert (width != None) == (height != None)
        if fit :
            width, height = tuple (self.wtk_object.allocation) [2:]
        if isinstance (filename, TFL.Filename) :
            filename = filename.name
        if width is None :
            self.wtk_object.set_from_file (filename)
        else :
            self.wtk_object.set_from_pixbuf \
                (GTK.gtk.gdk.pixbuf_new_from_file_at_size
                    (filename, width, height)
                )
    # end def load

# end class Image

if __name__ != "__main__" :
    GTK._Export ("Image")
### __END__ TGL.TKT.GTK.Image
