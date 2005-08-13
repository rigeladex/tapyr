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
#    TGL.TKT.GTK.Text_Tag
#
# Purpose
#    Wrapper for the GTK widget TextTag
#
# Revision Dates
#    28-Mar-2005 (MG) Automated creation
#     2-Apr-2005 (MG) `Styler` added
#     2-Apr-2005 (MG) `_sty_map` removed
#     5-Apr-2005 (MG) New signals added
#     5-Apr-2005 (MG) `_correct_indent` fixed
#    18-May-2005 (MG) Button signal handling added
#    20-May-2005 (MG) Don't use `weakref`
#    10-Jun-2005 (MG) Map `wrap` to `wrap_mode`
#    31-Jul-2005 (MG) New properties `paragraph_background*` added and used
#                     in `Styler` (requires new GTK+)
#    ««revision-date»»···
#--

from    predicate             import dict_from_list
from   _TGL                   import TGL
import _TGL._TKT._GTK.Object
import _TGL._TKT._GTK.Styler
import  gobject

GTK = TGL.TKT.GTK
gtk = GTK.gtk

for event_name in ( "enter-notify-event", "leave-notify-event"
                  , "button-press-event", "button-release-event"
                  ) :
    gobject.signal_new \
        ( event_name, gtk.TextTag, gobject.SIGNAL_RUN_LAST
        , bool, (object, )
        )
for kind in "single", "double", "triple" :
    for number in 1, 2, 3 :
        event = "%s-click-%d-event" % (kind, number)
        gobject.signal_new \
            (event, gtk.TextTag, gobject.SIGNAL_RUN_LAST, bool, (object, ))

class Text_Tag (GTK.Object) :
    """Wrapper for the GTK widget TextTag"""

    weakref = False

    class Styler (TGL.TKT.GTK.Styler) :
        Opts    = dict \
            ( dict_from_list
                ( ( "font", "foreground", "underline"
                  , "justify"
                  )
                )
            , background = ("background", "paragraph_background")
                ["paragraph-background" in
                   set (p.name for p in gobject.list_properties (gtk.TextTag))
                ]
            , wrap       = "wrap_mode"
            , lmargin1   = "indent"
            , lmargin2   = "left_margin"
            , rmargin    = "right_margin"
            )

        # GTK uses left-margin to indent the whole paragraph. If we
        # want a negative indent (for the first line) it adds the
        # absolute value of the negative indent to the left margin,
        # so we have to subtract it again here....
        def _correct_left_margin (self, value) :
            indent   = self.style.lmargin1 - value
            if indent < 0 :
                value += indent
            return value
        # end def _correct_left_margin

        def _correct_indent (self, value) :
            return value - self.style.lmargin2
        # end def _correct_indent

        _opt_mappers    = dict \
            ( lmargin1  = _correct_indent
            , lmargin2  = _correct_left_margin
            )

    # end class Styler

    GTK_Class        = GTK.gtk.TextTag
    __gtk_properties = \
        ( GTK.Property            ("background", get = None)
        , GTK.Property            ("background_full_height")
        , GTK.Property            ("background_full_height_set")
        , GTK.Property            ("background_gdk")
        , GTK.Property            ("background_set")
        , GTK.Property            ("background_stipple")
        , GTK.Property            ("background_stipple_set")
        , GTK.Property            ("direction")
        , GTK.Property            ("editable")
        , GTK.Property            ("editable_set")
        , GTK.Property            ("family")
        , GTK.Property            ("family_set")
        , GTK.Property            ("font")
        , GTK.Property            ("font_desc")
        , GTK.Property            ("foreground", get = None)
        , GTK.Property            ("foreground_gdk")
        , GTK.Property            ("foreground_set")
        , GTK.Property            ("foreground_stipple")
        , GTK.Property            ("foreground_stipple_set")
        , GTK.Property            ("indent")
        , GTK.Property            ("indent_set")
        , GTK.Property            ("invisible")
        , GTK.Property            ("invisible_set")
        , GTK.Property            ("justification")
        , GTK.Property            ("justification_set")
        , GTK.Property            ("language")
        , GTK.Property            ("language_set")
        , GTK.Property            ("left_margin")
        , GTK.Property            ("left_margin_set")
        , GTK.Property            ("name")
        , GTK.Property            ("paragraph_background", get = None)
        , GTK.Property            ("paragraph_background_gdk")
        , GTK.Property            ("paragraph_background_set")
        , GTK.Property            ("pixels_above_lines")
        , GTK.Property            ("pixels_above_lines_set")
        , GTK.Property            ("pixels_below_lines")
        , GTK.Property            ("pixels_below_lines_set")
        , GTK.Property            ("pixels_inside_wrap")
        , GTK.Property            ("pixels_inside_wrap_set")
        , GTK.Property            ("right_margin")
        , GTK.Property            ("right_margin_set")
        , GTK.Property            ("rise")
        , GTK.Property            ("rise_set")
        , GTK.Property            ("scale")
        , GTK.Property            ("scale_set")
        , GTK.Property            ("size")
        , GTK.Property            ("size_points")
        , GTK.Property            ("size_set")
        , GTK.Property            ("stretch")
        , GTK.Property            ("stretch_set")
        , GTK.Property            ("strikethrough")
        , GTK.Property            ("strikethrough_set")
        , GTK.Property            ("style")
        , GTK.Property            ("style_set")
        , GTK.Property            ("tabs")
        , GTK.Property            ("tabs_set")
        , GTK.Property            ("underline")
        , GTK.Property            ("underline_set")
        , GTK.Property            ("variant")
        , GTK.Property            ("variant_set")
        , GTK.Property            ("weight")
        , GTK.Property            ("weight_set")
        , GTK.Property            ("wrap_mode")
        , GTK.Property            ("wrap_mode_set")
        )

    def __init__ (self, * args, ** kw) :
        self.__super.__init__ (* args, ** kw)
        self._button_bindings = {}
        self._event_bindings  = None
    # end def __init__

    def bind_add (self, signal, callback, * args, ** kw) :
        if isinstance (signal, self.TNS.Mouse_Button_Binder) :
            if not self._event_bindings :
                self._event_bindings = self.wtk_object.connect \
                    ("event", self._event)
        return self.__super.bind_add (signal, callback, * args, ** kw)
    # end def bind_add

    button_events = \
        { GTK.gtk.gdk.BUTTON_PRESS   : True
        , GTK.gtk.gdk._2BUTTON_PRESS : True
        , GTK.gtk.gdk._3BUTTON_PRESS : True
        }

    def _event (self, tag, view, event, iter) :
        if event.type in self.button_events :
            self.emit (self.TNS.Signal.Button_Press, event)
    # end def _event

# end class Text_Tag

if __name__ != "__main__" :
    GTK._Export ("Text_Tag")
### __END__ TGL.TKT.GTK.Text_Tag
