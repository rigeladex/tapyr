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
#    TGL.UI.HTD
#
# Purpose
#    UI for hierarchical text display
#
# Revision Dates
#    30-Mar-2005 (CT) Creation (based loosely on T_Browser and TFL.UI.HTB)
#    31-Mar-2005 (CT) Creation continued
#     1-Apr-2005 (CT) Creation continued (style.callback handling corrected)
#     1-Apr-2005 (CT) `Style.__init__` improved
#     1-Apr-2005 (CT) `Styled` factored into a module of its own
#     2-Apr-2005 (CT) Small fixes
#     2-Apr-2005 (CT) `id`, `id_tag`, and `id_style` added and used
#     5-Apr-2005 (MG) Use `mouse_*` events instead of `any_*`
#    10-Apr-2005 (CT) `_insert_contents` changed to handle `callable` contents
#    14-Apr-2005 (CT)  `bot_pos`, `eot_pos`, and `current_pos` replaced by
#                      `buffer_head`, `buffer_tail`, and `insert_mark`,
#                      respectively
#    16-May-2005 (CT) `Observer` added
#    16-May-2005 (CT) `Node_C` added
#    16-May-2005 (CT) `_Node_Bs_` factored
#    16-May-2005 (CT) `_remove*` factored
#    17-May-2005 (CT) `node_at` factored
#    17-May-2005 (CT) `_insert_children` changed to not inster a leading `\n`
#                     into an empty `tkt_text`
#    17-May-2005 (CT) `_insert_butcon` changed to increment
#                     `Node_B._no_of_butcons` instead of
#                     `self.__class__._no_of_butcons` (which fails miserably
#                     when multiple derived classes are used in the same HDT)
#    18-May-2005 (CT) `Node_C.Observer.mouse_enter` changed to not scroll
#                     `observed`
#    18-May-2005 (CT) `Node_C._tag_callback_dict` added
#    18-May-2005 (CT) `click_3` added to `_Node_Bs_._button_callback_dict`
#    18-May-2005 (CT) `see` changed to use `_head_mark` if no arguments passed
#    18-May-2005 (CT) `Node_B3` added
#    19-May-2005 (CT) Use `self.style` instead of `self.Style.normal` or
#                     nothing for inserting whitespace around nodes/children
#    19-May-2005 (CT) Handling of callable `contents` simplified
#    ««revision-date»»···
#--

from   _TFL                  import TFL
from   _TGL                  import TGL
from   _TGL._UI.Styled       import Styled

import _TFL._Meta.Property
import _TFL._UI.Mixin
import _TFL._UI.Style
import _TFL._Meta.Property

import _TGL._UI.Mixin
import _TGL._UI.Style

import weakref

