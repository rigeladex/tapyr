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
//     GTW/jQ/buttonify.js
//
// Purpose
//    jQuery plugin to button-ify html elements
//
// Revision Dates
//    26-Nov-2011 (CT) Creation
//    30-Nov-2011 (CT) Add `disabled`
//    15-Dec-2011 (CT) Use `UI_Icon_Map`, add `gtw_iconify`
//    ««revision-date»»···
//--

"use strict";

( function ($, undefined) {
    $.fn.gtw_buttonify = function (icon_map, opts) {
        var icons   = new $GTW.UI_Icon_Map (icon_map);
        var options = $.extend
            ( { text      : false
              }
            , opts || {}
            );
        $(this).each
            ( function () {
                  var b$   = $(this);
                  var name = this.name;
                  if (name in icons.map) {
                      b$.button
                          ( { disabled : b$.hasClass ("disabled")
                            , icons    : { primary : icons.ui_class (name) }
                            , text     : options.text
                            }
                          );
                  };
              }
            );
        return this;
    };
    $.fn.gtw_iconify = function (icon_map, opts) {
        var icons   = new $GTW.UI_Icon_Map (icon_map);
        var options = $.extend
            ( {}
            , opts || {}
            );
        $(this).each
            ( function () {
                  var b$   = $(this);
                  var name = this.name;
                  if (name in icons.map) {
                      b$.addClass ("ui-icon " + icons.ui_class (name));
                      if (b$.hasClass ("disabled")) {
                          b$.addClass ("ui-state-disabled");
                      };
                  };
              }
            );
        return this;
    };
  } (jQuery)
);

// __END__  GTW/jQ/buttonify.js
