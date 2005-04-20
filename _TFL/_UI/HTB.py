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
#    25-Feb-2005 (RSC) `wtk_widget' and `exposed_widget' delegated from
#                      Browser to its Text
#     7-Mar-2005 (RSC) Corrected style-handling: Now the "normal" style
#                      is alway last, butcon also gets correct color.
#     8-Mar-2005 (RSC) `push_style' to butcon in _insert_button instead
#                      of `apply_style' (and pop it when not needed)
#     9-Mar-2005 (CT)  `destroy` exorcised of Tk-isms
#     9-Mar-2005 (CT)  Fix of `destroy` fixed
#    11-Mar-2005 (RSC) Fix for styles: Moved style caching from Node to
#                      Browser. Now retain old "insert" interface in
#                      Browser (using tags) and provide new _insert
#                      interface (using styles).
#    11-Mar-2005 (CT)  `_setup_styles` fixed (same defaults as in old option
#                      files)
#    11-Mar-2005 (CT)  Call of `set_tabs` moved from `_setup_styles` to
#                      `__init__` (must be done for *each* `Text` instance)
#    11-Mar-2005 (CT)  `_style` call in `insert` fixed (`*`)
#    11-Mar-2005 (CT)  `_style` changed to use `un_nested` (ugly legacy lifter)
#    11-Mar-2005 (CT)  `_tabs` moved to `styles` (after removing an overly
#                      paranoid guard in `Style.__getattr__`)
#    14-Mar-2005 (CT)  `Browser.__init__` changed to call `clear` at the very
#                      end (otherwise, descendents redefining `clear` to
#                      insert some text fail miserably)
#    14-Mar-2005 (CT)  Child `Widget configuration` removed from `help`
#                      (Tk-specific information)
#    14-Mar-2005 (RSC) __getitem__ = __getattr in Styles_Cache
#                      Fixed formatting of multi-line "name" of a node
#                      (RUP 14228)
#    14-Mar-2005 (RSC) Fixed auto-wrap of "name" line of a node.
#    15-Mar-2005 (RSC) Use `lift` parameter of Text.apply_style for
#                      hyper-links, search results, and selected nodes
#                      (in Node.enter)
#    15-Mar-2005 (RSC) `_insert_header` now again formats the `name`
#                      parameter of a node, now links in the name work
#                      again because _insert_header was overridden in
#                      Node_Linked.
#    21-Mar-2005 (RSC) Introduced anonymous nodes that consist only of a
#                      header, this gets rid of the body of a node and
#                      does everything with anonymous nodes.
#                      Now an open node may optionally have a different
#                      header when opened/closed (new optional argument
#                      `head_open`)
#    29-Mar-2005 (CT)  `add_contents` changed to pass named arguments to
#                      `self.__class__`
#    29-Mar-2005 (CT)  `_insert` changed to accept optional arguments
#                      `head_text` and `tail_text`
#    29-Mar-2005 (CT)  `_insert_header` streamlined and changed to use
#                      `head_text` and `tail_text`
#    29-Mar-2005 (CT)  `Browser._insert` changed to allow a callable for `text`
#    29-Mar-2005 (CT)  s/head_open/header_open/g
#    29-Mar-2005 (CT)  Handling of `header_open` changed to allow `""` for it
#                      (i.e., to treat `None` and `""` differently)
#     8-Apr-2005 (CT)  `Node.add_contents` changed to call `Node` instead of
#                      `self.__class__`
#    11-Apr-2005 (MZO) implemented xml_node, cmd_mgr
#    13-Apr-2005 (BRU) call `self.__class__` again in `add_contents`
#    12-Apr-2005 (MZO) removed TGW imports. UI shall tk-independ, i14841
#    14-Apr-2005 (MZO) fixed i14841 - TOM._TKT.Mixin => UI.Mixin
#    14-Apr-2005 (CT)  `bot_pos`, `eot_pos`, and `current_pos` replaced by
#                      `buffer_head`, `buffer_tail`, and `insert_mark`,
#                      respectively
#    14-Apr-2005 (BRU) Fixed gauge activation.
#    20-Apr-2005 (MZO) Moved pdf geneartion to X4T._U2X.HTB_as_XML
#    20-Apr-2005 (BRU) Added search to command manager, various fixes.
#    20-Apr-2005 (MZO) added tail/head_contents
#    ««revision-date»»···
#--