class _Node_ (TGL.UI.Mixin) :
    """Base class for nodes of a hierarchical text display"""

    callback_style      = TFL.UI.Style ("callback")
    children            = property (lambda s : s._children)
    contents            = property (lambda s : s._contents)
    root                = TFL.Meta.Lazy_Property \
        ("root",    lambda s : s.parent.root)
    Style               = TFL.Meta.Lazy_Property \
        ("Style",    lambda s : s.root.Style)
    tkt_text            = TFL.Meta.Lazy_Property \
        ("tkt_text", lambda s : s.root.tkt_text)

    _level_inc          = 1

    ### for compatibility with multi-state nodes
    butcon_bitmap       = None
    no_of_states        = 1
    state               = 0

    class Observer (TFL.Meta.Object) :
        """Model an observer of a node"""

        def dec_state (self, observed) :
            """Called whenever `observed.dec_state` is called"""
            pass
        # end def dec_state

        def goto (self, observed) :
            """Called whenever `observed.goto` is called"""
            pass
        # end def goto

        def inc_state (self, observed) :
            """Called whenever `observed.inc_state` is called"""
            pass
        # end def inc_state

        def mouse_enter (self, observed) :
            """Called whenever `observed.mouse_enter` is called"""
            pass
        # end def mouse_enter

        def mouse_leave (self, observed) :
            """Called whenever `observed.mouse_leave` is called"""
            pass
        # end def mouse_leave

    # end class Observer

    def __init__ (self, parent, contents = (), style = None, AC = None, ** kw) :
        self.__super.__init__ \
            ( parent    = parent
            , contents  = contents
            , style     = style
            , AC        = AC or parent.AC
            , ** kw
            )
        if isinstance (contents, (str, unicode)) :
            contents    = (contents, )
        self.parent     = parent
        self.level      = level \
                        = parent and (parent.level + self._level_inc) or 0
        self.u_style    = style
        self.style      = style  = self._base_style (style, level)
        self.styler     = styler = self.tkt_text.Tag_Styler (style)
        self._head_mark = self._midd_mark = self._tail_mark = None
        self._observers = []
        self.id_style   = TFL.UI.Style ("id")
        self._init_children ()
        self._init_contents (* contents)
        if parent :
            parent._add_child (parent._tail_mark, self)
            if self.root.active_node is None :
                self.root.active_node = self
    # end def __init__

    def add_contents (self, * contents) :
        tkt_text = self.tkt_text
        contents = self._add_contents (* contents)
        at_mark  = tkt_text.mark_at   (self._midd_mark)
        self._insert_contents         (at_mark, * contents)
        tkt_text.free_mark            (at_mark)
    # end def add_contents

    def add_observer (self, o) :
        self._observers.append (weakref.proxy (o))
    # end def add_observer

    def dec_state (self, event = None) :
        for o in self._observers :
            o.dec_state (self)
    # end def dec_state

    def goto (self, mark = None) :
        tkt_text = self.tkt_text
        if mark is None :
            mark = self._head_pos ()
        tkt_text.place_cursor (mark)
        self.see (mark)
        for o in self._observers :
            o.goto (self)
        self.mouse_enter ()
    # end def goto

    def goto_child (self, n = 0) :
        n = min (n, len (self.children) - 1)
        if n >= 0 :
            self.children [n].goto ()
    # end def goto_child

    def inc_state (self, event = None) :
        for o in self._observers :
            o.inc_state (self)
    # end def inc_state

    def mouse_enter (self, event = None) :
        if self.root.active_node is not self :
            self.root.active_node = self
            tkt_text = self.tkt_text
            head     = self._head_mark
            tail     = tkt_text.bol_pos (head, line_delta = 1)
            tkt_text.apply_style \
                (self.Style.active_node, head, tail, lift = True)
            for o in self._observers :
                o.mouse_enter (self)
            return self.TNS.stop_cb_chaining
    # end def mouse_enter

    def mouse_leave (self, event = None) :
        if self.root.active_node is self :
            self.root.active_node = None
            tkt_text = self.tkt_text
            tkt_text.remove_style \
                (self.Style.active_node, tkt_text.buffer_head)
            for o in self._observers :
                o.mouse_leave (self)
            return self.TNS.stop_cb_chaining
    # end def mouse_leave

    def see (self, * marks) :
        tkt_text = self.tkt_text
        if self._head_mark and not marks :
            marks = (self._head_mark, )
        for m in marks :
            tkt_text.see (m)
    # end def see

    def styled_text (self, value, style = None, styler = None) :
        return Styled (value, self._style (style), styler)
    # end def styled_text

    def _add_child (self, at_mark, * children) :
        add    = self.children.append
        off    = len (self.children)
        for i, c in enumerate (children) :
            c.number = n= i + off
            c.id     = ":".join ((self.id, str (n)))
            c.id_tag = "HTD::%s" % (c.id, )
            add (c)
        self._insert_children (at_mark, * children)
    # end def _add_child

    def _add_contents (self, * contents) :
        result = [Styled (c, self.style, self.styler) for c in (contents)]
        self.contents.extend (result)
        return result
    # end def _add_contents

    def _base_style (self, style, level) :
        result  = getattr (self.Style, "level%s" % (level, ))
        cb_dict = {}
        if style is not None :
            result  = style (** self.tkt_text.Tag_Styler (result).style_dict)
        if self.parent :
            result = result (callback = self._tag_callback_dict ())
        return result
    # end def _base_style

    def _head_pos (self) :
        return self.tkt_text.pos_at (self._head_mark)
    # end def _head_pos

    def _init_children (self) :
        self._children  = []
    # end def _init_children

    def _init_contents (self, * contents) :
        self._contents = []
        if contents :
            self._add_contents (* contents)
    # end def _init_contents

    def _insert (self, at_mark) :
        self.root._id_map [self.id_tag] = self
        tkt_text        = self.tkt_text
        self._head_mark = hm = tkt_text.mark_at \
            (at_mark, left_gravity = True, name = self._head_mark)
        self._insert_contents (at_mark, * self.contents)
        self._midd_mark = tkt_text.mark_at \
            (at_mark, left_gravity = True, name = self._midd_mark)
        tkt_text.apply_style  (self.id_style, hm, at_mark, tag = self.id_tag)
        self._insert_children (at_mark, * self.children)
        self._tail_mark = tkt_text.mark_at \
            (at_mark, delta = -1, name = self._tail_mark)
            ### `delta = -1` keeps the marks from overlapping
    # end def _insert

    def _insert_children (self, at_mark, * children) :
        tkt_text = self.tkt_text
        for c in children :
            if not tkt_text.is_empty :
                tkt_text.insert (at_mark, "\n", self.style)
            c._insert       (at_mark)
    # end def _insert_children

    def _insert_contents (self, at_mark, * contents) :
        if contents :
            tkt_text = self.tkt_text
            for c in contents :
                if callable (c.value) :
                    r = c.value ()
                    if isinstance (r, (str, unicode, Styled)) :
                        c = Styled (r, self.style, self.styler)
                    else :
                        for d in r :
                            d = Styled      (d, self.style, self.styler)
                            tkt_text.insert (at_mark, d.value, d.style)
                        continue
                tkt_text.insert (at_mark, c.value, c.style)
            tkt_text.insert (at_mark, " ", self.style)
    # end def _insert_contents

    def _remove (self, head = None) :
        self._remove_children ()
        self._remove_contents (head)
    # end def _remove

    def _remove_children (self) :
        pass
    # end def _remove_children

    def _remove_contents (self, head = None) :
        ### only do this if node is already displayed
        if self._head_mark :
            tkt_text = self.tkt_text
            if head is None :
                head = self._head_mark
            tail     = tkt_text.pos_at (self._tail_mark, delta = 1)
            tkt_text.remove (head, self._tail_mark)
    # end def _remove_contents

    def _style (self, style) :
        if isinstance (style, str) :
            style = getattr (self.Style, style)
        return style
    # end def _style

    def _tag_callback_dict (self, cb_dict = {}) :
        return dict \
            ( cb_dict
            , mouse_enter = self.mouse_enter
            , mouse_leave = self.mouse_leave
            )
    # end def _tag_callback_dict

