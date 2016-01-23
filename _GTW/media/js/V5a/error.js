// Copyright (C) 2016 Mag. Christian Tanzer All rights reserved
// Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <http://www.c-tanzer.at/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/error.js
//
// Purpose
//    Vanilla javascript function displaying an error
//
// Revision Dates
//    27-Jan-2016 (CT) Creation
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    $.error = function error (msg) {
        if (self.console) {
            console.error.apply (console, arguments);
        } else {
            alert (msg);
        };
    };
  } ($V5a)
);

// __END__ V5a/error.js
