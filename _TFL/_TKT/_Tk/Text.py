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
#    TFL.TKT.Tk.Text
#
# Purpose
#    Model simple text widget for Tkinter based GUI
#
# Revision Dates
#    15-Feb-2005 (CT)  Creation
#    16-Feb-2005 (CT)  Creation continued
#    17-Feb-2005 (CT)  `__test__` added and filled with
#                      `TFL.TKT.Text._interface_test`
#    17-Feb-2005 (CT)  `get` changed to remove the last `\n` (which is created
#                      by Tk)
#    17-Feb-2005 (CT)  `delta` made optional argument of `pos_at`
#    17-Feb-2005 (CT)  `_line_pos` corrected
#    17-Feb-2005 (CT)  s/widget/wtk_widget/g
#    18-Feb-2005 (CT)  `remove_style` added
#    18-Feb-2005 (CT)  `Text_Styler` added and `apply_style` (mostly)
#                      implemented
#    19-Feb-2005 (CT)  `_tag_map` moved from class to instance (Tk tags are
#                      specific to widget instances)
#    20-Feb-2005 (CT)  Small fixes to make `style` work
#    20-Feb-2005 (CT)  `Text_Styler` moved insed `Text` and renamed to `Styler`
#    20-Feb-2005 (CT)  `Widget` factored to handle `style`
#    21-Feb-2005 (CT)  `wtk_widget` set to `widget.body` (and `widget`
#                      re-introduced to refer to `CTK.C_Text` instance)
#    22-Feb-2005 (RSC) New tags (justify, wrap, margins) enabled
#    22-Feb-2005 (RSC) Fixed widget computation in insert_widget
#    22-Feb-2005 (CT)  `left_gravity` added to `mark_at`
#    22-Feb-2005 (CT)  `place_cursor` and `see` added
#    23-Feb-2005 (RSC) added Scrolled_Text widget,
#                      modified *_pos to return Tk magic value
#    23-Feb-2005 (RSC) Changed pos_at to return real position
#                      changed doctest to (hopefully) work again.
#    23-Feb-2005 (CT)  `_pos_at` factored and used internally everywhere
#    ««revision-date»»···
#--

from   _TFL                 import TFL
import _TFL._TKT._Tk
import _TFL._TKT._Tk.Styler
import _TFL._TKT._Tk.Widget
import _TFL._TKT.Text

from   CTK                  import *
from   predicate            import *

import weakref

