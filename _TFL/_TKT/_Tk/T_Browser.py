# -*- coding: iso-8859-15 -*-
# Copyright (C) 1998-2007 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
#
#++
# Name
#    T_Browser
#
# Purpose
#    Hierarchical browser implemented with TK Text widget
#
# Revision Dates
#    27-May-1998 (CT) Creation
#     1-Jun-1998 (CT) Protect change of state by finally-clause
#     5-Jun-1998 (CT) T_Node_Linked added (factored from TTA_Error_Widget)
#     6-Jun-1998 (CT) `transitive' added to `open' and `close'
#     6-Jun-1998 (CT) `name_tags', `header_tags', `contents_tags' added
#     6-Jun-1998 (CT) `header_head', `header_tail', `contents_head', and
#                     `contents_tail' added
#     7-Jun-1998 (CT) Merged `T_Bullet' and `T_Button' into `T_Button'
#     7-Jun-1998 (CT) Button naming corrected (`bid' introduced)
#    16-Jun-1998 (CT) Horizontal scrollbar added
#    16-Jun-1998 (CT) `grid' used instead of `pack' to layout the `T_Browser'
#                     widget
#    14-Jul-1998 (CT) `Control C' enabled to allow copying a text selection
#     5-Aug-1998 (CT) `T_Button' queries its fore- and background colors
#     5-Aug-1998 (CT) `bid' changed so that it works if nodes are deleted
#    11-Aug-1998 (CT) `Node_Linked_.hyper_tags' added
#    16-Aug-1998 (CT) Renamed `CT_TK.script_path' to `CT_TK.path'
#    16-Aug-1998 (CT) Use `Functor' instead of lambda for key-bindings
#    27-Aug-1998 (CT) Replaced `tkFileDialog.asksaveasfilename' by
#                     `ask_save_file_name'
#     6-Sep-1998 (CT) `Scrolled_Text' factored from `T_Browser'
#    30-Oct-1998 (CT) Converted `CTK.path' into `CTK.path ()'
#    13-Nov-1998 (CT) `t_open_1' shows busy cursor
#    13-Nov-1998 (CT) Button: use `t_open' instead of `node.open'
#     3-Mar-1999 (CT) `if not hasattr (o, "name") : break' added to
#                     `activate_links'
#    17-Mar-1999 (CT) Activate all occurences of a link (instead of only the
#                     first one)
#     4-Jun-1999 (CT) `T_Browser.clear' added
#    10-Aug-1999 (CT) `self.Ancestor' replaced by `T_Browser.Ancestor'
#    19-Oct-1999 (CT) `file_dialog_title' factored
#    19-Oct-1999 (CT) Extensions `.txt' and `.list' added to file dialog
#    19-Oct-1999 (CT) `print_*_head' factored
#    22-Oct-1999 (CT) Don't print `contents' of closed nodes
#    29-Oct-1999 (CT) Filter tags (somehow, an '' masquerading as a tag
#                     sneaked in and confused `_current_node')
#    29-Oct-1999 (CT) `print_nodes' added to `T_Browser'
#    29-Oct-1999 (CT) `find' and `search' added
#    31-Oct-1999 (CT) `find_next' and `find_prev' factored
#    31-Oct-1999 (CT) `search_re' added
#     2-Nov-1999 (CT) `cached_text' added to `T_Node' and used for searching
#     3-Nov-1999 (CT) Don't write to standard output if `ask_save_file_name'
#                     returns `None'
#     6-Dec-1999 (CT) `title' tag added
#    22-Dec-1999 (CT) `open_nodes' added
#    21-Jan-2000 (CT) `T_Browser.user_tags' added
#     7-Mar-2000 (CT) `_find_highlight' changed to `see' tail of matched
#                     node, too
#     7-Mar-2000 (CT) Tag `found_bg' added
#    29-Mar-2000 (CT) Use `CT_TK.image_mgr'
#    13-Apr-2000 (CT) Use `CTK.bitmap_mgr' instead of `CTK.image_mgr'
#    13-Apr-2000 (CT) `Ancestor' replaced by `__Ancestor'
#                     (can use `self.__Ancestor' instead of `<class>.Ancestor')
#    19-Sep-2000 (CT) Keep two lists `_find_forward' and `_find_bakward' plus
#                     `_find_current' instead of one multi-purpose list
#                     `_find_result'
#    13-Dec-2000 (CT) s/data base/database/g
#     4-Apr-2001 (CT) Use `Regexp' to be compatible with Python 2.0
#                     (`sre' doesn't export RegexObject, anymore)
#     7-Nov-2001 (CT) Tags for non-parent nodes changed
#    15-Apr-2002 (CT) String exception replaced by Name_Clash
#    11-Jun-2003 (CT) s/== None/is None/
#    15-Apr-2004 (CT) `apply` calls removed
#    15-Apr-2004 (CT) `map` with side effects replaced by loop
#    21-Apr-2004 (CT) `_set_cursor` factored
#    21-Apr-2004 (CT) `_set_cursor` changed to try both `tkTextSetCursor` and
#                     `tk::TextSetCursor` (the newest TK version uses a
#                     different name)
#    26-Apr-2004 (AHE) Missing `()` added to `close`
#    25-May-2004 (AHE) cosmetic changes to fit style guidelines
#    28-Sep-2004 (CT)  Use `isinstance` instead of type comparison
#    30-Aug-2005 (CT)  Use `in` instead of `find`
#     2-Aug-2007 (CED) Coding guidelines
#    19-Nov-2007 (CT)  Imports corrected
#    19-Nov-2007 (CT)  `string` functions replaced by `str` methods
#    ««revision-date»»···
#--

