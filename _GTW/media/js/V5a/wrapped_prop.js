// Copyright (C) 2016 Mag. Christian Tanzer All rights reserved
// Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <http://www.c-tanzer.at/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/wrapped_prop.js
//
// Purpose
//    Change properties of all elements of wrapped set
//
// Revision Dates
//    25-Jan-2016 (CT) Creation
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    $.$$.prototype.prop = function attr (val) {
        var map = {};
        ( arguments.length === 2
        ? map [val] = arguments [1]
        : map = val
        );
        return this.for_each (function (node) { $.merge (node, map); });
    };
  } ($V5a)
);

// __END__ V5a/wrapped_prop.js
