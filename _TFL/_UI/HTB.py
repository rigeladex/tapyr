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
#    TFL.UI.HTB
#
# Purpose
#    Hierarchical Text Browser, UI-specific part
#
# Revision Dates
#     2-Feb-2005 (RSC) Creation, refactored from lib/python/T_Browser
#     3-Feb-2005 (CT)  Superflous imports removed
#     3-Feb-2005 (CT)  Stylistic improvements of ancient code
#     4-Feb-2005 (RSC) renamed ui to tkt, tkt constructors get self.tkt
#                      fixed update of "tags" variable in insert
#                      see is now only used in tkt.
#    17-Feb-2005 (RSC) Added auto-delegation to self.tkt for Node
#    17-Feb-2005 (RSC) Button implemented using ButCon, moved from TKT to UI
#    21-Feb-2005 (RSC) Use styles for the button
#    23-Feb-2005 (RSC) Use TKT.Text, TKT.Tk.HTB is now obsolete
#    24-Feb-2005 (RSC) Style cache implemented,
#                      node_enter/leave functions of butcon removed to
#                      restore old (better) behaviour of original T_Browser,
#                      "break" replaced with self.TNS.stop_cb_chaining,
#                      mouse and keyboard events bound,
#                      cursor key movement corrected,
#                      some styles corrected to fit old T_Browser
#                      made text-widget non-editable :-)
#    24-Feb-2005 (RSC) Tabs implemented.
#    24-Feb-2005 (RSC) Print function fixed.
#    25-Feb-2005 (RSC) Node_Linked added, minor corrections in string
#                      searching, _apply_styles factored from
#                      find_highlight and Node_Linked.activate_links,
#                      mouse_cursor = "hand" added to hyper_link style,
#                      find_highlight/unhighlight moved from Browser->Node
#    ««revision-date»»···
#--

from   _TFL         import TFL
from   Regexp       import Regexp
from   Functor      import Functor

import _TFL._UI
import _TFL._UI.Mixin
from _TFL._UI.Style import *

import sys

callback_style = Style ("callback")

class Styles_Cache (object) :
    """Used to store module-wide styles."""
    styles = {}

    def __getattr__ (self, name) :
        if not name.startswith ('_') : 
            return self.styles [name]
    # end def __getattr__

    def __setattr__ (self, name, value) :
        self.styles [name] = value
    # end def __setattr__

    def __getitem__ (self, name) :
        return self.styles [name]
    # end def __getitem__

    __setitem__ = __setattr__

    has_key     = styles.has_key

# end class Styles_Cache

styles = Styles_Cache ()

class Button (TFL.TKT.Mixin) :

    clsd_bitmap_name = "closed_node"
    leaf_bitmap_name = "circle"
    open_bitmap_name = "open_node"

    def __init__ (self, node, is_leaf = 1) :
        self.__super.__init__ (AC = node.AC)
        self.node     = node
        self.is_leaf  = not is_leaf ### negate for `make_[non_]leaf'
        self.closed   = 0
        if is_leaf : bitmap = self.leaf_bitmap_name
        else       : bitmap = self.clsd_bitmap_name
        self.butcon = self.TNS.Butcon \
            ( self.AC
            , name   = ":button:" + node.bid
            , wc     = node.text
            , bitmap = bitmap
            )
        callback = dict \
            ( click_1   = self.ignore
            , click_2   = self.ignore
            , click_3   = self.ignore
            , any_enter = self.mouse_enter
            , any_leave = self.mouse_leave
            )
        self.leaf_style = callback_style (callback = callback)
        self.open_style = callback_style \
            (callback = dict (callback, click_1 = self.node.close))
        self.closed_style = callback_style \
            ( callback = dict 
                (callback, click_1 = self.t_open, click_3 = self.t_open_1)
            )
        if is_leaf :
            self.make_leaf ()
        else :
            self.make_non_leaf ()
        self.butcon.push_style (styles.normal)
    # end def __init__

    def mouse_enter (self, event = None) :
        self.node.mouse_enter (event)
        if not self.is_leaf :
            self.butcon.push_style (styles.active_button)
    # end def mouse_enter

    def mouse_leave (self, event = None) :
        self.node.mouse_leave (event)
        if not self.is_leaf :
            self.butcon.pop_style ()
    # end def mouse_leave

    def busy_cursor (self) :
        # XXXX FIXME
        #self.butcon.apply_style ('busy_cursor')
        #self.node.browser._busy_cursor   (cursor, self.window)
        pass
    # end def busy_cursor

    def normal_cursor (self) :
        # XXXX FIXME
        #self.butcon.apply_style ('normal_cursor')
        #self.node.browser._normal_cursor (self.window)
        pass
    # end def normal_cursor

    def t_open (self, event = None) :
        try     :
            self.busy_cursor     ()
            self.node.open (event)
        finally :
            self.normal_cursor   ()
    # end def t_open

    def t_open_1 (self, event = None) :
        try     :
            self.busy_cursor     ()
            self.node.open (event, 1)
        finally :
            self.normal_cursor   ()
    # end def t_open_1

    def t_open_all (self, event = None) :
        try     :
            self.busy_cursor     ()
            self.node.open (event, 1 << 30)
        finally :
            self.normal_cursor   ()
    # end def t_open_all

    def open (self, event = None) :
        if self.closed and not self.is_leaf :
            self.closed = 0
            self.butcon.apply_bitmap (bitmap = self.open_bitmap_name)
            self.butcon.apply_style  (self.open_style)
    # end def open

    def close (self, event = None) :
        if (not self.closed) and (not self.is_leaf) :
            self.closed = 1
            self.butcon.apply_bitmap (bitmap = self.clsd_bitmap_name)
            self.butcon.apply_style  (self.closed_style)
    # end def close

    def ignore (self, event = None) :
        return self.TNS.stop_cb_chaining
    # end def ignore

    def make_leaf (self) :
        if not self.is_leaf :
            self.is_leaf = 1
            self.closed  = 0
            self.butcon.apply_bitmap (bitmap = self.leaf_bitmap_name)
            self.butcon.apply_style  (self.leaf_style)
    # end def make_leaf

    def make_non_leaf (self) :
        if self.is_leaf :
            self.is_leaf = self.closed = 0
            self.close ()
    # end def make_non_leaf

