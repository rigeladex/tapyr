// Copyright (C) 2012 Martin Glueck All rights reserved
// Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
// #*** <License> ************************************************************#
// This script is licensed under the terms of either the
// MIT License or the GNU Affero General Public License (AGPL) Version 3.
// http://www.c-tanzer.at/license/mit_or_agpl.html
// #*** </License> ***********************************************************#
//
//++
// Name
//    GTW/jQ/Image_Selection
//
// Purpose
//    Special code for the handling of the image url selection
//
// Revision Dates
//    17-Aug-2012 (MG) Creation
//    17-Aug-2012 (MG) Make selection window url configurable
//    ««revision-date»»···
//--

"use strict";

( function ($) {
    var Image_Selection_Field = $GTW.AFS.Elements.Field.extend (
        { init      : function init (spec) {
              this._super (spec);
          }
        , _setup_field : function _setup_field (inp$) {
            var selection_url = this.selection_url;
            var url = inp$.val ();
            var img$ = $("<img />").attr ({ src : url, alt : this.label})
                                  .addClass ("afs-media-button");
            inp$.prop   ("type", "hidden")
                .after  (img$);
            img$.click (function (ev) {
                var this$ = $(this);
                window.SetUrl = function (url) {
                    img$.attr ("src", url);
                    inp$.val  (url).trigger ("change");
                };
                window.open (selection_url, "_blank");
            });
          }
        }
      , { type_name : "Image_Selection_Field" }
    );

    $GTW.AFS.Elements.Image_Selection_Field = Image_Selection_Field;
  } (jQuery)
);

// __END__ GTW/jQ/Image_Selection.js
