// Copyright (C) 2012-2013 Martin Glueck All rights reserved
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
//    24-Jan-2013 (MG) Use elfinder as media selection interface
//    28-Jan-2013 (MG) `_setup_field` now has two parameters
//    ««revision-date»»···
//--

"use strict";

( function ($) {
    var Image_Selection_Field = $GTW.AFS.Elements.Field.extend (
        { _setup_field : function _setup_field (inp$, Form) {
            var selection_url = this.selection_url;
            var url = inp$.val ();
            var img$ = $("<img />").attr ({ src : url, alt : this.label})
                                  .addClass ("afs-media-button");
            inp$.prop   ("type", "hidden")
                .after  (img$);
            var elfinder = $('<div />').dialogelfinder ({
                      url             : this.elfinder
                    , lang            : this.language
                    , width           : 840
                    , destroyOnClose  : false
                    , getFileCallback : function(files, fm) {
                          img$.attr ("src", files);
                          inp$.val  (files).trigger ("change");
                          console.log (files);
                      }
                    , commandsOptions : {
                        getfile : {
                              oncomplete : 'close'
                            , folders    : true
                        }
                      }
                    , autoOpen : false
                });
            img$.click (function (ev) {
                var this$ = $(this);
                window.SetUrl = function (url) {
                };
                elfinder.dialogelfinder ("open");
            });
          }
        }
      , { type_name : "Image_Selection_Field" }
    );

    $GTW.AFS.Elements.Image_Selection_Field = Image_Selection_Field;
  } (jQuery)
);

// __END__ GTW/jQ/Image_Selection.js
