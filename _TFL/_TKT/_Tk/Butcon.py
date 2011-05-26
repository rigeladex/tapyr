# -*- coding: iso-8859-15 -*-
# Copyright (C) 2005 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
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
#    20-Feb-2005 (CT)  Ancestor `Widget` and class `Styler` added,
#                      `*_style` methods removed
#    20-Feb-2005 (CT)  s/widget/wtk_widget/
#    23-Feb-2005 (CT)  `exposed_widget` added
#    25-Feb-2005 (RSC) Added _interface_test
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ««revision-date»»···
#--



from   _TFL                 import TFL
import _TFL._TKT._Tk
import _TFL._TKT._Tk.Styler
import _TFL._TKT._Tk.Widget
import _TFL._TKT.Butcon

from   CTK                  import *
from   predicate            import dict_from_list

import weakref

class _Tk_Butcon_ (TFL.TKT.Tk.Widget, TFL.TKT.Butcon) :
    """Model simple Button Control widget for Tkinter based GUI.
       to test: from _TFL._TKT._Tk.Butcon import *

       >>> from _TFL._UI.Style     import *
       >>> blue = Style ("blue", background = "lightblue")
       >>> yell = Style ("yell", background = "yellow", foreground = "red")
       >>> gray = Style ("gray", background = "gray80")
       >>> w = Butcon ()
       >>> w.wtk_widget.pack ()
       >>> w.apply_bitmap ('open_node')
       >>> w.apply_style (yell)
       >>> w.apply_bitmap ('closed_node')
       >>> w.apply_bitmap ('circle')
       >>> w.apply_style (gray)
    """

    _real_name  = "Butcon"

    class Styler (TFL.TKT.Tk.Styler) :

        Opts    = dict_from_list \
            (( "background", "font", "foreground"
             ### XXX any more ???
            ))

    # end class Styler

    Widget_Type = CTK.Label

    _sty_map    = weakref.WeakKeyDictionary ()

    def __init__ (self, AC = None, name = None, wc = None, bitmap = None) :
        self.__super.__init__ (AC = AC, name = name, wc = wc, bitmap = bitmap)
        # XXXX FIXME: bitmap_mgr add and caching of seen bitmaps should
        # probably be done by framework
        self.bitmaps = {}
        if bitmap :
            bitmap = self._get_bitmap (bitmap)
        master = None
        bg     = None
        if wc :
            master = wc.wtk_widget
            bg     = master.cget ('background')
        self.wtk_widget   = self.exposed_widget = self.Widget_Type \
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
        self.wtk_widget.configure (bitmap = self._get_bitmap (bitmap))
    # end def apply_bitmap

Butcon = _Tk_Butcon_ # end class _Tk_Butcon_

__test__ = dict (interface_test = TFL.TKT.Butcon._interface_test)

"""
from _TFL._TKT._Tk.Butcon    import *
from _TFL._UI.Style     import *
blue = Style ("blue", background = "lightblue")
yell = Style ("yell", background = "yellow", foreground = "red")
gray = Style ("gray", background = "gray80")
w = Butcon ()
w.wtk_widget.pack ()
w.apply_bitmap ('open_node')
w.apply_style (yell)
w.apply_bitmap ('closed_node')
w.apply_bitmap ('circle')

"""

if __name__ != "__main__" :
    TFL.TKT.Tk._Export ("*")
### __END__ TFL.TKT.Tk.Text
