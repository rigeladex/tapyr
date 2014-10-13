# -*- coding: utf-8 -*-
# Copyright (C) 2009-2010 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
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
            ( Rule_Class
                ( "align_left"
                , float            = "left"
                , margin           = "1px 5px 1px 0px"
                )
            , Rule_Class
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
