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
#    ««revision-date»»···
#--

from   _TFL                  import TFL
from   _TGL                  import TGL

from   Record                import Record

import _TFL._Meta.Property
import _TFL._UI.Mixin
import _TFL._UI.Style

import _TGL._UI.Mixin
import _TGL._UI.Style

class Styled (TFL.Meta.Object) :
    """Mode styled text object"""

    def __init__ (self, value, style = None, style_dict = None) :
        if not isinstance (value, (str, unicode)) :
            style = value.style or style
            value = value.value
            if style_dict :
                style = style (** style_dict)
        self.value = value
        self.style = style
    # end def __init__

    def __str__ (self) :
        return self.value
    # end def __str__

# end class Styled

class _Node_ (TGL.UI.Mixin) :
    """Base class for nodes of a hierarchical text display"""

    children            = property (lambda s : s._children)
    contents            = property (lambda s : s._contents)
    Style               = TFL.Meta.Lazy_Property \
        ("Style",    lambda s : s.parent.Style)
    tkt_text            = TFL.Meta.Lazy_Property \
        ("tkt_text", lambda s : s.parent.tkt_text)

    _level_inc          = 1

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
        self.style      = style = self._base_style (style, level)
        self.style_dict = sd = self.tkt_text.Tag_Styler (style).option_dict
        self._head_mark = self._midd_mark = self._tail_mark = None
        self.init_children ()
        self.init_contents (* contents)
        if parent :
            parent._add_child (parent._tail_mark, self)
    # end def __init__

    def add_contents (self, * contents) :
        tkt_text = self.tkt_text
        contents = self._add_contents (* contents)
        at_mark  = tkt_text.mark_at   (self._midd_mark)
        self._insert_contents         (at_mark, * contents)
        tkt_text.free_mark            (at_mark)
    # end def add_contents

    def init_children (self) :
        self._children  = []
    # end def init_children

    def init_contents (self, * contents) :
        self._contents = []
        self._add_contents (* contents)
    # end def init_contents

    def styled_text (self, value, style = None, style_dict = None) :
        return Styled (value, self._style (style), style_dict)
    # end def styled_text

    def _add_child (self, at_mark, * children) :
        add = self.children.append
        for c in children :
            add (c)
        self._insert_children (at_mark, * children)
    # end def _add_child

    def _add_contents (self, * contents) :
        style  = self.style
        sd     = self.style_dict
        result = [Styled (c, style, sd) for c in (contents)]
        self.contents.extend (result)
        return result
    # end def _add_contents

    def _base_style (self, style, level) :
        result = getattr (self.Style, "level%s" % (level, ))
        if style is not None :
            result = style (** self.TNS.Text.Tag_Styler (result).option_dict)
        return result
    # end def _base_style

    def _insert (self, at_mark) :
        tkt_text = self.tkt_text
        self._head_mark = tkt_text.mark_at \
            (at_mark, left_gravity = True, name = self._head_mark)
        self._insert_contents (at_mark, * self.contents)
        self._midd_mark = tkt_text.mark_at \
            (at_mark, left_gravity = True, name = self._midd_mark)
        self._insert_children (at_mark, * self.children)
        self._tail_mark = tkt_text.mark_at \
            (at_mark, delta = -1, name = self._tail_mark)
            ### `delta = -1` keeps the marks from overlapping
    # end def _display

    def _insert_children (self, at_mark, * children) :
        tkt_text = self.tkt_text
        for c in children :
            tkt_text.insert (at_mark, "\n", self.Style.normal)
            c._insert       (at_mark)
    # end def _insert_children

    def _insert_contents (self, at_mark, * contents) :
        if contents :
            tkt_text = self.tkt_text
            for c in contents :
                tkt_text.insert (at_mark, c.value, c.style)
            tkt_text.insert (at_mark, " ", self.Style.normal)
    # end def _insert_contents

    def _style (self, style) :
        if isinstance (style, str) :
            style = getattr (self.Style, style)
        return style
    # end def _style

# end class _Node_

class Node (_Node_) :
    """Model a simple node of a hierarchical text display"""

    _level_inc = 0

# end class _Node_

