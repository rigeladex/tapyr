// Copyright (C) 2016 Mag. Christian Tanzer All rights reserved
// Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <http://www.c-tanzer.at/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/externalize.js
//
// Purpose
//    Vanilla javascript function opening external links in separate window
//
// Revision Dates
//    18-Jan-2016 (CT) Creation
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    $.externalize = $.merge
        ( function externalize (opts) {
            var O  = $.merge ({}, externalize.defaults,  opts);
            var S  = $.merge ({}, externalize.selectors, O ["selectors"]);
            var ls = $.query (S.external);
            $.for_each
                ( ls
                , function (el) {
                    if (! $.has_class_any (el, O.skip_classes)) {
                        el.classList.add (O.x_class);
                        $.bind
                            ( el, "click"
                            , function (ev) {
                                window.open (el.href).focus ();
                                $.prevent_default (ev);
                              }
                            );
                    };
                  }
                );
          }
        , { defaults  :
              { skip_classes    : ["internal"]
              , x_class         : "external"
              }
          , selectors :
              { external        :
                  "a[href^='http://'], a[href^='https://'], a[href^='//']"
              }
          }
        );
  } ($V5a)
);

// __END__ V5a/externalize.js
