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
//    GTW/jQ/e_type_admin.js
//
// Purpose
//    jQuery plugin for GTW.NAV.E_Type.Admin pages
//
// Revision Dates
//    26-Nov-2011 (CT) Creation
//    21-Feb-2012 (CT) Use `$GTW.L` to create DOM elements
//    ««revision-date»»···
//--

"use strict";

( function ($) {
    var L = $GTW.L;
    $.fn.gtw_e_type_admin_postify = function gtw_e_type_admin_postify (opts) {
        var options  = $.extend
            ( { hidden_selector : "td"
              , parent_selector : "tr"
              }
            , opts || {}
            );
        $(this).gtw_postify_a (options);
        return this;
    };
    $.fn.gtw_e_type_admin_linkify = function gtw_e_type_admin_linkify (opts) {
        var options  = $.extend
            ( { a_selector  : "td.change a"
              , td_selector : "td"
              , tr_class    : "active"
              }
            , opts || {}
            );
        $(this).each
            ( function () {
                var tr$  = $(this);
                var ac$  = tr$.find (options.a_selector);
                var href = ac$.attr ("href");
                tr$
                  .addClass (options.tr_class)
                  .attr ("title", ac$.attr ("title"))
                  .find (options.td_selector).each
                    ( function () {
                        var td$ = $(this);
                        var inner_html = td$.html ();
                        if (! td$.hasClass ("cmd-button")) {
                          td$.html
                              ($(L ("a", { href : href, html : inner_html})));
                        };
                      }
                    );
              }
            );
        return this;
    };
    ( function () {
        var setup_obj_list = function setup_obj_list () {
            var options = $GTW.ETA$.options;
            $(options.obj_list_selector + " " + options.postify_selector)
                .gtw_e_type_admin_postify (options ["postify_options"]);
            $(options.obj_list_selector + " " + options.linkify_selector)
                .gtw_e_type_admin_linkify (options ["linkify_options"]);
        };
        $GTW.ETA$ = new $GTW.Module (
            { options            :
                { linkify_selector   : "tbody tr"
                , obj_list_selector  : ".Object-List"
                , postify_options    :
                    { display_value  : "table-cell"
                    }
                , postify_selector   : "a.delete"
                }
            , setup_obj_list     : setup_obj_list
            }
        );
      } ()
    );
  } (jQuery)
);

// __END__ GTW/jQ/e_type_admin.js
