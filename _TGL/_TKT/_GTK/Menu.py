# -*- coding: iso-8859-15 -*-
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
#    TGL.TKT.GTK.Menu
#
# Purpose
#    Wrapper for the GTK widget Menu
#
# Revision Dates
#    07-Apr-2005 (MG) Automated creation
#     8-Apr-2005 (MG) `item` added
#     9-Apr-2005 (MG) `popup` added
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Menu_Shell

class Menu (GTK.Menu_Shell) :
    """Wrapper for the GTK widget Menu"""

    item = None  ### reference to the Menu_Item which display's this menu if
                 ### this is a submenu

    GTK_Class        = GTK.gtk.Menu
    __gtk_properties = \
        ( GTK.SG_Property         ("tearoff_state")
        , GTK.Property            ("tearoff_title")
        )

    def popup ( self
              , parent_menu_shell = None
              , parent_menu_item  = None
              , func              = None
              , button            = 3
              , activate_time     = None
              ) :
        if isinstance (parent_menu_shell, GTK._Event_) :
            activate_time     = parent_menu_shell.time
            button            = parent_menu_shell.button
            parent_menu_shell = None
        elif activate_time is None :
            activate_time = GTK.gtk.get_current_event_time()
        return self.wtk_object.popup \
            (parent_menu_shell, parent_menu_item, func, button, activate_time)
    # end def popup

# end class Menu

if __name__ != "__main__" :
    GTK._Export ("Menu")
### __END__ TGL.TKT.GTK.Menu
