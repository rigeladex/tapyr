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