from   _TFL._TKT._Tk.CT_TK import *
from   _TFL.Functor        import Functor
from   _TFL.Regexp         import *
import sys

class T_Button :

    clsd_bitmap_name = "closed_node"
    leaf_bitmap_name = "circle"
    open_bitmap_name = "open_node"

    def __init__ (self, node, is_leaf = 1) :
        self.node     = node
        self.is_leaf  = not is_leaf ### negate for `make_[non_]leaf'
        self.closed   = 0
        self.c_bitmap = bitmap_mgr [self.clsd_bitmap_name]
        self.l_bitmap = bitmap_mgr [self.leaf_bitmap_name]
        self.o_bitmap = bitmap_mgr [self.open_bitmap_name]
        if is_leaf : bitmap = self.l_bitmap
        else       : bitmap = self.c_bitmap
        self.window   = Label ( node.master
                              , name        = ":button:" + node.bid
                              , bitmap      = bitmap
                              , borderwidth = 0
                              , background  = node.master.cget ("background")
                              )
        if is_leaf :
            self.make_leaf    ()
        else :
            self.make_non_leaf()
        self.window.bind      ("<Enter>",         self.mouse_enter)
        self.window.bind      ("<Leave>",         self.mouse_leave)
        self.bg = node.master.cget ("background")
        self.fg = node.master.cget ("foreground")
    # end def __init__

    def mouse_enter (self, event = None) :
        if not self.is_leaf :
            master = self.node.master
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
        self.node.browser._busy_cursor   (cursor, self.window)
    # end def busy_cursor

    def normal_cursor (self) :
        self.node.browser.normal_cursor  ()
        self.node.browser._normal_cursor (self.window)
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

# end class T_Button

class T_Node :
    """Model one node of hierarchical browser."""

    cleanup = ( (Regexp (r"[-+\s]+"),         r"_")
              , (Regexp (r"^([^a-zA-Z]*\d)"), r"A\1")
              )

    class Name_Clash (StandardError) : pass

    def __init__ ( self
                 , browser                # browser widget containing the node
                 , name                   # unique name of node, used as tag
                 , header        = ""     # header-text of node
                 , contents      = ""     # contents-text of node
                 , parent        = None   # parent T_Node
                 , number        = None   # index of self in `parent.children'
                 , name_tags     = ()     # additional tags for `name'
                 , header_tags   = ()     # additional tags for `header'
                 , contents_tags = ()     # additional tags for `contents'
                 ) :
        assert (  ((not parent) and (number is None))
               or ((parent)     and (number >= 0))
               )
        self.browser   = browser
        self.master    = browser.body
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
                self.master.last_key = None
                self.master.bind ("<Motion>",         self.activate_mouse)
