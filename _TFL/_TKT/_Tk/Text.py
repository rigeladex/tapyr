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
#    ««revision-date»»···
#--

from   _TFL                 import TFL
import _TFL._TKT._Tk
import _TFL._TKT.Text

from   CTK                  import *

class _Tk_Text_ (TFL.TKT.Text) :
    """Model simple text widget for Tkinter based GUI.

       >>> from _TFL._TKT._Tk.Text import *
       >>> w = Text ()
       >>> w.widget.pack ()
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
       >>> print w.get () [:-1]
       HiHoHaHum
       Diddle Dum
       >>> w.remove  (w.find ("Diddle"), delta = len ("Diddle"))
       >>> print w.get () [:-1]
       HiHoHaHum
        Dum
    """

    _real_name  = "Text"

    Widget_Type = CTK.C_Text

    bot_pos     = property (lambda s : s.widget.index (START))
    current_pos = property (lambda s : s.widget.index (INSERT))
    eot_pos     = property (lambda s : s.widget.index (END))

    def __init__ (self, AC = None, name = None, editable = True) :
        self.__super.__init__ (AC = AC, name = name, editable = editable)
        self.widget   = self.Widget_Type \
            ( master  = None
            , name    = name
            , state   = (DISABLED, NORMAL) [bool (editable)]
            )
        self._mark_no = 0
    # end def __init__

    def apply_style (self, style, head = None, tail = None, delta = 0) :
        self.widget.tag_add \
            ( self._tag (style)
            , self.pos_at (head or self.bot_pos, delta)
            , tail or self.eot_pos
            )
    # end def apply_style

    def bol_pos (self, pos_or_mark, delta = 0, line_delta = 0) :
        return self.widget.index \
            (self._line_pos ("linestart", pos_or_mark, delta, line_delta))
    # end def bol_pos

    def eol_pos (self, pos_or_mark, delta = 0, line_delta = 0) :
        return self.widget.index \
            (self._line_pos ("lineend", pos_or_mark, delta, line_delta))
    # end def eol_pos

    def find (self, text, head = None, tail = None, delta = 0) :
        return self.widget.search \
            ( text, self.pos_at (head or self.bot_pos, delta)
            , stopindex = tail
            , nocase    = False
            , regexp    = False
            ) or None
    # end def find

    def free_mark (self, * mark) :
        self.widget.mark_unset (* mark)
    # end def free_mark

    def get (self, head = None, tail = None, delta= 0) :
        return self.widget.get \
            ( self.pos_at (head, delta) or self.bot_pos
            , tail                      or self.eot_pos
            )
    # end def get

    def insert (self, pos_or_mark, text, style = None, delta = 0) :
        return self.widget.insert \
            (self.pos_at (pos_or_mark, delta), text, self._tag (style))
    # end def insert

    def insert_image (self, pos_or_mark, image, style = None, delta = 0) :
        result = self.widget.image_create \
            (self.pos_at (pos_or_mark, delta), image = image)
        if style is not None :
            pass ### XXX
        return result
    # end def insert_image

    def insert_widget (self, pos_or_mark, widget, style = None, delta = 0) :
        result = self.widget.window_create \
            (self.pos_at (pos_or_mark, delta), window = window)
        if style is not None :
            pass ### XXX
        return result
    # end def insert_widget

    def mark_at (self, pos, delta = 0, name = None) :
        if name is None :
            name           = "mark%d" % (self._mark_no, )
            self._mark_no += 1
        self.widget.mark_set (name, self.pos_at (pos, delta))
        return name
    # end def mark_at

    def pos_at (self, pos_or_mark, delta) :
        result = pos_or_mark
        if delta != 0 :
            result = "%s %+d chars" % (result, delta)
        return result
    # end def pos_at

    def remove (self, head, tail = None, delta = 0) :
        if tail is None :
            tail = self.pos_at (head, delta)
        self.widget.delete (head, tail)
    # end def remove

    def _line_pos (self, mod, pos_or_mark, delta = 0, line_delta = 0) :
        result = "%s %s" % (self.pos_at (pos_or_mark, delta), mod)
        if line_delta != 0 :
            result = "%s %+d lines" % (pos, line_delta)
        return result
    # end def _line_pos

    def _tag (self, style) :
        result = ()
        if style is not None :
            pass ### XXX
        return result
    # end def _tag

Text = _Tk_Text_ # end class _Tk_Text_

"""
from _TFL._TKT._Tk.Text import *
w = Text ()
w.widget.pack ()
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