# end class _Node_

class Node (_Node_) :
    """Model a simple node of a hierarchical text display"""

    _level_inc = 0

# end class _Node_

class Node_B (_Node_) :
    """Model a node with butcon of a hierarchical text display"""

    butcon_bitmap       = "node_leaf"
    _no_of_butcons      = 0

    def __init__ (self, * args, ** kw) :
        self.butcon = self._butt_mark = None
        self.__super.__init__ (* args, ** kw)
        self._abs = self.Style.active_button \
            (mouse_cursor = self.Style.active_cursor.mouse_cursor)
    # end def __init__

    def ignore (self, event = None) :
        return self.TNS.stop_cb_chaining
    # end def ignore

    def _button_callback_dict (self, cb_dict = {}) :
        ignore = self.ignore
        return dict \
            ( cb_dict
            , click_1     = ignore
            , click_2     = ignore
            , click_3     = ignore
            , mouse_enter = self.mouse_enter
            , mouse_leave = self.mouse_leave
            )
    # end def _button_callback_dict

    def _head_pos (self) :
        return self.tkt_text.pos_at (self._butt_mark)
    # end def _head_pos

    def _insert_butcon (self, at_mark) :
        if self.butcon is None :
            tkt_text = self.tkt_text
            Node_B._no_of_butcons += 1
            self.butcon  = b = self.TNS.Butcon \
                ( AC     = self.AC
                , wc     = tkt_text
                , bitmap = self.butcon_bitmap
                , name   = "b%s" % (self._no_of_butcons, )
                )
            b.apply_style \
                ( self.callback_style
                    (callback = self._button_callback_dict ())
                )
            b.push_style           (self.Style.normal)
            tkt_text.insert        \
                (at_mark, "\t" * (self.level - 1), self.style)
            tkt_text.insert_widget (at_mark, self.butcon)
            tkt_text.insert        (at_mark, "\t", self.style)
            self._butt_mark = tkt_text.mark_at \
                (at_mark, left_gravity = True, name = self._butt_mark)
            tkt_text.apply_style \
                ( getattr (self.Style, "level%sButtonLine" % (self.level, ))
                , self._head_mark, at_mark
                )
    # end def _insert_butcon

    def _insert_contents (self, at_mark, * contents) :
        self._insert_butcon           (at_mark)
        self.__super._insert_contents (at_mark, * contents)
    # end def _insert_contents

    def _remove_children (self) :
        for c in self.children :
            c.butcon = c._butt_mark = None
    # end def _remove_children

