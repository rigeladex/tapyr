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
#    TGL.TKT.GTK.Accel_Label
#
# Purpose
#    Wrapper for the GTK widget AccelLabel
#
# Revision Dates
#    12-May-2005 (MG) Automated creation
#    15-May-2005 (MG) `set_accel_widget` added
#    15-May-2005 (MG) `Mnemonic` support added
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Label

class Accel_Label (GTK.Label) :
    """Wrapper for the GTK widget AccelLabel"""

    GTK_Class        = GTK.gtk.AccelLabel
    __gtk_properties = \
        ( GTK.Property            ("accel_closure")
        , GTK.SG_Object_Property  ("accel_widget")
        )

    _wtk_delegation = GTK.Delegation \
        ( GTK.Delegator_O         ("set_accel_widget")
        )

    def __init__ (self, label = None, underline = None, widget = None, AC = None) :
        self.__super.__init__ ("", AC = AC)
        self.update_label     (label, underline)
        if widget :
            self.set_accel_widget                 (self)
            self.mnemonic_widget = widget
    # end def __init__

    def update_label (self, label, underline = None) :
        if underline is None :
            label = label.replace ("_", "__")
        else :
            head  = label [:underline].replace ("_", "__")
            h_len = len (head)
            label = "%s_%s" % (head, label [h_len:].replace ("_", "__"))
        self.wtk_object.set_text_with_mnemonic              (label)
    # end def update_label

# end class Accel_Label

if __name__ != "__main__" :
    GTK._Export ("Accel_Label")
### __END__ TGL.TKT.GTK.Accel_Label