###                self.master.bind ("<Any-Key>",        self.ignore)
                self.master.bind ("<Up>",             self.go_up)
                self.master.bind ("<Down>",           self.go_down)
                self.master.bind ("<Left>",           self.go_left)
                self.master.bind ("<Right>",          self.go_right)
                self.master.bind ("<Insert>",         self.expand)
                self.master.bind ("<Shift-Insert>",   self.expand_1)
                self.master.bind ("<Control Insert>", self.expand_all)
                self.master.bind ("<Delete>",         self.collapse)
                self.master.bind ("<Shift-Delete>",   self.collapse_1)
                self.master.bind ("<Control Delete>", self.collapse_all)
                self.master.bind ("<Home>",           self.show_head)
                self.master.bind ("<End>",            self.show_tail)
                self.master.bind ("<<print>>",        self.print_node)
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
        self.master.tag_bind (self.bind_tag, "<Enter>", self.mouse_enter)
        self.master.tag_bind (self.bind_tag, "<Leave>", self.mouse_leave)
        if name_tags     : self.name_tags     = filter (None, name_tags)
        if header_tags   : self.header_tags   = filter (None, header_tags)
        if contents_tags : self.contents_tags = filter (None, contents_tags)
        self.cached_text = ("%s" * 7) % \
           ( self.name
           , self.header_head,   self.header,   self.header_tail
           , self.contents_head, self.contents, self.contents_tail
           )
    # end def __init__

    def is_open (self) :
        return self.button and not self.button.closed
    # end def is_open

    def new_child (self, name, header = "", contents = "") :
        """Add child named `name' to T_Node `self'."""
        number = len              ( self.children)
        child  = self.__class__   ( self.browser, name
                                  , header, contents, self, number
                                  )
        self._insert_child        ( child)
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
        """Insert `self' into widget `self.master' at position `index'."""
        self.tags = filter (None, (self.tag, ) + tags)
        head = self.master.index (index)
        if self.level :
            self._insert         (index, "\t" * self.level)
        self.master.mark_set     (self.butt_mark, index)
        self.master.mark_gravity (self.butt_mark, LEFT)
        self._insert_button      ()
        self._insert             (index, "\t")
        self._insert_header      (index)
        body = tail = self.master.index (index)
        self._insert             (index, "\n")
        self.master.mark_set     (self.head_mark, head)
        self.master.mark_set     (self.body_mark, body)
        self.master.mark_set     (self.tail_mark, tail)
        self.master.mark_gravity (self.head_mark, LEFT)
        self.master.mark_gravity (self.body_mark, LEFT)
        self.master.tag_add      ( self.level_tag + ":head"
                                 , self.head_mark
                                 , self.head_mark + " lineend"
                                 )
    # end def insert

    def _insert_button (self) :
        if not self.button :
            self.button = T_Button    ( self
                                      , is_leaf =
                                          not (self.children or self.contents)
                                      )
            self.master.window_create ( self.butt_mark
                                      , window = self.button.window
                                      )
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

    print_node_head    = "*   " ### put in front of each node
                                ### (print_contents)
    print_level_head   = ".   " ### level indentation per node
                                ### (print_contents)
    print_content_head = "    " ### content indentation per node
                                ### (print_contents)

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
        head   = (self.print_level_head   * (self.level)
                 ) + self.print_node_head
        indent = (self.print_content_head * (self.level + 1))
        parts  = []
        open   = self.is_open ()
        parts.append (head + self.name)
        if self.header :
            parts.append (self.header_head + self.header + self.header_tail)
        if open and self.contents :
            if (parts [-1] [-1] != "\n") and (self.contents_head != "\n"):
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
        #self.master.see (self.tail_mark)
        #self.master.see (self.head_mark)
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

    def enter (self, event = None) :
        self.master.tag_add \
          ("active_node", self.head_mark, self.head_mark + " lineend +1 char")
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
        self.leave       (event)
        self._set_cursor ("%s + %rchars" % (node.head_mark, node.level + 2))
        node.enter       (event)
        node.master.see  (node.head_mark)
    # end def _go

    def set_cursor (self, index) :
        self._set_cursor         (index)
        self.browser.focus_force ()
    # end def set_cursor

    def _current_node (self) :
        self.browser.mouse_act = 0
        node = None
        tags = filter (None, self.master.tag_names ("insert"))
        if tags :
            node = self.browser.node_map.get (tags [-1])
            if node :
                node.leave ()
            ### else : print self.browser.node_map, tags
        return node
    # end def _current_node

    def activate_mouse (self, event = None) :
        self.browser.mouse_act = 1
    # end def activate_mouse

    def ignore      (self, event = None) :
        self.browser.mouse_act = 0
        key                    = event.keysym
        result                 = "break"
        if key in ("Control_L", "Control_R") : key = "Control"
        # print key
        if (  (self.master.last_key == "Control" and key in ("c", "C"))
           or (key in ("Control", "Next", "Prior"))
           ) :
            result = ""
        self.master.last_key = key
        return result
    # end def ignore

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
            node.master.see (node.head_mark)
            node.enter      ()
        return "break"
    # end def show_head

    def show_tail   (self, event = None) :
        node = self._current_node ()
        if node :
            node.master.see (node.tail_mark)
            node.enter      ()
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
            if pattern in f :
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