# end class Node_B

class _Node_Bs_ (Node_B) :

    def mouse_enter (self, event = None) :
        self.__super.mouse_enter (event)
        self.butcon.push_style   (self._abs)
        self.tkt_text.push_style (self.Style.active_cursor)
    # end def mouse_enter

    def mouse_leave (self, event = None) :
        self.__super.mouse_leave (event)
        self.butcon.pop_style    ()
        self.tkt_text.pop_style  ()
    # end def mouse_leave

    def _button_callback_dict (self, cb_dict = {}) :
        return dict \
            ( self.__super._button_callback_dict (cb_dict)
            , click_1        = self.inc_state
            , click_3        = self.dec_state
            )
    # end def _button_callback_dict

    def _change_state (self, state) :
        ### only do this if node is already displayed
        if self._head_mark :
            self.state = state % self.no_of_states
            self._remove (self._butt_mark)
            self._insert (self._tail_mark)
            self.butcon.apply_bitmap (bitmap = self.butcon_bitmap)
            self.see (self._tail_mark, self._head_mark)
    # end def _change_state

    def _insert_children (self, at_mark, * children) :
        if self.state != self.no_of_states - 1 :
            children = ()
        self.__super._insert_children (at_mark, * children)
    # end def _insert_children

# end class _Node_Bs_

class Node_Bs (_Node_Bs_) :
    """Model a multi-state node with butcon of a hierarchical text display"""

    butcon_bitmap       = property (lambda s : s._butcon_bitmaps [s.state])
    contents            = property (lambda s : s._contents       [s.state])
    no_of_states        = property (lambda s : len (s._butcon_bitmaps))
    state               = 0

    def dec_state (self, event = None) :
        """Decrement state to next state
           (circles back from first to last state).
        """
        self._change_state     (self.state - 1)
        self.__super.dec_state (event)
    # end def dec_state

    def goto_child (self, n = 0) :
        if self.state == self.no_of_states - 1 :
            self.__super.goto_child (n)
    # end def goto_child

    def inc_state (self, event = None) :
        """Increment state to next state
           (circles back from last to first state).
        """
        self._change_state     (self.state + 1)
        self.__super.inc_state (event)
    # end def inc_state

    def _add_contents (self, * contents_per_state) :
        old_state = self.state
        try :
            for self.state, contents in enumerate (contents_per_state) :
                if isinstance (contents, (str, unicode)) :
                    contents = (contents, )
                self.__super._add_contents (* contents)
        finally :
            self.state = old_state
    # end def _add_contents

    def _init_contents (self, * contents_per_state) :
        self._contents  = [[] for i in range (self.no_of_states)]
        self._add_contents (* contents_per_state)
    # end def _init_contents

