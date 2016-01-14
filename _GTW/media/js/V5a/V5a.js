// Copyright (C) 2016 Mag. Christian Tanzer All rights reserved
// Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <http://www.c-tanzer.at/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a
//
// Purpose
//    Modular library easing use of vanilla javascript (5)
//
// Revision Dates
//    14-Jan-2016 (CT) Creation
//    15-Jan-2016 (CT) Add `$` function for jQuery compatibility
//    19-Jan-2016 (CT) Add `for_each`
//    20-Jan-2016 (CT) Add class `js` to, remove class `no-js` from, <html>
//    20-Jan-2016 (CT) Add `prevent_default`, `stop_propagation`, `supports`
//    ««revision-date»»···
//--

;
( function () {
    "use strict";

    if (! ("$V5a" in self)) {
        var rcl   = document.documentElement.classList;
        rcl.add    ("js");
        rcl.remove ("no-js");
        self.$V5a =
          { author      : "christian.tanzer@swing.co.at"
          , copyright   : "Copyright (C) 2016 Christian Tanzer"
          , license     : "http://www.c-tanzer.at/license/bsd_3c.html"
          , supports    : {}
          , version     : "1.0"

          , for_each : function for_each (arr, fct) {
                return [].forEach.call (arr, fct);
            }
          , prevent_default : function prevent_default (ev) {
                try { ev.preventDefault (); } catch (exc) {};
            }
          , ready : function ready (cb) {
                if (document.readyState !== "loading") {
                    cb ();
                } else {
                    document.addEventListener ("DOMContentLoaded", cb);
                };
            }
          , stop_propagation : function stop_propagation (ev) {
                try { ev.stopPropagation (); } catch (exc) {};
            }
          };
        if (! ("$" in self)) {
            // jQuery compatibility
            self.$ = self.$V5a.ready;
        };
    };
  } ()
);

// __END__ V5a.js