# end class Button

class Node (TFL.UI.Mixin) :
    """ Model one node of a hierarchical browser."""

    cleanup = ( (Regexp (r"[-+\s]+"),         r"_")
              , (Regexp (r"^([^a-zA-Z]*\d)"), r"A\1")
              )

    class Name_Clash (StandardError) : pass

    def __init__ \
        ( self
        , browser                # browser widget containing the node
        , name                   # unique name of node, used as tag
        , header        = ""     # header-text of node
        , contents      = ""     # contents-text of node
        , parent        = None   # parent Node
        , number        = None   # index of self in `parent.children'
        , name_tags     = ()     # additional tags for `name'
        , header_tags   = ()     # additional tags for `header'
        , contents_tags = ()     # additional tags for `contents'
        , AC            = None   # for compatibility with __super
        ) :
        assert (  ((not parent) and (number is None))
               or ((parent)     and (number >= 0))
               )
        self.__super.__init__ \
            ( AC            = AC or browser.AC
            , browser       = browser
            , name          = name
            , header        = header
            , contents      = contents
            , parent        = parent
            , number        = number
            , name_tags     = name_tags
            , header_tags   = header_tags
            , contents_tags = contents_tags
            )
        self.browser   = browser
        self.text      = browser.text
        self.name      = name
        self.header    = header
        self.contents  = contents
        self.parent    = parent
        self.number    = number
        self.bid_seed  = 0
        if not self.parent :
            self.level       = 0
            self.number      = len (self.browser.nodes)
            self.bid         = `self.browser.bid_seed`
            self.tag         = self.name + "::" + self.bid
            browser.bid_seed = browser.bid_seed + 1
            browser.nodes.append (self)
            if self.number == 0 :
                # XXXXX FIXME:
                # self.browser.disable ()
                pass
        else :
            self.bid        = "%s:%d" % (parent.bid, parent.bid_seed)
            self.tag        = "%s::%s" % (self.bid, self.name)
            parent.bid_seed = parent.bid_seed + 1
            self.level      = parent.level + 1
        for clean, by in self.cleanup :
            self.tag   = clean.sub (by, self.tag)
        self.callback  = callback_style \
            ( callback = dict
                ( any_enter = self.mouse_enter
                , any_leave = self.mouse_leave
                )
            )
        self.level_tag = "level" + `self.level`
        if browser.node_map.has_key (self.tag) :
            raise Name_Clash, self.tag
        browser.node_map [self.tag] = self
        self.children  = []
        self.tags      = ()
        self.head_mark = None
        self.body_mark = None
        self.butt_mark = None
        self.tail_mark = None
        self.button    = None
        if name_tags     : self.name_tags     = filter (None, name_tags)
        if header_tags   : self.header_tags   = filter (None, header_tags)
        if contents_tags : self.contents_tags = filter (None, contents_tags)
        self.cached_text = ("%s" * 7) % \
           ( self.name
           , self.header_head,   self.header,   self.header_tail
           , self.contents_head, self.contents, self.contents_tail
           )
        if not self.parent and self.number == 0 :
            browser_binding_style    = callback_style \
                ( callback = dict 
                    ( mouse_motion   = self.activate_mouse
                    , cursor_up      = self.go_up
                    , cursor_down    = self.go_down
                    , cursor_left    = self.go_left
                    , cursor_right   = self.go_right
                    , cursor_home    = self.show_head
                    , cursor_end     = self.show_tail
                    , open_node      = self.expand
                    , open_node_1    = self.expand_1
                    , open_node_all  = self.expand_all
                    , close_node     = self.collapse
                    , close_node_1   = self.collapse_1
                    , close_node_all = self.collapse_all
                    , Print          = self.print_node
                    )
                )
            self.text.apply_style (browser_binding_style)
    # end def __init__

    def is_open (self) :
        return self.button and not self.button.closed
    # end def is_open

    def new_child (self, name, header = "", contents = "") :
        """Add child named `name' to `self'."""
        number = len              (self.children)
        child  = self.__class__   ( self.browser, name
                                  , header, contents, self, number
                                  )
        self._insert_child        (child)
        return child
    # end def new_child

    def _insert_child (self, child) :
        number = len         (self.children)
        self.children.append (child)
        if self.tags and not number :
            self.button.make_non_leaf ()
        if self.tags and not self.button.closed :
            child.insert (self.tail_mark, self.tags)
    # end def _insert_child

    def insert (self, mark, * tags) :
        """Insert `self' into widget `self.text' at position `mark'.
           Note that `mark' *must* be a mark with right gravity, e.g.,
           the current_pos in the text widget. We depend on the magic
           behaviour of the mark position (that it changes with
           insertions).
        """
        self.tags = filter (None, (self.tag, ) + tags)
        head = self.text.pos_at (mark)
        if self.level :
            self._insert (mark, "\t" * self.level)
        self.butt_mark = self.text.mark_at (mark, left_gravity = True)
        self._insert_button                ()
        self._insert                       (mark, "\t")
        self._insert_header                (mark)
        body = self.text.pos_at            (mark)
        self._insert                       (mark, "\n")
        self.head_mark = self.text.mark_at (head, left_gravity = True)
        self.body_mark = self.text.mark_at (body, left_gravity = True)
        self.tail_mark = self.text.mark_at (body)
        self.text.apply_style \
            ( styles [self.level_tag + ":head"]
            , self.head_mark
            , self.text.eol_pos (self.head_mark)
            )
    # end def insert

    def _insert_button (self) :
        if not self.button :
            self.button = Button \
                ( self
                , is_leaf = not (self.children or self.contents)
                )
        self.text.insert_widget \
            ( self.butt_mark
            , self.button.butcon
            )
    # end def _insert_button

    def _insert (self, index, text, * tags) :
        n = styles ['normal']
        tags = tuple ([t for t in self.tags + tags if styles.has_key (t)])
        if not styles.has_key (tags) :
            styles [tags] = Style (str (tags), n, * [styles [t] for t in tags])
        self.browser.insert (index, text, self.callback, styles [tags])
    # end def _insert

    def _delete (self, head, tail = None) :
        self.browser.delete (head, tail)
    # end def _delete

    name_tags          = ()     ### additional tags for `self.name'
    header_tags        = ()     ### additional tags for `self.header'
    contents_tags      = ()     ### additional tags for `self.contents'

    header_head        = "\n"   ### put in front of `self.header'
    header_tail        = ""     ### put in back  of `self.header'
    contents_head      = ""     ### put in front of `self.contents'
    contents_tail      = ""     ### put in back  of `self.contents'

    print_node_head    = "*   " ### put in front of each node (print_contents)
    print_level_head   = ".   " ### level indent per node     (print_contents)
    print_content_head = "    " ### content indent per node   (print_contents)

    def _insert_header (self, index) :
        self._insert (index, self.name, * self.name_tags)
        if self.header :
            self._insert \
                ( index
                , self.header_head + self.header + self.header_tail
                , self.level_tag
                , * self.header_tags
                )
    # end def _insert_header

    def _insert_contents (self, index) :
        if self.contents :
            self._insert \
                ( index
                , self.contents_head + self.contents + self.contents_tail
                , self.level_tag
                , * self.contents_tags
                )
    # end def _insert_contents

    def print_node (self, event = None) :
        node = self._current_node ()
        if node :
            file_name = self.text.ask_save_file_name \
                ( defaultextension  = ".txt"
                , filetypes         = ( ("data files", "*.dat")
                                      , ("text files", "*.txt")
                                      , ("list files", "*.list")
                                      , ("all  files", "*")
                                      )
                , title             = self.browser.file_dialog_title
                )
            if file_name :
                f = open (file_name, "w", -1)
                node.print_contents (f)
                f.close ()
        return self.TNS.stop_cb_chaining
    # end def print_node

    def print_contents (self, file = sys.stdout) :
        head   = (self.print_level_head   * (self.level)) + self.print_node_head
        indent = (self.print_content_head * (self.level + 1))
        parts  = []
        open   = self.is_open ()
        parts.append (head + self.name)
        if self.header :
            parts.append (self.header_head + self.header + self.header_tail)
        if open and self.contents :
            if (parts [-1] [-1] != "\n") and (self.contents_head != "\n") :
                parts.append ("\n")
            parts.append ( self.contents_head
                         + self.contents + self.contents_tail
                         )
        output = "".join (parts)
        output = output.replace ("\n", "\n" + indent) + "\n"
        file.write (output)
        if open :
            for c in self.children :
                c.print_contents (file)
    # end def print_contents

    def open (self, event = None, transitive = 0) :
        if self.button and not self.button.is_leaf :
            if self.button.closed :
                self.button.open ()
                self._insert          (self.tail_mark, "\n")
                self._insert_contents (self.tail_mark)
                for c in self.children :
                    c.insert (self.tail_mark, * self.tags)
            if transitive :
                for c in self.children :
                    c.open (event, transitive - 1)
    # end def open

    def close (self, event = None, transitive = 0) :
        if self.button and not self.button.is_leaf :
            if not self.button.closed :
                for c in self.children :
                    c.close  (event, transitive = 0)
                    c.tags   = ()
                    c.button = None
                self.button.close ()
                self._delete      (self.body_mark, self.tail_mark)
            if transitive and self.parent :
                self.parent.close (event, transitive - 1)
    # end def close

    def enter (self, event = None) :
        head = self.head_mark
        self.text.apply_style \
            (styles.active_node, head, self.text.bol_pos (head, line_delta = 1))
        self.browser.current_node = self
    # end def enter

    def leave (self, event = None) :
        self.text.remove_style (styles.active_node, self.text.bot_pos)
    # end def leave

    def _set_cursor (self, index, delta = None) :
        self.text.place_cursor (self, index, delta)
    # end def _set_cursor

    def mouse_enter (self, event = None) :
        if self.browser.mouse_act :
            self.enter             (event)
    # end def mouse_enter

    def mouse_leave (self, event = None) :
        self.leave             (event)
    # end def mouse_leave

    def set_cursor (self, index) :
        self._set_cursor         (index)
        self.browser.focus_force ()
    # end def set_cursor

    def _current_node (self) :
        self.browser.mouse_act = 0
        return self.browser.current_node
    # end def _current_node

    def activate_mouse (self, event = None) :
        self.browser.mouse_act = 1
    # end def activate_mouse

    def ignore (self, event = None) :
        self.browser.mouse_act = 0
        return self.TNS.stop_cb_chaining
