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
#    ««revision-date»»···
#--

from   _TFL         import TFL
from   Regexp       import Regexp

import _TFL._UI
import _TFL._UI.Mixin
import sys

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
        ) :
        assert (  ((not parent) and (number is None))
               or ((parent)     and (number >= 0))
               )
        self.__super.__init__ (AC = browser.AC)
        self.browser   = browser
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
                self.browser.disable ()
        else :
            self.bid        = "%s:%d" % (parent.bid, parent.bid_seed)
            self.tag        = "%s::%s" % (self.bid, self.name)
            parent.bid_seed = parent.bid_seed + 1
            self.level      = parent.level + 1
        for clean, by in self.cleanup :
            self.tag   = clean.sub (by, self.tag)
        self.bind_tag  = self.tag + "#bind"
        self.level_tag = "level" + `self.level`
        if browser.node_map.has_key (self.tag) :
            raise Name_Clash, self.tag
        browser.node_map [self.tag] = self
        self.children  = []
        self.tags      = ()
        self.head_mark = self.tag + ":head"
        self.body_mark = self.tag + ":body"
        self.butt_mark = self.tag + ":butt"
        self.tail_mark = self.tag + ":tail"
        self.button    = None
        if name_tags     : self.name_tags     = filter (None, name_tags)
        if header_tags   : self.header_tags   = filter (None, header_tags)
        if contents_tags : self.contents_tags = filter (None, contents_tags)
        self.cached_text = ("%s" * 7) % \
           ( self.name
           , self.header_head,   self.header,   self.header_tail
           , self.contents_head, self.contents, self.contents_tail
           )
        self.tkt = self.TNS.HTB.Node (self, browser)
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

    def insert (self, index, * tags) :
        self.tags = filter (None, (self.tag, ) + tags)
        self.tkt.insert (index, * tags)
    # end def insert

    def _insert_button (self) :
        if not self.button :
            self.button = self.TNS.HTB.Button \
                ( self.tkt
                , is_leaf = not (self.children or self.contents)
                )
            self.tkt._display_button ()
    # end def _insert_button

    def _insert (self, index, text, * tags) :
        tags = filter (None, self.tags + (self.bind_tag, ) + tags)
        self.browser.insert (index, text, tags)
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
            file_name = self.browser.ask_save_file_name \
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
            ### else : node.print_contents ()
        return "break"
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
        output = string.join (parts, "")
        output = string.replace (output, "\n", "\n" + indent) + "\n"
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

    def mouse_enter (self, event = None) :
        if self.browser.mouse_act        : self.enter (event)
    # end def mouse_enter

    def mouse_leave (self, event = None) : self.leave (event)

    def set_cursor (self, index) :
        self._set_cursor         (index)
        self.browser.focus_force ()
    # end def set_cursor

    def _current_node (self) :
        self.browser.mouse_act = 0
        return self.tkt._current_node ()
    # end def _current_node

    def activate_mouse (self, event = None) :
        self.browser.mouse_act = 1
    # end def activate_mouse

    def ignore (self, event = None) :
        self.browser.mouse_act = 0
        return self.tkt.ignore (event)
    # end def _current_node

    def expand (self, event = None, transitive = 0) :
        node = self._current_node ()
        if node :
            node.open  (event, transitive)
            node.enter ()
        return "break"
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
        return "break"
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
            node.see   (node.head_mark)
            node.enter ()
        return "break"
    # end def show_head

    def show_tail   (self, event = None) :
        node = self._current_node ()
        if node :
            node.see   (node.tail_mark)
            node.enter ()
        return "break"
    # end def show_tail

    def go_up       (self, event = None) : return self._go_up_down (-1, event)
    def go_down     (self, event = None) : return self._go_up_down (+1, event)

    def go_left     (self, event = None) :
        node = self._current_node ()
        if node :
            if node.parent :
                node._go (event, node.parent)
            else :
                node.enter ()
        return "break"
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
        return "break"
    # end def go_right

    def _go_up_down (self, dir, event = None) :
        node = self._current_node ()
        if node :
            n = node.number + dir
            if   node.parent : siblings = node.parent.children
            else             : siblings = node.browser.nodes
            n = min  (max (n, 0), len (siblings) - 1)
            node._go (event, siblings [n])
        return "break"
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
            if string.find (f, pattern) >= 0:
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

    def enter (self, event = None) : self.tkt.enter (event)
    def leave (self, event = None) : self.tkt.leave (event)

# end class Node

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

    def __init__ (self, AC, master, name = None, state = None, ** kw) :
        self.__super.__init__ (AC = AC)
        self.name      = name
        self.tkt       = self.TNS.HTB.Browser (master, name, state, **kw)
        self.clear     ()
        self.mouse_act = 1
    # end def __init__

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
        self.tkt.clear       ()
        self.node_map      = {}
        self.nodes         = []
        self.bid_seed      = 0
        self._find_forward = []
        self._find_bakward = []
        self._find_current = None
        self._find_pattern = None
    # end def clear

    # delegate to our tkt:
    def __getattr__ (self, name) :
        result = getattr (self.tkt, name)
        setattr (self, name, result)
        return result
    # end def __getattr__

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
