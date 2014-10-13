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
#    TGL.TKT.GTK.Menu_Bar
#
# Purpose
#    Wrapper for the GTK widget MenuBar
#
# Revision Dates
#    07-Apr-2005 (MG) Automated creation
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Menu_Shell

class Menu_Bar (GTK.Menu_Shell) :
    """Wrapper for the GTK widget MenuBar"""

    GTK_Class        = GTK.gtk.MenuBar
    __gtk_properties = \
        (
        )

# end class Menu_Bar

if __name__ != "__main__" :
    GTK._Export ("Menu_Bar")
### __END__ TGL.TKT.GTK.Menu_Bar
