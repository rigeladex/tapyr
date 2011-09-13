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
//    27-Jul-2011 (CT) `setup_completer` continued..,
//                     `$.gtw_ajax_2json` factored
//    27-Jul-2011 (CT) `fix_ui_autocomplete` added to allow html for
//                     auto-ccompletion labels
//    28-Jul-2011 (CT) `setup_completer` continued...
//     1-Aug-2011 (CT) `setup_completer` continued....,
//                     `_ec_response` refactored
//     7-Sep-2011 (CT) `setup_completer` continued.....
//     8-Sep-2011 (CT) `setup_completer` continued...... (guards added)
//    12-Sep-2011 (CT) `Field._get_completer_value` factored,
//                     `Field_Composite._get_completer_value` added
//    12-Sep-2011 (CT) Shortcut `var $AFS_E = $GTW.AFS.Elements` added
//    13-Sep-2011 (CT) `Field_Entity._get_completer_value` added
//    ««revision-date»»···
//--

"use strict";

( function ($) {
    var $AFS_E = $GTW.AFS.Elements;
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
    $.fn.afs_form = function (afs_form, opts) {
        var options  = $.extend
            ( {
              }
            , opts || {}
            );
        var setup_completer = function () {
            $AFS_E.Field.prototype._get_completer_value = function () {
                var result, value = this.inp$.val ();
                if (value && value.length > 0) {
                    result = value;
                };
                return result;
            };
            $AFS_E.Field_Composite.prototype._get_completer_value = function () {
                var field, fv, id, name, result, value;
                var map = this.field_name_map, n = 0, values = {};
                for (name in map) {
                    if (map.hasOwnProperty (name)) {
                        id    = map [name];
                        field = $AFS_E.id_map [id];
                        value = field._get_completer_value ();
                        if (value !== undefined) {
                            n += 1;
                            values [name] = value;
                        };
                    };
                };
                if (n > 0) {
                    result = values;
                };
                return result;
            };
            $AFS_E.Field_Entity.prototype._get_completer_value = function () {
                var result = this.value.edit.pid;
                return result;
            };
            $AFS_E.Field_Role_Hidden.prototype._get_completer_value =
                $AFS_E.Field_Entity.prototype._get_completer_value;
            var _get = function _get (options, elem, val, cb) {
                var completer = elem.completer, data, values;
                values = _get_field_values (elem);
                data   =
                    { complete_entity : completer ["entity_p"] || false
                    , fid             : elem.anchor_id
                    , trigger         : elem.$id
                    , values          : values
                    };
                $.gtw_ajax_2json
                    ( { async         : true
                      , data          : data
                      , success       : function (answer, status, xhr_i) {
                            _get_cb (options, elem, val, cb, answer);
                        }
                      , url           : options.completer_url
                      }
                    , "Completion"
                    );
            };
            var _get_cb = function _get_cb (options, elem, val, cb, response) {
                var n = response.completions, result = [];
                if (n > 0 && response.fields > 0) {
                    elem.completer.response = response;
                    for ( var i = 0, li = response.matches.length, match
                        ; i < li
                        ; i++
                        ) {
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
                var anchor = $AFS_E.id_map [elem.anchor_id];
                var map    = anchor.field_name_map;
                var result = {};
                for ( var i = 0, li = elem.completer.names.length, name
                    ; i < li
                    ; i++
                    ) {
                    name  = elem.completer.names [i];
                    if (name in map) {
                        id    = map [name];
                        field = $AFS_E.id_map [id];
                        value = field._get_completer_value ();
                        if (value !== undefined) {
                            result [name] = value;
                        };
                    };
                };
                return result;
            };
            var _put = function _put (options, elem, item) {
                var data;
                var anchor;
                var completer = elem.completer;
                var response  = completer.response;
                var match     = response.matches [item.index];
                var names     = completer.names.slice (0, response.fields);
                _update_field_values (options, elem, match, names);
                if (response.partial) {
                    // XXX ??? elem.inp$.autocomplete._trigger ("search");
                } else if (completer ["entity_p"]) {
                    data   =
                        { fid             : elem.anchor_id
                        , sid             : $AFS_E.root.value.sid
                        , allow_new       : elem.allow_new
                        , complete_entity : true
                        , trigger         : elem.$id
                        , values          : _get_field_values (elem)
                        };
                    $.gtw_ajax_2json
                        ( { async         : true
                          , data          : data
                          , success       : function (answer, status, xhr_i) {
                                _put_cb (options, elem, item, answer);
                            }
                          , url           : options.completed_url
                          }
                        , "Completion"
                        );
                };
            };
            var _put_cb = function put_cb (options, elem, item, response) {
                var s$;
                if (response.completions > 0) {
                    if (  (response.completions == 1)
                       && elem.completer ["entity_p"]
                       ) {
                        s$ = elem.inp$.closest ("section");
                        s$ = _ec_response (response, s$, elem);
                        _setup_callbacks
                            ( s$, add_cb, cancel_cb, copy_cb, delete_cb
                            , edit_cb, save_cb
                            );
                    } else if (response.fields > 0) {
                        _update_field_values
                            (options, elem, response.values, response.names);
                    };
                };
            };
            var _update_entity_init = function _update_entity_init
                    (options, elem, match, names) {
                var field, id;
                var anchor = $AFS_E.id_map [elem.anchor_id];
                var map    = anchor.field_name_map;
                for (var i = 0, li = names.length, name; i < li; i++) {
                    name = names [i];
                    if (name in map) {
                        id = map [name];
                        if (id in $AFS_E.id_map) {
                            field = $AFS_E.id_map [id];
                            field.value.init = match [i];
                        };
                    };
                };
            } ;
            var _update_field_values = function _update_field_values
                    (options, elem, match, names) {
                var field, id;
                var anchor = $AFS_E.id_map [elem.anchor_id];
                var map    = anchor.field_name_map;
                for (var i = 0, li = names.length, name; i < li; i++) {
                    name = names [i];
                    if (name in map) {
                        id = map [name];
                        if (id in $AFS_E.id_map) {
                            field = $AFS_E.id_map [id];
                            field.inp$.val (match [i]).trigger ("change");
                        };
                    };
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
        var _bind_click = function _bind_click (context, cb) {
            var sel;
            for (var i = 1, li = arguments.length, arg; i < li; i++) {
                arg = arguments [i];
                sel = $(arg.$selector, context);
                sel.click (arg);
            }
        };
        var _ac_response = function _ac_response
                (response, txt_status, p$, parent) {
            var anchor, root, new_elem, s$;
            if (txt_status == "success") {
                if (! response ["error"]) {
                    p$.append (response.html);
                    s$ = p$.children ().last ();
                    new_elem = $AFS_E.create (response.json);
                    anchor =
                        ( parent.anchor_id !== undefined
                        ? $AFS_E.get (parent.anchor_id)
                        : new_elem
                        );
                    root   =
                        ( parent.root_id !== undefined
                        ? $AFS_E.get (parent.root_id)
                        : new_elem
                        );
                    new_elem.setup_value
                        ( { anchor : anchor
                          , root   : root
                          , roots  : $AFS_E.root.roots
                          }
                        );
                    _setup_callbacks (s$, add_cb, cancel_cb, save_cb);
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
            new_elem = $AFS_E.create (response.json);
            anchor   = $AFS_E.get (elem.anchor_id);
            root     = $AFS_E.get (elem.root_id || anchor.root_id);
            new_elem.setup_value
                ( { anchor : anchor
                  , root   : root || anchor
                  , roots  : []
                  }
                );
            anchor.value [new_elem.$id] = new_elem.value;
            return s$;
        };
        var _setup_callbacks = function _setup_callbacks (context, cb) {
            _bind_click.apply (null, arguments);
            $(":input", context)
                .change (field_change_cb)
                .each
                    ( function (n) {
                        var inp$   = $(this);
                        var id     = inp$.attr ("id");
                        var elem   = $AFS_E.get (id);
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
            var parent    = $AFS_E.get (id);
            var child_idx = parent.new_child_idx ();
            $.getJSON
                ( options.expander_url
                , { fid           : id
                  , sid           : $AFS_E.root.value.sid
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
            var elem   = $AFS_E.get (id);
            var value  = elem ["value"];
            var pid    = value && value.edit.pid;
            if (pid != undefined) {
                $.getJSON
                    ( options.expander_url
                    , { fid       : id
                      , pid       : pid
                      , sid       : $AFS_E.root.value.sid
                      , allow_new : elem.allow_new
                      , collapsed : true
                      }
                    , function (response, txt_status) {
                          if (txt_status == "success") {
                              if (! response ["error"]) {
                                  s$ = _ec_response (response, s$, elem);
                                  _bind_click (s$, copy_cb, delete_cb, edit_cb);
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
            var elem      = $AFS_E.get (id);
            var value     = elem ["value"];
            var pid       = value && value.edit.pid;
            var parent    = $AFS_E.get (p$.attr ("id"));
            var child_idx = parent.new_child_idx ();
            $.getJSON
                ( options.expander_url
                , { fid           : id
                  , pid           : pid
                  , sid           : $AFS_E.root.value.sid
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
            var elem  = $AFS_E.get (id);
            var value = elem ["value"];
            var pid   = value && value.edit.pid;
            $.getJSON
                ( options.expander_url
                , { fid       : id
                  , pid       : pid
                  , sid       : $AFS_E.root.value.sid
                  , allow_new : elem.allow_new
                  }
                , function (response, txt_status) {
                      if (txt_status == "success") {
                          if (! response ["error"]) {
                              s$ = _ec_response (response, s$, elem);
                              _setup_callbacks
                                  ( s$, add_cb, cancel_cb, copy_cb, delete_cb
                                  , edit_cb, save_cb
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
            var afs_field = $AFS_E.get (id);
            var ini_value, new_value, old_value, anchor;
            if (afs_field !== undefined) {
                ini_value = afs_field.value.init;
                if (f$.attr ("type") == "checkbox") {
                    new_value = f$.attr ("checked") ? "yes" : "no";
                } else {
                    new_value = f$.val ();
                }
                old_value = afs_field.value.edit || ini_value;
                afs_field.value.edit = new_value;
                // trigger `afs_change` event of `anchor`
                // anchor = $AFS_E.get (afs_field.anchor_id);
            }
        };
        var save_cb = function save_cb (ev) {
            var b$     = $(this);
            var s$     = b$.closest ("section");
            var id     = s$.attr    ("id");
            var elem   = $AFS_E.get (id);
            var pvs    = $AFS_E.root.packed_values (elem);
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
                                    s$ = _ec_response (response, s$, elem);
                                    _setup_callbacks
                                        ( s$
                                        , add_cb, cancel_cb, copy_cb
                                        , delete_cb, edit_cb, save_cb
                                        );
                                } else {
                                    alert
                                        ( "Save missing response: \n"
                                        + $GTW.inspect.show (answer)
                                        );
                                }
                            }
                        } else {
                            alert
                                ( "Error: " + answer.error
                                + "\n\n"
                                + $GTW.inspect.show (json_data)
                                );
                        }
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
