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
#    02-Feb-2005 (RSC) Creation, refactored from lib/python/T_Browser
#    ««revision-date»»···
#--

from   _TFL         import TFL
from   CT_TK        import Scrolled_Text, NORMAL, Label, CENTER, NONE, WORD, INSERT, LEFT, bitmap_mgr, START, END
from   D_Dict       import D_Dict
from   Functor      import Functor
from   Regexp       import *
import _TFL._TKT._Tk
import _TFL._TKT.Mixin
import sys


class Button (TFL.TKT.Mixin) :
    clsd_bitmap_name = "closed_node"
    leaf_bitmap_name = "circle"
    open_bitmap_name = "open_node"

    def __init__ (self, node, is_leaf = 1) :
        self.__super.__init__ (AC = node.AC)
        self.node     = node
        self.is_leaf  = not is_leaf ### negate for `make_[non_]leaf'
        self.closed   = 0
        self.c_bitmap = bitmap_mgr [self.clsd_bitmap_name]
        self.l_bitmap = bitmap_mgr [self.leaf_bitmap_name]
        self.o_bitmap = bitmap_mgr [self.open_bitmap_name]
        if is_leaf : bitmap = self.l_bitmap
        else       : bitmap = self.c_bitmap
        self.window   = Label \
            ( node.ui.master
            , name        = ":button:" + node.bid
            , bitmap      = bitmap
            , borderwidth = 0
            , background  = node.ui.master.cget ("background")
            )
        if is_leaf :
            self.make_leaf    ()
        else :
            self.make_non_leaf()
        self.window.bind      ("<Enter>",         self.mouse_enter)
        self.window.bind      ("<Leave>",         self.mouse_leave)
        self.bg = node.ui.master.cget ("background")
        self.fg = node.ui.master.cget ("foreground")
    # end def __init__

    def mouse_enter (self, event = None) :
        if not self.is_leaf :
            master = self.node.ui.master
            self.bg = self.window.cget ("background")
            self.fg = self.window.cget ("foreground")
            self.window.configure ( background  = master.button_bg
                                  , foreground  = master.button_fg
                                  )
        self.node.mouse_enter (event)
    # end def mouse_enter

    def mouse_leave (self, event = None) :
        if not self.is_leaf :
            self.window.configure ( background  = self.bg
                                  , foreground  = self.fg
                                  )
        self.node.mouse_leave (event)
    # end def mouse_leave

    def busy_cursor (self, cursor = "watch") :
        self.node.browser.busy_cursor    (cursor)
        # Igitt: FIXME
        self.node.browser.ui.browser._busy_cursor   (cursor, self.window)
    # end def busy_cursor

    def normal_cursor (self) :
        self.node.browser.normal_cursor  ()
        # Igitt: FIXME
        self.node.browser.ui.browser._normal_cursor (self.window)
    # end def normal_cursor

    def t_open (self, event = None) :
        try     :
            self.busy_cursor     ()
            self.node.open       (event)
        finally :
            self.normal_cursor   ()
    # end def t_open

    def t_open_1 (self, event = None) :
        try     :
            self.busy_cursor     ()
            self.node.open       (event, 1)
        finally :
            self.normal_cursor   ()
    # end def t_open_1

    def t_open_all (self, event = None) :
        try     :
            self.busy_cursor     ()
            self.node.open       (event, 1 << 30)
        finally :
            self.normal_cursor   ()
    # end def t_open_all

    def open (self, event = None) :
        if self.closed and not self.is_leaf :
            self.closed = 0
            self.window.configure (bitmap = self.o_bitmap)
            self.window.bind      ("<ButtonPress-1>", self.node.close)
    # end def open

    def close (self, event = None) :
        if (not self.closed) and (not self.is_leaf) :
            self.closed = 1
            self.window.configure (bitmap = self.c_bitmap)
            self.window.bind      ("<ButtonPress-1>", self.t_open)
            self.window.bind      ("<ButtonPress-3>", self.t_open_1)
            #self.window.bind      ("<ButtonPress-3>", self.t_open_all)
    # end def close

    def ignore (self, event = None) :
        return "break"
    # end def ignore

    def make_leaf (self) :
        if not self.is_leaf :
            self.is_leaf = 1
            self.closed  = 0
            self.window.configure (bitmap = self.l_bitmap)
            self.window.bind      ("<ButtonPress-1>", self.ignore)
            self.window.bind      ("<ButtonPress-2>", self.ignore)
            self.window.bind      ("<ButtonPress-3>", self.ignore)
    # end def make_leaf

    def make_non_leaf (self) :
        if self.is_leaf :
            self.is_leaf = self.closed = 0
            self.close ()
    # end def make_non_leaf

# end class Button

