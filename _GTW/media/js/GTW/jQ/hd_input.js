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
//    GTW/jQ/hd_input.js
//
// Purpose
//    jQuery plugin to support input fields with display different from value
//
// Revision Dates
//    28-Nov-2011 (CT) Creation
//     7-Dec-2011 (CT) Change plugin name to `gtw_hd_input`
//    ««revision-date»»···
//--

"use strict";

( function ($, undefined) {
    $.fn.gtw_hd_input = function (opts) {
        var selectors = $.extend
            ( { container   : "li"
              , display     : ".value.display"
              , hidden      : ".value.hidden"
              }
            , opts && opts ["selectors"] || {}
            );
        var options  = $.extend
            ( { id_prefix   : ""
              }
            , opts || {}
            , { selectors : selectors
              }
            );
        var display$ = $(selectors.display, this);
        if ("callback" in options) {
            display$.bind ("focus click", options.callback);
        }
        display$.prop ("disabled", false);
        return this;
    }
  } (jQuery)
);

// __END__ GTW/jQ/hd_input.js
