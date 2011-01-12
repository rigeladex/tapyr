# -*- coding: iso-8859-1 -*-
# Copyright (C) 2011 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package JNJ.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    JNJ.CSS_Defaults
#
# Purpose
#    Provide defaults for CSS fragments in html/*.css
#
# Revision Dates
#     1-Jan-2011 (CT) Creation
#     2-Jan-2011 (CT) Creation continued
#     4-Jan-2011 (CT) Creation continued..
#    ««revision-date»»···
#--

from _GTW._CSS.import_CSS import *

from _TFL.Color           import Color as _C

_C.formatter = RGB_X

color_focus            = SVG_Color ("yellow")
color_heading          = RGB_X     ("#34444D")
color_lighter_grey     = RGB_X     ("#EDEDED")
color_light_grey       = RGB_X     ("#DEDEDE")
color_medium_grey      = RGB_X     ("#BEBEBE")
color_selected         = RGB_X     ("#FF6633")
color_target           = RGB_X     ("#FF6633")

css_arrow_color        = SVG_Color ("red")
css_arrow_width        = Em (1./2)

border_button          = "2px outset " + color_medium_grey
border_simple          = "1px solid "  + color_medium_grey
border_selected        = "2px solid "  + color_selected

button_spec            = dict \
    ( border           = border_button
    , margin           = TRBL0 (t = Em (1./4), b = Em (3./4))
    , padding          = TRBL  (Em (0.5), Em (1.5))
    )

col_padding            = Px (5)

background_color       = SVG_Color ("white")
link_color             = RGB_X     ("#0000EE")
no_link_color          = RGB_X     ("#333333")
text_color             = RGB_X     ("#000033")
visited_color          = RGB_X     ("#551A8B")

class nav_col :

    background_color       = RGB_X     ("#EFF3FE")

    button_spec            = dict \
        ( border           = border_button
        , color            = link_color
        , margin           = 0
        , text_align       = "center"
        )

    color_spec_heading     = dict \
        ( background_color = color_heading
        , color            = background_color
        )

    color_spec_label       = dict \
        ( background_color = background_color
        , color            = text_color
        )

    color_spec_link        = dict \
        ( background_color = background_color
        , color            = link_color
        )
    color_spec_link_current    = dict \
        ( background_color = link_color
        , color            = background_color
        )

    color_spec_no_link     = dict \
        ( background_color = background_color
        , color            = no_link_color
        )

    color_spec_section_current = dict \
        ( background_color = background_color
        , color            = color_heading
        )

    color_spec_visited     = dict \
        ( color_spec_link
        , color            = visited_color
        )

    color_spec_web_link_hover = dict \
        ( color_spec_link
        , background_color = RGB_8 (255, 153, 0)
        )

    li_left                = Em (0.75)
    mark_color_link        = css_arrow_color
    mark_color_section     = color_heading
    mark_width             = Em (0.40)

    vert_padding           = Em (0.2)
    width                  = Px (190)

    full_width             = width      + 2 * col_padding
    right                  = full_width + 2 * col_padding

### end class nav_col

class cal :

    date_bg                = RGB_X ("#DDDDDD")
    date_padding           = TRBL0 (r = Em (1./4), b = Em (1./10))
    event_bg               = RGB_X ("#FFF8AF")
    font_size              = Em    (0.7)
    line_height            = 1.5
    holiday_bg             = RGB_X ("#CCFFFF")
    month_color            = RGB_X ("#ABABAB")
    weekend_color          = RGB_X ("#00FFFF")
    week_color             = RGB_8 (255, 153, 0)
    week_height            = Em    (8)

# end class cal

color_spec_error       = dict \
    ( background_color = background_color
    , color            = SVG_Color ("red")
    )
color_spec_heading     = dict \
    ( background_color = background_color
    , color            = color_selected
    )
color_spec_gallery_heading = dict \
    ( background_color = RGB_P     (50, 75, 100)
    , color            = nav_col.background_color
    )
color_spec_normal      = dict \
    ( background_color = background_color
    , color            = text_color
    )
color_spec_pg_head     = dict \
    ( background_color = background_color
    , color            = RGB_X     ("#0200DE")
    )
color_spec_row1        = color_spec_meta = dict \
    ( background_color = color_lighter_grey
    , color            = text_color
    )
color_spec_row2        = color_spec_message = dict \
    ( background_color = color_light_grey
    , color            = text_color
    )
color_spec_selected    = dict \
    ( background_color = SVG_Color ("yellow")
    , color            = SVG_Color ("red")
    )
color_spec_strong      = dict \
    ( background_color = background_color
    , color            = SVG_Color ("blue")
    )

del_spec               = dict \
    ( text_decoration  = "line-through"
    # XXX ???
    )

font_family_normal     = """"Lucida Grande", verdana, sans-serif"""
font_family_print      = \
    """"Lucida Serif", Lucida, "Times New Roman", Times, serif"""
font_family_pre        = \
    """"Lucida Sans Typewriter", "Lucida Console", "Courier New", Courier, monospace"""
font_spec_normal       = dict \
    ( font_family      = font_family_normal
    , font_style       = "normal"
    , font_weight      = "normal"
    , line_height      = 1.44
    )

font_spec_print        = dict \
    ( font_spec_normal
    , font_family      = font_family_print
    )

font_spec_em           = dict \
    ( font_spec_normal
    , font_weight      = "bold"
    )
font_spec_pre          = dict \
    ( font_spec_normal
    , font_family      = font_family_pre
    )

grid_table_border      = "3px ridge gray"

h1_font_size           = Percent (125)
h1_font_weight         = "bold"

hbox_spec              = dict \
    ( display          = "block"
    , overflow         = "hidden"
    )

hr_spec                = dict \
    ( border           = 0
    , border_top       = "1px solid #CCC"
    , display          = "block"
    , height           = Px (1)
    , margin           = TRBL (Em (1), 0)
    , padding          = 0
    )

input_padding          = Em (0.2)

ins_spec               = dict \
    ( text_decoration  = "none"
    # XXX ???
    )

outline_focus          = "1px solid "   + color_focus
outline_target         = "1px dotted "  + color_target

pg_head_height         = Px (100)
pg_main_max_width      = Em (50)
pg_main_min_width      = Em (15)

thumbnail_size         = Px (155)
thumbnail_selected_color = color_selected

### __END__ JNJ.CSS_Defaults
