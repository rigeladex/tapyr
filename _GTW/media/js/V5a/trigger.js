// Copyright (C) 2016 Mag. Christian Tanzer All rights reserved
// Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <http://www.c-tanzer.at/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/trigger.js
//
// Purpose
//    Trigger an event for a single element
//
// Revision Dates
//    14-Jan-2016 (CT) Creation
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    $.trigger = function trigger (target, ev_type, properties) {
        var ev = document.createEvent ("HTMLEvents");
        ev.initEvent (ev_type, true, true);
        target.dispatchEvent ($.extend (ev, properties));
    };
  } ($V5a)
);

// __END__ V5a/trigger.js
