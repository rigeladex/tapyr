// Copyright (C) 2016 Mag. Christian Tanzer All rights reserved
// Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <http://www.c-tanzer.at/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/form_field.js
//
// Purpose
//    Vanilla javascript functions for getting and putting form field values
//
// Revision Dates
//    10-Jun-2016 (CT) Creation
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    var _ =
      { checked :
          { clear : function clear (ff) {
              ff.checked = false;
            }
          , get : function get (ff) {
              var result = ff.checked ? "yes" : (f.required ? null : "no");
              return result;
            }
          , put : function put (ff, value) {
              ff.checked = (value == "yes") ? true : false;
            }
          , truth : function truth (ff) {
              return ff.checked;
            }
          }
      , clear : function clear (ff) {
          var fft = _.normal;
          if (ff.type == "checkbox") {
              fft = _.checkbox;
          }
          return fft.clear (ff);
        }
      , get : function get (ff) {
          var fft = _.normal;
          if (ff.type == "checkbox") {
              fft = _.checkbox;
          }
          return fft.get (ff);
        }
      , normal :
          { clear : function clear (ff) {
              ff.value = "";
            }
          , get : function get (ff) {
              return ff.value;
            }
          , put : function put (ff, value) {
              ff.value = value || "";
            }
          , truth : function truth (ff) {
              return ff.value;
            }
          }
      , put : function put (ff, value) {
          var fft = _.normal;
          if (ff.type == "checkbox") {
              fft = _.checkbox;
          }
          return fft.put (ff, value);
        }
      , truth : function truth (ff) {
          var fft = _.normal;
          if (ff.type == "checkbox") {
              fft = _.checkbox;
          }
          return fft.truth (ff);
        }
      };
    $.form_field = _;
  } ($V5a)
);

// __END__ V5a/form_field.js
