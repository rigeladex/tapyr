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
#    TFL.TKT.Text
#
# Purpose
#    Model simple text widget
#
# Revision Dates
#    16-Feb-2005 (CT) Creation
#    17-Feb-2005 (CT) `_interface_test` added
#    ««revision-date»»···
#--

from   _TFL                 import TFL
import _TFL._TKT.Mixin

class Text (TFL.TKT.Mixin) :
    """Model simple text widget"""

    _interface_test   = """
        >>> w = Text ()
        >>> w.append ("Ha")
        >>> w.append ("Hum")
        >>> hum_p = w.find ("Hum")
        >>> hum_m = w.mark_at (hum_p)
        >>> w.insert (w.bot_pos, "Hi")
        >>> w.insert (w.bot_pos, "Ho", delta = 2)
        >>> print w.get (hum_p, w.pos_at (hum_p, 3))
        HoH
        >>> print w.get (hum_m, w.pos_at (hum_m, 3))
        Hum
        >>> for t in "Ha", "He", "Hi", "Ho", "Hu" :
        ...     p = w.find (t)
        ...     if p is not None :
        ...         print t, "found", w.get (p, w.pos_at (p, delta = len (t)))
        ...     else :
        ...         print t, "not found"
        ...
        Ha found Ha
        He not found
        Hi found Hi
        Ho found Ho
        Hu found Hu
        >>> w.insert (w.eot_pos, chr (10) + "Diddle Dum")
        >>> print w.get ()
        HiHoHaHum
        Diddle Dum
        >>> print w.get (w.bol_pos (hum_m), w.eol_pos (hum_m))
        HiHoHaHum
        >>> print w.get ( w.bol_pos (hum_m, line_delta = 1)
        ...             , w.eol_pos (hum_m, line_delta = 1))
        Diddle Dum
        >>> w.remove  (w.find ("Diddle"), delta = len ("Diddle"))
        >>> print w.get ()
        HiHoHaHum
         Dum

        """

    bot_pos           = None  ### descendents must redefine as property
    """Position of begin of buffer (use this to insert at the beginning).
       """

    current_pos       = None  ### descendents must redefine as property
    """Current position in the text buffer.
       """

    eot_pos           = None  ### descendents must redefine as property
    """Position of end of buffer (use this to insert at the end).
       """

    def append (self, text, style = None) :
        """Append `text` with `style` to buffer."""
        self.insert (self.eot_pos, text, style)
    # end def append

    def apply_style (self, style, head = None, tail = None, delta = 0) :
        """Apply `style` from position/mark `head` (default: `self.bot_pos`)
           plus `delta` to position/mark `tail` (default: `self.eot_pos`).
        """
        raise NotImplementedError, \
            "%s must define apply_style" % (self.__class__.__name__, )
    # end def apply_style

    def bol_pos (self, pos_or_mark, delta = 0, line_delta = 0) :
        """Return position of begin of physical line of `pos_or_mark` plus
           `delta` plus `line_delta`.
        """
        raise NotImplementedError, \
            "%s must define bol_pos" % (self.__class__.__name__, )
    # end def bol_pos

    def clear (self) :
        """Remove all text from buffer."""
        self.remove (self.bot_pos, self.eot_pos)
    # end def clear

    def eol_pos (self, pos_or_mark, delta = 0, line_delta = 0) :
        """Return position of end of physical line of `pos_or_mark` plus
           `delta` plus `line_delta`.
        """
        raise NotImplementedError, \
            "%s must define eol_pos" % (self.__class__.__name__, )
    # end def eol_pos

    def find (self, text, head = None, tail = None, delta = 0) :
        """Return the position of (the first character of) `text` in the
           buffer between position/mark `head` (default: `self.bot_pos`) plus
           `delta` and position/mark `tail` (default: `self.eot_pos`).
        """
        raise NotImplementedError, \
            "%s must define find" % (self.__class__.__name__, )
    # end def find

    def free_mark (self, * mark) :
        """Free all marks passed as arguments."""
        raise NotImplementedError, \
            "%s must define free_mark" % (self.__class__.__name__, )
    # end def free_mark

    def get (self, head = None, tail = None, delta= 0) :
        """Return `text` between position/mark `head` (default:
           `self.bot_pos`) plus `delta` to position/mark `tail` (default:
           `self.eot_pos`)."""
        raise NotImplementedError, \
            "%s must define get" % (self.__class__.__name__, )
    # end def get

    def insert (self, pos_or_mark, text, style = None, delta = 0) :
        """Insert `text` at `pos_or_mark` plus `delta`with `style`."""
        raise NotImplementedError, \
            "%s must define insert" % (self.__class__.__name__, )
    # end def insert

    def insert_image (self, pos_or_mark, image, style = None, delta = 0) :
        """Insert `image` at `pos_or_mark` plus `delta`with `style`."""
        raise NotImplementedError, \
            "%s must define insert_image" % (self.__class__.__name__, )
    # end def insert_image

    def insert_widget (self, pos_or_mark, widget, style = None, delta = 0) :
        """Insert `widget` at `pos_or_mark` plus `delta` with `style`."""
        raise NotImplementedError, \
            "%s must define insert_widget" % (self.__class__.__name__, )
    # end def insert_widget

    def mark_at (self, pos, delta = 0, name = None) :
        """Return a mark with `name` at position `pos` plus `delta`."""
        raise NotImplementedError, \
            "%s must define mark_at" % (self.__class__.__name__, )
    # end def mark_at

    def pos_at (self, pos, delta = 0) :
        """Return position `pos` plus `delta`."""
        raise NotImplementedError, \
            "%s must define pos_at" % (self.__class__.__name__, )
    # end def pos_at

    def remove (self, head, tail = None, delta = 0) :
        """Remove text between `head` and `tail` from buffer."""
        raise NotImplementedError, \
            "%s must define remove" % (self.__class__.__name__, )
    # end def remove

# end class Text

if __name__ != "__main__" :
    TFL.TKT._Export ("*")
### __END__ TFL.TKT.Text
