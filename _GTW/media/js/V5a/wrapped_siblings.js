// Copyright (C) 2016 Mag. Christian Tanzer All rights reserved
// Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <http://www.c-tanzer.at/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/wrapped_siblings.js
//
// Purpose
//    Vanilla javascript wrapper finding all of the matching siblings
//    of the wrapped nodes
//
// Revision Dates
//    27-Jan-2016 (CT) Creation
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    $.$$.siblings = function siblings (selector) {
        var result = this.reduce
            (function (node) { return $.siblings (node); });
        if (selector) {
            result = result.filter (selector);
        };
        return result;
    };
  } ($V5a)
);

// __END__ V5a/wrapped_siblings.js
