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
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    $.fn.gtw_mf3_form = function gtw_mf3_form (form_spec, opts) {
        var selectors = $.extend
            ( { container                : "div.Field"
              , entity_element           :
                  "fieldset.Entity[id], fieldset.Field-Entity[id], form[id]"
              , focusables               :
                  ".Field :input:not(:hidden):not(.prefilled)"
              , input_field              :
                  ".Field :input:not(:hidden):not(.prefilled)"
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
            var aid      = closest$.attr ("id");
            var pip      = closest$.prop ("id");
            return closest$.prop ("id");
        };
        var field_change_cb = function field_change_cb (ev) {
            var S         = options.selectors;
            var form_spec = options.form_spec;
            var f$        = $(this);
            var E_id      = closest_el_id (f$, S.entity_element);
            var F_id      = f$.prop ("id");
            var req       = f$.prop ("required");
            var l$        = $("label[for='" + F_id + "']");
            var b$        = $(S.status, l$);
            var mf3_value = form_spec.cargo.field_values [F_id];
            var checker   = form_spec.checkers [F_id];
            var status    = true;
            var ini_value, new_value;
            if (mf3_value !== undefined) {
                ini_value = mf3_value.init;
                if (f$.attr ("type") == "checkbox") {
                    new_value = f$.prop ("checked")
                        ? "yes" : (req ? null : "no");
                } else {
                    new_value = f$.val ();
                };
                if (! f$.hasClass ("display")) {
                    mf3_value.edit = new_value;
                    if (checker) {
                        status = checker (E_id, F_id, form_spec, mf3_value);
                    };
                };
                b$.toggleClass ("bad",  !  status)
                  .toggleClass ("good", !! status);
                f$.toggleClass ("bad",  !  status);
                if (req) {
                    b$.toggleClass ("missing", !  (new_value))
                      .toggleClass ("good",    !! (new_value && status));
                    f$.toggleClass ("missing", !  (new_value));
                };
            };
        };
        var _setup_callbacks = function _setup_callbacks (context) {
            var S         = options.selectors;
            $(S.input_field, context)
                .change  (field_change_cb)
                .trigger ("change")
                .filter  (".completer")
                    .each    (_setup_completer)
                    .end     ()
                .filter  (".Selector .display")
                    .each    (_setup_esf_selector)
                    .end     ();
            $(S.focusables, context)
                .addClass  ("focusable")
                .first     (":input")
                    .focus ();
        };
        var _setup_completer = function _setup_completer (n) {
            var f$        = $(this);
            var F_id      = f$.prop ("id");
            var completer = form_spec.completers [F_id];
            if ("choices" in completer) {
                f$.gtw_autocomplete
                    ( { minLength : completer.treshold
                      , source    : completer.choices
                      }
                    );
            } else {
                // XXX TBD;
            };
            if (completer.treshold === 0) {
                f$.focus
                    ( function (ev) {
                        if (f$.val () === "" && "autocomplete" in f$) {
                            f$.autocomplete ("search");
                        };
                      }
                    );
            };
        };
        var _setup_esf_selector = function _setup_esf_selector (n) {
            var S         = options.selectors;
            var form_spec = options.form_spec;
            var f$        = $(this);
            var E_id      = closest_el_id (f$, S.entity_element);
            var F_id      = f$.prop ("id");
            var mf3_value = form_spec.cargo.field_values [F_id];
            var s$        = f$.closest (S.container);
            var selector  = s$.data ("gtw_e_type_selector_mf3");
            var apply_cb  = function apply_cb (display, value) {
                f$.val (display).trigger ("change");
                if ( ! ("edit" in mf3_value)) {
                    mf3_value.edit = {};
                };
                mf3_value.edit.pid = value;
                if ("cid" in mf3_value.edit) {
                    delete mf3_value.edit.cid;
                };
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
                        $(":input, button, .cmd-button a", options.form$)
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
        this.delegate    (selectors.submit, "click", submit_cb);
        this.submit      (function (ev) { return false; });
        _setup_callbacks (this);
        return this;
    };
  } (jQuery)
);

// __END__ GTW/jQ/mf3.js
