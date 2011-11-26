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
//    ««revision-date»»···
//--

"use strict";

( function ($, undefined) {
    $.fn.gtw_buttonify = function (icon_map, opts) {
        var options  = $.extend
            ( { text      : false
              }
            , opts || {}
            );
        $(this).each
            ( function () {
                  var b$   = $(this);
                  var name = this.name;
                  if (name in icon_map) {
                      b$.button
                          ( { icons :
                                { primary : "ui-icon-" + icon_map [name]
                                }
                            , text  : options.text
                            }
                          );
                  };
              }
            );
        return this;
    }
  } (jQuery)
);

// __END__  GTW/jQ/buttonify.js
