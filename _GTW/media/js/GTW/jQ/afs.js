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
//    13-Sep-2011 (CT) `setup_completer._put` changed to continue for partial
//                     completions
//    15-Sep-2011 (CT) `Field_Entity._get_completer_value` fixed
//    21-Sep-2011 (CT) Support for `completer.embedded_p` added
//     7-Oct-2011 (CT) `_put_cb` corrected
//                     (pass `anchor` instead of `elem` to `_ec_response`)
//    10-Oct-2011 (CT) `Field._get_completer_value` guarded for `inp$`
//    10-Oct-2011 (CT) `_get_cb` corrected
//                     (if `embedded_p` use `anchor.completer...`)
//    10-Oct-2011 (CT) s/_ac_response/_response_append/
//                     s/_ec_response/_response_replace/
//    10-Oct-2011 (CT) `clear_cb` added
//    13-Oct-2011 (CT) `delete_cb` added
//    13-Oct-2011 (CT) `_renderItem` changed locally, not globally
//    13-Oct-2011 (CT) `gtw_autocomplete` factored into separate module
//    14-Oct-2011 (CT) `callback`, `cmd_menu`, and `_cmds` added,
//                     `_setup_cmd_menu` started
//    18-Oct-2011 (CT) `_setup_cmd_menu` continued
//    ««revision-date»»···
//--

"use strict";