class Node (TFL.TKT.Mixin) :
    def __init__ (self, ui, browser) :
        self.__super.__init__ (AC = ui.AC)
        self.ui      = ui
        self.browser = browser
        self.master  = browser.ui.browser.body
        if not self.ui.parent and self.ui.number == 0 :
            self.master.last_key = None
            self.master.bind ("<Motion>",         self.ui.activate_mouse)
            self.master.bind ("<Up>",             self.ui.go_up)
            self.master.bind ("<Down>",           self.ui.go_down)
            self.master.bind ("<Left>",           self.ui.go_left)
            self.master.bind ("<Right>",          self.ui.go_right)
            self.master.bind ("<Insert>",         self.ui.expand)
            self.master.bind ("<Shift-Insert>",   self.ui.expand_1)
            self.master.bind ("<Control Insert>", self.ui.expand_all)
            self.master.bind ("<Delete>",         self.ui.collapse)
            self.master.bind ("<Shift-Delete>",   self.ui.collapse_1)
            self.master.bind ("<Control Delete>", self.ui.collapse_all)
            self.master.bind ("<Home>",           self.ui.show_head)
            self.master.bind ("<End>",            self.ui.show_tail)
            self.master.bind ("<<print>>",        self.ui.print_node)
        self.master.tag_bind (self.ui.bind_tag, "<Enter>", self.ui.mouse_enter)
        self.master.tag_bind (self.ui.bind_tag, "<Leave>", self.ui.mouse_leave)
        #print "Tk.Node", self.AC, ui, browser
    # end def __init__

    def insert (self, index, * tags) :
        """Insert `self' into widget `self.master' at position `index'."""
        head = self.master.index (index)
        if self.ui.level :
            self.ui._insert      (index, "\t" * self.ui.level)
        self.master.mark_set     (self.ui.butt_mark, index)
        self.master.mark_gravity (self.ui.butt_mark, LEFT)
        self.ui._insert_button   ()
        self.ui._insert          (index, "\t")
        self.ui._insert_header   (index)
        body = tail = self.master.index (index)
        self.ui._insert          (index, "\n")
        self.master.mark_set     (self.ui.head_mark, head)
        self.master.mark_set     (self.ui.body_mark, body)
        self.master.mark_set     (self.ui.tail_mark, tail)
        self.master.mark_gravity (self.ui.head_mark, LEFT)
        self.master.mark_gravity (self.ui.body_mark, LEFT)
        self.master.tag_add      ( self.ui.level_tag + ":head"
                                 , self.ui.head_mark
                                 , self.ui.head_mark + " lineend"
                                 )
    # end def insert

    def _display_button (self) :
        self.master.window_create \
            ( self.ui.butt_mark
            , window = self.ui.button.window
            )
    # end def _display_button

    def enter (self, event = None) :
        mark = self.ui.head_mark
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
            self.master.tk.call ("tk::TextSetCursor",  self.master._w, index)
        except TclError :
            self.master.tk.call ("tkTextSetCursor",  self.master._w, index)
    # end def _set_cursor

    def _go (self, event, node) :
        self.ui.leave      (event)
        self._set_cursor   ("%s + %rchars" % (node.head_mark, node.level + 2))
        node.enter         (event)
        node.ui.master.see (node.head_mark)
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
        pos = pos1 = m.search (match, self.ui.head_mark, self.ui.tail_mark)
        while pos :
            end = "%s + %s chars" % (pos, len (match))
            m.tag_add ("found", pos, end)
            pos = m.search (match, end, self.ui.tail_mark)
        if pos1 :
            if apply_found_bg :
                m.tag_add ("found_bg", pos1, self.ui.tail_mark)
            m.see     (self.ui.tail_mark)
            m.see     (pos1)
    # end def _find_highlight

    def find_unhighlight (self, match) :
        m   = self.master
        pos = m.search (match, self.ui.head_mark, self.ui.tail_mark)
        if pos :
            try :
                m.tag_remove ("found_bg", pos, self.ui.tail_mark)
            except TclError :
                pass
        while pos :
            end = "%s + %s chars" % (pos, len (match))
            m.tag_remove ("found", pos, end)
            pos = m.search (match, end, self.ui.tail_mark)
    # end def _find_unhighlight

# end class Node

class _Browser (Scrolled_Text) :
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
            self.body.tag_configure    ( level + ":head"
                                       , lmargin1  = 0
                                       , lmargin2  = i * indent + indent_inc
                                       , font      = h_font
                                       )
            self.body.tag_configure    ( level
                                       , lmargin1  = i * indent
                                       , lmargin2  = i * indent + indent_inc
                                       )
            tabs.append                (`i * indent`)
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

# end class _Browser

class Browser (TFL.TKT.Mixin) :
    """Tk wrapper for Hierarchical browser widget."""

    def __init__ (self, master, name = None, state = None, ** kw) :
        self.browser = _Browser (master, name, state, **kw)
    # end def __init__

    def clear         (self)       : self.browser.clear         ()
    def disable       (self)       : self.browser.disable       ()
    def normal_cursor (self)       :
        self.browser.normal_cursor  ()

    def busy_cursor (self, cursor) :
        self.browser.busy_cursor  (cursor)

    def insert (self, idx, txt, * tags) :
        self.browser.insert  (idx, txt, * tags)

    def delete (self, head, tail) :
        self.browser.delete  (head, tail)
# end class Browser

for n in ( Button.clsd_bitmap_name
         , Button.leaf_bitmap_name
         , Button.open_bitmap_name
         ) :
    bitmap_mgr.add (n + ".xbm")


TFL.TKT.Tk._Export_Module ()