# end class T_Node

class T_Node_Linked (T_Node) :
    """T_Node with hyper-link elements."""

    def __init__ ( self
                 , browser                # browser widget containing the node
                 , name                   # unique name of node, used as tag
                 , header        = ""     # header-text of node
                 , contents      = ""     # contents-text of node
                 , parent        = None   # parent T_Node
                 , number        = None   # index of self in `parent.children'
                 , name_tags     = ()     # additional tags for `name'
                 , header_tags   = ()     # additional tags for `header'
                 , contents_tags = ()     # additional tags for `contents'
                 , o_links       = []     # objects to hyper-link
                 ) :
        T_Node.__init__ ( self, browser, name, header, contents, parent, number
                        , name_tags, header_tags, contents_tags
                        )
        self.o_links = o_links
    # end def __init__

    def _insert_header (self, index) :
        start = self.master.index (index)
        T_Node._insert_header     (self,  index)
        self.activate_links       (start, index)
    # end def _insert_header

    def _insert_contents (self, index) :
        start = self.master.index (index)
        T_Node._insert_contents   (self,  index)
        self.activate_links       (start, index)
    # end def _insert_contents

    def _link_name (self, o) :
        if hasattr (o, "name") :
            nam = o.name
        else :
            nam = o
        return nam
    # end def _link_name

    def activate_links (self, head, tail) :
        m               = self.master
        self.hyper_tags = []
        for l in self.o_links :
            if not isinstance (l, (list, tuple)) :
                l = (l, )
            for o in l :
                nam = self._link_name (o)
                pos = m.search        (nam, head, tail)
                if pos :
                    tag = nam + ":link"
                    self.hyper_tags.append (tag)
                    while pos :
                        end = "%s + %d chars" % (pos, len (nam))
                        for t in tag, "hyper_link" :
                            m.tag_add (t, pos, end)
                        pos = m.search (nam, end, tail)
                    m.tag_raise     ( self.tag)
                    m.tag_bind      ( tag, "<ButtonRelease-1>"
                                    , Functor (self.follow, head_args = (o, ))
                                    )
                    m.tag_bind      ( tag, "<Double-Button-1>", break_event)
    # end def activate_links

    def follow (self, o, event = None) :
        return "break"
    # end def follow

# end class T_Node_Linked