# XXXXX FIXME
#        key    = event.keysym
#        result = self.TNS.stop_cb_chaining
#        if key in ("Control_L", "Control_R") : key = "Control"
#        # print key
#        if (  (self.master.last_key == "Control" and key in ("c", "C"))
#           or (key in ("Control", "Next", "Prior"))
#           ) :
#            result = ""
#        self.master.last_key = key
#        return result
    # end def ignore

    def expand (self, event = None, transitive = 0) :
        node = self._current_node ()
        if node :
            node.open  (event, transitive)
            node.enter ()
        return self.TNS.stop_cb_chaining
    # end def expand

    def expand_1 (self, event = None) :
        return self.expand (event, transitive = 1)
    # end def expand_1

    def expand_all (self, event = None) :
        return self.expand (event, transitive = 1 << 30)
    # end def expand_all

    def collapse (self, event = None, transitive = 0) :
        node = self._current_node ()
        if node :
            node.close (event, transitive)
            node.enter ()
        return self.TNS.stop_cb_chaining
    # end def collapse

    def collapse_1 (self, event = None) :
        return self.collapse (event, transitive = 1)
    # end def collapse_1

    def collapse_all (self, event = None) :
        return self.collapse (event, transitive = 1 << 30)
    # end def collapse_all

    def show_head   (self, event = None) :
        node = self._current_node ()
        if node :
            node.text.see (node.head_mark)
            node.enter    ()
        return self.TNS.stop_cb_chaining
    # end def show_head

    def show_tail   (self, event = None) :
        node = self._current_node ()
        if node :
            node.text.see (node.tail_mark)
            node.enter    ()
        return self.TNS.stop_cb_chaining
    # end def show_tail

    def _go (self, event, node) :
        self.leave    (event)
        self.text.place_cursor \
            (self.text.pos_at (node.head_mark, delta = node.level + 2))
        node.enter    (event)
        node.text.see (node.head_mark)
    # end def _go

    def go_up       (self, event = None) :
        return self._go_up_down (-1, event)
    # end def go_up

    def go_down     (self, event = None) :
        return self._go_up_down (+1, event)
    # end def go_down

    def go_left     (self, event = None) :
        node = self._current_node ()
        if node :
            if node.parent :
                node._go (event, node.parent)
            else :
                node.enter ()
        return self.TNS.stop_cb_chaining
    # end def go_left

    def go_right    (self, event = None) :
        node = self._current_node ()
        if node :
            if (node.is_open () and (not node.button.is_leaf)) :
                if node.children :
                    node._go (event, node.children [0])
                else :
                    node.enter ()
            else :
                node.enter ()
        return self.TNS.stop_cb_chaining
    # end def go_right

    def _go_up_down (self, dir, event = None) :
        node = self._current_node ()
        if node :
            n = node.number + dir
            if   node.parent : siblings = node.parent.children
            else             : siblings = node.browser.nodes
            n = min  (max (n, 0), len (siblings) - 1)
            node._go (event, siblings [n])
        return self.TNS.stop_cb_chaining
    # end def _go_up_down

    def destroy (self) :
        self.parent = None
        for c in self.children :
            c.destroy ()
        if self.level == 0 :
            self._delete (self.head_mark, self.tail_mark + " lineend +1 char")
            self.browser.nodes.remove (self)
        if self.browser.node_map.has_key (self.tag) :
            del self.browser.node_map [self.tag]
    # end def destroy

    def __str__ (self) :
        return "(%s, %d)" % (self.name, self.level)
    # end def __str__

    __repr__ = __str__

    def search_re (self, pattern, tagged_as = None, result = None) :
        """Search for occurence of `pattern' and return the node containing
           the `pattern', if any (this is either `self' or any of `self's
           children).

           If `tagged_as' is specified, `pattern' must be contained in a text
           tagged with `tagged_as' to be considered a match.
        """
        if result is None :
            result = []
        f    = self.cached_text
        tags = self.name_tags + self.header_tags + self.contents_tags
        if f :
            match = pattern.search (f)
            if match :
                if (not tagged_as) or (tagged_as in tags) :
                    result.append ((self, match.group ()))
        for c in self.children :
            c.search_re (pattern, tagged_as, result)
        return result
    # end def search_re

    def search_string (self, pattern, tagged_as = None, result = None) :
        """Search for occurence of `pattern' and return the node containing
           the `pattern', if any (this is either `self' or any of `self's
           children).

           If `tagged_as' is specified, `pattern' must be contained in a text
           tagged with `tagged_as' to be considered a match.
        """
        if result is None :
            result = []
        f    = self.cached_text
        tags = self.name_tags + self.header_tags + self.contents_tags
        if f :
            if f.find (pattern) >= 0 :
                if (not tagged_as) or (tagged_as in tags) :
                    result.append ((self, pattern))
        for c in self.children :
            c.search_string (pattern, tagged_as, result)
        return result
    # end def search_string

    def search (self, pattern, tagged_as = None, result = None) :
        if isinstance (pattern, Regexp) :
            pattern = pattern._pattern
        if isinstance (pattern, re_RegexObject) :
            return self.search_re     (pattern, tagged_as, result)
        else :
            return self.search_string (pattern, tagged_as, result)
    # end def search

    def _apply_styles (self, match, head, tail, * sty) :
        pos = pos1 = self.text.find (match, head, tail)
        while pos :
            end = self.text.pos_at (pos, delta = len (match))
            for s in sty :
                self.text.apply_style (s, pos, end)
            pos = self.text.find (match, end, tail)
        return pos1
    # end def _apply_styles

    def find_highlight (self, match, apply_found_bg = 0) :
        pos1 = self._apply_styles \
            (match, self.head_mark, self.tail_mark, styles.found)
        if pos1 :
            if apply_found_bg :
                self.text.apply_style (styles.found_bg, pos1, self.tail_mark)
            self.text.see     (self.model.tail_mark)
            self.text.see     (pos1)
    # end def find_highlight

    def find_unhighlight (self, match) :
        """Quick & dirty way is to remove *all* found styles"""
        self.text.remove_style (styles.found, self.text.bot_pos)
        # XXXXX FIXME: does the above work? if yes remove following.
