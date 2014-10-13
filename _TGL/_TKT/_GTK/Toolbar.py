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
#    TGL.TKT.GTK.Toolbar
#
# Purpose
#    Wrapper for the GTK widget Toolbar
#
# Revision Dates
#    09-Apr-2005 (MG) Automated creation
#     9-Apr-2005 (MG) `insert` added to`_wtk_delegation`
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Container

class Toolbar (GTK.Container) :
    """Wrapper for the GTK widget Toolbar"""

    GTK_Class        = GTK.gtk.Toolbar
    __gtk_properties = \
        ( GTK.SG_Property         ("orientation")
        , GTK.SG_Property         ("show_arrow")
        , GTK.Property            ("toolbar_style")
        )
    _wtk_delegation  = GTK.Delegation \
        ( GTK.Delegator_O ("insert"))

# end class Toolbar

if __name__ != "__main__" :
    GTK._Export ("Toolbar")
### __END__ TGL.TKT.GTK.Toolbar
