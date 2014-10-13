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
#    TGL.TKT.GTK.Menu_Item
#
# Purpose
#    Wrapper for the GTK widget MenuItem
#
# Revision Dates
#    07-Apr-2005 (MG) Automated creation
#     7-Apr-2005 (MG) Properties `submenu` and `right_justified` added
#     8-Apr-2005 (MG) `_set_submenu` added
#    15-May-2005 (MG) `__init__` added to support `underline`
#    15-May-2005 (MG) `update_label` added
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Item

class Menu_Item (GTK.Item) :
    """Wrapper for the GTK widget MenuItem"""

    def _set_submenu (self, submenu) :
        self.wtk_object.set_submenu (submenu and submenu.wtk_object)
        if submenu :
            submenu.item = self
    # end def _set_submenu

    GTK_Class        = GTK.gtk.MenuItem
    __gtk_properties = \
        ( GTK.SG_Object_Property ("submenu", set = _set_submenu)
        , GTK.SG_Property        ("right_justified")
        )

    def __init__ ( self
                 , label     = None
                 , name      = None
                 , underline = None
                 , AC        = None
                 ) :
        self.__super.__init__ (AC = AC, name = name)
        if label :
            self.label = label = self.TNS.Accel_Label \
                (label, underline, self, AC = self.AC)
            label.show ()
            self.add   (label)
            label.xalign = 0.0
    # end def __init__

    def update_label (self, label, underline = None) :
        self.label.update_label (label, underline)
    # end def update_label

# end class Menu_Item

if __name__ != "__main__" :
    GTK._Export ("Menu_Item")
### __END__ TGL.TKT.GTK.Menu_Item
