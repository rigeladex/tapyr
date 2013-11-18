# -*- coding: utf-8 -*-
# Copyright (C) 2008 Mag. Christian Tanzer. All rights reserved
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
#    TFL.TKT.Batch.Gauge
#
# Purpose
#    Gauge for batch applications that sets the terminal title for X terms
#
# Revision Dates
#    14-Aug-2008 (CT) Creation
#    21-Aug-2008 (CT) `set_label` and `set_value` added
#    ««revision-date»»···
#--

from   _TFL               import TFL

import _TFL._Meta.Object
import _TFL._TKT._Batch

from   _TFL import sos

import sys

class Gauge (TFL.Meta.Object) :

    ### `<ESC>]2;` followed by a `string` followed by `^G` sets the
    ### window title of a xterm to `string`
    _control_seq      = "\x1b]2;%s\x07"

    _xterm            = None

    ### This list is copied from gentoo's /usr/lib/portage/pym/output.py
    _xterm_compatible = set \
        (( "xterm", "Eterm", "aterm", "rxvt", "screen", "kterm"
         , "rxvt-unicode", "gnome"
        ))

    def __init__ (self) :
        self.__super.__init__ ()
        terminal  = sys.__stderr__
        term_name = sos.environ.get ("TERM")
        if terminal.isatty () and term_name in self._xterm_compatible :
            self._xterm = terminal
    # end def __init__

    def activate (self, title = "", label = " ", * args, ** kw) :
        self._set_title (label)
    # end def activate

    def deactivate (self) :
        self._set_title ()
    # end def deactivate

    def inc (self, * args, ** kw) :
        pass
    # end def inc

    def reset (self, label = "", * args, ** kw) :
        self._set_title (label)
    # end def reset

    def set_label (self, label) :
        self._set_title (label)
    # end def set_label

    def set_value (self, value) :
        pass
    # end def set_value

    def _set_title (self, s = "") :
        if self._xterm :
            self._xterm.write (self._control_seq % s)
    # end def _set_title

# end class Gauge

if __name__ != "__main__" :
    TFL.TKT.Batch._Export ("Gauge")
### __END__ TFL.TKT.Batch.Gauge
