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
//    ««revision-date»»···
//--

"use strict";

( function () {
    var default_icon_map =
        { ADD         : "plusthick"
        , APPLY       : "check"
        , CANCEL      : "closethick"
        , CLEAR       : "trash"
        , DISABLE     : "minusthick"
        , ENABLE      : "plusthick"
        , FIRST       : "arrowthick-1-n"
        , LAST        : "arrowthick-1-s"
        , NEXT        : "arrowthick-1-e"
        , PREV        : "arrowthick-1-w"
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
