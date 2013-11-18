# -*- coding: utf-8 -*-
# Copyright (C) 2005-2013 Mag. Christian Tanzer. All rights reserved
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
#    24-Feb-2005 (RSC) `set_tabs' added. Minimal test for event bindings
#                      added, more needs an app context.
#    25-Feb-2005 (CT)  Doctests changed to use `_doctest_AC`
#    25-Feb-2005 (RSC) left_gravity added to doctest with value False
#    25-Feb-2005 (RSC) added mark_at tests with a mark as parameter
#     2-Mar-2005 (RSC) added test for left_gravity mark insertion
#     2-Mar-2005 (RSC) added test for current_pos insertion:
#                      check that current_pos really returns a mark!
#                      So two insertions at x=current_pos work...
#     2-Mar-2005 (RSC) Test that eot_pos is a mark.
#    10-Mar-2005 (RSC) added `show'
#    10-Mar-2005 (RSC) `show' removed again. Use make_active instead!
#    15-Mar-2005 (RSC) `lift` parameter added to `apply_style`
#    15-Mar-2005 (RSC) Note added to docstring of `apply_style`
#     1-Apr-2005 (CT)  Optional argument `tag` added to `apply_style` and
#                      `_tag`
#     1-Apr-2005 (CT)  `tags_at` added
#    14-Apr-2005 (CT)  `bot_pos`, `eot_pos`, and `current_pos` replaced by
#                      `buffer_head`, `buffer_tail`, and `insert_mark`,
#                      respectively
#    21-Apr-2005 (BRU) Introduced property `buffer_empty`.
#    25-Apr-2005 (CT)  s/buffer_empty/is_empty/
#    28-May-2013 (CT)  Use `@subclass_responsibility` instead of home-grown code
#    ««revision-date»»···
#--

from   __future__  import print_function

from   _TFL                 import TFL
from   _TFL.Decorator       import subclass_responsibility

import _TFL._TKT.Mixin