#        m   = self.master
#        pos = m.search (match, self.model.head_mark, self.model.tail_mark)
#        if pos :
#            try :
#                m.tag_remove ("found_bg", pos, self.model.tail_mark)
#            except TclError :
#                pass
#        while pos :
#            end = "%s + %s chars" % (pos, len (match))
#            m.tag_remove ("found", pos, end)
#            pos = m.search (match, end, self.model.tail_mark)
    # end def find_unhighlight

# end class Node


class Node_Linked (Node) :
    def __init__ \
        ( self
        , browser                # browser widget containing the node
        , name                   # unique name of node, used as tag
        , header        = ""     # header-text of node
        , contents      = ""     # contents-text of node
        , parent        = None   # parent Node
        , number        = None   # index of self in `parent.children'
        , name_tags     = ()     # additional tags for `name'
        , header_tags   = ()     # additional tags for `header'
        , contents_tags = ()     # additional tags for `contents'
        , o_links       = ()     # objects to hyper-link
        , AC            = None   # for compatibility with __super
        ) :
        self.__super.__init__ \
            ( browser       = browser
            , name          = name
            , header        = header
            , contents      = contents
            , parent        = parent
            , number        = number
            , name_tags     = name_tags
            , header_tags   = header_tags
            , contents_tags = contents_tags
            , AC            = AC or browser.AC
            )
        self.o_links        = o_links
    # end def __init__

    def _insert_header (self, index) :
        start = self.text.pos_at    (index)
        self.__super._insert_header (index)
        self.activate_links         (start, index)
    # end def _insert_header

    def _insert_contents (self, index) :
        start = self.text.pos_at      (index)
        self.__super._insert_contents (index)
        self.activate_links           (start, index)
    # end def _insert_contents

    def _link_name (self, o) :
        if hasattr (o, "name") :
            nam = o.name
        else :
            nam = o
        return nam
    # end def _link_name

    def activate_links (self, head, tail) :
        hstyle = styles.hyper_link
        for l in self.o_links :
            if not isinstance (l, (list, tuple)) :
                l = (l, )
            for o in l :
                nam = self._link_name  (o)
                callback       = callback_style \
                    ( callback = dict \
                        ( click_1        = Functor
                            (self.follow, head_args = (o, ))
                        , double_click_1 = self.ignore
                        )
                    )
                self._apply_styles (nam, head, tail, callback, hstyle)
    # end def activate_links

    def follow (self, o, event = None) :
        return self.TNS.stop_cb_chaining
    # end def follow

