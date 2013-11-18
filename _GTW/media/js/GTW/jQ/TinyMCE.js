// Copyright (C) 2012-2013 Martin Glueck All rights reserved
// Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
// #*** <License> ************************************************************#
// This software is licensed under the terms of either the
// MIT License or the GNU Affero General Public License (AGPL) Version 3.
// http://www.c-tanzer.at/license/mit_or_agpl.html
// #*** </License> ***********************************************************#
//
//++
// Name
//    GTW/jQ/TinyMCE
//
// Purpose
//    Special code for handling the TinyMCE WYSIWYG editor
//
// Revision Dates
//    16-Aug-2012 (MG) Creation
//    18-Aug-2012 (MG) Fix `pre_submit_callbacks` handling
//    19-Aug-2012 (MG) Set `domain` to allow serving of tinymce from a
//                     different subdomain
//    28-Jan-2013 (MG) `_setup_field` now has two parameters//    ««revision-date»»···
//--

"use strict";

( function ($) {
    var TinyMCE_Field = $GTW.AFS.Elements.Field.extend (
        { _setup_field : function _setup_field (inp$, Form) {
            var file_browser = this.file_browser;
            var _open_selector = function (field_name, url, type, win) {
                tinyMCE.activeEditor.windowManager.open
                  ( { file            : file_browser.url
                    , title           : file_browser.title
                    , width           : file_browser.width
                    , height          : file_browser.height
                    , resizable       : 'yes'
                    , inline          : 'yes'  // This parameter only has an effect if you use the inlinepopups plugin!
                    , popup_css       : false  // Disable TinyMCE's default popup CSS
                    , close_previous  : 'no'
                    }
                  , { window          : win
                    , input           : field_name
                    }
                  );
                return false;
            };
            var options  = this.tinymce;
            var domain_a = document.domain.split (".").slice (-2);
            options.file_browser_callback = _open_selector;
            options.mode                  = "exact";
            options.elements              = inp$.attr ("id");
            document.domain               = domain_a.join (".");
            var TE = tinyMCE.init (options);
            var pre_submit = function pre_submit () {
                tinymce.get  (options.elements).save ();
                inp$.trigger ("change");
            };
            Form.pre_submit_callbacks.push (pre_submit);
          }
        }
      , { type_name : "TinyMCE_Field" }
    );

    $GTW.AFS.Elements.TinyMCE_Field = TinyMCE_Field;
  } (jQuery)
);

// __END__ GTW/jQ/TinyMCE.js