class Node_B (_Node_) :
    """Model a node with butcon of a hierarchical text display"""

    butcon_bitmap       = "circle"
    callback_style      = TFL.UI.Style ("callback")
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

    def mouse_enter (self, event = None) :
        tkt_text = self.tkt_text
        head     = self._head_mark
        tail     = tkt_text.bol_pos (head, line_delta = 1)
        tkt_text.apply_style (self.Style.active_node, head, tail, lift = True)
    # end def mouse_enter

    def mouse_leave (self, event = None) :
        tkt_text = self.tkt_text
        tkt_text.remove_style (self.Style.active_node, tkt_text.bot_pos)
    # end def mouse_leave

    def _button_callback_dict (self) :
        ignore = self.ignore
        return dict \
            ( click_1   = ignore
            , click_2   = ignore
            , click_3   = ignore
            , any_enter = self.mouse_enter
            , any_leave = self.mouse_leave
            )
    # end def _button_callback_dict

    def _insert_butcon (self, at_mark) :
        tkt_text = self.tkt_text
        if self.butcon is None :
            self.__class__._no_of_butcons += 1
            self.butcon  = b = self.TNS.Butcon \
                ( AC     = self.AC
                , wc     = tkt_text
                , bitmap = self.butcon_bitmap
                , name   = "b%s" % (self.__class__._no_of_butcons, )
                )
            b.apply_style \
                ( self.callback_style
                      (callback = self._button_callback_dict ())
                )
            for s in self.Style.normal, self.style :
                b.push_style (s)
            tkt_text.insert        (at_mark, "\t" * (self.level - 1))
            tkt_text.insert_widget (at_mark, self.butcon)
            tkt_text.insert        (at_mark, "\t")
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

# end class Node_B

class Node_Bs (Node_B) :
    """Model a multi-state node with butcon of a hierarchical text display"""

    butcon_bitmap       = property \
        (lambda s : s._butcon_bitmaps [s.state])
    contents            = property \
        (lambda s : s._contents [s.state])
    no_of_states        = property (lambda s : len (s._butcon_bitmaps))
    state               = 0

    def inc_state (self, event = None) :
        """Increment state to next state
           (circles back from last to first state).
        """
        self.state = (self.state + 1) % self.no_of_states
        tkt_text   = self.tkt_text
        for c in self.children :
            c.butcon = None
        tail = tkt_text.pos_at   (self._tail_mark, delta = 1)
        tkt_text.remove          (self._butt_mark, tail)
        self._insert             (self._tail_mark)
        self.butcon.apply_bitmap (bitmap = self.butcon_bitmap)
    # end def inc_state

    def init_contents (self, * contents_per_state) :
        self._contents  = [[] for i in range (self.no_of_states)]
        self._add_contents (* contents_per_state)
    # end def init_contents

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

    def _button_callback_dict (self) :
        return dict \
            ( self.__super._button_callback_dict ()
            , click_1   = self.inc_state
            )
    # end def _button_callback_dict

    def _insert_children (self, at_mark, * children) :
        if self.state == self.no_of_states - 1 :
            self.__super._insert_children (at_mark, * children)
    # end def _insert_children

# end class Node_Bs

class Node_B2 (Node_Bs) :
    """Model a two-state node with butcon of a hierarchical text display"""

    _butcon_bitmaps     = ("closed_node", "open_node")

# end class Node_B2

class Root (_Node_) :
    """Model the root node of a hierarchical text display"""

    Style               = TFL.UI.Style.__class__ ()

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
        , indent                 = 22
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
        self.name       = name
        self.tkt_text   = tkt_text = self.get_TNS (AC).Scrolled_Text \
            ( AC        = AC
            , name      = name
            , wc        = wc
            , editable  = False
            )
        Style           = self.Style
        if not hasattr (Style, "active_node") :
            self._setup_styles (tkt_text)
        tkt_text.apply_style   (Style.normal)
        tkt_text.set_tabs      (* Style._tabs)
        self.__super.__init__ \
            ( parent    = None
            , contents  = contents
            , style     = style
            , AC        = AC
            , name      = name
            , wc        = wc
            , ** kw
            )
        self._insert    (tkt_text.current_pos)
        ### insert a blank line to avoid `_tail_mark` and `current_pos` to
        ### coincide
        tkt_text.insert (tkt_text.current_pos, "\n", self.style)
    # end def __init__

    def _setup_styles (self, w) :
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
        for color in "red", "blue", "black" :
            add (color, foreground = color)
        add ("light_blue", foreground = "deep sky blue")
        tabs = Style._tabs = []
        for i in range (16) :
            level = "level%s" % (i, )
            lm1   = i   * d.indent
            lm2   = lm1 + d.indent_inc
            add (level, lmargin1 = lm1, lmargin2 = lm2)
            if i :
                add ("%sButtonLine" % level, lmargin1 = 0, lmargin2 = lm2)
                tabs.append (lm1)
        Style.T = self.styled_text
    # end def _setup_styles

# end class Root

if __name__ != "__main__" :
    TGL.UI._Export_Module ()
### __END__ TGL.UI.HTD
