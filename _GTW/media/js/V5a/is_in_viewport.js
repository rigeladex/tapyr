// Copyright (C) 2017 Mag. Christian Tanzer All rights reserved
// Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <http://www.c-tanzer.at/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/is_in_viewport.js
//
// Purpose
//    Vanilla javascript functions deciding if an element is visible in viewport
//
// Revision Dates
//    19-Jan-2017 (CT) Creation
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    $.is_in_viewport = function is_in_viewport (el, h_tolerance, w_tolerance) {
        var parent   = el.offsetParent || document.documentElement;
        var bcr      = el.getBoundingClientRect ();
        var height   = Math.min (window.innerHeight, parent.clientHeight);
        var width    = Math.min (window.innerWidth,  parent.clientWidth);
        var h_factor = h_tolerance != null ? h_tolerance : 1.0;
        var w_factor = w_tolerance != null ? w_tolerance : h_factor;
        var result   =
            (  bcr.bottom > 0
            && bcr.left   > 0
            && bcr.right  > 0
            && bcr.top    > 0
            && bcr.left   < w_factor * width
            && bcr.top    < h_factor * height
            );
        return result;
    };
  } ($V5a)
);

// __END__ V5a/is_in_viewport.js
