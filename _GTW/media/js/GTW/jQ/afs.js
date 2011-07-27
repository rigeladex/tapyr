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
//    13-Apr-2011 (CT) Creation continued.....
//     2-May-2011 (CT) Creation continued......
//    31-May-2011 (MG) `field_change_cb` special handling for checkboxes added
//    25-Jul-2011 (CT) `_setup_callbacks` factored, `setup_completer` started
//    26-Jul-2011 (CT) `setup_completer` continued
//    27-Jul-2011 (CT) `setup_completer` continued.., `$.gtw_ajax_2json` factored
//    27-Jul-2011 (CT) `fix_ui_autocomplete` added to allow html for
//                     auto-ccompletion labels
//    ««revision-date»»···
//--

"use strict";

( function ($) {
    var bwrap = function bwrap (v) {
        return "<b>" + v + "</b>";
    };
    ( function fix_ui_autocomplete () {
        $.extend
            ( $.ui.autocomplete.prototype
            , { _renderItem : function (ul, item) {
                  var result = $("<li></li>")
                      .data     ("item.autocomplete", item)
                      .append   ($("<a></a>").html (item.label))
                      .appendTo (ul);
                  return result;
                }
              }
            );
      } ()
    );
    var setup_completer = function () {
        var _get = function _get (options, elem, val, cb) {
            var completer = elem.completer, data, values;
            values = _get_field_values (elem);
            data   =
                { complete_entity : completer ["complete_entity"] || false
                , trigger         : elem.$id
                , values          : values
                };
            $.gtw_ajax_2json
                ( { async         : true
                  , data          : data
                  , success       : function (answer, status, xhr_instance) {
                        _get_cb (options, elem, val, cb, answer);
                    }
                  , url           : options.completer_url
                  }
                , "Completion"
                );
        };
        var _get_cb = function _get_cb (options, elem, val, cb, response) {
            var n = response.completions, result = [];
            if (response.completions > 0 && response.fields > 0) {
                elem.completer.response = response;
                for (var i = 0, li = response.matches.length, match; i < li; i++) {
                    match = response.matches [i];
                    result.push
                        ( { index : i
                          , label : $.map (match, bwrap).join ("")
                          , value : match [0]
                          }
                        );
                };
            };
            cb (result);
        };
        var _get_field_values = function _get_field_values (elem) {
            var field, id, value;
            var anchor = $GTW.AFS.Elements.id_map [elem.anchor_id];
            var map    = anchor.field_name_map;
            var result = {};
            for ( var i = 0, li = elem.completer.names.length, name
                ; i < li
                ; i++
                ) {
                name  = elem.completer.names [i];
                id    = map [name];
                field = $GTW.AFS.Elements.id_map [id];
                value = field.inp$.val ();
                if (value && value.length > 0) {
                    result [name] = value;
                };
            };
            return result;
        };
        var _put = function _put (options, elem, item) {
            var completer = elem.completer;
            var response  = completer.response;
            var match     = response.matches [item.index];
            if (completer ["complete_entity"]) {
                // XXX;
                alert ("Selected completion " + $GTW.inspect.show (match));
            } else {
                _update_field_values (options, elem, match);
            }
        };
        var _update_field_values = function _update_field_values (options, elem, match) {
            var field, id, value;
            var anchor = $GTW.AFS.Elements.id_map [elem.anchor_id];
            var map    = anchor.field_name_map;
            var names  = elem.completer.names;
            for (var i = 0, li = names.length; i < li; i++) {
                id    = map [names [i]];
                field = $GTW.AFS.Elements.id_map [id];
                field.inp$
                    .val     (match [i])
                    .trigger ("change");
            };
        };
        return function setup_completer (options, elem) {
            var completer = elem.completer;
            if ("choices" in completer) {
                elem.inp$.autocomplete
                    ( { minLength : completer.treshold
                      , source    : completer.choices
                      }
                    );
            } else {
                elem.inp$.autocomplete
                    ( { focus    : function (event, ui) {
                            elem.inp$.val (ui.item.value);
                            return false;
                        }
                      , minLength : completer.treshold
                      , select    : function (event, ui) {
                            _put (options, elem, ui.item);
                            return false;
                        }
                      , source    : function (request, cb) {
                            _get (options, elem, request.term, cb);
                        }
                      }
                    );
            };
        };
    } ();
    $.fn.afs_form = function (afs_form, opts) {
        var options  = $.extend
            ( {
              }
            , opts || {}
            );
        var _ac_response = function _ac_response (response, txt_status, p$, parent) {
            var anchor, root, new_elem, s$;
            if (txt_status == "success") {
                if (! response ["error"]) {
                    p$.append (response.html);
                    s$ = p$.children ().last ();
                    _setup_callbacks (s$, add_cb, cancel_cb, save_cb);
                    new_elem = $GTW.AFS.Elements.create (response.json);
                    anchor =
                        ( parent.anchor_id !== undefined
                        ? $GTW.AFS.Elements.get (parent.anchor_id)
                        : new_elem
                        );
                    root   =
                        ( parent.root_id !== undefined
                        ? $GTW.AFS.Elements.get (parent.root_id)
                        : new_elem
                        );
                    new_elem.setup_value
                        ( { anchor : anchor
                          , root   : root
                          , roots  : $GTW.AFS.Elements.root.roots
                          }
                        );
                } else {
                    alert ("Error: " + response.error);
                }
            }
        };
        var _ec_response = function _ec_response (response, s$, elem) {
            var anchor, new_elem, root;
            s$ = s$
                .html       (response.html)
                .children   ()
                    .unwrap ();
            _bind_click (s$, copy_cb, delete_cb, edit_cb);
            anchor   = $GTW.AFS.Elements.get (elem.anchor_id);
            root     = $GTW.AFS.Elements.get (elem.root_id || anchor.root_id);
            new_elem = $GTW.AFS.Elements.create (response.json);
            new_elem.setup_value
                ( { anchor : anchor
                  , root   : root
                  , roots  : []
                  }
                );
            anchor.value [new_elem.$id] = new_elem.value;
        };
        var _bind_click = function _bind_click (context, cb) {
            for (var i = 1, li = arguments.length, arg; i < li; i++) {
                arg = arguments [i];
                $(arg.$selector, context).click (arg);
            }
        };
        var _setup_callbacks = function _setup_callbacks (context, cb) {
            _bind_click.apply (null, arguments);
            $(":input", context)
                .change (field_change_cb)
                .each
                    ( function (n) {
                        var inp$   = $(this);
                        var id     = inp$.attr ("id");
                        var elem   = $GTW.AFS.Elements.get (id);
                        elem.inp$  = inp$;
                        if ("completer" in elem) {
                            setup_completer (options, elem);
                        }
                      }
                    );
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
                  , sid           : $GTW.AFS.Elements.root.value.sid
                  , new_id_suffix : child_idx
                  // XXX need to pass `pid` of `hidden_role` if any
                  }
                , function (response, txt_status)
                    { _ac_response (response, txt_status, p$, parent); }
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
                      , sid       : $GTW.AFS.Elements.root.value.sid
                      , allow_new : elem.allow_new
                      , collapsed : true
                      }
                    , function (response, txt_status) {
                          var anchor, root, new_elem;
                          if (txt_status == "success") {
                              if (! response ["error"]) {
                                  _ec_response (response, s$, elem);
                              } else {
                                  alert ("Error: " + response.error);
                              }
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
                  , sid           : $GTW.AFS.Elements.root.value.sid
                  , new_id_suffix : child_idx
                  , allow_new     : elem.allow_new
                  , copy          : true
                  }
                , function (response, txt_status)
                    { _ac_response (response, txt_status, p$, elem); }
                );
        };
        var delete_cb = function delete_cb (ev) {
            // XXX;
            alert ("Please implement the `delete_cb`");
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
                , { fid       : id
                  , pid       : pid
                  , sid       : $GTW.AFS.Elements.root.value.sid
                  , allow_new : elem.allow_new
                  }
                , function (response, txt_status) {
                      var anchor, root, new_elem;
                      if (txt_status == "success") {
                          if (! response ["error"]) {
                              s$ = s$
                                  .html       (response.html)
                                  .children   ()
                                      .unwrap ();
                              _setup_callbacks
                                  ( s$, add_cb, cancel_cb, copy_cb, delete_cb
                                  , edit_cb, save_cb
                                  );
                              anchor   = $GTW.AFS.Elements.get (elem.anchor_id);
                              root     = $GTW.AFS.Elements.get
                                  (elem.root_id || anchor.root_id);
                              new_elem = $GTW.AFS.Elements.create (response.json);
                              new_elem.setup_value
                                  ( { anchor : anchor
                                    , root   : root
                                    , roots  : []
                                    }
                                  );
                          } else {
                              alert ("Error: " + response.error);
                          }
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
                anchor    = $GTW.AFS.Elements.get (afs_field.anchor_id);
                ini_value = afs_field.value.init;
                if (f$.attr ("type") == "checkbox") {
                    new_value = f$.attr ("checked") ? "yes" : "no";
                } else {
                    new_value = f$.val ();
                }
                old_value = afs_field.value.edit || ini_value;
                afs_field.value.edit = new_value;
                // trigger `afs_change` event of `anchor`
            }
        };
        var save_cb = function save_cb (ev) {
            var b$     = $(this);
            var s$     = b$.closest ("section");
            var id     = s$.attr    ("id");
            var elem   = $GTW.AFS.Elements.get (id);
            var pvs    = $GTW.AFS.Elements.root.packed_values (elem);
            var json_data =
                  { cargo       : pvs
                  , allow_new   : elem.allow_new
                  , collapsed   : true
                  };
            $.gtw_ajax_2json
                ( { url         : document.URL
                  , data        : json_data
                  , success     : function (answer, status, xhr_instance) {
                        var response;
                        var anchor, root, new_elem;
                        if (! answer ["error"]) {
                            if (answer ["conflicts"]) {
                                // XXX
                                alert ( "Conflicts: \n"
                                      + $GTW.inspect.show (answer.conflicts)
                                      );
                            } else if (answer ["expired"]) {
                                // XXX display re-authorization form
                                alert ("Expired: " + answer.expired);
                            } else if (id === answer.$child_ids [0]) {
                                response = answer [id];
                                if (response !== undefined) {
                                    _ec_response (response, s$, elem);
                                } else {
                                    alert
                                        ( "Save missing response: \n"
                                        + $GTW.inspect.show (answer)
                                        );
                                }
                            }
                        } else {
                            alert ("Error: " + answer.error + "\n\n" + $GTW.inspect.show (json_data));
                        }
                        //alert ("Save response: \n" + $GTW.inspect.show (answer));
                    }
                  }
                , "Save"
                );
        };
        options.form$       = this;
        add_cb.$selector    = ".add.button";
        cancel_cb.$selector = ".cancel.button";
        copy_cb.$selector   = ".copy.button";
        delete_cb.$selector = ".delete.button";
        edit_cb.$selector   = ".edit.button";
        save_cb.$selector   = ".save.button";
        _setup_callbacks (this, add_cb, copy_cb, delete_cb, edit_cb, save_cb);
        return this;
    };
  } (jQuery)
);

// __END__ GTW/jQ/afs.js
