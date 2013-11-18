# -*- coding: utf-8 -*-
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
