// Copyright (C) 2011-2012 Mag. Christian Tanzer All rights reserved
// Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
// #*** <License> ************************************************************#
// This software is licensed under the terms of either the
// MIT License or the GNU Affero General Public License (AGPL) Version 3.
// http://www.c-tanzer.at/license/mit_or_agpl.html
// #*** </License> ***********************************************************#
//
//++
// Name
//    autocomplete
//
// Purpose
//    Wrap jquery-ui.autocomplete
//
// Revision Dates
//    13-Oct-2011 (CT) Creation
//    ««revision-date»»···
//--

"use strict";

( function ($) {
    var L = $GTW.L;
    var renderer =
        { html          : function _ac_render_item_html (ul, item) {
              var result = $("<li>")
                  .data     ("item.autocomplete", item)
                  .append   ($("<a>").html (item.label))
                  .appendTo (ul);
              return result;
          }
        , orig          : $.ui.autocomplete.prototype._renderItem
        };
    $.fn.gtw_autocomplete = function (opts, render_item) {
        var ri = render_item;
        if (typeof ri === "string") {
            ri = renderer [render_item];
        };
        this.each
            ( function (n) {
                var self = $(this);
                self.autocomplete (opts);
                if (ri) {
                    self.data ("autocomplete")._renderItem = ri;
                };
              }
            );
        return this;
    };
  } (jQuery)
);

// __END__ autocomplete.js