class _Tk_Text_ (TFL.TKT.Tk.Widget, TFL.TKT.Text) :
    """Model simple text widget for Tkinter based GUI.

       >>> w = Text ()
       >>> w.widget.pack ()
       >>> eot = w.eot_pos
       >>> cur = w.current_pos
       >>> w.bot_pos, w.pos_at (eot), w.pos_at (cur), w.bol_pos (w.current_pos)
       ('1.0', '2.0', '1.0', '1.0')
       >>> w.append ("Ha")
       >>> w.bot_pos, w.pos_at (eot), w.pos_at (cur), w.bol_pos (w.current_pos)
       ('1.0', '2.0', '1.2', '1.0')
       >>> w.append ("Hum")
       >>> w.insert (w.bot_pos, "Hi")
       >>> w.insert (w.bot_pos, "Ho", delta = 2)
       >>> for t in "Ha", "He", "Hi", "Ho", "Hu" :
       ...     print t, w.find (t)
       ...
       Ha 1.4
       He None
       Hi 1.0
       Ho 1.2
       Hu 1.6
       >>> w.bot_pos, w.pos_at (eot), w.pos_at (cur), w.bol_pos (w.current_pos)
       ('1.0', '2.0', '1.9', '1.0')
       >>> w.insert (w.eot_pos, chr (10) + "Diddle Dum")
       >>> w.bot_pos, w.pos_at (eot), w.pos_at (cur), w.bol_pos (w.current_pos)
       ('1.0', '3.0', '2.10', '2.0')
       >>> print w.get ()
       HiHoHaHum
       Diddle Dum
       >>> w.remove  (w.find ("Diddle"), delta = len ("Diddle"))
       >>> print w.get ()
       HiHoHaHum
        Dum
    """

    _real_name  = "Text"

    class Tag_Styler (TFL.TKT.Tk.Styler) :
        Opts    = dict_from_list \
            ( ( "background", "font", "foreground", "underline"
              , "justify", "lmargin1", "lmargin2", "rmargin", "wrap"
              )
            )
    # end class Tag_Styler

    class Styler (Tag_Styler) :
        Opts    = dict_from_list (("cursor", ))
    # end class Styler

    Widget_Type = CTK.C_Text

    bot_pos     = property (lambda s : START)
    current_pos = property (lambda s : INSERT)
    eot_pos     = property (lambda s : END)

    def __init__ (self, AC = None, name = None, editable = True, wc = None) :
        self.__super.__init__ (AC = AC, name = name, editable = editable)
        self.widget = self.Widget_Type \
            ( master    = wc
            , name      = name
            , state     = (DISABLED, NORMAL) [bool (editable)]
            )
        self.wtk_widget = self.widget.body
        self._tag_map   = weakref.WeakKeyDictionary ()
        self._tag_no    = 0
        self._mark_no   = 0
    # end def __init__

    def apply_style (self, style, head = None, tail = None, delta = 0) :
        if head is None :
            self.__super.apply_style \
                ( style, head = head, tail = tail, delta = delta)
        else :
            self.wtk_widget.tag_add \
                ( self._tag    (style)
                , self._pos_at (head, delta)
                , tail or self.eot_pos
                )
    # end def apply_style

    def bol_pos (self, pos_or_mark, delta = 0, line_delta = 0) :
        return self.wtk_widget.index \
            (self._line_pos ("linestart", pos_or_mark, delta, line_delta))
    # end def bol_pos

    def eol_pos (self, pos_or_mark, delta = 0, line_delta = 0) :
        return self.wtk_widget.index \
            (self._line_pos ("lineend", pos_or_mark, delta, line_delta))
    # end def eol_pos

    def find (self, text, head = None, tail = None, delta = 0) :
        return self.wtk_widget.search \
            ( text, self._pos_at (head or self.bot_pos, delta)
            , stopindex = tail
            , nocase    = False
            , regexp    = False
            ) or None
    # end def find

    def free_mark (self, * mark) :
        self.wtk_widget.mark_unset (* mark)
    # end def free_mark

    def get (self, head = None, tail = None, delta = 0) :
        widget = self.wtk_widget
        if head is None :
            head = self.bot_pos
        if tail is None :
            tail = self.eot_pos
        result = widget.get (self._pos_at (head, delta), tail)
        if widget.index (tail) == widget.index (self.eot_pos) :
            result = result [:-1]
        return result
    # end def get

    def insert (self, pos_or_mark, text, style = None, delta = 0) :
        return self.wtk_widget.insert \
            (self._pos_at (pos_or_mark, delta), text, self._tag (style))
    # end def insert

    def insert_image (self, pos_or_mark, image, style = None, delta = 0) :
        result = self.wtk_widget.image_create \
            (self._pos_at (pos_or_mark, delta), image = image)
        if style is not None :
            pass ### XXX
        return result
    # end def insert_image

    def insert_widget (self, pos_or_mark, widget, style = None, delta = 0) :
        result = self.wtk_widget.window_create \
            (self._pos_at (pos_or_mark, delta), window = widget.wtk_widget)
        if style is not None :
            pass ### XXX
        return result
    # end def insert_widget

    def mark_at (self, pos, delta = 0, name = None, left_gravity = False) :
        if name is None :
            name = "mark%d" % (self._mark_no, )
            self._mark_no += 1
        w = self.wtk_widget
        w.mark_set (name, self._pos_at (pos, delta))
        if left_gravity :
            w.mark_gravity (name, CTK.LEFT)
        return name
    # end def mark_at

    def place_cursor (self, pos_or_mark, delta = 0) :
        self.wtk_widget.place_cursor (self._pos_at (pos_or_mark, delta))
    # end def place_cursor

    def pos_at (self, pos_or_mark, delta = 0) :
        return self.wtk_widget.index (self._pos_at (pos_or_mark, delta))
    # end def pos_at

    def remove (self, head, tail = None, delta = 0) :
        if tail is None :
            tail = self._pos_at (head, delta)
        self.wtk_widget.delete (head, tail)
    # end def remove

    def remove_style (self, style, head, tail = None, delta = 0) :
        self.wtk_widget.tag_remove \
            ( self._tag_map [style]
            , self._pos_at  (head, delta)
            , tail or self.eot_pos
            )
    # end def remove_style

    def see (self, pos_or_mark, delta = 0) :
        self.wtk_widget.see (self._pos_at (pos_or_mark, delta))
    # end def see

    def _line_pos (self, mod, pos_or_mark, delta = 0, line_delta = 0) :
        result = pos_or_mark
        if line_delta != 0 :
            result = "%s %+d lines" % (result, line_delta)
        result = "%s %s" % (self._pos_at (result, delta), mod)
        return result
    # end def _line_pos

    def _pos_at (self, pos_or_mark, delta = 0) :
        result = pos_or_mark
        if delta != 0 :
            result = "%s %+d chars" % (result, delta)
        return result
    # end def _pos_at

    def _tag (self, style) :
        result = ()
        if style is not None :
            if style not in self._tag_map :
                tag                    = "tag:%s" % (self._tag_no, )
                self._tag_no          += 1
                self._tag_map [style]  = tag
                self.wtk_widget.tag_configure \
                    (tag, ** self._styler (style, self.Tag_Styler).option_dict)
                self._apply_style_bindings \
                    (style, lambda e, b : self.wtk_widget.bind_tag (tag, e, b))
            result = (self._tag_map [style])
        return result
    # end def _tag

