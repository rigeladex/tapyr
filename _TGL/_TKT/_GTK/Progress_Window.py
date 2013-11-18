# -*- coding: utf-8 -*-
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
#    TGL.TKT.GTK.Progress_Window
#
# Purpose
#    A toplevel window with contains a progress bar.
#
# Revision Dates
#    20-May-2005 (MG) Creation
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Window
import _TGL._TKT._GTK.Progress_Bar
import _TGL._TKT._GTK.V_Box
import _TGL._TKT._GTK.Button
import _TGL._TKT._GTK.H_Button_Box
import _TGL._TKT._GTK.Label

class Progress_Window (GTK.Window) :
    """Provide a toplevel widget containing a progress bar"""

    cycle        = False
    show_percent = True
    button       = None

    def __init__ ( self
                 , master        = None
                 , label         = ""
                 , active        = False
                 , cursor        = None
                 , title         = None
                 , cancel_button = False
                 , AC            = None
                 , ** kw
                 ) :
        self.__super.__init__ (title = title, AC = AC, ** kw)
        self._activations  = 0
        self._kbi_pending  = None
        self.box           = self.TNS.V_Box        (AC = AC)
        self.gauge         = self.TNS.Progress_Bar (AC = AC)
        self.label         = self.TNS.Label        (AC = AC)
        self.add        (self.box)
        self.box.pack   (self.label)
        self.box.pack   (self.gauge, expand = False)
        self.box.show   ()
        self.label.show ()
        self.gauge.show ()
        if cancel_button :
            self._bbox  = self.TNS.H_Button_Box ()
            self.button = self.TNS.Button (stock = "gtk-cancel", AC = AC)
            self.button.show     ()
            self.button.bind_add (self.TNS.Signal.Clicked, self.kb_interrupt)
            self._bbox.show      ()
            self.box.pack        (self._bbox, expand = False, fill = True)
            self._bbox.pack      (self.button)
            ### XXX make transient
        self.reset (label)
        if active :
            self.activate ()
    # end def __init__

    def activate (self, title = "", label = " ", g_range = 100, g_delta = 1, cycle = False) :
        self.reset     (label, g_range, g_delta, cycle = cycle)
        self.present   ()
        self.cycle         = bool (cycle)
        self.show_percent  = not cycle
        self._activations += 1
        if self.button :
            self.button.grab_add ()
        if title :
            self.title = title
            if label == " " :
                self.set_label (title)
        self._kbi_pending = None
    # end def activate

    def deactivate (self, force = False) :
        self._activations -= 1
        if force or self._activations <= 0 :
            self._activations = 0
            if self.button :
                self.button.grab_remove ()
            self.hide ()
    # end def deactivate

    def reset (self, label = None, g_range = 100, g_delta = 1, cycle = False) :
        self.cycle        = bool (cycle)
        self.show_percent = not cycle
        if g_range < 0 :
            ### This is an error of the caller
            raise ValueError, "Range must be positive (got %d)" % g_range
        if label :
            self.set_label (label)
        self.set_value (0)
        self._g_range = g_range
        self._g_delta = g_delta
        self._g_index = 0
        self._g_value = 0
    # end def reset

    def inc (self, delta) :
        cycle = self.cycle
        delta = (delta * (cycle or 1))
        gi    = self._g_index = self._g_index + delta
        gv    = self._g_value = self._g_value + delta
        gr    = self._g_range
        if abs (gv) >= self._g_delta :
            if cycle :
                if gi > gr:
                    self._g_index = gi = gr - delta
                    self.cycle    = -1
                elif gi < 0 :
                    self._g_index = gi = abs (delta)
                    self.cycle    = +1
            val = (100.0 * gi) // gr
            self.set_value (val)
            self._g_value = 0
        elif self.button :
            self._update_and_check_kbi ()
    # end def inc

    def set_label (self, text) :
        self.label.label = text
    # end def set_label

    def set_value (self, value) :
        value = max (value, 0)
        value = min (value, 100)
        self.gauge.fraction = value / 100.0
        if self.show_percent :
            self.gauge.text = "%3d%%" % (value, )
        self._update_and_check_kbi ()
    # end def set_value

    def _update_and_check_kbi (self) :
        self.update_idletasks ()
        if self._kbi_pending :
            self._kbi_pending = None
            raise KeyboardInterrupt
    # end def _update_and_check_kbi

    def kb_interrupt (self, event = None) :
        self._kbi_pending = 1
    # end def kb_interrupt

# end class Progress_Window

if __name__ != "__main__" :
    GTK._Export ("Progress_Window")
### __END__ TGL.TKT.GTK.Progress_Window


