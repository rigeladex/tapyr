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
#    TFL.TKT.Tk.HTB
#
# Purpose
#    Hierarchical Text Browser, Tk-specific part
#
# Revision Dates
#     2-Feb-2005 (RSC) Creation, refactored from lib/python/T_Browser
#     3-Feb-2005 (CT)  Superflous imports removed
#     3-Feb-2005 (CT)  Stylistic improvements of ancient code
#     3-Feb-2005 (CT)  `Browser` streamlined by auto-delegation (__getattr__)
#     4-Feb-2005 (RSC) renamed ui to model and made it a weakref
#                      Node and Button now get a TKT.Tk.Node.
#    17-Feb-2005 (RSC) Button implemented using ButCon, moved from TKT to UI
#    21-Feb-2005 (RSC) renamed widget -> wtk_widget
#    ««revision-date»»···
#--

from   _TFL         import TFL
import _TFL._TKT._Tk
import _TFL._TKT.Mixin
import _TFL._TKT._Tk.Butcon

from   CT_TK        import Scrolled_Text, NORMAL, Label, CENTER, NONE, WORD, INSERT, LEFT, START, END
from   Regexp       import *
import sys
import weakref

class Node (TFL.TKT.Mixin) :

    def __init__ (self, model, browser) :
        self.__super.__init__ (AC = model.AC)
        self.model   = weakref.proxy (model)
        self.browser = browser
        self.master  = browser.wtk_widget.body
        if not self.model.parent and self.model.number == 0 :
            self.master.last_key = None
            self.master.bind ("<Motion>",         self.model.activate_mouse)
            self.master.bind ("<Up>",             self.model.go_up)
            self.master.bind ("<Down>",           self.model.go_down)
            self.master.bind ("<Left>",           self.model.go_left)
            self.master.bind ("<Right>",          self.model.go_right)
            self.master.bind ("<Insert>",         self.model.expand)
            self.master.bind ("<Shift-Insert>",   self.model.expand_1)
            self.master.bind ("<Control Insert>", self.model.expand_all)
            self.master.bind ("<Delete>",         self.model.collapse)
            self.master.bind ("<Shift-Delete>",   self.model.collapse_1)
            self.master.bind ("<Control Delete>", self.model.collapse_all)
            self.master.bind ("<Home>",           self.model.show_head)
            self.master.bind ("<End>",            self.model.show_tail)
            self.master.bind ("<<print>>",        self.model.print_node)
        self.master.tag_bind \
            (self.model.bind_tag, "<Enter>", self.model.mouse_enter)
        self.master.tag_bind \
            (self.model.bind_tag, "<Leave>", self.model.mouse_leave)
    # end def __init__

    def insert (self, index, * tags) :
        """Insert `self' into widget `self.master' at position `index'."""
        head = self.master.index  (index)
        if self.model.level :
            self.model._insert    (index, "\t" * self.model.level)
        self.master.mark_set      (self.model.butt_mark, index)
        self.master.mark_gravity  (self.model.butt_mark, LEFT)
        self.model._insert_button ()
        self.model._insert        (index, "\t")
        self.model._insert_header (index)
        body = tail = self.master.index (index)
        self.model._insert        (index, "\n")
        self.master.mark_set      (self.model.head_mark, head)
        self.master.mark_set      (self.model.body_mark, body)
        self.master.mark_set      (self.model.tail_mark, tail)
        self.master.mark_gravity  (self.model.head_mark, LEFT)
        self.master.mark_gravity  (self.model.body_mark, LEFT)
        self.master.tag_add \
            ( self.model.level_tag + ":head"
            , self.model.head_mark
            , self.model.head_mark + " lineend"
            )
    # end def insert

    def _display_button (self) :
        self.master.window_create \
            ( self.model.butt_mark
            , window = self.model.button.butcon.wtk_widget
            )
    # end def _display_button

    def enter (self, event = None) :
        mark = self.model.head_mark
        self.master.tag_add \
            ("active_node", mark, mark + " lineend +1 char")
        self.master.tag_lower ("active_node")
    # end def enter

    def leave (self, event = None) :
        self.master.tag_remove ("active_node", START, END)
    # end def leave

    def _set_cursor (self, index) :
        ### Default binding of text widget as shown by wish :
        ### % bind Text <Key-Up>
        ###     tkTextSetCursor %W [tkTextUpDownLine %W -1]
        ### The newest version of TK shows:
        ###     tk::TextSetCursor %W [tk::TextUpDownLine %W -1]
        try :
            self.master.tk.call ("tk::TextSetCursor", self.master._w, index)
        except TclError :
            self.master.tk.call ("tkTextSetCursor",   self.master._w, index)
    # end def _set_cursor

    def _go (self, event, node) :
        self.leave      (event)
        self._set_cursor \
            ("%s + %rchars" % (node.model.head_mark, node.model.level + 2))
        node.enter      (event)
        node.master.see (node.model.head_mark)
    # end def _go

    def _current_node (self) :
        node = None
        tags = filter (None, self.master.tag_names ("insert"))
        if tags :
            node = self.browser.node_map.get (tags [-1])
            if node :
                node.leave ()
            ### else : print self.browser.node_map, tags
        return node
    # end def _current_node

    def ignore      (self, event = None) :
        key    = event.keysym
        result = "break"
        if key in ("Control_L", "Control_R") : key = "Control"
        # print key
        if (  (self.master.last_key == "Control" and key in ("c", "C"))
           or (key in ("Control", "Next", "Prior"))
           ) :
            result = ""
        self.master.last_key = key
        return result
    # end def ignore

    def see (self, mark) :
        self.master.see (mark)
    # end def see

    def find_highlight (self, match, apply_found_bg = 0) :
        m   = self.master
        pos = pos1 = m.search \
            (match, self.model.head_mark, self.model.tail_mark)
        while pos :
            end = "%s + %s chars" % (pos, len (match))
            m.tag_add ("found", pos, end)
            pos = m.search (match, end, self.model.tail_mark)
        if pos1 :
            if apply_found_bg :
                m.tag_add ("found_bg", pos1, self.model.tail_mark)
            m.see     (self.model.tail_mark)
            m.see     (pos1)
    # end def _find_highlight

    def find_unhighlight (self, match) :
        m   = self.master
        pos = m.search (match, self.model.head_mark, self.model.tail_mark)
        if pos :
            try :
                m.tag_remove ("found_bg", pos, self.model.tail_mark)
            except TclError :
                pass
        while pos :
            end = "%s + %s chars" % (pos, len (match))
            m.tag_remove ("found", pos, end)
            pos = m.search (match, end, self.model.tail_mark)
    # end def _find_unhighlight