# end class Node_Bs

class Node_B2 (Node_Bs) :
    """Model a two-state node with butcon of a hierarchical text display"""

    _butcon_bitmaps     = ("node_closed", "node_open")

# end class Node_B2

class Node_B3 (Node_Bs) :
    """Model a three-state node with butcon of a hierarchical text display"""

    _butcon_bitmaps     = ("node_closed", "node_half_open", "node_open")

# end class Node_B3

class Node_B8 (Node_Bs) :
    """Model a two-state node with butcon of a hierarchical text display"""

    _butcon_bitmaps     = ["node_s%d" % i for i in range (1, 9)]

# end class Node_B2

class Node_C (_Node_Bs_) :
    """Model a node controlling another node (living in a different
       HTD.root).
    """

    class Observer (_Node_Bs_.Observer) :

        def __init__ (self, observer) :
            self.observer = weakref.proxy (observer)
        # end def __init__

        def dec_state (self, observed) :
            self.observer._dec_state ()
        # end def dec_state

        def goto (self, observed) :
            self.observer._goto ()
        # end def goto

        def inc_state (self, observed) :
            self.observer._inc_state ()
        # end def inc_state

        def mouse_enter (self, observed) :
            self.observer._mouse_enter ()
            self.observer.see ()
        # end def mouse_enter

        def mouse_leave (self, observed) :
            self.observer._mouse_leave ()
        # end def mouse_leave

    # end class Observer

    butcon_bitmap       = property (lambda s : s.controlled.butcon_bitmap)
    dec_state           = property (lambda s : s.controlled.dec_state)
    goto                = property (lambda s : s.controlled.goto)
    inc_state           = property (lambda s : s.controlled.inc_state)
    mouse_enter         = property (lambda s : s.controlled.mouse_enter)
    mouse_leave         = property (lambda s : s.controlled.mouse_leave)
    no_of_states        = property (lambda s : s.controlled.no_of_states)
    state               = property \
        (lambda s : s.controlled.state, lambda s, v : True)

    def __init__ (self, controlled, * args, ** kw) :
        self.controlled = weakref.proxy (controlled)
        self._observer  = o = self.Observer (self)
        self.__super.__init__   (* args, ** kw)
        controlled.add_observer (o)
    # end def __init__

    def _dec_state (self) :
        self._change_state (self.state)
    # end def _dec_state

    def _goto (self) :
        self.__super.goto ()
    # end def _goto

    _inc_state = _dec_state

    def _mouse_enter (self) :
        self.__super.mouse_enter ()
    # end def _mouse_enter

    def _mouse_leave (self) :
        self.__super.mouse_leave ()
    # end def _mouse_leave

    def _tag_callback_dict (self, cb_dict = {}) :
        return dict \
            ( self.__super._tag_callback_dict (cb_dict)
            , click_1        = lambda event = None : self.controlled.see ()
            , double_click_1 = self.inc_state
            )
    # end def _tag_callback_dict

# end class Node_C

