// Copyright (C) 2016 Mag. Christian Tanzer All rights reserved
// Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <http://www.c-tanzer.at/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/closest.js
//
// Purpose
//    Vanilla javascript function finding closest inclusive ancestor
//    matching selector
//
// Revision Dates
//    24-Jan-2016 (CT) Creation
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    $.closest =
        ( document.documentElement.closest
        ? function closest (el, selector) {
              return el.closest (selector);
          }
        : function closest (el, selector) {
              while (el) {
                  if ($.matches (el, selector)) {
                      break;
                  };
                  el = el.parentElement;
              };
              return el;
          }
        );
  } ($V5a)
);

// __END__ V5a/closest.js
