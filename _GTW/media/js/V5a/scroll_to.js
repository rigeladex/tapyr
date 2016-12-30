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
//    30-Dec-2016 (CT) Rename `scroll_to` to `_scroll_to` to avoid name clash
//                     inside `$.scroll_to`
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
    function _scroll_to (el, rel_pos, S) {
        // Beware::
        // the `offsetParent` of `el` must have `overflow` set to `scroll`
        //   otherwise, the assignment to `scrollLeft` or `scrollTop` will
        //   silently do nothing
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
        _scroll_to (el, rel_pos, spec_h);
    };
    $.scroll_to_v = function scroll_to_v (el, rel_pos) {
        _scroll_to (el, rel_pos, spec_v);
    };
    $.scroll_to   = function scroll_to   (el, rel_pos_h, rel_pos_v) {
        _scroll_to (el, rel_pos_h, spec_h);
        _scroll_to (el, rel_pos_v, spec_v);
    };
  } ($V5a)
);

// __END__ V5a/scroll_to.js
