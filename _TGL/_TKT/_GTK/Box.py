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
#    TGL.TKT.GTK.Box
#
# Purpose
#    Wrapper for the GTK widget Box
#
# Revision Dates
#    22-Mar-2005 (MG) Automated creation
#    22-Mar-2005 (MG) Creation continued
#    27-Mar-2005 (MG) `Pack_Mixin` factored
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Container
import _TGL._TKT._GTK.Pack_Mixin

class Box (GTK.Container, GTK.Pack_Mixin) :
    """Wrapper for the GTK widget Box"""

    GTK_Class        = GTK.gtk.Box
    __gtk_properties = \
        ( GTK.SG_Property  ("homogeneous")
        , GTK.SG_Property  ("spacing")
        )

# end class Box

if __name__ != "__main__" :
    GTK._Export ("Box")
### __END__ TGL.TKT.GTK.Box