class Text (TFL.TKT.Mixin) :
    """Model simple text widget"""

    _interface_test   = """
        >>> from _TFL._UI.Style import *
        >>> blue = Style ("blue", background = "lightblue")
        >>> yell = Style ("yell", background = "yellow", foreground = "red")
        >>> gray = Style ("gray", background = "gray80")
        >>> hand = Style ("hand", mouse_cursor = "hand")
        >>> cb   = Style ("cb",   callback = {'click_1' : lambda x : 1})
        >>> w = Text (_doctest_AC ())
        >>> w.is_empty
        True
        >>> w.set_tabs (42, 84)
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
        >>> w.is_empty
        False
        >>> w.append ("Hum", blue)
        >>> hum_p = w.find ("Hum")
        >>> hum_m = w.mark_at (hum_p, left_gravity = False)
        >>> grmpf = w.mark_at (hum_m, left_gravity = True)
        >>> grmml = w.mark_at (w.pos_at (hum_m), left_gravity = True)
        >>> w.place_cursor (w.buffer_head)
        >>> w.insert (w.insert_mark, "Hi", yell)
        >>> w.insert (w.insert_mark, "Ho", delta = 2)
        >>> w.apply_style  ( gray, w.bol_pos (hum_p), w.eol_pos (hum_p)
        ...                , tag ="foo")
        >>> tags = w.tags_at (hum_p)
        >>> print (len (tags), tags [0])
        1 foo
        >>> #applying an eventbinding is impossible here because this
        >>> #needs an app context for looking up the event name.
        >>> #w.apply_style  (cb,   w.bol_pos (hum_p), w.eol_pos (hum_p))
        >>> w.remove_style (gray, w.buffer_head, w.buffer_tail)

        >>> print (w.get (hum_p, w.pos_at (hum_p, 3)))
        HaH
        >>> print (w.get (hum_m, w.pos_at (hum_m, 3)))
        Hum
        >>> p = True
        >>> for t in "Ha", "He", "Hi", "Ho", "Hu" :
        ...     p = w.find (t, backwards = not p)
        ...     if p is not None :
        ...         print (t, "found", w.get (p, w.pos_at (p, delta = len (t))))
        ...     else :
        ...         print (t, "not found")
        ...
        Ha found Ha
        He not found
        Hi found Hi
        Ho found Ho
        Hu found Hu
        >>> w.insert (w.buffer_tail, chr (10) + "Diddle Dum")
        >>> w.apply_style (gray, w.bol_pos (w.buffer_tail), w.eol_pos (w.buffer_tail))
        >>> print (w.get ())
        HiHaHoHum
        Diddle Dum
        >>> print (w.get (w.bol_pos (hum_m), w.eol_pos (hum_m)))
        HiHaHoHum
        >>> print (w.get ( w.bol_pos (hum_m, line_delta = 1)
        ...             , w.eol_pos (hum_m, line_delta = 1)))
        Diddle Dum
        >>> w.see (w.buffer_tail)
        >>> w.see (w.buffer_head)
        >>> w.remove  (w.find ("Diddle"), delta = len ("Diddle"))
        >>> print (w.get ())
        HiHaHoHum
         Dum

        >>> w.insert (grmpf, "GRMPF", blue)
        >>> w.insert (grmpf, "jup", blue)
        >>> print (w.get ())
        HiHajupGRMPFHoHum
         Dum

        >>> w.insert (w.insert_mark, "cp1", blue)
        >>> w.insert (w.insert_mark, "cp2", yell)
        >>> print (w.get ())
        Hicp1cp2HajupGRMPFHoHum
         Dum

        >>> x = w.insert_mark
        >>> w.insert (x, "CP1", blue)
        >>> w.insert (x, "CP2", yell)
        >>> print (w.get ())
        Hicp1cp2CP1CP2HajupGRMPFHoHum
         Dum

        >>> x = w.buffer_tail
        >>> w.insert (x, "X1", blue)
        >>> w.insert (x, "Y2", yell)
        >>> print (w.get ())
        Hicp1cp2CP1CP2HajupGRMPFHoHum
         DumX1Y2

        >>> t1 = Text (_doctest_AC ())
        >>> t2 = Text (_doctest_AC ())
        >>> from _TFL.Apply_All import *
        >>> all = Apply_All (t1, t2)
        >>> all.append ("Ha")
        >>> all.append ("Hum", blue)
        >>> all.insert (t1.buffer_head, "Hi", yell)
        >>> all.insert (t1.buffer_head, "Ho", delta = 2)
        >>> all.apply_style (gray, t1.bol_pos (t1.insert_mark), t1.eol_pos (t1.insert_mark))
        >>> t1.remove_style (gray, t1.buffer_head, t1.buffer_tail)

        ### check styles of t1 and t2 (`t2` still should have style `gray`)
        """

    buffer_head       = None  ### descendents must redefine as property
    """Position of begin of buffer (use this to insert at the beginning).
       """

    buffer_tail       = None  ### descendents must redefine as property
    """Mark at end of buffer (use this to insert at the end).
       """

    insert_mark       = None  ### descendents must redefine as property
    """Mark of insert position in the text buffer.
       """

    is_empty          = False ### descendents must redefine as property

    def append (self, text, style = None) :
        """Append `text` with `style` to buffer."""
        self.insert (self.buffer_tail, text, style)
    # end def append

    @subclass_responsibility
    def apply_style (self, style, head = None, tail = None, delta = 0, lift = False, tag = None) :
        """Apply `style` from position/mark `head` (default:
           `self.buffer_head`) plus `delta` to position/mark `tail` (default:
           `self.buffer_tail`). Parameter `lift` specifies that this style
           should have the maximum priority. If `tag` is specified, use its
           value as tag-name.

           Note: Due to implementation restrictions, lmargin1 and
           lmargin2 must alway be applied in the same style (this is an
           implementation restriction of GTK).
        """
    # end def apply_style

    @subclass_responsibility
    def bol_pos (self, pos_or_mark, delta = 0, line_delta = 0) :
        """Return position of begin of physical line of `pos_or_mark` plus
           `delta` plus `line_delta`.
        """
    # end def bol_pos

    def clear (self) :
        """Remove all text from buffer."""
        self.remove (self.buffer_head, self.buffer_tail)
    # end def clear

    @subclass_responsibility
    def eol_pos (self, pos_or_mark, delta = 0, line_delta = 0) :
        """Return position of end of physical line of `pos_or_mark` plus
           `delta` plus `line_delta`.
        """
    # end def eol_pos

    @subclass_responsibility
    def find (self, text, head = None, tail = None, delta = 0, backwards = False) :
        """Return the position of (the first character of) `text` in the
           buffer between position/mark `head` (default: `self.buffer_head`)
           plus `delta` and position/mark `tail` (default: `self.buffer_tail`).
        """
    # end def find

    @subclass_responsibility
    def free_mark (self, * mark) :
        """Free all marks passed as arguments."""
    # end def free_mark

    @subclass_responsibility
    def get (self, head = None, tail = None, delta= 0) :
        """Return `text` between position/mark `head` (default:
           `self.buffer_head`) plus `delta` to position/mark `tail` (default:
           `self.buffer_tail`)."""
    # end def get

    @subclass_responsibility
    def insert (self, pos_or_mark, text, style = None, delta = 0) :
        """Insert `text` at `pos_or_mark` plus `delta`with `style`."""
    # end def insert

    @subclass_responsibility
    def insert_image (self, pos_or_mark, image_name, style = None, delta = 0) :
        """Insert image with name `image_name` at `pos_or_mark` plus
           `delta` with `style`.
        """
    # end def insert_image

    @subclass_responsibility
    def insert_widget (self, pos_or_mark, widget, style = None, delta = 0) :
        """Insert `widget` at `pos_or_mark` plus `delta` with `style`."""
    # end def insert_widget

    @subclass_responsibility
    def mark_at (self, pos, delta = 0, name = None, left_gravity = False) :
        """Return a mark with `name` at position `pos` plus `delta`."""
    # end def mark_at

    @subclass_responsibility
    def place_cursor (self, pos_or_mark) :
        """Move the insertion cursor to `pos_or_mark`"""
    # end def place_cursor

    @subclass_responsibility
    def pop_style (self) :
        """Pop lastly pushed `style` (and remove its effect from
           `self.wtk_widget`).
        """
    # end def pop_style

    @subclass_responsibility
    def pos_at (self, pos, delta = 0) :
        """Return position `pos` plus `delta`."""
    # end def pos_at

    @subclass_responsibility
    def push_style (self, style) :
        """Push `style` (i.e., apply it in a way that can be reversed by
           calling `pop_style` later).
        """
        assert style.callback is None
    # end def push_style

    @subclass_responsibility
    def remove (self, head, tail = None, delta = 0) :
        """Remove text between `head` and `tail` from buffer."""
    # end def remove

    @subclass_responsibility
    def remove_style (self, style, head, tail = None, delta = 0) :
        """Remove `style` from position/mark `head` plus `delta` to
           position/mark `tail` (default: `self.buffer_tail`).
        """
    # end def remove_style

    @subclass_responsibility
    def see (self, pos_or_mark) :
        """Adjust view of `self` so that `pos_or_mark` is completely visible.
        """
    # end def see

    @subclass_responsibility
    def set_tabs (self, * tabs) :
        """Set tabulator positions. Unit is pixels."""
    # end def set_tabs

    @subclass_responsibility
    def tags_at (self, pos_or_mark) :
        """Return the names of all tags active at position specified by
           `pos_or_mark`.
        """
    # end def tags_at

# end class Text

if __name__ != "__main__" :
    TFL.TKT._Export ("*")
### __END__ TFL.TKT.Text
