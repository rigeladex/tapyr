# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.cluster
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
#    TFL.TKT.Tk.Butcon
#
# Purpose
#    Model simple Button Control widget for Tkinter based GUI
#
# Revision Dates
#    17-Feb-2005 (RSC) Creation
#    ««revision-date»»···
#--

from   _TFL                 import TFL
import _TFL._TKT._Tk
import _TFL._TKT.Butcon

from   CTK                  import *

class _Tk_Butcon_ (TFL.TKT.Butcon) :
    """Model simple Button Control widget for Tkinter based GUI.
       to test: from _TFL._TKT._Tk.Butcon import *

       >>> w = Butcon ()
       >>> w.widget.pack ()
       >>> w.apply_bitmap ('open_node')
       >>> w.apply_bitmap ('closed_node')
       >>> w.apply_bitmap ('circle')
    """

    _real_name  = "Butcon"

    Widget_Type = CTK.Label

    def __init__ (self, AC = None, name = None, wc = None, bitmap = None) :
        self.__super.__init__ (AC = AC, name = name, wc = wc, bitmap = bitmap)
        # XXXX FIXME: bitmap_mgr add and caching of seen bitmaps should
        # probably be done by framework
        self.bitmaps = {}
        if bitmap : bitmap = self._get_bitmap (bitmap)
        master = None
        bg     = None
        if wc :
            master = wc.widget
            bg     = master.cget ('background')

        self.widget       = self.Widget_Type \
            ( master      = master
            , name        = name
            , bitmap      = bitmap
            , borderwidth = 0
            , background  = bg
            )
    # end def __init__

    # XXXX FIXME: bitmap_mgr add and caching of seen bitmaps should
    # probably be done by framework
    def _get_bitmap (self, bitmap) :
        if not self.bitmaps.has_key (bitmap) :
            CTK.bitmap_mgr.add (bitmap + '.xbm')
            self.bitmaps [bitmap] = 1
        return CTK.bitmap_mgr [bitmap]
    # end def _get_bitmap

    def apply_bitmap (self, bitmap) :
        self.widget.configure (bitmap = self._get_bitmap (bitmap))
    # end def apply_bitmap

    def apply_style (self, style) :
        pass
    # end def apply_bitmap

    def remove_style (self, style) :
        pass
    # end def apply_bitmap

Butcon = _Tk_Butcon_ # end class _Tk_Butcon_

#__test__ = dict (interface_test = TFL.TKT.Butcon._interface_test)

if __name__ != "__main__" :
    TFL.TKT.Tk._Export ("*")
### __END__ TFL.TKT.Tk.Text
