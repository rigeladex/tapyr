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
#    15-Feb-2005 (CT) Creation
#    16-Feb-2005 (CT) Creation continued
#    17-Feb-2005 (CT) `__test__` added and filled with
#                     `TFL.TKT.Text._interface_test`
#    17-Feb-2005 (CT) `get` changed to remove the last `\n` (which is created
#                     by Tk)
#    17-Feb-2005 (CT) `delta` made optional argument of `pos_at`
#    17-Feb-2005 (CT) `_line_pos` corrected
#    17-Feb-2005 (CT) s/widget/wtk_widget/g
#    18-Feb-2005 (CT) `remove_style` added
#    ««revision-date»»···
#--

from   _TFL                 import TFL
import _TFL._TKT._Tk
import _TFL._TKT.Text

from   CTK                  import *

import weakref

class _Tk_Text_ (TFL.TKT.Text) :
    """Model simple text widget for Tkinter based GUI.

       >>> w = Text ()
       >>> w.wtk_widget.pack ()
       >>> w.bot_pos, w.eot_pos, w.current_pos, w.bol_pos (w.current_pos)
       ('1.0', '2.0', '1.0', '1.0')
       >>> w.append ("Ha")
       >>> w.bot_pos, w.eot_pos, w.current_pos, w.bol_pos (w.current_pos)
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
       >>> w.bot_pos, w.eot_pos, w.current_pos, w.bol_pos (w.current_pos)
       ('1.0', '2.0', '1.9', '1.0')
       >>> w.insert (w.eot_pos, chr (10) + "Diddle Dum")
       >>> w.bot_pos, w.eot_pos, w.current_pos, w.bol_pos (w.current_pos)
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

    Widget_Type = CTK.C_Text

    bot_pos     = property (lambda s : s.wtk_widget.index (START))
    current_pos = property (lambda s : s.wtk_widget.index (INSERT))
    eot_pos     = property (lambda s : s.wtk_widget.index (END))

    _tag_map    = weakref.WeakKeyDictionary ()
    _tag_no     = 0

    def __init__ (self, AC = None, name = None, editable = True, wc = None) :
        self.__super.__init__ (AC = AC, name = name, editable = editable)
        self.wtk_widget   = self.Widget_Type \
            ( master  = wc
            , name    = name
            , state   = (DISABLED, NORMAL) [bool (editable)]
            )
        self._mark_no = 0
    # end def __init__

    def apply_style (self, style, head = None, tail = None, delta = 0) :
        if head is None :
            pass ### XXX
        else :
            self.wtk_widget.tag_add \
                ( self._tag (style)
                , self.pos_at (head, delta)
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
            ( text, self.pos_at (head or self.bot_pos, delta)
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
        result = widget.get (self.pos_at (head, delta), tail)
        if widget.index (tail) == widget.index (self.eot_pos) :
            result = result [:-1]
        return result
    # end def get

    def insert (self, pos_or_mark, text, style = None, delta = 0) :
        return self.wtk_widget.insert \
            (self.pos_at (pos_or_mark, delta), text, self._tag (style))
    # end def insert

    def insert_image (self, pos_or_mark, image, style = None, delta = 0) :
        result = self.wtk_widget.image_create \
            (self.pos_at (pos_or_mark, delta), image = image)
        if style is not None :
            pass ### XXX
        return result
    # end def insert_image

    def insert_widget (self, pos_or_mark, widget, style = None, delta = 0) :
        result = self.wtk_widget.window_create \
            (self.pos_at (pos_or_mark, delta), window = window)
        if style is not None :
            pass ### XXX
        return result
    # end def insert_widget

    def mark_at (self, pos, delta = 0, name = None) :
        if name is None :
            name = "mark%d" % (self._mark_no, )
            self._mark_no += 1
        self.wtk_widget.mark_set (name, self.pos_at (pos, delta))
        return name
    # end def mark_at

    def pos_at (self, pos_or_mark, delta = 0) :
        result = pos_or_mark
        if delta != 0 :
            result = "%s %+d chars" % (result, delta)
        return result
    # end def pos_at

    def remove (self, head, tail = None, delta = 0) :
        if tail is None :
            tail = self.pos_at (head, delta)
        self.wtk_widget.delete (head, tail)
    # end def remove

    def remove_style (self, style, head, tail = None, delta = 0) :
        self.wtk_widget.tag_remove \
            ( self._tag_map [style]
            , self.pos_at (head, delta)
            , tail or self.eot_pos
            )
    # end def remove_style

    def _line_pos (self, mod, pos_or_mark, delta = 0, line_delta = 0) :
        result = pos_or_mark
        if line_delta != 0 :
            result = "%s %+d lines" % (result, line_delta)
        result = "%s %s" % (self.pos_at (result, delta), mod)
        return result
    # end def _line_pos

    def _styler (self, style) :
        pass ### XXX
    # end def _styler

    def _tag (self, style) :
        result = ()
        if style is not None :
            if style not in self._tag_map :
                tag = "tag:%s" % (self._tag_no, )
                self.__class__._tag_no += 1
                self._tag_map [style] = tag
                self.wtk_widget.tag_configure \
                    (tag, ** self._styler (style).option_dict)
            result = (self._tag_map [style])
        return result
    # end def _tag

Text = _Tk_Text_ # end class _Tk_Text_

__test__ = dict (interface_test = TFL.TKT.Text._interface_test)

"""
from _TFL._TKT._Tk.Text import *
w = Text ()
w.wtk_widget.pack ()
w.bot_pos, w.eot_pos, w.current_pos, w.bol_pos (w.current_pos)
w.append ("Ha")
w.bot_pos, w.eot_pos, w.current_pos, w.bol_pos (w.current_pos)
w.append ("Hum")
w.insert (w.bot_pos, "Hi")
w.insert (w.bot_pos, "Ho", delta = 2)
for t in "Ha", "He", "Hi", "Ho", "Hu" :
    print t, w.find (t)

w.bot_pos, w.eot_pos, w.current_pos, w.bol_pos (w.current_pos)
w.insert (w.eot_pos, '''\nDiddle Dum''')
w.bot_pos, w.eot_pos, w.current_pos, w.bol_pos (w.current_pos)
w.get ()
w.remove  (w.find ("Diddle"), delta = len ("Diddle"))
w.get ()
"""

if __name__ != "__main__" :
    TFL.TKT.Tk._Export ("*")
### __END__ TFL.TKT.Tk.Text
