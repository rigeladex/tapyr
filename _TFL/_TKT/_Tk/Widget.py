# -*- coding: iso-8859-1 -*-
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
#    TFL.TKT.Tk.Widget
#
# Purpose
#    Model widget for Tkinter based GUI
#
# Revision Dates
#    20-Feb-2005 (CT) Creation
#    21-Feb-2005 (CT) `push_style` and `pop_style` added
#                     (stubs only for a start)
#    ««revision-date»»···
#--

from   _TFL                 import TFL
import _TFL._TKT.Mixin
import _TFL._TKT._Tk

class Widget (TFL.TKT.Mixin) :
    """Model widget for Tkinter based GUI"""

    def __init__ (self, * args, ** kw) :
        self.__super.__init__ (* args, ** kw)
        self._sty_stack = []
    # end def __init__

    def apply_style (self, style, * args, ** kw) :
        w = self.wtk_widget
        w.configure (** self._styler (style).option_dict)
        self._apply_style_bindings   (style)
        if style.mouse_cursor is not None :
            ### `cursor` can be `configure`d with option `cursor`
            ### XXX but should we support the `restore` cursor functionality
            ### XXX supported by the CT_TK methods
            ### XXX `busy_cursor`/`normal_cursor` ???
            pass ### XXX change cursor
    # end def apply_style

    def pop_style (self) :
        self.wtk_widget.configure (** self._sty_stack.pop ())
    # end def pop_style

    def push_style (self, style) :
        assert style.callback is None
        self._sty_stack.append (style) ### XXX need to invert before pushing
        self.apply_style (style)
    # end def push_style

    def remove_style (self, style) :
        ### XXX ??? does this make sense ???
        pass
    # end def apply_bitmap

    def _apply_style_bindings (self, style, binder = None) :
        if style is not None and style.callback :
            if binder is None :
                binder = self.wtk_widget.bind
            for name, cb in style.callback.iteritems () :
                binder (getattr (self.TNS.Eventname, name), cb)
    # end def _apply_style_bindings

    def _styler (self, style) :
        sty_map = self._sty_map
        if style not in sty_map :
            sty_map [style] = self.Styler (style)
        return sty_map [style]
    # end def _styler

# end class Widget

if __name__ != "__main__" :
    TFL.TKT.Tk._Export ("*")
### __END__ TFL.TKT.Tk.Widget
