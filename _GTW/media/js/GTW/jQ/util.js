// Copyright (C) 2011-2013 Mag. Christian Tanzer All rights reserved
// Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
// #*** <License> ************************************************************#
// This software is licensed under the terms of either the
// MIT License or the GNU Affero General Public License (AGPL) Version 3.
// http://www.c-tanzer.at/license/mit_or_agpl.html
// #*** </License> ***********************************************************#
//
//++
// Name
//    util
//
// Purpose
//    Utility functions for jQuery use
//
// Revision Dates
//    27-Jul-2011 (CT) Creation
//    18-Apr-2013 (CT) Add `alert` to `options.error`
//    ««revision-date»»···
//--

"use strict";

( function ($) {
    $.gtw_ajax_2json = function (opts, name) {
        var options  = $.extend
            ( { async       : false                  // defaults settings
              , error       : function (xhr_instance, status, exc) {
                    var msg = (name || "Ajax request") + " failed: ";
                    alert
                        (msg + ": " + exc + "\n\n" + xhr_instance.esponseText);
                    console.error (msg, status, exc, opts.data);
                }
              , timeout     : 30000
              }
            , opts                                   // arguments
            , { contentType : "application/json"     // mandatory settings
              , dataType    : "json"
              , processData : false
              , type        : "POST"
              }
            );
        var data = options.data;
        if (typeof data !== "string") {
            options.data = $GTW.jsonify (data);
        };
        $.ajax (options);
    }
  } (jQuery)
);

// __END__ util.js
