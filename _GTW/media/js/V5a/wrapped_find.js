// Copyright (C) 2016 Mag. Christian Tanzer All rights reserved
// Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <http://www.c-tanzer.at/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/wrapped_find.js
//
// Purpose
//    Vanilla javascript function finding all the matching descendants of
//    of wrapped set
//
// Revision Dates
//    24-Jan-2016 (CT) Creation
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    $.$$.prototype.find = function find (selector) {
        var result = this.reduce
            ( function (node) {
                return new $.$$ (selector || "*", node).wrapped;
              }
            );
        return result;
    };
  } ($V5a)
);

// __END__ V5a/wrapped_find.js