from   _TFL         import TFL
from   Regexp       import Regexp, re_RegexObject
from   Functor      import Functor

import _TFL._UI
import _TFL._UI.Mixin
from   _TFL._UI.Style import *

from   predicate      import un_nested

import sys
import sos

from   _X4T         import X4T
import _X4T._U2X
import _X4T._U2X.HTB_as_XML
import _X4T._X2P
import _X4T._X2P.XML_to_PDF

import _TFL.Environment

callback_style = Style ("callback")

class Styles_Cache (object) :
    """Used to store module-wide styles."""

    styles = {}

    def __getattr__ (self, name) :
        return self.styles [name]
    # end def __getattr__

    def __setattr__ (self, name, value) :
        self.styles [name] = value
    # end def __setattr__

    __getitem__  = __getattr__

    __setitem__  = __setattr__

    __contains__ = has_key = styles.has_key

# end class Styles_Cache

styles = Styles_Cache ()

class Button (TFL.UI.Mixin) :

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

    eager_pre                  = lambda *args : True
    eager_pre.evaluate_eagerly = True


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
        , header_open   = None   # header-text of open node
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
            , header_open   = header_open
            )
        if AC is not None :
            self.gauge      = AC.ui_state.gauge
        else :
            self.gauge      = None
        if header_open is None :
            header_open  = header
        self.browser     = browser
        self.text        = browser.text
        self.name        = name
        self.header      = header
        self.header_open = header_open
        self.parent      = parent
        self.number      = number
        self.bid_seed    = 0
        self.anonymous   = header and not (contents or name)
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
            self.bid        = "%s:%d"  % (parent.bid, parent.bid_seed)
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
        self.head_tag  = self.level_tag + ':head'
        if browser.node_map.has_key (self.tag) :
            raise Name_Clash, self.tag
        browser.node_map [self.tag] = self
        self.children               = []
        self.tags                   = ()
        self.head_mark              = None
        self.body_mark              = None
        self.butt_mark              = None
        self.tail_mark              = None
        self.button                 = None
        if name_tags     : self.name_tags     = filter (None, name_tags)
        if header_tags   : self.header_tags   = filter (None, header_tags)
        if contents_tags : self.contents_tags = filter (None, contents_tags)
        self.cached_text = ("%s" * 4) % \
           ( self.name, self.header_head,   self.header,   self.header_tail)
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
        if contents :
            self.add_contents (contents)
    # end def __init__

    def is_open (self) :
        return self.button and not self.button.closed
    # end def is_open

    def add_contents (self, contents) :
        """Add an anonymous child inheriting several attributes from the
           parent to guarantee correct formatting as a contents node.
        """
        number = len (self.children)
        child = self.__class__ \
            ( browser     = self.browser
            , name        = ''
            , header      = contents
            , contents    = ''
            , parent      = self
            , number      = number
            , header_tags = self.contents_tags
            )
        self._insert_child  (child)
        child.header_head = self.contents_head
        child.header_tail = self.contents_tail
        child.level_tag   = self.level_tag
        child.head_tag    = self.level_tag
        # Delegate enter/leave events to parent
        child.enter       = self.enter
        child.leave       = self.leave
        return child
    # end def add_contents

    def new_child (self, name, header = "", contents = "") :
        """Add child named `name' to `self'."""
        number = len              (self.children)
        child  = self.__class__   \
            ( self.browser, name
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
           the insert_mark in the text widget. We depend on the magic
           behaviour of the mark position (that it changes with
           insertions).
        """
        self.tags = filter (None, (self.tag, ) + tags)
        head = self.text.pos_at (mark)
        if not self.anonymous :
            if self.level :
                self._insert (mark, "\t" * self.level)
            self.butt_mark   = self.text.mark_at (mark, left_gravity = True)
            self._insert_button                  ()
            self._insert                         (mark, "\t")
            self._insert_name                    (mark)
        body = self.text.pos_at                  (mark)
        self._insert_header                      (mark)
        tail = self.text.pos_at                  (mark)
        self._insert                             (mark, "\n")
        self.head_mark       = self.text.mark_at (head, left_gravity = True)
        self.body_mark       = self.text.mark_at (body, left_gravity = True)
        self.tail_mark       = self.text.mark_at (tail)
        self.text.apply_style \
            ( styles [self.head_tag]
            , self.head_mark
            , self.text.eol_pos (self.head_mark)
            )
        self.text.apply_style \
            ( styles [self.level_tag]
            , self.text.bol_pos (self.head_mark, line_delta = 1)
            , body
            )
    # end def insert

    def _style (self, * tags) :
        return self.browser._style (* (self.tags + tags))
    # end def _style

    def _insert_button (self) :
        if not self.button :
            self.button = Button \
                ( self
                , is_leaf = not self.children
                )
        else :
            self.button.butcon.pop_style ()
        self.text.insert_widget \
            ( self.butt_mark
            , self.button.butcon
            )
        self.button.butcon.push_style (self._style ())
    # end def _insert_button

    def _insert (self, index, text, * tags, ** kw) :
        self.browser._insert \
            (index, text, self.callback, self._style (* tags), ** kw)
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

    def _insert_name (self, index) :
        if not self.anonymous :
            self._insert (index, self.name, "header", * self.name_tags)
    # end def _insert_name

    def _insert_header (self, index) :
        header = self.header
        if (   self.button
           and not self.button.is_leaf
           and not self.button.closed
           ) :
            header = self.header_open
        if header :
            self._insert \
                ( index, header, self.level_tag
                , * self.header_tags
                , ** dict
                      ( head_text = self.header_head
                      , tail_text = self.header_tail
                      )
                )
    # end def _insert_header

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
        output = "".join (parts)
        output = output.replace ("\n", "\n" + indent) + "\n"
        file.write (output)
        if open :
            for c in self.children :
                c.print_contents (file)
    # end def print_contents


    def open (self, event = None, transitive = 0, show_gauge = False) :
        if self.button and not self.button.is_leaf :
            if show_gauge and self.gauge :
                self.gauge.pulse ()        
            if self.button.closed :
                self.button.open ()
                self._delete        (self.body_mark, self.tail_mark)
                self._insert_header (self.tail_mark)
                self._insert        (self.tail_mark, "\n")
                for c in self.children :
                    c.insert (self.tail_mark, * self.tags)
            if transitive :
                for c in self.children :
                    c.open (event, transitive - 1, show_gauge = show_gauge)
    # end def open

    def close (self, event = None, transitive = 0) :
        if self.button and not self.button.is_leaf :
            if not self.button.closed :
                for c in self.children :
                    c.close  (event, transitive = 0)
                    c.tags   = ()
                    c.button = None
                self.button.close   ()
                self._delete        (self.body_mark, self.tail_mark)
                self._insert_header (self.tail_mark)
            if transitive and self.parent :
                self.parent.close (event, transitive - 1)
    # end def close

    def enter (self, event = None) :
        head = self.head_mark
        bol  = self.text.bol_pos (head, line_delta = 1)
        self.text.apply_style \
            (styles.active_node, head, bol, lift = True)
        self.browser.current_node = self
    # end def enter

    def leave (self, event = None) :
        self.text.remove_style (styles.active_node, self.text.buffer_head)
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
            text = self.browser.text
            tail = text.pos_at (text.eol_pos (self.tail_mark), delta = 1)
            self._delete (self.head_mark, tail)
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
                self.text.apply_style (s, pos, end, lift = True)
            pos = self.text.find (match, end, tail)
        return pos1
    # end def _apply_styles

    def find_highlight (self, match, apply_found_bg = 0) :
        pos1 = self._apply_styles \
            (match, self.head_mark, self.tail_mark, styles.found)
        if pos1 :
            if apply_found_bg :
                self.text.apply_style (styles.found_bg, pos1, self.tail_mark)
            self.text.see (self.tail_mark)
            self.text.see (pos1)
    # end def find_highlight

    def find_unhighlight (self, match) :
        """Quick & dirty way is to remove *all* found styles"""
        self.text.remove_style (styles.found, self.text.buffer_head)
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
        , header_open   = None   # different header for opened node
        , AC            = None   # for compatibility with __super
        ) :
        self.o_links        = o_links
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
            , header_open   = header_open
            , AC            = AC or browser.AC
            )
    # end def __init__

    def _insert_name (self, index) :
        start = self.text.pos_at    (index)
        self.__super._insert_name   (index)
        self.activate_links         (start, index)
    # end def _insert_name

    def _insert_header (self, index) :
        start = self.text.pos_at    (index)
        self.__super._insert_header (index)
        self.activate_links         (start, index)
    # end def _insert_header

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

    def add_contents (self, contents) :
        """Add an anonymous child inheriting several attributes from the
           parent to guarantee correct formatting as a contents node.
        """
        child = self.__super.add_contents (contents)
        child.o_links = self.o_links
    # end def add_contents

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
        self.gauge          = AC.ui_state.gauge
        self._dialog_title  = AC.ANS.Version.productname
        self._parent        = wc
        self.name           = name
        self.mouse_act      = 1
        self.current_node   = None
        self.nodes          = []
        self.text           = self.TNS.Scrolled_Text \
            (AC = AC, name = name, wc = wc, editable = False)
        self._setup_command_mgr  (AC, self.TNS)
        if self._ci_context_menu is not None :
            sig_binder = self.TNS.Eventname.click_3
            sig_binder.bind_add (self.text.wtk_widget, self._cb_context_menu)
        # delegate some parts from our text:
        self.buffer_head    = self.text.buffer_head
        self.insert_mark    = self.text.insert_mark
        self.buffer_tail    = self.text.buffer_tail
        self.delete         = self.text.remove
        self.wtk_widget     = self.text.wtk_widget

        self.wtk_widget.ui = self   # back reference


        self.exposed_widget = self.text.exposed_widget
        if not styles.has_key  ("active_node") :
            self._setup_styles ()
        self.text.apply_style  (styles.normal)
        self.text.set_tabs     (* styles._tabs)
        self.clear ()
        self.cmd_mgr_widget.update_state        ()
    # end def __init__

    def _setup_styles (self) :
        indent             = self.num_opt_val ("indent",     22)
        indent_inc         = self.num_opt_val ("indent_inc",  0)
        # Colors
        std_bg             = self.option_value \
            ("Background",             "lightyellow2")
        std_fg             = self.option_value \
            ("Foreground",             "black")
        link_bg            = self.option_value \
            ("hyperLinkBackground",    std_bg)
        link_fg            = self.option_value \
            ("hyperLinkForeground",    "blue")
        found_fg           = self.option_value \
            ("foundForeground",        "black")
        found_bg           = self.option_value \
            ("foundBackground",        "light sky blue")
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
            ("headerFontWeight",   "normal")
        link_font_family   = self.option_value \
            ("linkFontFamily",     normal_font_family)
        link_font_style    = self.option_value \
            ("linkFontStyle",      normal_font_style)
        title_font_family  = self.option_value \
            ("titleFontFamily",    "Sans")
        title_font_size    = self.option_value \
            ("titleFontSize",      "x-large")
        title_font_weight  = self.option_value \
            ("titleFontWeight",    "normal")
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
        styles.noindent    = Style \
            ( "noindent"
            , lmargin1     = 0
            , lmargin2     = 0
            )
        styles.header      = Style \
            ( "header"
            , font_family  = header_font_family
            , font_size    = header_font_size
            , font_style   = header_font_style
            , font_weight  = header_font_weight
            )
        tabs = styles._tabs = []
        for i in range (1, 16) :
            level = "level" + `i-1`
            head  = level + ':head'
            styles [level] = Style \
                ( level
                , lmargin1  = i * indent
                , lmargin2  = i * indent + indent_inc
                )
            styles [head] = Style \
                ( head
                , styles [level]
                , lmargin1  = 0
                )
            tabs.append (i * indent)
    # end def _setup_styles

    def _insert (self, pos, text, * styles, ** kw) :
        before = self.text.pos_at (pos)
        for t in kw.get ("head_text"), text, kw.get ("tail_text") :
            if callable (t) :
                t (self.text, pos)
            elif t :
                self.text.insert (pos, t)
        after = self.text.eol_pos (pos)
        for s in styles :
            self.text.apply_style (s, before, after)
        self.cmd_mgr_widget.update_state ()
    # end def _insert

    def _style (self, * tags) :
        """Implement style chaching"""
        tags = [t for t in un_nested (tags) if t in styles]
        tags.reverse ()
        tags.append  ('normal')
        tags = tuple (tags)
        if tags not in styles :
            styles [tags] = Style (str (tags), * [styles [t] for t in tags])
        return styles [tags]
    # end def _style

    def head_contents (self) : 
        # return text before first node
        # MZO 20-Apr-2005 future : adapt anonymous nodes (handle text between 
        #     nodes... Currently anonymous nodes designed for content 
        #     i.e. as child (has parent node) and nodes always appended.
        mark_0   = self.text.buffer_head
        mark_end = None  
        if self.nodes :  
            mark_end = self.nodes[0].head_mark
        return self.text.get (mark_0, mark_end)
    # end def head_contents
        
    def tail_contents (self) : 
        # return text after last node or "\n"
        mark_0   = None
        mark_end = self.text.buffer_tail
        if self.nodes :  
            mark_0 = self.nodes[-1].tail_mark
        return self.text.get (mark_0, mark_end)
    # end def tail_contents
    
    def insert (self, pos, text, * tags) :
        # ?? expected pos START, INSERT, END
        self._insert (pos, text, self._style (* tags))
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

    def open_nodes (self, event = None) :
        """Open all nodes transitively"""
        self._activate_gauge (label = "Opening nodes")
        try     :
            for n in self.nodes :
                n.open (transitive = 1, show_gauge = True)
        finally :
            self._deactivate_gauge ()
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

    def _activate_gauge (self, label = "") :
        self.gauge.activate_activity_mode \
            ( title = self._dialog_title
            , label = label
            )
    # end def _activate_gauge

    def _deactivate_gauge (self) :
        self.gauge.deactivate ()
    # end def _deactivate_gauge

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
        self.cmd_mgr_widget.update_state ()       
    # end def clear

    def _setup_command_mgr (self, AC, TNS) :
        """ create und setup command_mgr
        """
        if hasattr (self._parent, "new_menubar") : # wc = Toplevel
            self._ci_mb           = self._parent.new_menubar ()
        else :
            self._ci_mb           = None
        if hasattr (self.text, "new_context_menu") : # context menu from text
            self._ci_context_menu = self.text.new_context_menu ()
        else :
            self._ci_context_menu = None
        interfacers   = dict \
            ( [ (name, i)
                for (name, i) in
                    [ ( "cm", self._ci_context_menu), ("mb", self._ci_mb) ]
                    if i is not None
              ]
            )
        if_n = interfacers.keys ()
        ANS = AC.ANS
        self.change_counter  = ANS.UI.Change_Counter (scope = None)
        self.cmd_mgr_widget  = ANS.UI.Command_Mgr \
            ( AC             = AC
            , change_counter = self.change_counter
            , interfacers    = interfacers
            )
        cmd_mgr = self.cmd_mgr_widget
        file_g = cmd_mgr.add_group \
            ( "File"
            , "Commands which are applied to the file menu"
            , if_names = if_n
            )
        edit_g = cmd_mgr.add_group \
            ( "Edit"
            , "Commands which are applied to the edit menu"
            , if_names = if_n
            )
        ### XXX FIXME - no pdf for TK toolkit
        Cmd = self.ANS.UI.Command
        file_g.add_command \
            ( Cmd ( "Generate_PDF"
                  , self._cb_generate_pdf
                  , precondition = self._pre_generate_pdf
                  )
            , if_names     = if_n
            )
        # insert clipboard cmds.....
        edit_g.add_command \
            ( Cmd ( "Expand All"
                  , self.open_nodes
                  , precondition = self._pre_has_nodes
                  )
            , if_names     = if_n
            )
        edit_g.add_command \
            ( Cmd ( "Find"
                  , self._ask_find
                  , precondition = self._pre_has_find
                  )
            , if_names     = if_n
            , underline    = 0
            , accelerator  = self.TNS.Eventname.search
            )
        edit_g.add_command \
            ( Cmd ( "Find next"
                  , self._do_find_next
                  , precondition = self._pre_has_find_next
                  )
            , if_names     = if_n
            , underline    = 5
            , accelerator  = self.TNS.Eventname.search_next
            )
        edit_g.add_command \
            ( Cmd ( "Find previous"
                  , self._do_find_prev
                  , precondition = self._pre_has_find_prev
                  )
            , if_names     = if_n
            , underline    = 5
            , accelerator  = self.TNS.Eventname.search_prev
            )                   
        cmd_mgr.set_auto_short_cuts ()
    # end def _setup_command_mgr

    def _ask_find (self) :
        # XXX extend to present dialog with search options
        pattern = self.text.ask_string \
            (title = self._dialog_title, prompt = "Search for:")
        self._do_find (self.find, pattern)
    # end def _ask_find

    def _do_find (self, func, *args) :
        result = func (*args)
        if result is None :
            print "%s not found" % self._find_pattern
    # end def _do_find

    def _do_find_next (self) :
        self._do_find (self.find_next)
    # end def _do_find_next

    def _do_find_prev (self) :
        self._do_find (self.find_prev)
    # end def _do_find_prev

    def _pre_generate_pdf (self, *args) : 
        return TFL.Environment.system == "win32" and self._pre_has_nodes ()
    # end def _pre_generate_pdf
    _pre_generate_pdf.evaluate_eagerly = True

    def _pre_has_find (self) :
        return (self.text.pos_at (self.text.buffer_tail) > 0)
    # end def _pre_has_find
    _pre_has_find.evaluate_eagerly = True

    def _pre_has_find_next (self) :
        return self._find_pattern is not None
    # end def _pre_has_find_next
    _pre_has_find_next.evaluate_eagerly = True
    _pre_has_find_prev = _pre_has_find_next

    def _pre_has_nodes (self) :
        return self.nodes
    # end def _pre_has_nodes
    _pre_has_nodes.evaluate_eagerly = True

    def _cb_context_menu (self, event) :
        """ cb mouse pressed => popup context menu
        """
        self.cmd_mgr_widget.interfacers ["cm"].popup (event)
        return self.TNS.stop_cb_chaining
    # end def _cb_context_menu

    def _cb_generate_pdf (self, event = None) : 
        self._activate_gauge (label = "Generate PDF")
        try :
            xml = X4T.U2X.HTB_as_XML (self)
            filename = "".join ([sos.tempfile_name (), ".pdf"])
            message_win = self.AC.ui_state.message
            message_win.write ("Create file: %s\n" % filename)
            pdf = X4T.X2P.XML_to_PDF (xml, filename = filename, gui = self.text)
            pdf.open_pdf ()
        finally :
            self._deactivate_gauge ()
    # end def _cb_generate_pdf

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
    return r
# end def help

if __name__ != "__main__" :
    TFL.UI._Export_Module ()
### __END__ TFL.UI.HTB
