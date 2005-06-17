# -*- coding: iso-8859-1 -*-
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
#    TGL.TKT.GTK.Message_Window
#
# Purpose
#    Message widnow for applications
#
# Revision Dates
#    20-May-2005 (MG) Creation
#    21-May-2005 (MG) `write` added, `editable` set to `False`, scrolling
#                     after `push_help`
#    21-May-2005 (MG) `push_style` and `pop_style` added, `write` changed to
#                     use current style
#    21-May-2005 (MG) `see` added
#    17-Jun-2005 (MG) `write` missing `see` call added
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Text

class Message_Window (GTK.Scrolled_Text) :
    """Text extension with provides additional functions for a message window
    """

    def __init__ (self, * args, ** kw) :
        self.__super.__init__ (* args, ** kw)
        self._text.editable = False
        self.help_marks     = []
        self.styles         = []
    # end def __init__

    def clear_help (self) :
        wtk = self._text.wtk_object
        for start, end in self.help_marks :
            i_start = wtk.iter_at_mark (start)
            i_end   = wtk.iter_at_mark (end)
            wtk.delete_mark (start)
            wtk.delete_mark (end)
            wtk.delete (i_start, i_end)
        self.help_marks = []
    # end def clear_help

    def put (self, text, style = None) :
        self._text.insert      (self._text.buffer_tail, text, style)
    # end def put

    def put_help (self, text) :
        self.clear_help ()
        self.push_help (text)
    # end def put_help

    def push_help  (self, text) :
        if text and text [-1] != "\n" :
            text = text + "\n"
        tw       = self._text
        tw._buffer.wtk_object.place_cursor (tw.eot_iter)
        start    = tw.mark_at  (tw.insert_mark, left_gravity = True)
        self._text.insert      (self._text.buffer_tail, text)
        self.help_marks.append ((start, tw.mark_at (tw.insert_mark)))
        self._text.see (start)
    # end def push_help

    push_err_msg = push_help

    def push_style (self, style) :
        self.styles.append (style)
    # end def push_style

    def pop (self) :
        if self.help_marks :
            wtk        = self._text._buffer.wtk_object
            start, end = self.help_marks [-1]
            del self.help_marks          [-1]
            i_start = wtk.get_iter_at_mark (start)
            i_end   = wtk.get_iter_at_mark (end)
            wtk.delete_mark            (start)
            wtk.delete_mark            (end)
            wtk.delete                 (i_start, i_end)
    # end def pop

    pop_help = pop_err_msg = pop

    def pop_style (self) :
        if self.styles :
            return self.styles.pop ()
    # end def pop_style

    def see (self, pos_or_mark = None) :
        self._text.see (pos_or_mark or self._text.insert_mark)
    # end def see

    def write (self, text) :
        if self.styles :
            style = self.styles [-1]
        else :
            style = None
        self._text.insert      (self._text.buffer_tail, text, style)
        self._text.see         (self._text.buffer_tail)
    # end def write

# end class Message_Window

if __name__ != "__main__" :
    GTK._Export ("Message_Window")
### __END__ TGL.TKT.GTK.Message_Window
