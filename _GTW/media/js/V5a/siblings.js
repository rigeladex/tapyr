// Copyright (C) 2016 Mag. Christian Tanzer All rights reserved
// Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <http://www.c-tanzer.at/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/siblings.js
//
// Purpose
//    Return all siblings of element
//
// Revision Dates
//    27-Jan-2016 (CT) Creation
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    $.siblings = function siblings (el) {
        var result = $.filter
            (el.parentNode.children, function (c) { return c !== el; });
        return result;
    };
  } ($V5a)
);

// __END__ V5a/siblings.js
