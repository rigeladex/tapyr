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
//     1-Apr-2011 (CT) Creation continued..
//    ««revision-date»»···
//--

( function ($) {
    $.fn.afs_form = function (afs_form, opts) {
        var options  = $.extend
            ( {
              }
            , opts || {}
            );
        var add_cb = function add_cb (ev) {
            var b$       = $(this);
            var s$       = b$.closest ("section");
            var id       = s$.attr    ("id");
            var parent   = $GTW.AFS.Elements.get (id);
            var child_id = parent.new_child_id ();
            $.getJSON
                ( options.expander_url
                , { fid      : id
                  , child_id : child_id
                  }
                , function (response) {
                      if (response) {
                          s$.append (response.html);
                          // alert ($GTW.inspect.show (response.json, undefined, 1));
                          // XXX merge response.json
                      }
                  }
                );
        };
        var copy_cb = function copy_cb (ev) {
            var b$       = $(this);
            var s$       = b$.closest ("section.closed");
            var p$       = s$.parent  ();
            var id       = s$.attr    ("id");
            var elem     = $GTW.AFS.Elements.get (id);
            var value    = elem ["value"];
            var pid      = value && value.edit.pid;
            var parent   = $GTW.AFS.Elements.get (p$.attr ("id"));
            var child_id = parent.new_child_id ();
            // alert ($GTW.inspect.show ($GTW.AFS.Elements.get (p$.attr ("id")), undefined, 1));
            $.getJSON
                ( options.expander_url
                , { fid      : id
                  , pid      : pid
                  , child_id : child_id
                  , copy     : true
                  }
                , function (response) {
                      if (response) {
                          p$.append (response.html);
                          // alert ($GTW.inspect.show (response.json, undefined, 1));
                          // XXX merge response.json
                      }
                  }
                );
        };
        var edit_cb = function edit_cb (ev) {
            var b$    = $(this);
            var s$    = b$.closest ("section.closed");
            var id    = s$.attr    ("id");
            var elem  = $GTW.AFS.Elements.get (id);
            var value = elem ["value"];
            var pid   = value && value.edit.pid;
            $.getJSON
                ( options.expander_url
                , { fid      : id
                  , pid      : pid
                  }
                , function (response) {
                      if (response) {
                          s$.html (response.html);
                          // alert ( elem.name + "[" + pid + "]: " + $GTW.inspect.show (response.json, undefined, 1));
                          // XXX merge response.json
                      }
                  }
                );
        };
        var field_change_cb = function field_change_cb (ev) {
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
        options.inputs$.change (field_change_cb);
        $(".add.button",  this).click (add_cb);
        $(".copy.button", this).click (copy_cb);
        $(".edit.button", this).click (edit_cb);
        return this;
    };
  } (jQuery)
);

// __END__ GTW/jQ/afs.js