# end class Node_Linked

class Browser (TFL.UI.Mixin) :
    """Hierarchical Text Browser Widget"""

    user_tags    = dict \
        ( arial     = "use arial font"
        , center    = "center text"
        , courier   = "use courier font"
        , nowrap    = "don't wrap long lines"
        , quote     = "use left and right margin " \
                      "with size of standard indentation"
        , rindent   = "use right margin with size of standard indentation"
        , title     = "use title font"
        , underline = "underline text"
        , wrap      = "wrap long lines"
        )

    file_dialog_title = "Hierarchical browser filename"

    def __init__ (self, AC, wc = None, name = None, ** kw) :
        self.__super.__init__ (AC = AC)
        self.name         = name
        self.mouse_act    = 1
        self.current_node = None
        self.text              = self.TNS.Scrolled_Text \
            (AC = AC, name = name, wc = wc, editable = False)
        # delegate some parts from our text:
        self.bot_pos      = self.text.bot_pos
        self.current_pos  = self.text.current_pos
        self.eot_pos      = self.text.eot_pos
        self.delete       = self.text.remove
        self.clear ()
        # XXXX FIXME:
        # For option lookup we should know our widget class (T_Browser?)

        if not styles.has_key ("active_node") :
            self._setup_styles ()
    # end def __init__

    def _setup_styles (self) :
        indent             = self.num_opt_val ("indent",     42)
        indent_inc         = self.num_opt_val ("indent_inc",  0)
        # Colors
        std_bg             = self.option_value \
            ("Background",             "white")
        std_fg             = self.option_value \
            ("Foreground",             "black")
        link_bg            = self.option_value \
            ("hyperLinkBackground",    std_bg)
        link_fg            = self.option_value \
            ("hyperLinkForeground",    "blue")
        found_fg           = self.option_value \
            ("foundForeground",        "black")
        found_bg           = self.option_value \
            ("foundBackground",        "deep sky blue")
        active_bg          = self.option_value \
            ("activeBackground",       "yellow")
        active_fg          = self.option_value \
            ("activeForeground",       "red")
        butt_bg            = self.option_value \
            ("activeButtonBackground", "red")
        butt_fg            = self.option_value \
            ("activeButtonForeground", "yellow")

        # Fonts
        normal_font_family = self.option_value \
            ("normalFontFamily",   "Monospace")
        normal_font_style  = self.option_value \
            ("normalFontStyle",    "normal")
        normal_font_size   = self.option_value \
            ("normalFontSize",     "medium")
        normal_font_weight = self.option_value \
            ("normalFontWeight",   "normal")
        cour_font_family   = self.option_value \
            ("courierFontFamily",  "Monospace")
        header_font_family = self.option_value \
            ("headerFontFamily",   "Sans")
        header_font_size   = self.option_value \
            ("headerFontSize",     normal_font_size)
        header_font_style  = self.option_value \
            ("headerFontStyle",    normal_font_style)
        header_font_weight = self.option_value \
            ("headerFontWeight",   "bold")
        link_font_family   = self.option_value \
            ("linkFontFamily",     normal_font_family)
        link_font_style    = self.option_value \
            ("linkFontStyle",      normal_font_style)
        title_font_family  = self.option_value \
            ("titleFontFamily",    "Sans")
        title_font_size    = self.option_value \
            ("titleFontSize",      "large")
        title_font_weight  = self.option_value \
            ("titleFontWeight",    "bold")

        styles.active_node = Style \
            ( "active_node"
            , background   = active_bg
            , foreground   = active_fg
            )
        styles.active_button = Style \
            ( "active_button"
            , background   = butt_bg
            , foreground   = butt_fg
            )
        styles.arial       = Style \
            ( "arial"
            , font_family  = "Sans"
            )
        styles.center      = Style \
            ( "center"
            , justify      = "center"
            )
        styles.courier     = Style \
            ( "courier"
            , font_family  = cour_font_family
            )
        styles.found       = Style \
            ( "found"
            , background   = found_bg
            , foreground   = found_fg
            )
        # XXXXX FIXME: Hysterical raisins? why not use found_bg above?
        styles.found_bg    = Style \
            ( "found_bg"
            , background   = "gray95"
            )
        styles.hyper_link  = Style \
            ( "hyper_link"
            , background   = link_bg
            , foreground   = link_fg
            , font_family  = link_font_family
            , font_style   = link_font_style
            , underline    = "single"
            , mouse_cursor = "hand"
            )
        styles.normal      = Style \
            ( "normal"
            , background   = std_bg
            , foreground   = std_fg
            , font_family  = normal_font_family
            , font_size    = normal_font_size
            , font_style   = normal_font_style
            , font_weight  = normal_font_weight
            , wrap         = "word"
            )
        styles.nowrap      = Style \
            ( "nowrap"
            , wrap         = "none"
            )
        styles.quote       = Style \
            ( "quote"
            , rmargin      = indent
            , lmargin1     = indent
            , lmargin2     = indent
            )
        styles.rindent     = Style \
            ( "rindent"
            , rmargin      = indent
            )
        styles.title       = Style \
            ( "title"
            , font_family  = title_font_family
            , font_size    = title_font_size
            , font_weight  = title_font_weight
            )
        styles.underline   = Style \
            ( "underline"
            , underline    = "single"
            )
        styles.wrap        = Style \
            ( "wrap"
            , wrap         = "word"
            )

        tabs = []
        for i in range (1, 16) :
            level     = "level" + `i-1`
            head_name = level + ":head"
            styles [head_name] = Style \
                ( head_name
                , lmargin1    = 0
                , lmargin2    = i * indent + indent_inc
                , font_family = header_font_family
                , font_size   = header_font_size
                , font_style  = header_font_style
                , font_weight = header_font_weight
                )
            styles [level] = Style \
                ( level
                , lmargin1  = i * indent
                , lmargin2  = i * indent + indent_inc
                )
            tabs.append (i * indent)
        self.text.set_tabs (* tabs)

    # end def _setup_styles

    def insert (self, pos, text, * styles) :
        before = self.text.pos_at (pos)
        self.text.insert (pos, text)
        after  = self.text.eol_pos (pos)
        for s in styles :
            self.text.apply_style (s, before, after)
    # end def insert

    def option_value (self, name, default) :
        # XXXXX FIXME: should be defined toolkit independent
        return default
    # end def option_value
    num_opt_val = option_value

    def print_nodes (self, file = None) :
        for n in self.nodes :
            n.print_contents (file or sys.stdout)
    # end def print_nodes

    def open_nodes (self) :
        """Open all nodes transitively"""
        try     :
            self.busy_cursor     ()
            for n in self.nodes :
                n.open (transitive = 1)
        finally :
            self.normal_cursor   ()
    # end def open_nodes

    def open (self, node) :
        """Open `node' and all its `parent' nodes."""
        parent = node
        nodes  = []
        while parent and not parent.is_open () :
            nodes.insert (0, parent)
            parent = parent.parent
        for n in nodes :
            n.open (transitive = 0)
    # end def open

    def search (self, pattern, tagged_as = None, in_nodes = ()) :
        """Search for occurence of `pattern' and return all nodes containing
           the `pattern', if any.

           If `tagged_as' is specified, `pattern' must be contained in a text
           tagged with `tagged_as' to be considered a match.

           If `in_nodes' is specified, the nodes contained in that list and
           their children are considered for the search. Otherwise,
           `self.nodes' is searched.
        """
        result = []
        for n in in_nodes or self.nodes :
            n.search (pattern, tagged_as, result)
        return result
    # end def search

    def _find_highlight (self, (node, match), apply_found_bg = 0) :
        self.open (node)
        node.find_highlight (match, apply_found_bg = 0)
    # end def _find_highlight
    
    def _find_unhighlight (self, (node, match)) :
        node.find_unhighlight (match)
    # end def _find_unhighlight

    def _find_equal (self, pattern) :
        if self._find_pattern :
            if isinstance (pattern, re_RegexObject) :
                pattern = pattern.pattern
            if isinstance (self._find_pattern, re_RegexObject) :
                old_pattern = self._find_pattern.pattern
            else :
                old_pattern = self._find_pattern
            return pattern == old_pattern
    # end def _find_equal

    def find (self, pattern, tagged_as = None, in_nodes = (), apply_found_bg = 0) :
        """Find the node containing `pattern' (tagged with `tagged_as', if
           given) and highlight that node, putting the focus into it.

           If `in_nodes' is specified, the nodes contained in that list and
           their children are considered for the search. Otherwise,
           `self.nodes' is searched.

           `pattern' can be a string or a regular expression object.
        """
        result = [None, None]
        if not pattern : return result
        if not (self._find_equal (pattern) and self._find_forward) :
            self._find_pattern = pattern
            self._find_forward = self.search (pattern, tagged_as, in_nodes)
            self._find_bakward = []
        return self.find_next ()
    # end def find

    def find_next (self) :
        """Find next occurence of `pattern' passed to last call of `find'."""
        result = None
        if self._find_current :
            self._find_unhighlight (self._find_current)
            self._find_current = []
        if self._find_forward :
            self._find_current = self._find_forward [0]
            self._find_forward = self._find_forward [1:]
            result             = self._find_current [0]
            self._find_bakward.append (self._find_current)
            self._find_highlight      (self._find_current)
        return result
    # end def find_next

    def find_prev (self) :
        """
            Find previous occurence of `pattern' passed to last call of
            `find'.
        """
        result = None
        if self._find_current :
            self._find_unhighlight     (self._find_current)
            self._find_current       = []
        if self._find_bakward :
            self._find_current       = self._find_bakward [-1]
            self._find_bakward       = self._find_bakward [:-1]
            result                   = self._find_current [0]
            self._find_forward [0:0] = [self._find_current]
            self._find_highlight       (self._find_current)
        return result
    # end def find_prev

    def clear (self) :
        self.text.clear      ()
        self.node_map      = {}
        self.nodes         = []
        self.bid_seed      = 0
        self._find_forward = []
        self._find_bakward = []
        self._find_current = None
        self._find_pattern = None
    # end def clear