# end class Node

class _Tk_Browser_ (Scrolled_Text) :
    """Tk part of Hierarchical browser widget."""

    widget_class = "T_Browser"

    __Ancestor   = Ancestor = Scrolled_Text

    file_dialog_title = "Hierarchical browser filename"

    def __init__ (self, master, name = None, state = None, ** kw) :
        Scrolled_Text.__init__ (self, master, name, state, ** kw)
        self.state = state
        if self.state is None : self.state = NORMAL
        self.clear ()
        self.body.active_bg = self.option_value \
            ("activeBackground",       "yellow")
        self.body.active_fg = self.option_value \
            ("activeForeground",       "red")
        self.body.button_bg = self.option_value \
            ("activeButtonBackground", "red")
        self.body.button_fg = self.option_value \
            ("activeButtonForeground", "yellow")
        indent     = self.winfo_pixels (self.option_value ("indent",     "1c"))
        indent_inc = self.winfo_pixels (self.option_value ("indent_inc", "2m"))
        h_font     = self.option_value ("hFont", "")
        tabs       = []
        for i in range (1, 16) :
            level = "level" + `i-1`
            self.body.tag_configure \
                ( level + ":head"
                , lmargin1  = 0
                , lmargin2  = i * indent + indent_inc
                , font      = h_font
                )
            self.body.tag_configure \
                ( level
                , lmargin1  = i * indent
                , lmargin2  = i * indent + indent_inc
                )
            tabs.append (`i * indent`)
        link_bg    = self.option_value ("hyperLinkBackground", "")
        link_fg    = self.option_value ("hyperLinkForeground", "blue")
        link_font  = self.option_value ("hyperLinkFont",       "")
        cour_font  = self.option_value ("courierFont",         "courier")
        arial_font = self.option_value ("arialFont",           "arial")
        title_font = self.option_value ("titleFont",           "arial 14")
        found_fg   = self.option_value ("foundForeground",     "black")
        found_bg   = self.option_value ("foundBackground",     "deep sky blue")
        self.body.tag_configure        ("active_node"
                                       , background = self.body.active_bg
                                       , foreground = self.body.active_fg
                                       )
        self.body.tag_configure        ("center",      justify   = CENTER)
        self.body.tag_configure        ("courier",     font      = cour_font)
        self.body.tag_configure        ("arial",       font      = arial_font)
        self.body.tag_configure        ("title",       font      = title_font)
        self.body.tag_configure        ("nowrap",      wrap      = NONE)
        self.body.tag_configure        ("rindent",     rmargin   = indent)
        self.body.tag_configure        ("quote",       rmargin   = indent
                                       ,               lmargin1  = indent
                                       ,               lmargin2  = indent
                                       )
        self.body.tag_configure        ("underline",   underline = 1)
        self.body.tag_configure        ("wrap",        wrap      = WORD)
        self.body.tag_configure        ("hyper_link"
                                       , background = link_bg
                                       , foreground = link_fg
                                       , font       = link_font
                                       , underline  = 1
                                       )
        self.body.tag_configure        ("found"
                                       , background = found_bg
                                       , foreground = found_fg
                                       )
        self.body.tag_configure        ("found_bg"
                                       , background = "gray95"
                                       )
        self.body.configure            (tabs = " ".join (tabs))
    # end def __init__

# end class _Tk_Browser_

class Browser (TFL.TKT.Mixin) :
    """Tk wrapper for Hierarchical browser widget."""

    def __init__ (self, master, name = None, state = None, ** kw) :
        self.wtk_widget = _Tk_Browser_ (master, name, state, **kw)
    # end def __init__

    def __getattr__ (self, name) :
        result = getattr (self.wtk_widget, name)
        setattr (self, name, result)
        return result
    # end def __getattr__

# end class Browser

if __name__ != "__main__" :
    TFL.TKT.Tk._Export_Module ()
### __END__ TFL.TKT.Tk.HTB
