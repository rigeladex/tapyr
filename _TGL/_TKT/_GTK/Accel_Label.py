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
