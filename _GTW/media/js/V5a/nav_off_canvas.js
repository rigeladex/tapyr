// Copyright (C) 2016 Mag. Christian Tanzer All rights reserved
// Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <http://www.c-tanzer.at/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/nav_off_canvas.js
//
// Purpose
//    Vanilla javascript function supporting off-canvas navigation
//
// Revision Dates
//    15-Jan-2016 (CT) Creation
//    24-Jan-2016 (CT) Use `$.$$`
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    $.nav_off_canvas = $.merge
        ( function nav_off_canvas (opts) {
            var O = $.merge ({}, nav_off_canvas.defaults, opts);
            var S = $.merge ({}, nav_off_canvas.selectors, O ["selectors"]);
            var hide_els$   = $.$$     (S.hide);
            var main_el     = $.query1 (S.main);
            var toggle_els$ = $.$$     (S.toggle);
            var mcl         = main_el.classList;
            var off_cls     = O.off_class;
            var on_cls      = O.on_class;
            var toggle_vp   = 0;
            var hide_cb     = function hide_cb (ev) {
                mcl.add    (off_cls);
                mcl.remove (on_cls);
                $.prevent_default (ev);
            };
            var toggle_cb   = function toggle_cb (ev) {
                mcl.toggle (off_cls);
                mcl.toggle (on_cls);
                $.prevent_default (ev);
            };
            hide_els$.bind ("click", hide_cb);
            toggle_els$
                .bind ("click", toggle_cb)
                .for_each
                    ( function (el) {
                        var style =
                                el.currentStyle || window.getComputedStyle (el);
                        if (style.display === O.toggle_display) {
                            toggle_vp ++;
                        };
                      }
                    );
            if (toggle_vp > 0) {
                hide_cb ();
            };
          }
        , { defaults :
              { hide_class     : "pg_nav_hide"
              , off_class      : "nav-off-canvas"
              , on_class       : "nav-on-canvas"
              , toggle_display : "inline-block"
              }
          , selectors :
              { main           : "[id=main]"
              , hide           : "a[href='#nav_off']"
              , toggle         : ".pg_nav_show > a"
              }
          }
        );
  } ($V5a)
);

// __END__ V5a/nav_off_canvas.js
