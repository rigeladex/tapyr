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
#    TGL.TKT.GTK.Menu_Shell
#
# Purpose
#    Wrapper for the GTK widget MenuShell
#
# Revision Dates
#    07-Apr-2005 (MG) Automated creation
#     9-Apr-2005 (MG) `insert` added to`_wtk_delegation`
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Container

class Menu_Shell (GTK.Container) :
    """Wrapper for the GTK widget MenuShell"""

    GTK_Class        = GTK.gtk.MenuShell
    __gtk_properties = \
        (
        )
    _wtk_delegation  = GTK.Delegation \
        ( GTK.Delegator_O ("insert"))

# end class Menu_Shell

if __name__ != "__main__" :
    GTK._Export ("Menu_Shell")
### __END__ TGL.TKT.GTK.Menu_Shell
