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
#    ««revision-date»»···
#--

from   _TFL         import TFL
from   _TGL         import TGL

import _TFL._Meta.Property
import _TFL._UI.Mixin
import _TFL._UI.Style

import _TGL._UI.Mixin
import _TGL._UI.Style

from   Record import Record

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

class Node (TGL.UI.Mixin) :
    """Model a simple node of a hierarchical text display"""

    contents            = property (lambda s : s._contents)
    Style               = TFL.Meta.Lazy_Property \
        ("Style",    lambda s : s.parent.Style)
    tkt_text            = TFL.Meta.Lazy_Property \
        ("tkt_text", lambda s : s.parent.tkt_text)

    def __init__ (self, parent, contents = (), style = None, AC = None, ** kw) :
        self.__super.__init__ \
            ( parent    = parent
            , contents  = contents
            , style     = style
            , AC        = AC or parent.AC
            , ** kw
            )
        self.parent     = parent
        self.level      = level = parent and (parent.level + 1) or 0
        self.style      = style = self._base_style (style, level)
        self.style_dict = sd = self.tkt_text.Tag_Styler (style).option_dict
        if isinstance (contents, (str, unicode)) :
            contents    = (contents, )
        self._contents  = [Styled (c, style, sd) for c in (contents)]
        self._insert (self.tkt_text.current_pos)
    # end def __init__

    def styled_text (self, value, style = None, style_dict = None) :
        return Styled (value, self._style (style), style_dict)
    # end def styled_text

    def _base_style (self, style, level) :
        result = getattr (self.Style, "level%s" % (level, ))
        if style is not None :
            result = style (** self.TNS.Text.Tag_Styler (result).option_dict)
        return result
    # end def _base_style

    def _insert (self, at_mark) :
        tkt_text = self.tkt_text
        self._head_mark = tkt_text.mark_at (at_mark, left_gravity = True)
        for c in self.contents :
            tkt_text.insert (at_mark, c.value, c.style)
        if not c.value.endswith ("\n") :
            tkt_text.insert (at_mark, "\n", self.style)
        self._tail_mark = tkt_text.mark_at (at_mark, left_gravity = False)
    # end def _display

    def _style (self, style) :
        if isinstance (style, str) :
            style = getattr (self.Style, style)
        return style
    # end def _style

# end class Node

class Top_Node (Node) :
    """Model the toplevel node of a hierarchical text display"""

    Style               = TFL.UI.Style.__class__ ()
    _style_defaults     = dict \
        ( Background             = "lightyellow2"
        , Foreground             = "black"
        , activeBackground       = "yellow"
        , activeButtonBackground = "red"
        , activeButtonForeground = "yellow"
        , activeForeground       = "red"
        , courierFontFamily      = "Monospace"
        , headerFontFamily       = "Sans"
        , headerFontSize         = "medium"
        , headerFontStyle        = "normal"
        , headerFontWeight       = "normal"
        , hyperLinkBackground    = "lightyellow2"
        , hyperLinkCursor        = "hand"
        , hyperLinkForeground    = "blue"
        , indent                 = 11 # 22
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
        add ( "arial",     font_family = "Sans")
        add ( "center",    justify     = "center")
        add ( "courier",   font_family = d.courierFontFamily)
        add ( "nowrap",    wrap        = "none")
        add ( "rindent",   rmargin     = d.indent)
        add ( "underline", underline   = "single")
        add ( "wrap",      wrap        = "word")
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
            add ( level
                , lmargin1  = lm1
                , lmargin2  = lm2
                )
            tabs.append (lm1 + d.indent)
        Style.T = self.styled_text
    # end def _setup_styles

# end class Top_Node

"""
from   _TGL._UI.HTD import *
from   _TFL._UI.App_Context import App_Context
import _TGL._TKT._Tk
import _TGL._TKT._Tk.Text
ac  = App_Context (TGL)

tn = Top_Node (ac, "First try")
tn.tkt_text.exposed_widget.pack (expand = "yes", fill = "both")
tn.tkt_text.pos_at (tn.tkt_text.eot_pos), tn.tkt_text.pos_at (tn.tkt_text.current_pos)
tc = Node ( tn
          , ( Styled ("Second try", Top_Node.Style.red)
            , "\n", "third line"
            , Styled ("fourth line", Top_Node.Style.blue)
            )
          )
tn.tkt_text.pos_at (tn.tkt_text.eot_pos), tn.tkt_text.pos_at (tn.tkt_text.current_pos)

"""
if __name__ != "__main__" :
    TGL.UI._Export_Module ()
### __END__ TGL.UI.HTD
