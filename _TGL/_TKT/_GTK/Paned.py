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

    def _pack (self, where, child, resize = False, shrink = True) :
        pack  = getattr (self.wtk_object, "pack%d"   % (where, ))
        frame = getattr (self,            "frame_%d" % (where, ))
        if frame and not isinstance (child, GTK.Frame) :
            f = self.TNS.Frame ()
            f.shadow_type = frame
            f.show ()
            f.add  (child)
            child = f
        pack \
            (child.exposed_widget.wtk_object, resize = resize, shrink = shrink)
    # end def _pack

# end class Paned

class H_Paned (Paned) :

    GTK_Class        = GTK.gtk.HPaned

    frame_1 = GTK.SHADOW_IN  ### left
    frame_2 = GTK.SHADOW_IN  ### right

    def __init__ ( self
                 , left          = None
                 , right         = None
                 , left_frame    = None
                 , right_frame   = None
                 , AC           = None
                 ) :
        self.__super.__init__ (AC = AC)
        for v, a, n, c in ( (left_frame,  "frame_1", 1, left)
                          , (right_frame, "frame_2", 2, right)
                          ) :
            if v is not None :
                setattr (self, a, v)
            if c :
                self._pack (n, c)
    # end def __init__

    def pack_left (self, child, ** kw) :
        return self._pack (1, child, ** kw)
    # end def pack_left

    def pack_right (self, child, ** kw) :
        return self._pack (2, child, ** kw)
    # end def pack_right

# end class H_Paned

class V_Paned (Paned) :

    GTK_Class        = GTK.gtk.VPaned

    frame_1 = GTK.SHADOW_IN  ### top
    frame_2 = GTK.SHADOW_IN  ### bottom

    def __init__ ( self
                 , top          = None
                 , bottom       = None
                 , top_frame    = None
                 , bottom_frame = None
                 , AC           = None
                 ) :
        self.__super.__init__ (AC = AC)
        for v, a, n, c in ( (top_frame,    "frame_1", 1, top)
                          , (bottom_frame, "frame_2", 2, bottom)
                          ) :
            if v is not None :
                setattr (self, a, v)
            if c :
                self._pack (n, c)
    # end def __init__

    def pack_top (self, child, ** kw) :
        return self._pack (1, child, ** kw)
    # end def pack_top

    def pack_bottom (self, child, ** kw) :
        return self._pack (2, child, ** kw)
    # end def pack_bottom

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
