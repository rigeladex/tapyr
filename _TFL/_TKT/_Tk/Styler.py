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
#    TFL.TKT.Tk.Styler
#
# Purpose
#    Map a UI.Style object to a TK specific dictionary of options
#
# Revision Dates
#    18-Feb-2005 (CT)  Creation
#    20-Feb-2005 (CT)  Use `_real_name` to allow descendents to be named
#                      `Styler`
#    21-Feb-2005 (CT)  `cursor` handling added
#    24-Feb-2005 (CT)  `_font_weight_map` added and used
#    24-Feb-2005 (RSC) font_weight computation fixed & tested
#    ««revision-date»»···
#--

from   _TFL                 import TFL
import _TFL._TKT._Tk
import _TFL._TKT.Styler

import tkFont

class _TKT_Tk_Styler_ (TFL.TKT.Styler) :

    _real_name        = "Styler"

    _cursor_map       = dict \
        ( default     = None
        , hand        = "hand2"
        , hourglass   = "watch"
        , text        = "xterm"
        )

    _font_family_map  = dict \
        ( Monospace   = "courier"
        , Normal      = "times"
        , Sans        = "arial"
        )

    _font_size_map    = dict \
        ( { "xx-small"  : 6
          , "x-small"   : 8
          , "x-large"   : 14
          , "xx-large"  : 16
          }
        , small       = 8
        , medium      = 10
        , large       = 12
        )

    _font_weight_map  = dict \
        ( bold        = "bold"
        , ultrabold   = "bold"
        , heavy       = "bold"
        )
    _opt_mappers      = dict \
        ( underline   = lambda s, v : (False, True) [v != "none"]
        )

    def __init__ (self, style) :
        self.__super.__init__ (style)
        if "font" in self.Opts :
            f = style.font_family
            d = {}
            if f is not None :
                d ["family"] = self._font_family_map [f]
            s = style.font_size
            if s is not None :
                d ["size"] = self._font_size_map [s]
            w = style.font_weight
            if w is not None :
                d ["weight"] = self._font_weight_map.get (w, "normal")
            if d :
                self.option_dict ["font"] = tkFont.Font (** d)
        if "cursor" in self.Opts :
            c = style.mouse_cursor
            if c is not None :
                self.option_dict ["cursor"] = self._cursor_map.get (c, c)
    # end def __init__

Styler = _TKT_Tk_Styler_ # end class _TKT_Tk_Styler_

if __name__ != "__main__" :
    TFL.TKT.Tk._Export ("*")
### __END__ TFL.TKT.Tk.Styler
