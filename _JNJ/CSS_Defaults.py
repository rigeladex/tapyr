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
#    ««revision-date»»···
#--

from _GTW._CSS.import_CSS import *

from _TFL.Color           import Color as _C

_C.formatter = RGB_X

button_spec            = dict \
    ( border           = "2px outset"
    , margin           = TRBL (t = Em (1./4), b = Em (3./4))
    , padding          = TRBL (t = Em (1./8), b = Em (1./8))
    )

col_padding            = Px (5)
color_spec_error       = dict \
    ( background_color = SVG_Color ("white")
    , color            = SVG_Color ("red")
    )
color_spec_heading     = dict \
    ( background_color = SVG_Color ("white")
    , color            = RGB_X     ("#FF6633")
    )
color_spec_normal      = dict \
    ( background_color = SVG_Color ("white")
    , color            = RGB_X     ("#000033")
    )
color_spec_pg_head     = dict \
    ( background_color = SVG_Color ("white")
    , color            = RGB_X     ("#0200DE")
    )
color_spec_row1        = dict \
    ( background_color = RGB_X     ("#EBEBEB")
    , color            = RGB_X     ("#000033")
    )
color_spec_row2        = dict \
    ( background_color = RGB_X     ("#BEBEBE") ### XXX ??? white
    , color            = RGB_X     ("#000033")
    )
color_spec_selected    = dict \
    ( background_color = SVG_Color ("yellow")
    , color            = SVG_Color ("red")
    )
color_spec_strong      = dict \
    ( background_color = SVG_Color ("blue")
    , color            = SVG_Color ("white")
    )

font_family_normal     = """"Lucida Grande", verdana, sans-serif"""
font_family_pre        = """monospace"""
font_spec_normal       = dict \
    ( font_family      = font_family_normal
    , font_style       = "normal"
    , font_weight      = "normal"
    )
font_spec_em           = dict \
    ( font_spec_normal
    , font_weight      = "bold"
    )
font_spec_pre          = dict \
    ( font_spec_normal
    , font_family      = font_family_pre
    )

h1_font_size           = Percent (120)
h1_font_weight         = "bold"

link_color             = RGB_X ("#0050FF")

class nav_col :

    background_color       = RGB_X ("#EFF3FE")

    color_spec_heading     = dict \
        ( background_color = background_color
        , color            = RGB_X ("#666666")
        )

    color_spec_link        = dict \
        ( background_color = background_color
        , color            = link_color
        )
    color_spec_link_current= dict \
        ( background_color = link_color
        , color            = background_color
        )

    color_spec_visited     = dict \
        ( color_spec_link
        , color            = RGB_X ("#54AAFF")
        )

    color_spec_web_link_hover = dict \
        ( color_spec_link
        , background_color = RGB_8 (255, 153, 0)
        )

    vert_padding           = Em (0.2)
    width                  = Px (190)

    full_width             = width      + 2 * col_padding
    right                  = full_width + 2 * col_padding

### end class nav_col

pg_head_height         = Px (100)
pg_main_max_width      = Em (50)
pg_main_min_width      = Em (15)

### __END__ JNJ.CSS_Defaults
