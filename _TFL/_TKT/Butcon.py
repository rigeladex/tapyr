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
#    TFL.TKT.Butcon
#
# Purpose
#    Model simple Button Control widget
#
# Revision Dates
#    17-Feb-2005 (RSC) Creation
#    25-Feb-2005 (ABR) Fixed doctest (uses png's instead of xbm's)
#    25-Feb-2005 (RSC) Re-added bitmaps that fail TGW doctest
#    25-Feb-2005 (RSC) Removed bitmaps for which no xbm exists -- Tk
#                      can't read PNG. Now left one xbm to document
#                      failing doctest of TGW.
#    25-Feb-2005 (RSC) Added style-related doctests
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ««revision-date»»···
#--



from   _TFL                 import TFL
import _TFL._TKT.Mixin

class Butcon (TFL.TKT.Mixin) :
    """Model simple Button Control widget."""

    _interface_test   = """
        >>> from _TFL._UI.Style import *
        >>> w = Butcon ()
        >>> w.apply_bitmap ('open_node')
        >>> w.apply_bitmap ('closed_node')
        >>> w.apply_bitmap ('circle')
        >>> w.apply_bitmap ('small_circle')
        >>> blue = Style ("blue", background = "lightblue")
        >>> w.apply_style (blue)
        >>> w.push_style  (blue)
        >>> w.pop_style   ()
        >>> w.pop_style   ()
        Traceback (most recent call last):
        ...
        IndexError: pop from empty list
    """

    def apply_bitmap (self, bitmap) :
        """Apply `bitmap` to our widget, replacing existing bitmap."""
        raise NotImplementedError, \
            "%s must define apply_bitmap" % (self.__class__.__name__, )
    # end def apply_bitmap

    def apply_style (self, style) :
        """Apply `style` to our widget."""
        raise NotImplementedError, \
            "%s must define apply_style" % (self.__class__.__name__, )
    # end def apply_style

    def remove_style (self, style) :
        """Remove `style` from our widget."""
        raise NotImplementedError, \
            "%s must define remove_style" % (self.__class__.__name__, )
    # end def apply_style

# end class Butcon

if __name__ != "__main__" :
    TFL.TKT._Export ("*")
### __END__ TFL.TKT.Tk.Text
