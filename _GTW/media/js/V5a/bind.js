// Copyright (C) 2016 Mag. Christian Tanzer All rights reserved
// Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <http://www.c-tanzer.at/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/bind.js
//
// Purpose
//    Bind and unbind event listeners for an element or a list of elements.
//
// Revision Dates
//    14-Jan-2016 (CT) Creation
//    ««revision-date»»···
//--

// bind has the signature:
// target     : a single element or a list of elements
// ev_spec    : a string of space-separated event-type names
// handler    : a function to execute each time the event is triggered
// capture    : a boolean indicating whether to capture the event
//
// alternatively, bind also supports the signature:
// target     : a single element or a list of elements
// ev_spec    : a object containing mapping ev_spec keys to handler values
// null
// capture    : a boolean indicating whether to capture the event
//
// event-type names can contain namespace indicators separated by a period.
// Namespacing allows to unbind some event handlers of a specific event-type
// without affecting others

;
( function ($) {
    "use strict";

    var bind_map = {};

    function add (target, ev_key, ev_type, cb, capture) {
        var bindings;
        if (ev_key in bind_map) {
            bindings = bind_map [ev_key];
        } else {
            bindings = bind_map [ev_key] = [];
        };
        bindings.push ([ev_type, cb, capture]);
        target.addEventListener (ev_type, cb, capture);
    };

    $.bind = function bind (target, ev_spec, handler, capture) {
        var ev_map = {};
        var one_p  = ! ("length" in target);
        capture    = capture || false;
        if (handler === null || handler === undefined) {
            ev_map = ev_spec;
        } else {
            ev_map [ev_spec] = handler;
        };
        for (ev_spec in ev_map) {
            var cb = ev_map [ev_spec];
            ev_spec.split (/\s+/).forEach
                ( function (ev_key) {
                    var ev_type = ev_key.split (".") [0];
                    if (one_p) {
                        add (target, ev_key, ev_type, cb, capture);
                    } else {
                        for (var j = 0, lj = target.length; j < lj; j++) {
                            add (target [j], ev_key, ev_type, cb, capture);
                        };
                    };
                  }
                );
        };
    };

    $.unbind = function unbind (target, ev_spec) {
        var one_p = ! ("length" in target);
        ev_spec.split (/\s+/).forEach
            ( function (ev_key) {
                if (ev_key in bind_map) {
                    var bindings = bind_map [ev_key], el;
                    for (var i = 0, li = bindings.length, args; i < li; i++) {
                        args = bindings [i];
                        if (one_p) {
                            target.removeEventListener.apply (target, args);
                        } else {
                            for (var j = 0, lj = target.length; j < lj; j++) {
                                el = target [j];
                                el.removeEventListener.apply (el, args);
                            };
                        };
                    };
                    delete bind_map [ev_key];
                };
              }
            );
    };
  } ($V5a)
);

// __END__ V5a/bind.js