class T_Browser (Scrolled_Text) :
    """Hierarchical browser widget."""

    widget_class = "T_Browser"

    __Ancestor   = Ancestor = Scrolled_Text

    file_dialog_title = "Hierarchical browser filename"

    user_tags    = dict \
      ( arial     = "use arial font"
      , center    = "center text"
      , courier   = "use courier font"
      , nowrap    = "don't wrap long lines"
      , quote     =
          "use left and right margin with size of standard indentation"
      , rindent   = "use right margin with size of standard indentation"
      , title     = "use title font"
      , underline = "underline text"
      , wrap      = "wrap long lines"
      )

    def __init__ (self, master, name = None, state = NORMAL, ** kw) :
        Scrolled_Text.__init__ (self, master, name, state, ** kw)
        self.clear ()
        self.mouse_act = 1
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
        ### ??? ###
        #        btags = list (self.body.bindtags ())
        #        btags.remove ("Text")
        #        self.body.bindtags (btags)
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
        m   = node.master
        pos = pos1 = m.search (match, node.head_mark, node.tail_mark)
        while pos :
            end = "%s + %s chars" % (pos, len (match))
            m.tag_add ("found", pos, end)
            pos = m.search (match, end, node.tail_mark)
        if pos1 :
            if apply_found_bg :
                m.tag_add ("found_bg", pos1, node.tail_mark)
            m.see     (node.tail_mark)
            m.see     (pos1)
        ### else : print "%s not found in node %s" % (match, node)
    # end def _find_highlight

    def _find_unhighlight (self, (node, match)) :
        m   = node.master
        pos = m.search (match, node.head_mark, node.tail_mark)
        if pos :
            try :
                m.tag_remove ("found_bg", pos, node.tail_mark)
            except TclError :
                pass
        while pos :
            end = "%s + %s chars" % (pos, len (match))
            m.tag_remove ("found", pos, end)
            pos = m.search (match, end, node.tail_mark)
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

    def find \
        (self, pattern, tagged_as = None, in_nodes = (), apply_found_bg = 0) :
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
        """Find previous occurence of `pattern' passed to last
           call of `find'.
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
        self.__Ancestor.clear (self)
        self.node_map      = {}
        self.nodes         = []
        self.bid_seed      = 0
        self._find_forward = []
        self._find_bakward = []
        self._find_current = None
        self._find_pattern = None
    # end def clear
# end class T_Browser

def T_help (browser) :
    """Returns a T_Node providing help on the usage of T_Browser `browser'."""
    name = browser.__class__.__name__
    r = T_Node  ( browser, "Help", " "
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
    n.new_child ( "<Up>"
                , "Move to previous element on same hierarchy level. If "
                  "already on first element of current hierarchy level, "
                  "move to last element of this level."
                )
    n.new_child ( "<Down>"
                , "Move to next element on same hierarchy level. If "
                  "already on last element of current hierarchy level, "
                  "move to first element of this level."
                )
    n.new_child ( "<Left>"
                , "Move to parent element (one hierarchy level up). "
                )
    n.new_child ( "<Right>"
                , "Move to first child element (one hierarchy level down). "
                  "This works only if the current element has children and "
                  "is already expanded."
                )
    n.new_child ( "<Insert>"
                , "Expand current element (show children), if possible."
                )
    n.new_child ( "<Delete>"
                , "Collapse current element (hide children), if possible."
                )
    n.new_child ( "<Home>"
                , "Show start of current element."
                )
    n.new_child ( "<End>"
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
    n.new_child ( "indent", ""
                , "The `indent' configuration parameter defines the amount "
                  "of indentation added for each hierarchy level. A pure "
                  "number specifies the indentation in pixels. By appending "
                  "`c', `m', or `i', you can specify the indentation in "
                  "centimeters, millimeters, or inches, respectively."
                  "\n"
                )
    n.new_child ( "indent_inc", ""
                , "The `indent_inc' configuration parameter defines the "
                  "indentation added for wrapped lines. It is added to the "
                  "indent parameter."
                  "\n"
                )
    n.new_child ( "hFont", ""
                , "The `hFont' configuration parameter specifies the font "
                  "used for the first line of an element. "
                )
    return r
# end def T_help

if root :
    for n in ( T_Button.clsd_bitmap_name
             , T_Button.leaf_bitmap_name
             , T_Button.open_bitmap_name
             ) :
        bitmap_mgr.add (n + ".xbm")

if __name__ == "__main__":
    def mknode (tb, name) :
        n = T_Node (tb, name, "1. test line\n2. test line\n3. test line")
        n.insert   (INSERT, "nowrap")
        return n

    def mkchild (tn, name) :
        n = tn.new_child (name, "1. test line\n2. test line\n3. test line")
        return n

    tb = T_Browser     (root, "test", state = NORMAL)
    tb.pack            (expand = YES, fill = BOTH)
    tb.insert          (INSERT, "**             Test me             **\n")
    tn = T_help        (tb)
    tn.insert          (INSERT, "rindent")
    tn = mknode        (tb,     "n1")
    mkchild            (tn,     "s1")
    mkchild            (tn,     "s2")
    nn = mkchild       (tn,     "s3")
    mkchild            (nn,     "ss1")
    nnn = mkchild      (nn,     "ss2")
    tn = mknode        (tb,     "n2")
    mkchild            (tn,     "s-a")
    mkchild            (tn,     "s-b")
    tn.open            ()
    tn = mknode        (tb,     "n3")
    mkchild            (tn,     "s-x")
    mkchild            (tn,     "s-y")
    tn = mknode        (tb,     "n4")
    tb.mainloop        ()