class Root (_Node_) :
    """Model the root node of a hierarchical text display"""

    Style               = TFL.UI.Style.__class__ ()

    id                  = "0"
    id_tag              = "HDT::0"

    _style_defaults     = dict \
        ( Background             = "lightyellow2"
        , Foreground             = "black"
        , activeBackground       = "yellow"
        , activeButtonBackground = "red"
        , activeButtonForeground = "yellow"
        , activeCursor           = "hand"
        , activeForeground       = "red"
        , courierFontFamily      = "Monospace"
        , headerFontFamily       = "Sans"
        , headerFontSize         = "medium"
        , headerFontStyle        = "normal"
        , headerFontWeight       = "normal"
        , hyperLinkBackground    = "lightyellow2"
        , hyperLinkCursor        = "hand"
        , hyperLinkForeground    = "blue"
        , indent                 = 16
        , indent_inc             = 0
        , linkFontFamily         = "Monospace"
        , linkFontStyle          = "normal"
        , normalFontFamily       = "Monospace"
        , normalFontSize         = "medium"
        , normalFontStyle        = "normal"
        , normalFontWeight       = "normal"
        , titleFontFamily        = "Sans"
        , titleFontSize          = "x-large"
        , titleFontWeight        = "normal"
        )

    def __init__ (self, AC, contents = (), style = None, name = None, wc = None, ** kw) :
        self.active_node = None
        self.name        = name
        self.number      = -1
        self.root        = self
        self._id_map     = {}
        Style            = self.Style
        self.tkt_text    = tkt_text = self.get_TNS (AC).Scrolled_Text \
            ( AC         = AC
            , name       = name
            , wc         = wc
            , editable   = False
            )
        if not hasattr (Style, "active_node") :
            self._setup_styles (tkt_text)
        tkt_text.apply_style   (Style.normal)
        tkt_text.set_tabs      (* Style._tabs)
        self.__super.__init__ \
            ( parent     = None
            , contents   = contents
            , style      = style
            , AC         = AC
            , name       = name
            , wc         = wc
            , ** kw
            )
        self._setup_bindings (tkt_text)
        self._insert         (tkt_text.insert_mark)
    # end def __init__

    def clear (self) :
        self.active_node  = None
        self._id_map      = {}
        self.tkt_text.clear ()
        self._init_contents ()
        self._init_children ()
    # end def clear

    def node_at (self, pos = None) :
        tkt_text = self.tkt_text
        if pos is None :
            pos = tkt_text.bol_pos (tkt_text.insert_mark)
        tags = tkt_text.tags_at (pos)
        for t in reversed (tags) :
            if t.startswith ("HTD::") :
                result = self._id_map [t]
                break
        else :
            result = self.root.active_node
        return result
    # end def node_at

    def _setup_bindings (self, w) :
        w.apply_style \
            (self.callback_style (callback = self._text_callback_dict ()))
    # end def _setup_bindings

    def _setup_styles (self, w) :
        from Record import Record
        d = Record ()
        for name, default in self._style_defaults.iteritems () :
            if isinstance (default, (str)) :
                getter = w.option_value
            else :
                getter = w.num_opt_val
            setattr (d, name, getter (name, default))
        Style = self.Style
        add   = Style.add
        add ( "active_cursor", mouse_cursor = d.activeCursor)
        add ( "arial",         font_family = "Sans")
        add ( "center",        justify     = "center")
        add ( "courier",       font_family = d.courierFontFamily)
        add ( "nowrap",        wrap        = "none")
        add ( "rindent",       rmargin     = d.indent)
        add ( "underline",     underline   = "single")
        add ( "wrap",          wrap        = "word")
        add ( "active_button"
            , background   = d.activeButtonBackground
            , foreground   = d.activeButtonForeground
            )
        add ( "active_node"
            , background   = d.activeBackground
            , foreground   = d.activeForeground
            )
        add ( "header"
            , font_family  = d.headerFontFamily
            , font_size    = d.headerFontSize
            , font_style   = d.headerFontStyle
            , font_weight  = d.headerFontWeight
            )
        add ( "hyper_link"
            , Style.underline
            , background   = d.hyperLinkBackground
            , font_family  = d.linkFontFamily
            , font_style   = d.linkFontStyle
            , foreground   = d.hyperLinkForeground
            , mouse_cursor = d.hyperLinkCursor
            )
        add ( "noindent"
            , lmargin1     = 0
            , lmargin2     = 0
            )
        add ( "normal"
            , Style.wrap
            , background   = d.Background
            , foreground   = d.Foreground
            , font_family  = d.normalFontFamily
            , font_size    = d.normalFontSize
            , font_style   = d.normalFontStyle
            , font_weight  = d.normalFontWeight
            )
        add ( "quote"
            , rmargin      = d.indent
            , lmargin1     = d.indent
            , lmargin2     = d.indent
            )
        add ( "title"
            , font_family  = d.titleFontFamily
            , font_size    = d.titleFontSize
            , font_weight  = d.titleFontWeight
            )
        for color in "yellow", "green", "gray", "cyan" :
            add (color, background = color)
        add ("light_gray", background = "gray90")
        for color in "red", "orange", "blue", "black" :
            add (color, foreground = color)
        add ("light_blue", foreground = "deep sky blue")
        tabs = Style._tabs = []
        for i in range (16) :
            level = "level%s" % (i, )
            lm1   = i   * d.indent
            lm2   = lm1 + d.indent_inc
            add (level, lmargin1 = lm1, lmargin2 = lm2)
            add ("%sButtonLine" % level, lmargin1 = 0, lmargin2 = lm2)
            if i :
                tabs.append (lm1)
        Style.T = self.styled_text
    # end def _setup_styles

    def _text_callback_dict (self, cb_dict = {}) :
        return dict \
            ( cb_dict
            , close_node     = self.close_node
            , node_down      = self.go_down
            , node_end       = self.show_tail
            , node_home      = self.show_head
            , node_left      = self.go_left
            , node_right     = self.go_right
            , node_up        = self.go_up
            , open_node      = self.open_node
            )
    # end def _text_callback_dict

    ### event callbacks follow
    def _node_binding (method) :
        def wrapper (self, event = None, node = None, ** kw) :
            tkt_text = self.tkt_text
            pos      = tkt_text.bol_pos (tkt_text.insert_mark)
            if node is None :
                node = self.node_at (pos)
            if node is not None :
                method (self, node, ** kw)
                tkt_text.place_cursor (pos)
            return self.TNS.stop_cb_chaining
        wrapper.__name__ = method.__name__
        wrapper.__doc__  = method.__doc__
        return wrapper
    # end def _node_binding

    @_node_binding
    def close_node (self, node) :
        node.dec_state ()
    # end def close_node

    @_node_binding
    def go_down (self, node, count = 1) :
        self._goto_sibling (node, + count)
    # end def go_down

    @_node_binding
    def go_left (self, node) :
        if node.parent :
            node.mouse_leave ()
            node.parent.goto ()
    # end def go_left

    @_node_binding
    def go_right (self, node) :
        if node.children :
            node.goto_child  (0)
    # end def go_right

    @_node_binding
    def go_up (self, node, count = 1) :
        self._goto_sibling (node, - count)
    # end def go_up

    @_node_binding
    def open_node (self, node) :
        node.inc_state ()
    # end def open_node

    @_node_binding
    def show_head (self, node) :
        node.goto ()
    # end def show_head

    @_node_binding
    def show_tail   (self, node) :
        node.goto (node._tail_mark)
    # end def show_tail

    def _goto_sibling (self, node, dir) :
        if node.parent :
            siblings = node.parent.children
        else :
            siblings = node.children
        n        = min (max ((node.number + dir), 0), len (siblings) - 1)
        target   = siblings [n]
        node.mouse_leave ()
        target.goto      ()
    # end def _goto_sibling

# end class Root

if __name__ != "__main__" :
    TGL.UI._Export_Module ()
### __END__ TGL.UI.HTD
