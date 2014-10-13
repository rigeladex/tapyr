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
#    TGL.TKT.GTK.Text_Child_Anchor
#
# Purpose
#    Wrapper for the GTK widget TextChildAnchor
#
# Revision Dates
#    28-Mar-2005 (MG) Automated creation
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.G_Object

class Text_Child_Anchor (GTK.G_Object) :
    """Wrapper for the GTK widget TextChildAnchor"""

    GTK_Class        = GTK.gtk.TextChildAnchor
    __gtk_properties = \
        ( 
        )

# end class Text_Child_Anchor

if __name__ != "__main__" :
    GTK._Export ("Text_Child_Anchor")
### __END__ TGL.TKT.GTK.Text_Child_Anchor