( function ($) {
    var $AFS_E = $GTW.AFS.Elements;
    var bwrap = function bwrap (v) {
        return "<b>" + v + "</b>";
    };
    var _get_completer_values_nested = function _get_completer_values_nested () {
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
    $AFS_E.Field.prototype._get_completer_value = function () {
        var result, value;
        if ("inp$" in this) {
            value = this.inp$.val ();
            if (value && value.length > 0) {
                result = value;
            };
        };
        return result;
    };
    $AFS_E.Field_Composite.prototype._get_completer_value =
        _get_completer_values_nested;
    $AFS_E.Field_Entity.prototype._get_completer_value = function () {
        var result, value = this.value.edit.pid;
        if (value != null) {
            result = value;
        } else {
            result = _get_completer_values_nested.call (this);
        };
        return result;
    };
    $.fn.afs_form = function (afs_form, opts) {
        var options  = $.extend
            ( {
              }
            , opts || {}
            );
        var setup_completer = function () {
            var _get = function _get (options, elem, val, cb) {
                var anchor    = elem;
                var completer = elem.completer;
                var data, values;
                while (completer.embedded_p) {
                    anchor    = $AFS_E.id_map [anchor.anchor_id];
                    completer = anchor.completer;
                };
                values = _get_field_values (anchor);
                data   =
                    { complete_entity : completer ["entity_p"] || false
                    , fid             : anchor.anchor_id
                    , trigger         : anchor.$id
                    , trigger_n       : elem.$id
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
                var anchor    = elem;
                var completer = elem.completer;
                var l, n      = response.completions;
                var result    = [];
                if (n > 0 && response.fields > 0) {
                    while (completer.embedded_p) {
                        anchor    = $AFS_E.id_map [anchor.anchor_id];
                        completer = anchor.completer;
                    };
                    l = Math.min (response.fields, completer.names.length);
                    elem.completer.response = response;
                    for ( var i = 0, li = response.matches.length, match
                        ; i < li
                        ; i++
                        ) {
                        match = response.matches [i];
                        result.push
                            ( { index : i
                              , label :
                                  $.map (match.slice (0, l), bwrap).join ("")
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
                var anchor    = elem;
                var completer = elem.completer;
                var response  = completer.response;
                var match     = response.matches [item.index];
                var names     = completer.names.slice (0, response.fields);
                while (completer.embedded_p) {
                    anchor    = $AFS_E.id_map [elem.anchor_id];
                    completer = anchor.completer;
                };
                if (response.partial) {
                    _update_field_values (options, elem, match, names);
                    setTimeout
                        ( function () {
                            elem.inp$.autocomplete ("search");
                          }
                        , 1
                        );
                } else if (completer ["entity_p"]) {
                    if (! elem.completer.embedded_p) {
                        _update_field_values (options, elem, match, names);
                    };
                    data   =
                        { allow_new       : anchor.allow_new
                        , complete_entity : true
                        , fid             : anchor.anchor_id
                        , pid             : match [response.fields - 1]
                        , sid             : $AFS_E.root.value.sid
                        , trigger         : anchor.$id
                        , trigger_n       : elem.$id
                        };
                    $.gtw_ajax_2json
                        ( { async         : true
                          , data          : data
                          , success       : function (answer, status, xhr_i) {
                                _put_cb (options, anchor, answer, true);
                            }
                          , url           : options.completed_url
                          }
                        , "Completion"
                        );
                };
            };
            var _put_cb = function put_cb (options, elem, response, entity_p) {
                var anchor, s$;
                if (response.completions > 0) {
                    if ((response.completions == 1) && entity_p) {
                        anchor = $AFS_E.get (elem.anchor_id);
                        s$ = $("[id='" + response.json.$id + "']");
                        s$ = _response_replace (response, s$, anchor);
                        _setup_callbacks
                            ( s$, add_cb, cancel_cb, clear_cb, copy_cb
                            , delete_cb, edit_cb, save_cb
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
                            if ("inp$" in field) {
                                field.inp$.val (match [i]).trigger ("change");
                            };
                        };
                    };
                };
            };
            return function setup_completer (options, elem) {
                var ac, completer = elem.completer;
                if ("choices" in completer) {
                    elem.inp$.gtw_autocomplete
                        ( { minLength : completer.treshold
                          , source    : completer.choices
                          }
                        );
                } else {
                    elem.inp$.gtw_autocomplete
                        ( { focus    : function (event, ui) {
                                if (! elem.completer.embedded_p) {
                                    elem.inp$.val (ui.item.value);
                                };
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
                        , "html"
                        );
                };
            };
        } ();
        var _bind_click = function _bind_click (context) {
            var sel;
            for (var i = 1, li = arguments.length, arg; i < li; i++) {
                arg = arguments [i];
                sel = $(arg.$selector, context);
                sel.click (arg);
            }
        };
        var _clear_field = function _clear_field (elem) {
            var child, value = elem ["value"];
            if ("inp$" in elem) {
                elem.inp$.val ("");
            }
            if (value) {
                elem._clear_value ();
                if ("$child_ids" in value) {
                    for (var i = 0, li = value.$child_ids.length, child_id
                        ; i < li
                        ; i++
                        ) {
                        child_id = value.$child_ids [i];
                        child    = $AFS_E.get (child_id);
                        if (child) {
                            _clear_field (child);
                        };
                    };
                };
            };
        };
        var _cmds = function _cmds () {
            var map = options.menu_cmds, result = [];
            for (var i = 0, li = arguments.length, name; i < li; i++) {
                name = arguments [i];
                if (name in map) {
                    result.push
                        ( { callback : callback [name]
                          , label    : map      [name]
                          , name     : name
                          }
                        );
                } else {
                    alert ("Unknown command " + name);
                }
            };
            return result;
        } ;
        var _response_append = function _response_append
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
                    _setup_callbacks (s$, add_cb, cancel_cb, clear_cb, save_cb);
                } else {
                    alert ("Error: " + response.error);
                }
            }
        };
        var _response_replace = function _response_replace (response, s$, elem) {
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
        var _setup_callbacks = function _setup_callbacks (context) {
            _bind_click.apply (null, arguments);
            $(":input", context).each
                ( function (n) {
                    var inp$ = $(this);
                    var id     = inp$.attr ("id");
                    var elem   = $AFS_E.get (id);
                    elem.inp$  = inp$;
                    inp$.change (field_change_cb);
                    if ("completer" in elem) {
                        setup_completer (options, elem);
                    };
                  }
                );
            $(".cmd-menu", context).each
                ( function (n) {
                    _setup_cmd_menu ($(this));
                  }
                );
        };
        var _setup_cmd_menu = function _setup_cmd_menu (cmc$) {
            var s$     = cmc$.closest ("div[id],section");
            var id     = s$.attr    ("id");
            var elem   = $AFS_E.get (id);
            var source = cmd_menu [elem.type] (elem);
            var cmd    = source [0];
            var cb     = callback [cmd.name];
            var menu, drop_butt;
            $("<a class=\"default button\">")
                .append   (cmd.label)
                .appendTo (cmc$)
                .click    (cmd.callback);
            if (source.length > 1) {
                menu = $("<ul class=\"drop-menu\">");
                for (var i = 1, li = source.length, cmdi; i < li; i++) {
                    cmdi = source [i];
                    menu.append
                            ( $("<li>")
                                .append ( $("<a class=\"button\" href=\"#\">")
                                            .append (cmdi.label)
                                        )
                                .bind   ("cmd_menu_do", cmdi.callback);
                            )
                }
                drop_butt = $("<a class=\"drop button\">")
                    .append   ($("<i>"))
                    .appendTo (cmc$)
                    .click
                      ( function (ev) {
                          var menu = drop_butt.menu;
                          if (menu.element.is (":visible")) {
                              menu.element.hide ();
                          } else {
                              menu.element.show ()
                                  .position
                                    ( { my         : "right top"
                                      , at         : "right bottom"
                                      , of         : drop_butt
                                      , collision  : "none"
                                      }
                                    );
                          };
                        }
                      );
                drop_butt.menu = menu
                    .menu
                        ( { select    : function (event, ui) {
                                $(ui.item).trigger ("cmd_menu_do");
                            }
                          }
                        )
                    .appendTo (cmc$)
                    .css      ({ top: 0, left: 0, position : "absolute" })
                    .hide     ()
                    .zIndex   (cmc$.zIndex () + 1)
                    .data     ("menu");
            };
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
                    { _response_append (response, txt_status, p$, parent); }
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
                                  s$ = _response_replace (response, s$, elem);
                                  _bind_click
                                      ( s$
                                      , clear_cb, copy_cb, delete_cb, edit_cb
                                      );
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
        var clear_cb  = function clear_cb (ev) {
            var b$    = $(this);
            var s$    = b$.closest ("section");
            var id    = s$.attr    ("id");
            var elem  = $AFS_E.get (id);
            _clear_field (elem);
            $.getJSON
                ( options.expander_url
                , { fid       : id
                  , pid       : null
                  , sid       : $AFS_E.root.value.sid
                  , allow_new : elem.allow_new
                  }
                , function (response, txt_status) {
                      if (txt_status == "success") {
                          if (! response ["error"]) {
                              s$ = _response_replace (response, s$, elem);
                              _setup_callbacks
                                  ( s$, add_cb, cancel_cb, clear_cb, copy_cb
                                  , delete_cb, edit_cb, save_cb
                                  );
                          } else {
                              alert ("Error: " + response.error);
                          }
                      }
                  }
                );
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
                    { _response_append (response, txt_status, p$, elem); }
                );
        };
        var delete_cb = function delete_cb (ev) {
            var b$    = $(this);
            var s$    = b$.closest ("section");
            var id    = s$.attr    ("id");
            var elem  = $AFS_E.get (id);
            var value = elem ["value"];
            var pid   = value && value.edit.pid;
            if (pid !== undefined && pid !== "") {
                $.gtw_ajax_2json
                    ( { url         : options.deleter_url
                      , data        :
                          { fid     : id
                          , pid     : pid
                          , sid     : $AFS_E.root.value.sid
                          }
                      , success     : function (response, status) {
                            if (! response ["error"]) {
                                s$ = _response_replace (response, s$, elem);
                                _setup_callbacks
                                    ( s$, add_cb, cancel_cb, clear_cb, copy_cb
                                    , delete_cb, edit_cb, save_cb
                                    );
                            } else {
                                alert ("Error: " + response.error);
                            };
                        }
                      }
                    );
            };
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
                              s$ = _response_replace (response, s$, elem);
                              _setup_callbacks
                                  ( s$, add_cb, cancel_cb, clear_cb, copy_cb
                                  , delete_cb, edit_cb, save_cb
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
                                    s$ = _response_replace (response, s$, elem);
                                    _setup_callbacks
                                        ( s$
                                        , add_cb, cancel_cb, clear_cb, copy_cb
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
        var callback =
            { add                       : add_cb
            , cancel                    : cancel_cb
            , clear                     : clear_cb
            , copy                      : copy_cb
            , delete                    : delete_cb
            , edit                      : edit_cb
            , save                      : save_cb
            };
        var cmd_menu =
            { Entity                    : function cmd_menu_entity (elem) {
                  return _cmds ("save", "clear");
              }
            , Entity_Link               : function cmd_menu_entity_link (elem) {
                  var names = [];
                  if (elem.collapsed) {
                      names.push ("edit", "copy");
                  } else {
                      names.push ("save", "cancel", "clear");
                  };
                  if (elem.value.edit.pid) {
                      names.push ("delete");
                  }
                  return _cmds.apply (null, names);
              }
            , Entity_List               : function cmd_menu_entity_list (elem) {
                  return _cmds ("add");
              }
            , Field_Composite           : function cmd_menu_entity_list (elem) {
                  return _cmds ("clear");
              }
            , Field_Entity              : function cmd_menu_field_entity (elem) {
                  var names = [];
                  if (elem.collapsed) {
                      names.push ("edit");
                  } else {
                      names.push ("save", "cancel");
                  };
                  var names = ["clear"];
                  return _cmds.apply (null, names);
              }
            };
        options.form$       = this;
        add_cb.$selector    = ".add.button";
        cancel_cb.$selector = ".cancel.button";
        clear_cb.$selector  = ".clear.button";
        copy_cb.$selector   = ".copy.button";
        delete_cb.$selector = ".delete.button";
        edit_cb.$selector   = ".edit.button";
        save_cb.$selector   = ".save.button";
        _setup_callbacks
            (this, add_cb, clear_cb, copy_cb, delete_cb, edit_cb, save_cb);
        return this;
    };
  } (jQuery)
);

// __END__ GTW/jQ/afs.js
