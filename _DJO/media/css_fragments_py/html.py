# -*- coding: iso-8859-15 -*-
# Copyright (C) 2009 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
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
#    DJO.media.css_fragments_py.html
#
# Purpose
#    CSS fragment for plain `html` styling
#
# Revision Dates
#     7-Sep-2009 (CT) Creation
#    ««revision-date»»···
#--

if "just for testing" :
    ### import html; print html.style_sheet
    font_spec_em               = dict \
        ( font_family          = "verdana, sans-serif"
        , font_style           = "normal"
        , font_weight          = "bold"
        )
    font_spec_normal           = dict \
        ( font_family          = "verdana, sans-serif"
        , font_style           = "normal"
        , font_weight          = "normal"
        )
    font_spec_pre              = dict \
        ( font_family          = "monospace"
        , font_style           = "normal"
        , font_weight          = "normal"
        )
    normal_background          = "white"
    normal_foreground          = "#000033"

    from _DJO.CSS import *

style_sheet = Style_Sheet \
    ( Rule
        ( "em", ".em"
        , ** font_spec_em
        )
    , Rule
        ( "html"
        , background_color     = normal_background
        , color                = normal_foreground
        , padding              = "0"
        , ** font_spec_normal
        )
    , Rule
        ( "html", "table"
        , margin               = "0"
        )
    , Rule
        ( "img", "table", "td", "tr"
        , border_width         = "0"
        )
    , Rule
        ( "pre"
        , ** font_spec_pre
        )
    , Rule
        ( "td"
        , padding              = "0 0.5em 0 0"
        , vertical_align       = "top"
        , children             =
            [ Rule_Attr
                ( "[colspan]"
                , text_align   = "center"
                )
            ]
        )
    , Rule
        ( "tr"
        , padding              = "0"
        )
    )

### __END__ html
