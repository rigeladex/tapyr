# -*- coding: iso-8859-1 -*-
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
#    DJO.media.css_fragments_py.rest
#
# Purpose
#    CSS fragment for ReST-specific classes
#
# Revision Dates
#     7-Sep-2009 (CT) Creation
#    ««revision-date»»···
#--

if "just for testing" :
    ### import rest; print rest.style_sheet
    from _DJO.CSS import *

first_and_last = \
    ( Rule_Class ("first", margin = "0")
    , Rule_Class ("last",  margin = "0.2em 0 0.2em 0")
    )

style_sheet = Style_Sheet \
    ( Rule
        ( "dd"
        , children             = first_and_last
        )
    , Rule
        ( "hr.docutils"
        , clear                = "right"
        )
    , Rule
        ( "img"
        , children             =
            ( Rule
                ( "align_left"
                , float            = "left"
                , margin           = "1px 5px 1px 0px"
                )
            , Rule
                ( "align_right"
                , float            = "right"
                , margin           = "1px 0px 1px 5px"
                )
            )
        )
    , Rule
        ( "table.docutils p"
        , border               = "0"
        , margin               = "0.2em 0 0 0"
        , padding              = "0"
        , children             = first_and_last
        )
    )

### __END__ DJO.media.css_fragments_py.rest
