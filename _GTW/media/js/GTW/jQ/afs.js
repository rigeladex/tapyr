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
//    31-Mar-2011 (CT) Creation continued
//    ««revision-date»»···
//--

( function ($) {
    $.fn.afs_form = function (afs_form, opts) {
        var options  = $.extend
            ( {
              }
            , opts || {}
            );
        var edit = function edit (ev, opts) {
            var b$    = $(this);
            var s     = b$.closest ("section.closed");
            var id    = s.attr ("id");
            var elem  = $GTW.AFS.Elements.get (id);
            var value = elem ["value"];
            var pid   = value && value.edit.pid;
            var cargo = $.extend
                ( { fid     : id
                  , pid     : pid
                  }
                , opts || {}
                );
            $.getJSON
                ( options.expander_url, cargo
                , function (response) {
                      if (response) {
                          alert (elem.name + "[" + pid + "]: "+ response.html);
                          // XXX
                      }
                  }
                );
        };
        var field_change = function field_change (ev) {
            var f$ = $(this);
            var id = f$.attr ("id");
            var afs_field = $GTW.AFS.Elements.get (id);
            var ini_value, new_value, old_value, anchor;
            if (afs_field !== undefined) {
                anchor    = $GTW.AFS.Elements.get (afs_field.$anchor_id);
                ini_value = afs_field.value.init;
                new_value = f$.attr ("value");
                old_value = afs_field.value.edit || ini_value;
                afs_field.value.edit = new_value;
                // trigger `afs_change` event of `anchor`
            }
        };
        options.form$   = this;
        options.inputs$ = $(":input", this);
        options.inputs$.change (field_change);
        $(".edit.button", this).click (edit);
        return this;
    };
  } (jQuery)
);

// __END__ GTW/jQ/afs.js