Text = _Tk_Text_ # end class _Tk_Text_

class Scrolled_Text (Text) :

    Widget_Type = CTK.Scrolled_Text

# end class Scrolled_Text

__test__ = dict (interface_test = TFL.TKT.Text._interface_test)

"""
from _TFL._TKT._Tk.Text import *
from _TFL._UI.Style     import *
blue  = Style ("blue", background = "lightblue")
yell  = Style ("yell", background = "yellow", foreground = "red")
gray  = Style ("gray", background = "gray80")
hand  = Style ("hand", mouse_cursor = "hand")
defa  = Style ("hand", mouse_cursor = "default")
fleur = Style ("hand", mouse_cursor = "fleur")
w = Text ()
eot = w.eot_pos
cur = w.current_pos
w.widget.pack ()
w.push_style  (hand)
w.bot_pos, w.pos_at (eot), w.pos_at (cur), w.bol_pos (w.current_pos)
w.append ("Ha")
w.bot_pos, w.pos_at (eot), w.pos_at (cur), w.bol_pos (w.current_pos)
w.append ("Hum", blue)
w.insert (w.bot_pos, "Hi", yell)
w.insert (w.bot_pos, "Ho", delta = 2)
w.apply_style  (gray, w.bol_pos (w.current_pos), w.eol_pos (w.current_pos))
w.remove_style (gray, w.bot_pos, w.eot_pos)
for t in "Ha", "He", "Hi", "Ho", "Hu" :
    print t, w.find (t)

w.bot_pos, w.pos_at (eot), w.pos_at (cur), w.bol_pos (w.current_pos)
w.insert (w.eot_pos, '''\nDiddle Dum''')
w.apply_style (gray, w.bol_pos (w.current_pos), w.eol_pos (w.current_pos))
w.remove_style (yell, w.bot_pos, w.eot_pos)
w.bot_pos, w.pos_at (eot), w.pos_at (cur), w.bol_pos (w.current_pos)
w.get ()
w.remove  (w.find ("Diddle"), delta = len ("Diddle"))
w.get ()
"""

if __name__ != "__main__" :
    TFL.TKT.Tk._Export ("*")
### __END__ TFL.TKT.Tk.Text
