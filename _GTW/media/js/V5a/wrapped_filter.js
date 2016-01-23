// Copyright (C) 2016 Mag. Christian Tanzer All rights reserved
// Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <http://www.c-tanzer.at/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/wrapped_filter.js
//
// Purpose
//    Vanilla javascript filter method for $V5a.wrapped
//
// Revision Dates
//    24-Jan-2016 (CT) Creation
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    $.$$.prototype.filter = function filter (arg) {
        var pred =
            ( (typeof arg === "function")
            ? function (node) { return arg (node); }
            : function (node) { return $.matches (node, arg || "*"); }
            )
        return new $.$$ (this.wrapped.filter (pred));
    };
  } ($V5a)
);

// __END__ V5a/wrapped_filter.js
