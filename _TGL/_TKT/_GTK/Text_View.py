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
#    TGL.TKT.GTK.Text_View
#
# Purpose
#    Wrapper for the GTK widget TextView
#
# Revision Dates
#    28-Mar-2005 (MG) Automated creation
#     2-Apr-2005 (MG) `__init__` added
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Container

class Text_View (GTK.Container) :
    """Wrapper for the GTK widget TextView"""

    GTK_Class        = GTK.gtk.TextView
    __gtk_properties = \
        ( GTK.SG_Property         ("accepts_tab")
        , GTK.SG_Object_Property  ("buffer")
        , GTK.SG_Property         ("cursor_visible")
        , GTK.SG_Property         ("editable")
        , GTK.SG_Property         ("indent")
        , GTK.SG_Property         ("justification")
        , GTK.SG_Property         ("left_margin")
        , GTK.SG_Property         ("overwrite")
        , GTK.SG_Property         ("pixels_above_lines")
        , GTK.SG_Property         ("pixels_below_lines")
        , GTK.SG_Property         ("pixels_inside_wrap")
        , GTK.SG_Property         ("right_margin")
        , GTK.SG_Property         ("tabs")
        , GTK.SG_Property         ("wrap_mode")
        )

    def __init__ (self, AC = None, ** kw) :
        if buffer not in kw :
            kw ["buffer"] = GTK.Text_Buffer (AC = AC)
        ### we need the `_buffer` reference to prevent that the garbage
        ### collector destroys the `Text_Buffer`
        self._buffer      = b = kw ["buffer"]
        kw ["buffer"]     = b.wtk_object
        self.__super.__init__ (** kw)
    # end def __init__


# end class Text_View

if __name__ != "__main__" :
    GTK._Export ("Text_View")
### __END__ TGL.TKT.GTK.Text_View
