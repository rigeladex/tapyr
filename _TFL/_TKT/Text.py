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
#    16-Feb-2005 (CT)  Creation
#    17-Feb-2005 (CT)  `_interface_test` added
#    17-Feb-2005 (CT)  Test case added to `_interface_test`
#    18-Feb-2005 (CT)  `remove_style` added
#    20-Feb-2005 (CT)  Test cases for `style` added to `_interface_test`
#    20-Feb-2005 (CT)  Test case for two text widgets added (using `Apply_All')
#    22-Feb-2005 (CT)  Test cases for `push_style` and `pop_style` added to
#                      `_interface_test`
#    22-Feb-2005 (RSC) TODO list started.
#    22-Feb-2005 (CT)  `push_style` and `pop_style` added
#    22-Feb-2005 (CT)  `left_gravity` added to `mark_at`
#    22-Feb-2005 (CT)  `place_cursor` and `see` added
#    23-Feb-2005 (CT)  Doctests for `place_cursor` and `see` added
#    23-Feb-2005 (CT)  `backwards` added to `find` and doctest
#    23-Feb-2005 (CT)  `insert_image` changed to take an `image_name` instead
#                      of an `image` argument
#    ««revision-date»»···
#--

from   _TFL                 import TFL
import _TFL._TKT.Mixin

### TODO:
### - tab-handling. Suggest that positions are in pixels.
###   API may be something like set_tabs (tab, tab, ...) or set_tabs
###   (tablist)

class Text (TFL.TKT.Mixin) :
    """Model simple text widget"""

    _interface_test   = """
        >>> from _TFL._UI.Style import *
        >>> blue = Style ("blue", background = "lightblue")
        >>> yell = Style ("yell", background = "yellow", foreground = "red")
        >>> gray = Style ("gray", background = "gray80")
        >>> hand = Style ("hand", mouse_cursor = "hand")
        >>> w = Text ()
        >>> w.pop_style ()
        Traceback (most recent call last):
          ...
        IndexError: pop from empty list
        >>> w.push_style (hand)
        >>> w.pop_style ()
        >>> w.pop_style ()
        Traceback (most recent call last):
          ...
        IndexError: pop from empty list
        >>> w.apply_style (hand)
        >>> w.get ()
        ''
        >>> w.append ("Ha")
        >>> w.append ("Hum", blue)
        >>> hum_p = w.find ("Hum")
        >>> hum_m = w.mark_at (hum_p)
        >>> w.place_cursor (w.bot_pos)
        >>> w.insert (w.current_pos, "Hi", yell)
        >>> w.insert (w.current_pos, "Ho", delta = 2)
        >>> w.apply_style  (gray, w.bol_pos (hum_p), w.eol_pos (hum_p))
        >>> w.remove_style (gray, w.bot_pos, w.eot_pos)

        >>> print w.get (hum_p, w.pos_at (hum_p, 3))
        HaH
        >>> print w.get (hum_m, w.pos_at (hum_m, 3))
        Hum
        >>> p = True
        >>> for t in "Ha", "He", "Hi", "Ho", "Hu" :
        ...     p = w.find (t, backwards = not p)
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
        >>> w.apply_style (gray, w.bol_pos (w.eot_pos), w.eol_pos (w.eot_pos))
        >>> print w.get ()
        HiHaHoHum
        Diddle Dum
        >>> print w.get (w.bol_pos (hum_m), w.eol_pos (hum_m))
        HiHaHoHum
        >>> print w.get ( w.bol_pos (hum_m, line_delta = 1)
        ...             , w.eol_pos (hum_m, line_delta = 1))
        Diddle Dum
        >>> w.see (w.eot_pos)
        >>> w.see (w.bot_pos)
        >>> w.remove  (w.find ("Diddle"), delta = len ("Diddle"))
        >>> print w.get ()
        HiHaHoHum
         Dum

        >>> t1 = Text ()
        >>> t2 = Text ()
        >>> from _TFL.Apply_All import *
        >>> all = Apply_All (t1, t2)
        >>> all.append ("Ha")
        >>> all.append ("Hum", blue)
        >>> all.insert (t1.bot_pos, "Hi", yell)
        >>> all.insert (t1.bot_pos, "Ho", delta = 2)
        >>> all.apply_style (gray, t1.bol_pos (t1.current_pos), t1.eol_pos (t1.current_pos))
        >>> t1.remove_style (gray, t1.bot_pos, t1.eot_pos)

        ### check styles of t1 and t2 (`t2` still should have style `gray`)
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

    def find (self, text, head = None, tail = None, delta = 0, backwards = False) :
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

    def insert_image (self, pos_or_mark, image_name, style = None, delta = 0) :
        """Insert image with name `image_name` at `pos_or_mark` plus
           `delta` with `style`.
        """
        raise NotImplementedError, \
            "%s must define insert_image" % (self.__class__.__name__, )
    # end def insert_image

    def insert_widget (self, pos_or_mark, widget, style = None, delta = 0) :
        """Insert `widget` at `pos_or_mark` plus `delta` with `style`."""
        raise NotImplementedError, \
            "%s must define insert_widget" % (self.__class__.__name__, )
    # end def insert_widget

    def mark_at (self, pos, delta = 0, name = None, left_gravity = False) :
        """Return a mark with `name` at position `pos` plus `delta`."""
        raise NotImplementedError, \
            "%s must define mark_at" % (self.__class__.__name__, )
    # end def mark_at

    def place_cursor (self, pos_or_mark) :
        """Move the insertion cursor to `pos_or_mark`"""
        raise NotImplementedError, \
            "%s must define place_cursor" % (self.__class__.__name__, )
    # end def place_cursor

    def pop_style (self) :
        """Pop lastly pushed `style` (and remove its effect from
           `self.wtk_widget`).
        """
        raise NotImplementedError, \
            "%s must define pop_style" % (self.__class__.__name__, )
    # end def pop_style

    def pos_at (self, pos, delta = 0) :
        """Return position `pos` plus `delta`."""
        raise NotImplementedError, \
            "%s must define pos_at" % (self.__class__.__name__, )
    # end def pos_at

    def push_style (self, style) :
        """Push `style` (i.e., apply it in a way that can be reversed by
           calling `pop_style` later).
        """
        assert style.callback is None
        raise NotImplementedError, \
            "%s must define push_style" % (self.__class__.__name__, )
    # end def push_style

    def remove (self, head, tail = None, delta = 0) :
        """Remove text between `head` and `tail` from buffer."""
        raise NotImplementedError, \
            "%s must define remove" % (self.__class__.__name__, )
    # end def remove

    def remove_style (self, style, head, tail = None, delta = 0) :
        """Remove `style` from position/mark `head` plus `delta` to
           position/mark `tail` (default: `self.eot_pos`).
        """
        raise NotImplementedError, \
            "%s must define remove_style" % (self.__class__.__name__, )
    # end def remove_style

    def see (self, pos_or_mark) :
        """Adjust view of `self` so that `pos_or_mark` is completely visible.
        """
        raise NotImplementedError, \
            "%s must define see" % (self.__class__.__name__, )
    # end def see

# end class Text

if __name__ != "__main__" :
    TFL.TKT._Export ("*")
### __END__ TFL.TKT.Text
