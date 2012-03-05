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
//    GTW/UI_Icon_Map.js
//
// Purpose
//    Provide a map of icons for jQueryUI use
//
// Revision Dates
//    15-Dec-2011 (CT) Creation
//    16-Jan-2012 (CT) Add `CONFIG`
//    29-Feb-2012 (CT) Add `COPY`, `DELETE`, `EDIT`, and `RESET`
//     5-Mar-2012 (CT) Add `HELP`, `INFO`, `REFRESH`, and `SELECT`,
//                     change icons of `CONFIG` and `RESET`
//    ««revision-date»»···
//--

"use strict";

( function () {
    // http://jqueryui.com/themeroller/ has a list of jquery framework icons
    var default_icon_map =
        { ADD         : "plusthick"
        , APPLY       : "check"
        , CANCEL      : "closethick"
        , CLEAR       : "trash"
        , CONFIG      : "gear"
        , COPY        : "copy"
        , DELETE      : "trash"
        , DISABLE     : "minusthick"
        , DONE        : "check"
        , EDIT        : "pencil"
        , ENABLE      : "plusthick"
        , FIRST       : "arrowthick-1-n"
        , HELP        : "help"
        , INFO        : "info"
        , LAST        : "arrowthick-1-s"
        , NEXT        : "arrowthick-1-e"
        , PREV        : "arrowthick-1-w"
        , REFRESH     : "refresh"
        , RESET       : "arrowreturnthick-1-n"
        , SELECT      : "pencil"
        , SORT_ASC    : "triangle-1-s"
        , SORT_DESC   : "triangle-1-n"
        };
    var selectors = {};
    var UI_Icon_Map = $GTW.Class.extend (
        { init        : function init (icon_map) {
              this.defaults = $GTW.UI_Icon_Map.defaults;
              if ("map" in icon_map) {
                  this.map       = icon_map.map;
                  this.selectors = icon_map.selectors;
                  this.ui_class  = icon_map.ui_class;
              } else {
                  this.map       = $.extend ({}, this.defaults, icon_map || {});
                  this.selectors = { button : "button[name]" };
                  this.ui_class  = {};
                  for (var name in this.map) {
                      if (this.map.hasOwnProperty (name)) {
                          this.selectors [name.toLowerCase () + "_button"] =
                              "button[name=" + name + "]";
                          this.ui_class [name] = "ui-icon-" + this.map [name];
                      };
                  };
              };
          }
        }
      , { defaults    : default_icon_map
        }
    );
    $GTW.UI_Icon_Map = UI_Icon_Map;
  } ()
);

// __END__ GTW/UI_Icon_Map.js
