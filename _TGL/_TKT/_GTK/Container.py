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
#    TGL.TKT.GTK.Container
#
# Purpose
#    Wrapper for the GTK widget Container
#
# Revision Dates
#    22-Mar-2005 (MG) Automated creation
#    22-Mar-2005 (MG) Creation continued
#    27-Mar-2005 (MG) `add` and `remove` replaced by propper
#                     `_wtk_delegation` entries
#    27-Mar-2005 (MG) `children` converted to a `SG_Object_List_Property`
#     1-Apr-2005 (MG) `_wtk_delegation` changed
#    18-May-2005 (MG) Use new `Delegator_EO`
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Widget

class Container (GTK.Widget) :
    """Wrapper for the GTK widget Container"""

    GTK_Class        = GTK.gtk.Container
    __gtk_properties = \
        ( GTK.SG_Property             ("border_width")
        , GTK.SG_Property             ("resize_mode")
        , GTK.SG_Object_List_Property ("children", set = None)
        )

    _wtk_delegation  = GTK.Delegation \
        (GTK.Delegator_EO ("add"), GTK.Delegator_EO ("remove"))

# end class Container

if __name__ != "__main__" :
    GTK._Export ("Container")
### __END__ TGL.TKT.GTK.Container
