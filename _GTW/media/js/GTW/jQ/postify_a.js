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
//    postify_a
//
// Purpose
//    Use POST request for <a> elements meant to change state of the web app
//
// Revision Dates
//     1-Jun-2011 (CT) Creation
//     7-Jun-2011 (CT) Typos fixed
//     7-Jun-2011 (CT) Support for `answer ["error"]` added to `success` handler
//    27-Jul-2011 (CT) Use `gtw_ajax_2json` instead of home-grown code
//    21-Nov-2011 (CT) Add `hidden_selector`
//    30-Nov-2011 (CT) Use `return false` instead of .`preventDefault`
//    19-Apr-2012 (CT) If `"hidden_selector" in options` --> set `display` of
//                     `this` to `"inherit"` to placate Chrome
//    29-Apr-2013 (CT) Use `$GTW.show_message`, not `console.error`
//    ««revision-date»»···
//--

"use strict";

( function ($) {
    $.fn.gtw_postify_a = function (opts) {
        var options  = $.extend
            ( { display_value   : "block"
              , parent_selector : "tr"
              }
            , opts || {}
            );
        var delete_cb  = function delete_cb (ev) {
            var a   = $(this);
            var p   = a.closest (options.parent_selector);
            var url = a.attr    ("href");
            do_ajax
                ( url
                , function (answer, status, xhr_instance) {
                      var repl;
                      if ("error" in answer && answer ["error"]) {
                          $GTW.show_message ("Delete error", answer.error);
                      } else if (answer ["replacement"]) {
                          repl = answer.replacement;
                          p.html (repl.html);
                          if (repl ["postify_selector"]) {
                              $(repl.postify_selector, p)
                                  .postify_a (repl ["postify_opts"]);
                          }
                      } else {
                          p.remove ();
                      }
                  }
                );
            return false;
        };
        var do_ajax  = function do_ajax (url, success) {
            $.gtw_ajax_2json
                ( { url         : url
                  , data        : ""
                  , error       : function (xhr_instance, status, exc) {
                        alert ("Post to " + url + " failed: " + status);
                    }
                  , success     : success
                  }
                );
        };
        this.click (delete_cb);
        if ("hidden_selector" in options) {
            this.each
                ( function () {
                      var a = $(this);
                      var p = a.closest (options.hidden_selector);
                      p.css ({ display : options.display_value }).show ();
                  }
                );
            this.css ({ display : "inherit" }).show ();
        } else {
            this.css ({ display : options.display_value }).show ();
        };
        return this;
    }
  }
) (jQuery);

// __END__ postify_a.js
