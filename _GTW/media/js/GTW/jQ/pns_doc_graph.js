// Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
// Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
// #*** <License> ************************************************************#
// This software is licensed under the terms of either the
// MIT License or the GNU Affero General Public License (AGPL) Version 3.
// http://www.c-tanzer.at/license/mit_or_agpl.html
// #*** </License> ***********************************************************#
//
//++
// Name
//    GTW/jQ/pns_doc_graph.js
//
// Purpose
//    jQuery plugin to enhance svg-graph displaying a package namespace's
//    object graph
//
// Revision Dates
//    25-Sep-2012 (CT) Creation
//    26-Sep-2012 (CT) Use `.click` not `.on` to bind `cb_click_node`
//    ««revision-date»»···
//--

;
( function ($, undefined) {
    "use strict";
    $.fn.gtw_pns_doc_graph = function gtw_pns_doc_graph (opts) {
        var selectors = $.extend
            ( { node  : "g.E_Type[id]"
              }
            , opts && opts ["selectors"] || {}
            );
        var options  = $.extend
            ( {
              }
            , opts || {}
            , { selectors : selectors
              }
            );
        var cb_click_node = function cb_click_node (ev) {
            var target$ = $(ev.target).closest (selectors.node);
            var name    = target$.attr ("id");
            var url     = options.qurl + name;
            window.open (url).focus ();
        };
        options.svg$ = this;
        this.find  (selectors.node)
            .click (cb_click_node)
            .css   ("cursor", "pointer");
        return this;
    };
  } (jQuery)
);

// __END__ GTW/jQ/pns_doc_graph.js
