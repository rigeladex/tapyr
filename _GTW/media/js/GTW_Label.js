//-*- coding: iso-8859-1 -*-
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
//    GTW_Label
//
// Purpose
//    jQuery plugin for improving labels
//
//
// Revision Dates
//    12-Jan-2011 (CT) Creation
//    26-Jan-2011 (CT) Style change
//    ««revision-date»»···
//--

( function ($) {
    var label_target = function (label$) {
        var id = label$.attr ("for");
        var result;
        if (id) {
            result = $("#" + id).get (0);
        };
        return result;
    };
    $.fn.gtw_label_as_placeholder = function (options)  {
        var options  = $.extend
            ( { hide_parent : false
              }
            , options || {}
            );
        this.each (
            function () {
                var label$ = $(this);
                var target = label_target (label$);
                if (target) {
                    var target$ = $(target);
                    var placeholder = target$.attr ("placeholder");
                    if (! placeholder) {
                        target$.attr ("placeholder", label$.text ());
                        var to_hide$ = options.hide_parent
                            ? label$.closest (options.hide_parent) : label$;
                        to_hide$.css ("display", "none");
                    };
                };
            }
        );
        return this;
    };
    $.fn.gtw_label_clicker = function (options) {
        var options  = $.extend
            ( { l_class : "clickable"
              }
            , options || {}
            );
        this.each (
            function () {
                var label$ = $(this);
                var target = label_target (label$);
                if (target) {
                    label$.click (function (ev) { target.focus (); });
                    options.l_class && label$.addClass (options.l_class);
                };
            }
        );
        return this;
    };
  }
) (jQuery);

// __END__ GTW_Label.js
