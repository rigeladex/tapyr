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
#    TGL.TKT.GTK.Bin
#
# Purpose
#    Wrapper for the GTK widget Bin
#
# Revision Dates
#    22-Mar-2005 (MG) Automated creation
#    22-Mar-2005 (MG) Creation continued
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Container

class Bin (GTK.Container) :
    """Wrapper for the GTK widget Bin"""

    GTK_Class        = GTK.gtk.Bin
    __gtk_properties = ()

    def __init__ (self, child = None, ** kw) :
        self.__super.__init__ (** kw)
        if child :
            self.add (child)
    # end def __init__

    def child (self) :
        child = self.wtk_object.get_child ()
        if child :
            child = child.get_data ("ktw_object")
        return child
    child = property (child)

# end class Bin

if __name__ != "__main__" :
    GTK._Export ("Bin")
### __END__ TGL.TKT.GTK.Bin
