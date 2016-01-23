// Copyright (C) 2016 Mag. Christian Tanzer All rights reserved
// Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <http://www.c-tanzer.at/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/ematches.js
//
// Purpose
//    Vanilla javascript function matching a selector on an element
//
// Revision Dates
//    24-Jan-2016 (CT) Creation
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    var mk;
    var names =
        [ "matches"
        , "msMatchesSelector"
        , "oMatchesSelector"
        , "webkitMatchesSelector"
        ];
    var node = document.documentElement;
    for (var i = 0, li = names.length, name; i < li; i++) {
        name = names [i];
        if (name in node) {
            mk = name;
            break;
        };
    };

    $.matches = function matches (el, selector) {
        return el [mk] (selector);
    };
  } ($V5a)
);

// __END__ V5a/ematches.js
