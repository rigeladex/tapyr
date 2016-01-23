// Copyright (C) 2016 Mag. Christian Tanzer All rights reserved
// Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <http://www.c-tanzer.at/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/scroll_to.js
//
// Purpose
//    Vanilla javascript functions for scrolling an element in a container
//
// Revision Dates
//    21-Jan-2016 (CT) Creation
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    var scroll_min = 0;
    var spec_h     =
        { offset         : "offsetLeft"
        , scroll_size    : "scrollWidth"
        , scroll_pos     : "scrollLeft"
        , size           : "width"
        };
    var spec_v     =
        { offset         : "offsetTop"
        , scroll_size    : "scrollHeight"
        , scroll_pos     : "scrollTop"
        , size           : "height"
        };
    function scroll_to (el, rel_pos, S) {
        var parent       = el.offsetParent || el;
        var el_offset    = el [S.offset];
        var el_size      = el.getBoundingClientRect     () [S.size];
        var vp_size      = parent.getBoundingClientRect () [S.size];
        var scroll_size  = parent [S.scroll_size];
        var scroll_max   = scroll_size - el_size;
        var scroll_off   = (vp_size - el_size) * (rel_pos || 0);
        var scroll_pos   = Math.min
            (Math.max (el_offset - scroll_off, 0), scroll_max);
        parent [S.scroll_pos] = scroll_pos;
    };
    $.scroll_to_h = function scroll_to_h (el, rel_pos) {
        scroll_to (el, rel_pos, spec_h);
    };
    $.scroll_to_v = function scroll_to_v (el, rel_pos) {
        scroll_to (el, rel_pos, spec_v);
    };
    $.scroll_to   = function scroll_to   (el, rel_pos_h, rel_pos_v) {
        scroll_to (el, rel_pos_h, spec_h);
        scroll_to (el, rel_pos_v, spec_v);
    };
  } ($V5a)
);

// __END__ V5a/scroll_to.js
