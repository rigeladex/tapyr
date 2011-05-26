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
#    TGL.TKT.GTK.Combo_Box
#
# Purpose
#    Wrapper for the GTK widget ComboBox
#
# Revision Dates
#    21-May-2005 (MG) Automated creation
#    21-May-2005 (MG) `get` added
#    21-May-2005 (MG) `__init__` added to create a own model, `append_text`
#                     added
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Bin
import _TGL._TKT._GTK.Model

class Combo_Box (GTK.Bin) :
    """Wrapper for the GTK widget ComboBox"""

    GTK_Class        = GTK.gtk.ComboBox
    __gtk_properties = \
        ( GTK.SG_Property         ("active")
        , GTK.Property            ("add_tearoffs")
        , GTK.SG_Property         ("column_span_column")
        , GTK.SG_Property         ("focus_on_click")
        , GTK.Property            ("has_frame")
        , GTK.SG_Object_Property  ("model")
        , GTK.SG_Property         ("row_span_column")
        , GTK.SG_Property         ("wrap_width")
        )

    _wtk_delegation = GTK.Delegation \
        ( GTK.Delegator_O ("pack_start")
        , GTK.Delegator_O ("add_attribute")
        )

    def __init__ (self, * args, ** kw) :
        TNS = self.get_TNS (kw ["AC"])
        if "model" not in kw :
            model = TNS.List_Model (str, AC = self.AC)
        else :
            mode = kw ["model"]
            del kw ["model"]
        self.__super.__init__ (model = model.wtk_object, * args, ** kw)
    # end def __init__

    def get (self):
        active = self.active
        if active < 0:
            return None
        return self.model [active] [0]
    # end def get

    def append_text (self, text) :
        self.model.add ((text, ))
    # end def append_text

# end class Combo_Box

if __name__ != "__main__" :
    GTK._Export ("Combo_Box")
### __END__ TGL.TKT.GTK.Combo_Box
