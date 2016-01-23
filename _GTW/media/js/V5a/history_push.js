// Copyright (C) 2016 Mag. Christian Tanzer All rights reserved
// Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <http://www.c-tanzer.at/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/history_push.js
//
// Purpose
//    Vanilla javascript function supporting history-push
//
// Revision Dates
//    20-Jan-2016 (CT) Creation
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    $.history_push = function history_push (url, title, state) {
        if ($.supports.history) {
            history.pushState (state, title, url);
        } else {
            try { location.hash = url; } catch (e) {};
        };
    };
  } ($V5a)
);

// __END__ V5a/history_push.js
