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
//    GTW/jQ/afs.js
//
// Purpose
//    jQuery plugin for AJAX-enhanced forms
//
// Revision Dates
//    29-Mar-2011 (CT) Creation
//    ««revision-date»»···
//--

( function ($) {
    $.fn.afs_form = function (afs_form, opts) {
        var options  = $.extend
            ( {
              }
            , opts || {}
            );
        var field_change = function field_change (ev) {
            var f$ = $(this); // XXX ???
            var id = f$.attr ("id");
            var afs_field = $GTW.AFS.Elements.get (id);
            if (afs_field !== undefined) {
                afs_field.value.edit = f$.attr ("value");
                // XXX validate;
            }
        };
        options.form$   = this;
        options.inputs$ = $(":input", this);
        options.inputs$.change (field_change);
        return this;
    };
  } (jQuery)
);

// __END__ GTW/jQ/afs.js
