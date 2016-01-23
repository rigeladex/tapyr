// Copyright (C) 2016 Mag. Christian Tanzer All rights reserved
// Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <http://www.c-tanzer.at/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/select.js
//
// Purpose
//    Vanilla javascript function to select specific elements
//
// Revision Dates
//    23-Jan-2016 (CT) Creation
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    $.select = function select (expr, context) {
        if (! context) {
            // try specific selection functions (these don't support context)
            if (/^\.[\w\-]+$/.test (expr)) {
                return document.getElementsByClassName (expr);
            } else if (/^\w+$/.test (expr)) {
                return document.getElementsByTagName (expr);
            } else if (/^\#[\w\-]+$/.test (expr)) {
                return [document.getElementById (expr)];
            };
        };
        return (context || document).querySelectorAll (expr);
    };
  } ($V5a)
);

// __END__ V5a/select.js
