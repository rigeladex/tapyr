# -*- coding: iso-8859-1 -*-
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
#    TGL.TKT.GTK.Paned
#
# Purpose
#    Wrapper for the GTK widget Paned
#
# Revision Dates
#    18-May-2005 (MG) Automated creation
#    18-May-2005 (MG) Simplified (o;
#    19-May-2005 (CT) Simplified more drastically
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Container
import _TGL._TKT._GTK.Frame
import _TGL._TKT._GTK.Constants

class Paned (GTK.Container) :
    """Wrapper for the GTK widget Paned"""

    GTK_Class        = GTK.gtk.Paned
    __gtk_properties = \
        ( GTK.Property            ("max_position", set = None)
        , GTK.Property            ("min_position", set = None)
        , GTK.SG_Property         ("position")
        , GTK.Property            ("position_set")
        )

    def __init__ (self, one = None, two = None, AC = None) :
        self.__super.__init__ (AC = AC)
        if one is not None :
            self.pack_1 (one)
        if two is not None :
            self.pack_2 (two)
    # end def __init__

    def _pack (self, child) :
        if not isinstance (child, (GTK.Frame, Paned)) :
            f = self.TNS.Frame ()
            f.show ()
            f.add  (child)
            child = f
        return child
    # end def _pack

    def pack_1 (self, child, ** kw) :
        child = self._pack (child)
        return self.wtk_object.pack1 (child.exposed_widget.wtk_object, ** kw)
    # end def pack_1

    def pack_2 (self, child, ** kw) :
        child = self._pack (child)
        return self.wtk_object.pack2 (child.exposed_widget.wtk_object, ** kw)
    # end def pack_2

# end class Paned

class H_Paned (Paned) :

    GTK_Class        = GTK.gtk.HPaned

    def __init__ (self, left = None, right = None, AC = None) :
        self.__super.__init__ (left, right, AC)
    # end def __init__

    pack_left  = Paned.pack_1
    pack_right = Paned.pack_2

# end class H_Paned

class V_Paned (Paned) :

    GTK_Class        = GTK.gtk.VPaned

    def __init__ (self, top = None, bottom = None, AC = None) :
        self.__super.__init__ (top, bottom, AC)
    # end def __init__

    pack_top    = Paned.pack_1
    pack_bottom = Paned.pack_2

# end class V_Paned

if __name__ != "__main__" :
    GTK._Export ("H_Paned", "V_Paned")
else :
    from   _TGL                   import TGL
    from   _TGL._UI.App_Context   import App_Context
    import _TGL._TKT._GTK.Label
    import _TGL._TKT._GTK.Test_Window
    import _TGL._TKT._GTK.H_Box
    import _TGL._TKT._GTK.V_Box
    GTK = TGL.TKT.GTK

    AC  = App_Context     (TGL)

    l_lt = GTK.Label ("left_top")
    l_rt = GTK.Label ("right_top")
    l_lb = GTK.Label ("left_bottom")
    l_rb = GTK.Label ("right_bottom")
    pt = H_Paned     (l_lt, l_rt, AC = AC)
    pb = H_Paned     (l_lb, l_rb, AC = AC)
    ph = V_Paned     (pt, pb, AC = AC)
    #ph = V_Paned     (pt, pb, False, False, AC = AC)
    win = GTK.Test_Window ("Paned Test", AC = AC)
    win.add               (ph)
    win.show_all          ()
    GTK.main              ()
### __END__ TGL.TKT.GTK.Paned
