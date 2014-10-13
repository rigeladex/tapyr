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
#    TGL.TKT.GTK.Cell_Renderer_Pixbuf
#
# Purpose
#    Wrapper for the GTK widget CellRendererPixbuf
#
# Revision Dates
#    27-Mar-2005 (MG) Automated creation
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.CellRenderer

class Cell_Renderer_Pixbuf (GTK.CellRenderer) :
    """Wrapper for the GTK widget CellRendererPixbuf"""

    GTK_Class        = GTK.gtk.CellRendererPixbuf
    __gtk_properties = \
        ( GTK.Property     ("pixbuf")
        , GTK.Property     ("pixbuf_expander_closed")
        , GTK.Property     ("pixbuf_expander_open")
        , GTK.Property     ("stock_detail")
        , GTK.Property     ("stock_id")
        , GTK.Property     ("stock_size")
        )

# end class Cell_Renderer_Pixbuf

if __name__ != "__main__" :
    GTK._Export ("Cell_Renderer_Pixbuf")
### __END__ TGL.TKT.GTK.Cell_Renderer_Pixbuf
