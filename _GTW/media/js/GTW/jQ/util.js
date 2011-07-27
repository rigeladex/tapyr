// Copyright (C) 2011 Mag. Christian Tanzer All rights reserved
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
//    ««revision-date»»···
//--

"use strict";

( function ($) {
    $.gtw_ajax_2json = function (opts, name) {
        var options  = $.extend
            ( { async       : false                  // defaults settings
              , error       : function
                (xhr_instance, status, exc) {
                    alert
                        ( (name || "Ajax request") + " failed: "
                        + status + " " + exc + "\n\n"
                        + $GTW.inspect.show (opts.data)
                        );
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
