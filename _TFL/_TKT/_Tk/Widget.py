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
#    21-Feb-2005 (CT) `_sty_map` definition moved in here and `Styler` added
#                     to `_sty_map` index
#    21-Feb-2005 (CT) `push_style` and `pop_style` implemented (and
#                     `remove_style` removed as it doesn't work, anyway)
#    21-Feb-2005 (RSC) Added import of Eventname
#    24-Feb-2005 (CT)  `num_opt_val` and `option_value` added
#    24-Feb-2005 (CT)  `busy_cursor` and `normal_cursor` added
#    24-Feb-2005 (CT)  `__getattr__` for `ask_*` added
#    24-Feb-2005 (CT)  `__getattr__` changed to delegate to `exposed_widget`
#     8-Mar-2005 (CT)  `make_active` added
#     1-Apr-2005 (CT)  `_sty_map` removed (caching now done by `Styler` itself)
#     2-Apr-2005 (MG)  `_before_styler` simplified
#    ««revision-date»»···
#--

from   _TFL                 import TFL
import _TFL._TKT.Mixin
import _TFL._TKT._Tk
import _TFL._TKT._Tk.Eventname

import weakref

class Widget (TFL.TKT.Mixin) :
    """Model widget for Tkinter based GUI"""

    widget_class = None ### redefine this if you want to change the `Class`
                        ### used for option lookup

    def __init__ (self, * args, ** kw) :
        self.__super.__init__ (* args, ** kw)
        self._sty_stack = []
    # end def __init__

    def apply_style (self, style, * args, ** kw) :
        w = self.wtk_widget
        w.configure (** self._styler (style).option_dict)
        self._apply_style_bindings   (style)
    # end def apply_style

    def busy_cursor (self, * args, ** kw) :
        """Legacy lifter activating gauge (ignores all arguments)"""
        gauge = self.AC.ui_state.gauge
        if gauge :
            gauge.activate ()
    # end def busy_cursor

    def make_active (self) :
        """Make widget `self` active"""
        toplevel = self.exposed_widget.winfo_toplevel ()
        toplevel.deiconify                            ()
        toplevel.lift                                 ()
        self.wtk_widget.focus_set                     ()
    # end def make_active

    def normal_cursor (self, * args, ** kw) :
        """Legacy lifter de-activating gauge (ignores all arguments)"""
        if gauge :
            gauge.deactivate ()
    # end def normal_cursor

    def num_opt_val (self, name, default) :
        """Return numeric value of option `name` or `default` if that option
           isn't defined (`default` isn't converted, so it'd better be
           numeric).
        """
        return self.exposed_widget.num_opt_val \
            (name, default, className = self.widget_class)
    # end def num_opt_val

    def option_value (self, name, default, separator = None) :
        """Return value of option `name` or `default` if that option isn't
           defined. If `separator` is specified, the option value (but not
           the default) is split by it.
        """
        return self.exposed_widget.option_value \
            ( name, default
            , className = self.widget_class
            , separator = separator
            )
    # end def option_value

    def pop_style (self) :
        self.wtk_widget.configure (** self._sty_stack.pop ())
    # end def pop_style

    def push_style (self, style) :
        assert style.callback is None
        w      = self.wtk_widget
        styler = self._styler  (style)
        self._sty_stack.append (self._before_styler (w, styler))
        w.configure            (** styler.option_dict)
    # end def push_style

    def _apply_style_bindings (self, style, binder = None) :
        if style is not None and style.callback :
            if binder is None :
                binder = self.wtk_widget.bind
            for name, cb in style.callback.iteritems () :
                binder (getattr (self.TNS.Eventname, name), cb)
    # end def _apply_style_bindings

    def _before_styler (self, w, styler) :
        return dict \
            ([(p, w.cget (p)) for p in styler.option_dict.iterkeys ()])
        return result
    # end def _before_styler

    def _styler (self, style, Styler = None) :
        if Styler is None :
            Styler = self.Styler
        return Styler (style)
    # end def _styler

    def __getattr__ (self, name) :
        if name.startswith ("ask_") :
            return getattr (self.exposed_widget, name)
        raise AttributeError, name
    # end def __getattr__

# end class Widget

if __name__ != "__main__" :
    TFL.TKT.Tk._Export ("*")
### __END__ TFL.TKT.Tk.Widget
