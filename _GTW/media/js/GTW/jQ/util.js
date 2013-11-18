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
//    29-Apr-2013 (CT) Move `gtw_externalize` and `fix_a_nospam` in here
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
                    $GTW.show_message (msg, status, exc, opts.data);
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
    };
    $.fn.gtw_externalize = function () {
        this.click
            ( function (event) {
                  window.open (this.href).focus ();
                  if (event && "preventDefault" in event) {
                      event.preventDefault ();
                  };
              }
            ).addClass ("external");
        return this;
    };
    $GTW.update
        ( { fix_a_nospam   : function ($) {
                $("a.nospam").each (
                    function () {
                        var data = $(this).next ("b.nospam").attr ("title");
                        if (data != null) {
                            var aia = $GTW.as_int_array (data);
                            $(this).replaceWith
                                (String.fromCharCode.apply (null, aia));
                        };
                    }
                );
            }
          }
        );
  } (jQuery)
);

// __END__ util.js