# end class Browser


def help (browser) :
    """Returns a Node providing help on the usage of Browser `browser'."""
    name = browser.__class__.__name__
    r = Node \
        ( browser, "Help", " "
        , "The " + name + " widget displays an hierarchical structure "
          "and provides the possibility to expand or collapse various "
          "levels of the hierarchy. "
          "\n\n"
          "Different hierarchy levels are displayed with different "
          "indentation. The outermost level starts at the right "
          "margin of the window and each successive level starts at "
          "a bigger indentation level."
          "\n\n"
          "Each element of the hierarchical structure is marked by a "
          "circular or triangular button. A circular button means "
          "that the element doesn't contain any embedded elements, "
          "i.e., the element is a leaf. "
          "\n\n"
          "A triangular button means that the element contains "
          "embedded elements. If the triangle points to the right "
          "the embedded elements are collapsed. By clicking on the "
          "triangular button with the left mouse button you can "
          "expand them -- the triangle now points downwards. "
          "\n\n"
        )
    n = r.new_child \
        ( "Key bindings", ""
        , "The " + name + " is a read-only widget. The keybindings "
          "available allow navigation between elements and "
          "expansion and collapsing of elements."
          "\n\n"
        )
    n.new_child \
        ( "<Up>"
        , "Move to previous element on same hierarchy level. If "
          "already on first element of current hierarchy level, "
          "move to last element of this level."
        )
    n.new_child \
        ( "<Down>"
        , "Move to next element on same hierarchy level. If "
          "already on last element of current hierarchy level, "
          "move to first element of this level."
        )
    n.new_child \
        ( "<Left>"
        , "Move to parent element (one hierarchy level up). "
        )
    n.new_child \
        ( "<Right>"
        , "Move to first child element (one hierarchy level down). "
          "This works only if the current element has children and "
          "is already expanded."
        )
    n.new_child \
        ( "<Insert>"
        , "Expand current element (show children), if possible."
        )
    n.new_child \
        ( "<Delete>"
        , "Collapse current element (hide children), if possible."
        )
    n.new_child \
        ( "<Home>"
        , "Show start of current element."
        )
    n.new_child \
        ( "<End>"
        , "Show end of current element."
        )
    n = r.new_child \
        ( "Widget configuration", ""
        , "The " + name + " widget can be configured via the TK "
          "resource database. The full semantics of the TK "
          "resource database is described in the Tcl/TK "
          "documentation. "
          "\n\n"
          "To configure all " + name + " widgets in an application, "
          "you add statements like "
          "\n\n"
          "    `*" + name + "*activeBackground: yellow'"
          "\n\n"
          "to the configuration file of the application. "
          "\n\n"
          "To configure a specific " + name + " widget, "
          "you add statements like "
          "\n\n"
          "    `*" + browser.name +  "*activeForeground: red'"
          "\n\n"
          "to the configuration file of the application. "
          "\n\n"
        )
    n.new_child \
        ( "indent", ""
        , "The `indent' configuration parameter defines the amount "
          "of indentation added for each hierarchy level. A pure "
          "number specifies the indentation in pixels. By appending "
          "`c', `m', or `i', you can specify the indentation in "
          "centimeters, millimeters, or inches, respectively."
          "\n"
        )
    n.new_child \
        ( "indent_inc", ""
        , "The `indent_inc' configuration parameter defines the "
          "indentation added for wrapped lines. It is added to the "
          "indent parameter."
          "\n"
        )
    n.new_child \
        ( "hFont", ""
        , "The `hFont' configuration parameter specifies the font "
          "used for the first line of an element. "
        )
    return r
# end def help

if __name__ != "__main__" :
    TFL.UI._Export_Module ()
### __END__ TFL.UI.HTB
