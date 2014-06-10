// Copyright (C) 2014 Mag. Christian Tanzer All rights reserved
// Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
// #*** <License> ************************************************************#
// This software is licensed under the terms of either the
// MIT License or the GNU Affero General Public License (AGPL) Version 3.
// http://www.c-tanzer.at/license/mit_or_agpl.html
// #*** </License> ***********************************************************#
//
//++
// Name
//    GTW/jQ/mf3.js
//
// Purpose
//    Query plugin for MF3-forms
//
// Revision Dates
//    28-Apr-2014 (CT) Creation
//     3-May-2014 (CT) Ignore `input` elements with class `readonly`
//     9-May-2014 (CT) Add `completer`
//    10-May-2014 (CT) Change `completer.get_values` to use `cargo.field_values`
//    13-May-2014 (CT) Fix typos; bind `field_change_cb` after `completer.setup`
//    13-May-2014 (CT) Add argument `cargo` tp `completer.put_values`
//    14-May-2014 (CT) Change `completer.get_completions.success_cb` to
//                     handle `feedback`
//    15-May-2014 (CT) Factor `field_type` (`.checkbox`, `.id_ref`, `.normal`)
//    16-May-2014 (CT) Add support for `.Entity-Field .Display`
//    16-May-2014 (CT) Add `action_callback`
//    18-Jun-2014 (CT) Add `action_callback.add_rev_ref`;
//                     factor `setup_sub_form`
//    19-Jun-2014 (CT) Add `action_callback.remove`; DRY `setup_sub_form`
//    19-Jun-2014 (CT) Change `action_callback.close` to set `display` <input>
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    var bwrap  = function bwrap (v) {
        return "<b>" + v + "</b>";
    };

    $.fn.gtw_mf3_form = function gtw_mf3_form (form_spec, opts) {
        var field_map = {};
        var selectors = $.extend
            ( { closable                 : "section"
              , container                : "div.Field"
              , display_field            : ".Field.Display"
              , display_id_ref           : ".value.display.id_ref"
              , entity_list              : ".Entity-List"
              , form_element             : "form[id]"
              , focusables               :
                  ".Field :input[id]:not(:hidden):not(.prefilled):not(.readonly)"
              , hidden_id_ref            : ".value.hidden.id_ref"
              , input_field              :
                  ".Field :input[id]:not(.prefilled):not(.readonly)"
              , status                   : "b.Status"
              , submit                   : "[type=submit]"
              }
            , opts && opts ["selectors"] || {}
            );
        var options   = $.extend
            ( { pre_submit_callbacks : []
              , form_spec            : form_spec
              }
            , opts || {}
            , { selectors : selectors
              }
            );
        var closest_el_id = function closest_el_id (self, selector) {
            var closest$ = $(self).closest (selector);
            return closest$.prop ("id");
        };
        var action_callback =
            { add_rev_ref : function add_rev_ref (ev) {
                var S          = options.selectors;
                var a$         = $(this);
                var c$         = a$.closest (S.entity_list);
                var form_spec  = options.form_spec;
                var cargo      = form_spec.cargo;
                var F_id       = c$.prop ("id");
                var data       =
                    { sid             : cargo.sid
                    , sigs            : cargo.sigs
                    , trigger         : F_id
                    };
                var success_cb = function success_cb (answer, status, xhr) {
                    var new$;
                    if (! answer ["error"]) {
                        var fsu  = answer ["form_spec_update"];
                        var html = answer ["html"];
                        c$.append (html);
                        $GTW.inspect.update_transitive (form_spec, fsu);
                        new$ = c$.children ().last ();
                        setup_sub_form (new$);
                    } else {
                        $GTW.show_message
                            ("Ajax completion error: ", answer.error);
                    };
                };
                var url        = options.url.add_rev_ref;
                $.gtw_ajax_2json
                    ( { async         : true
                      , data          : data
                      , success       : success_cb
                      , url           : url
                      }
                    , "Add Rev_Ref"
                    );
              }
            , clear : function clear (ev) {
                var S     = options.selectors;
                var a$    = $(this);
                var c$    = a$.closest (S.closable);
                $(S.input_field, c$).each
                    ( function (n) {
                        var f$ = $(this);
                        var ft = f$.data ("field_type");
                        ft.clear (f$);
                      }
                    );
                return false;
              }
            , close : function close (ev) {
                var S     = options.selectors;
                var a$    = $(this);
                var c$    = a$.closest (S.closable);
                var d$    = $(S.display_id_ref, c$).first ();
                var d     = d$.attr ("value"); // want initial value here
                var fvs   = [];
                var acc   = function acc (n) {
                    var f$   = $(this);
                    var v    = f$.val ();
                    if (v !== "") {
                        fvs.push (v);
                    };
                };
                var fs$;
                if (d === "") {
                    fs$ = $(":input[id]:not(.prefilled):not(.display)", c$);
                    fs$.each (acc);
                    d$.val   (fvs.join (", "));
                };
                c$.addClass ("closed");
                return false;
              }
            , open : function open (ev) {
                var S     = options.selectors;
                var a$    = $(this);
                var c$    = a$.closest (S.closable);
                c$.removeClass ("closed");
                $(S.focusables, c$).first ().focus ();
                return false;
              }
            , remove : function remove (ev) {
                var S          = options.selectors;
                var a$         = $(this);
                var c$         = a$.closest (S.closable);
                var d$         = $(S.display_id_ref, c$).first ();
                var i$         = $(S.hidden_id_ref,  c$).first ();
                var elem_pid   = i$.val ();
                var form_spec  = options.form_spec;
                var cargo      = form_spec.cargo;
                var f_values   = cargo.field_values;
                var sigs       = cargo.sigs;
                var F_id       = d$.prop ("id");
                var url        = options.url.remove;
                var cleanup    = function cleanup (msg) {
                    delete f_values [elem_pid];
                    delete sigs     [elem_pid];
                    $(":input[id]", c$).each
                        ( function (n) {
                            var f$   = $(this);
                            var F_id = f$.prop ("id");
                            delete f_values [F_id];
                            delete sigs     [F_id];
                          }
                        );
                    if (msg) {
                        c$.html (msg);
                    } else {
                        c$.remove ();
                    };
                };
                var data, success_cb;
                if (elem_pid !== "") {
                    data       =
                        { elem_pid : elem_pid
                        , form_pid : cargo.pid
                        , sid      : cargo.sid
                        , sigs     : sigs
                        , trigger  : F_id
                        }
                    success_cb = function success_cb (answer, status, xhr) {
                        if (! answer ["error"]) {
                            cleanup (answer ["html"]);
                        } else {
                            $GTW.show_message
                                ("Ajax completion error: ", answer.error);
                        };
                    };
                    $.gtw_ajax_2json
                        ( { async         : true
                          , data          : data
                          , success       : success_cb
                          , url           : url
                          }
                        , "Remove"
                        );
                } else {
                    cleanup ();
                };
                return false;
              }
            , reset : function reset (ev) {
                var S     = options.selectors;
                var a$    = $(this);
                var c$    = a$.closest (S.closable);
                $(S.input_field, c$).each
                    ( function (n) {
                        var f$ = $(this);
                        var ft = f$.data ("field_type");
                        ft.reset (f$);
                      }
                    );
                return false;
              }
            };
        var completer =
            { completed_cb : function completed_cb
                    (f$, f_completer, response, entity_p, cargo) {
                if (response.completions > 0) {
                    if (response.fields > 0) {
                        completer.put_values (response, response.values, cargo);
                    };
                    if ((response.completions == 1) && entity_p) {
                        action_callback.close.apply (f$);
                        // TBD (cf. afs.js: _put_cb)
                        // * move focus to following focusable <input>
                    };
                };
              }
            , get_completions : function get_completions
                    (f$, request, response_cb) {
                var F_id         = f$.prop ("id");
                var c_id         = f$.data ("completer");
                var form_spec    = options.form_spec;
                var f_completer  = form_spec.completers [c_id];
                var field_values = completer.get_values (f_completer);
                var data         =
                    { complete_entity : f_completer ["entity_p"] || false
                    , field_values    : field_values
                    , sid             : form_spec.cargo.sid
                    , sigs            : form_spec.cargo.sigs
                    , trigger         : F_id
                    };
                var success_cb = function success_cb (answer, status, xhr) {
                    if (! answer ["error"]) {
                        if (answer.completions > 0 && answer.fields > 0) {
                            completer.get_completions_cb
                                (f$, request, response_cb, f_completer, answer);
                        } else if ("feedback" in answer) {
                            response_cb
                                ( [ { disabled : true
                                    , index    : null
                                    , label    : answer.feedback
                                    , value    : null
                                    }
                                  ]
                                );
                        } else {
                            response_cb ([]);
                        };
                    } else {
                        $GTW.show_message
                            ("Ajax completion error: ", answer.error);
                    };
                };
                // current value not in form_spec.cargo.field_values yet
                field_values [F_id] = f$.val ();
                $.gtw_ajax_2json
                    ( { async         : true
                      , data          : data
                      , success       : success_cb
                      , url           : options.url.completer
                      }
                    , "Completion"
                    );
              }
            , get_completions_cb : function get_completions_cb
                    (f$, request, response_cb, f_completer, answer) {
                var l, n   = answer.completions;
                var rl     = answer.fields -
                    (f_completer ["entity_p"] && ! answer.partial); // skip pid
                var v      = answer.fields - 1;
                var result = [];
                if (n > 0 && answer.fields > 0) {
                    l = Math.min (rl, f_completer.fields.length);
                    f$.data ("gtw_mf3_completer_response", answer);
                    for ( var i = 0, li = answer.matches.length, match
                        ; i < li
                        ; i++
                        ) {
                        match = answer.matches [i];
                        result.push
                            ( { index : i
                              , label :
                                  $.map (match.slice (0, l), bwrap).join ("")
                              , value : match [v]
                              }
                            );
                    };
                };
                response_cb (result);
              }
            , get_values : function get_values (f_completer) {
                var fields = f_completer.fields;
                var values = form_spec.cargo.field_values;
                var result = {};
                var id, f$, ft, fv, val;
                for (var i = 0, li = fields.length; i < li; i++) {
                    id = fields [i];
                    fv = values [id];
                    if (fv != undefined) {
                        f$  = field_map [id];
                        ft  = f$.data   ("field_type");
                        val = ft.get_cargo (fv);
                        if (val != undefined) {
                            result [id] = val;
                        };
                    };
                };
                return result;
              }
            , put_values : function put_values (response, match, cargo) {
                var f$, ft, fv, id, val;
                var values = cargo.field_values;
                for (var i = 0, li = response.field_ids.length; i < li; i++) {
                    id   = response.field_ids [i];
                    f$   = $("[id=\"" + id + "\"]");
                    val  = match [i];
                    if (f$.length) {
                        ft = f$.data ("field_type");
                        ft.put_input (f$, val);
                    } else {
                        fv = values [id];
                        if (fv != undefined) {
                            fv.edit = val;
                        };
                    };
                };
              }
            , select_cb : function select_cb (ev, f$, item) {
                var data;
                var F_id         = f$.prop ("id");
                var c_id         = f$.data ("completer");
                var form_spec    = options.form_spec;
                var cargo        = form_spec.cargo;
                var f_completer  = form_spec.completers [c_id];
                var response     = f$.data ("gtw_mf3_completer_response");
                var match        = response.matches [item.index];
                var success_cb = function success_cb (answer, status, xhr) {
                    completer.completed_cb
                        (f$, f_completer, answer, true, cargo);
                };
                completer.put_values (response, match, cargo);
                if (response.partial) {
                    setTimeout (function () { completer.trigger (f$); }, 1);
                } else if (f_completer ["entity_p"]) {
                    data  =
                        { complete_entity : true
                        , field_values    : completer.get_values (f_completer)
                        , pid             : item.value
                        , sid             : cargo.sid
                        , sigs            : cargo.sigs
                        , trigger         : F_id
                        };
                    $.gtw_ajax_2json
                        ( { async         : true
                          , data          : data
                          , success       : success_cb
                          , url           : options.url.completed
                          }
                        , "Completion"
                        );
                };
              }
            , setup : function setup (n) {
                var f$           = $(this);
                var F_id         = f$.prop ("id");
                var c_id         = f$.data ("completer");
                var form_spec    = options.form_spec;
                var f_completer  = form_spec.completers [c_id];
                if ("choices" in f_completer) {
                    f$.gtw_autocomplete
                        ( { minLength : f_completer.treshold
                          , source    : f_completer.choices
                          }
                        );
                } else {
                    f$.gtw_autocomplete
                        ( { focus    : function (ev, ui) {
                                return false;
                            }
                          , minLength : f_completer.treshold
                          , select    : function (ev, ui) {
                                completer.select_cb (ev, f$, ui.item);
                                return false;
                            }
                          , source    : function (request, response_cb) {
                                completer.get_completions
                                    (f$, request, response_cb);
                            }
                          }
                        , "html"
                        );
                };
                if (f_completer.treshold === 0) {
                    f$.focus (completer.trigger_auto_cb);
                };
              }
            , trigger : function trigger (f$) {
                f$.focus ();
                return f$.autocomplete ("search");
              }
            , trigger_auto_cb : function trigger_auto_cb (ev) {
                var f$ = $(this);
                if (f$.val () === "") {
                    f$.autocomplete ("search");
                };
              }
            };
        var entity_display_open_cb = function entity_display_open_cb (ev) {
            var k = ev.which;
                // Unicode value of key pressed
                //   8     backspace
                //   9     tab
                //  10     new line
                //  13     carriage return
                //  27     escape
                // 127     delete
            if (k >= 9 && k <= 27) {
                return true;
            };
            action_callback.open.apply (this, ev);
            if (k in {8 : 1, 127:1}) {
                action_callback.clear.apply (this, ev);
            };
            return false;
        };
        var field_change_cb = function field_change_cb (ev) {
            var S         = options.selectors;
            var form_spec = options.form_spec;
            var f$        = $(this);
            var ft        = f$.data ("field_type");
            var E_id      = closest_el_id (f$, S.form_element);
            var F_id      = f$.prop ("id");
            var req       = f$.prop ("required");
            var l$        = $("label[for='" + F_id + "']");
            var b$        = $(S.status, l$);
            var mf3_value = form_spec.cargo.field_values [F_id];
            var checker   = form_spec.checkers [F_id];
            var status    = true;
            var ini_value, new_value, new_value_p;
            if (mf3_value !== undefined) {
                ini_value      = mf3_value.init;
                new_value      = ft.get_input (f$);
                mf3_value.edit = new_value;
                if (checker) {
                    status = checker (E_id, F_id, form_spec, mf3_value);
                };
                b$.toggleClass ("bad",  !  status)
                  .toggleClass ("good", !! status);
                f$.toggleClass ("bad",  !  status);
                if (req) {
                    new_value_p = ft.truth (new_value);
                    b$.toggleClass ("missing", !  (new_value_p))
                      .toggleClass ("good",    !! (new_value_p && status));
                    f$.toggleClass ("missing", !  (new_value_p));
                };
            };
        };
        var field_type =
            { checkbox   :
                { clear : function clear (f$) {
                    field_type.checkbox.put_input (f$, "");
                  }
                , get_cargo : function get_cargo_checkbox (fv) {
                    return field_type.normal.get_cargo (fv);
                  }
                , get_input : function get_input_checkbox (f$) {
                    var req    = f$.prop ("required");
                    var result = f$.prop ("checked")
                        ? "yes" : (req ? null : "no");
                    return result;
                  }
                , put_cargo : function put_cargo_id_ref (id, value) {
                    field_type.normal.put_cargo (id, value);
                  }
                , put_input : function put_input_checkbox (f$, value) {
                    // XXX ??? is this correct ???
                    f$.val ((value == "yes") ? true : false).trigger ("change");
                  }
                , reset : function reset (f$) {
                    field_type.normal.reset (f$);
                  }
                , truth : function truth_checkbox (value) {
                    return field_type.normal.truth (value);
                  }
                }
            , id_ref :
                { clear : function clear (f$) {
                    field_type.id_ref.put_input (f$, {});
                  }
                , get_cargo : function get_cargo_id_ref (fv) {
                    var edit   = fv ["edit"];
                    var init   = fv ["init"];
                    var result = edit || init;
                    if (result) {
                        result = result.pid;
                    };
                    return result;
                  }
                , get_input : function get_input_id_ref (f$) {
                    var h$ = f$.siblings (".value.hidden.id_ref");
                    var result =
                        { display : f$.val ()
                        , pid     : h$.val ()
                        };
                    return result;
                  }
                , put_cargo : function put_cargo_id_ref (id, value) {
                    if (typeof value === "object") {
                        field_type.normal.put_cargo (id, value);
                    };
                  }
                , put_input : function put_input_id_ref (f$, value) {
                    var h$ = f$.siblings (".value.hidden.id_ref");
                    var id = f$.prop ("id");
                    var fv, pid;
                    if (typeof value === "object") {
                        pid = value ["pid"];
                        h$.val (pid);
                        f$.val (value ["display"] || "");
                        if (pid !== undefined) {
                            field_type.normal.put_cargo (id, value);
                        } else {
                            fv      = form_spec.cargo.field_values [id];
                            fv.edit = undefined;
                        };
                    } else {
                        h$.val (value);
                    };
                  }
                , reset : function reset (f$) {
                    field_type.normal.reset (f$);
                  }
                , truth : function truth_checkbox (value) {
                    if (typeof value === "object") {
                        return !! (value ["pid"])
                    } else {
                        return !! value;
                    };
                  }
                }
            , normal :
                { clear : function clear (f$) {
                    field_type.normal.put_input (f$, "");
                  }
                , get_cargo : function get_cargo_normal (fv) {
                    var edit   = fv ["edit"];
                    var init   = fv ["init"];
                    var result = (edit !== undefined) ? edit : init;
                    if (edit === "" && edit === init) {
                        result = undefined;
                    };
                    return result;
                  }
                , get_input : function get_input_normal (f$) {
                    return f$.val ();
                  }
                , put_cargo : function put_cargo_normal (id, value) {
                    var fv = form_spec.cargo.field_values [id];
                    if (fv != undefined) {
                        fv.edit = value;
                    };
                  }
                , put_input : function put_input_normal (f$, value) {
                    f$.val (value).trigger ("change");
                  }
                , reset : function reset (f$) {
                    var id = f$.prop ("id");
                    var fv = form_spec.cargo.field_values [id];
                    field_type.normal.put_input (f$, fv.init);
                  }
                , truth : function truth_checkbox (value) {
                    return !! value;
                  }
                }
            , _setup : function _classify (n) {
                var f$ = $(this);
                var id = f$.prop ("id");
                var typ;
                if (f$.attr ("type") == "checkbox") {
                    typ = field_type.checkbox;
                } else if (f$.is (".id_ref")) {
                    typ = field_type.id_ref;
                } else {
                    typ = field_type.normal;
                };
                f$.data ("field_type", typ);
                field_map [id] = f$;
              }
            };
        var setup_entity_display = function setup_entity_display (n) {
            var S  = options.selectors;
            var f$ = $(this);
            var s$ = f$.closest (S.container);
            s$.gtw_hd_input
                ( { callback      : entity_display_open_cb
                  , trigger_event : "click keydown"
                  }
                );
        };
        var setup_esf_selector = function setup_esf_selector (n) {
            var S         = options.selectors;
            var f$        = $(this);
            var E_id      = closest_el_id (f$, S.form_element);
            var F_id      = f$.prop ("id");
            var s$        = f$.closest (S.container);
            var selector  = s$.data ("gtw_e_type_selector_mf3");
            var apply_cb  = function apply_cb (display, value) {
                field_type.id_ref.put_input
                    (f$, { display : display, pid : value});
            };
            if (! selector) {
                s$.gtw_e_type_selector_hd_mf3
                    ( { mf3 :
                          { apply_cb  : apply_cb
                          , E_id      : E_id
                          , F_id      : F_id
                          }
                      , url : options.url
                      }
                    );
            };
        };
        var setup_fields = function setup_fields (context) {
            var S = options.selectors;
            $(S.display_field, context)
                .each    (setup_entity_display);
            $(S.input_field, context)
                .each    (field_type._setup)
                .filter  ("[data-completer]")
                    .each    (completer.setup)
                    .end     ()
                .filter  (".Selector .display")
                    .each    (setup_esf_selector)
                    .end     ()
                .change  (field_change_cb)
                .trigger ("change");
            $(S.focusables, context)
                .addClass  ("focusable")
                .first     (":input")
                    .focus ();
        };
        var setup_sub_form = function setup_sub_form (f$) {
            var action;
            setup_fields (f$);
            for (action in action_callback) {
                if (action_callback.hasOwnProperty (action)) {
                    $("[data-action=\"" + action + "\"]", f$)
                        .on ("click", action_callback [action]);
                };
            };
        };
        var submit_cb = function submit_cb (ev) {
            var form$        = options.form$;
            var target$      = $(ev.target);
            var form_spec    = options.form_spec;
            var name         = target$.prop ("name");
            var url          = form$.prop ("action") || document.URL;
            var json_data    =
                { cancel : (name == "cancel")
                , cargo  : form_spec.cargo
                , next   : options.url.next
                };
            var pre_submit_callbacks = options.pre_submit_callbacks;
            var success_cb = function success_cb (answer, status, xhr) {
                if (! answer ["error"]) {
                    if (answer ["conflicts"]) {
                        // XXX
                        $GTW.show_message
                            ("Submit conflicts", answer.conflicts);
                    } else if (answer ["errors"]) {
                        $GTW.show_message ("Submit errors: ", answer.errors);
                        // XXX _display_error_map (answer.errors);
                    } else if (answer ["expired"]) {
                        // XXX display re-authorization form
                        $GTW.show_message ("Expired: ", answer.expired);
                    } else if (answer ["feedback"]) {
                        $(":input, button, .action-button a", options.form$)
                            .addClass ("ui-state-disabled") // ???
                            .prop     ("disabled", true);
                        options.form$.before (answer.feedback);
                    } else {
                        // Need timeout here for IE
                        setTimeout
                            ( function () {
                                window.location.href = options.url.next;
                              }
                            , 0
                            );
                    };
                } else {
                    $GTW.show_message ("Submit error: ", answer ["error"]);
                };
            };
            json_data [name] = true;
            if (ev && "preventDefault" in ev) {
                ev.preventDefault ();
            };
            for (var i = 0, li = pre_submit_callbacks.length; i < li; i++) {
                pre_submit_callbacks [i] ();
            };
            $.gtw_ajax_2json
                ( { url         : url
                  , data        : json_data
                  , success     : success_cb
                  }
                , "Submit"
                );
            return false;
        };
        options.form$ = this;
        // bind `submit_cb` to `click` of submit buttons (need button name)
        // disable `submit` event for form to avoid IE to do normal form
        // submit after running `submit_cb`
        this.delegate  (selectors.submit, "click", submit_cb);
        this.submit    (function (ev) { return false; });
        setup_sub_form (this);
        return this;
    };
  } (jQuery)
);

// __END__ GTW/jQ/mf3.js
