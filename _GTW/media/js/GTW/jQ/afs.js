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
//     4-Apr-2011 (CT) Creation continued...
//     5-Apr-2011 (CT) Creation continued....
//    ««revision-date»»···
//--

( function ($) {
    $.fn.afs_form = function (afs_form, opts) {
        var options  = $.extend
            ( {
              }
            , opts || {}
            );
        var _ac_response = function _ac_response (response, p$, parent) {
            var anchor, root, new_elem, s$;
            if (response) {
                p$.append (response.html);
                s$ = p$.children ().last ();
                $(".cancel.button", s$).click (cancel_cb);
                new_elem = $GTW.AFS.Elements.create (response.json);
                anchor =
                    ( parent.$anchor_id !== undefined
                    ? $GTW.AFS.Elements.get (parent.$anchor_id)
                    : new_elem
                    );
                root   =
                    ( parent.$root_id !== undefined
                    ? $GTW.AFS.Elements.get (parent.$root_id)
                    : new_elem
                    );
                new_elem.setup_value
                    ( { anchor : anchor
                      , root   : root
                      , roots  : $GTW.AFS.Elements.root.roots
                      }
                    );
            }
        };
        var add_cb = function add_cb (ev) {
            var b$        = $(this);
            var p$        = b$.closest ("section");
            var id        = p$.attr    ("id");
            var parent    = $GTW.AFS.Elements.get (id);
            var child_idx = parent.new_child_idx ();
            $.getJSON
                ( options.expander_url
                , { fid           : id
                  , new_id_suffix : child_idx
                  }
                , function (response) { _ac_response (response, p$, parent); }
                );
        };
        var cancel_cb = function cancel_cb (ev) {
            var b$     = $(this);
            var s$     = b$.closest ("section");
            var id     = s$.attr    ("id");
            var elem   = $GTW.AFS.Elements.get (id);
            var value  = elem ["value"];
            var pid    = value && value.edit.pid;
            if (pid != undefined) {
                $.getJSON
                    ( options.expander_url
                    , { fid       : id
                      , pid       : pid
                      , collapsed : true
                      }
                    , function (response) {
                          var anchor, root, new_elem;
                          if (response) {
                              s$ = s$
                                  .html       (response.html)
                                  .children   ()
                                      .unwrap ();
                              $(".copy.button", s$).click (copy_cb);
                              $(".edit.button", s$).click (edit_cb);
                              anchor = $GTW.AFS.Elements.get (elem.$anchor_id);
                              root   = $GTW.AFS.Elements.get
                                  (elem.$root_id || anchor.$root_id);
                              new_elem = $GTW.AFS.Elements.create
                                  (response.json);
                              new_elem.setup_value
                                  ( { anchor : anchor
                                    , root   : root
                                    , roots  : []
                                    }
                                  );
                              anchor.value [new_elem.$id] = new_elem.value;
                          }
                      }
                    );
            } else {
                elem.remove ()
                s$.remove   ();
            };
        };
        var copy_cb = function copy_cb (ev) {
            var b$        = $(this);
            var s$        = b$.closest ("section.closed");
            var p$        = s$.parent  ();
            var id        = s$.attr    ("id");
            var elem      = $GTW.AFS.Elements.get (id);
            var value     = elem ["value"];
            var pid       = value && value.edit.pid;
            var parent    = $GTW.AFS.Elements.get (p$.attr ("id"));
            var child_idx = parent.new_child_idx ();
            $.getJSON
                ( options.expander_url
                , { fid           : id
                  , pid           : pid
                  , new_id_suffix : child_idx
                  , copy          : true
                  }
                , function (response) { _ac_response (response, p$, elem); }
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
                      var anchor, root, new_elem;
                      if (response) {
                          s$ = s$
                              .html       (response.html)
                              .children   ()
                                  .unwrap ();
                          $(".cancel.button", s$).click (cancel_cb);
                          anchor   = $GTW.AFS.Elements.get (elem.$anchor_id);
                          root     = $GTW.AFS.Elements.get
                              (elem.$root_id || anchor.$root_id);
                          new_elem = $GTW.AFS.Elements.create (response.json);
                          new_elem.setup_value
                              ( { anchor : anchor
                                , root   : root
                                , roots  : []
                                }
                              );
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
        $(".add.button",     this).click (add_cb);
        $(".copy.button",    this).click (copy_cb);
        $(".edit.button",    this).click (edit_cb);
        return this;
    };
  } (jQuery)
);

// __END__ GTW/jQ/afs.js
