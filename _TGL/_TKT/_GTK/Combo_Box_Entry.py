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
#    TGL.TKT.GTK.Combo_Box_Entry
#
# Purpose
#    Wrapper for the GTK widget ComboBoxEntry
#
# Revision Dates
#    21-May-2005 (MG) Automated creation
#    21-May-2005 (MG) `get` and `set` added
#     6-Jun-2005 (MG) Set the cursor position at the after a `set`
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Combo_Box

class Combo_Box_Entry (GTK.Combo_Box) :
    """Wrapper for the GTK widget ComboBoxEntry"""

    GTK_Class        = GTK.gtk.ComboBoxEntry
    __gtk_properties = \
        ( GTK.SG_Property         ("text_column")
        ,
        )

    def get (self) :
        return self.wtk_object.child.get_text ()
    # end def get

    def set (self, text) :
        result = self.wtk_object.child.set_text (text)
        self.wtk_object.child.set_position      (-1)
        return result
    # end def set

# end class Combo_Box_Entry

if __name__ != "__main__" :
    GTK._Export ("Combo_Box_Entry")
### __END__ TGL.TKT.GTK.Combo_Box_Entry
