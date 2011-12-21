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
//    GTW/jQ/e_type_selector.js
//
// Purpose
//    jQuery plugin for selecting an specific instance of a MOM E_Type using
//    autocompletion
//
// Revision Dates
//    15-Dec-2011 (CT) Creation
//    16-Dec-2011 (CT) Cache `ajax_response`
//    21-Dec-2011 (CT) Set `title` in `apply_cb`
//    21-Dec-2011 (CT) Change `select_cb` to not repeat partial search after
//                     a single match
//    ««revision-date»»···
//--

"use strict";

( function ($, undefined) {
    var bwrap = function bwrap (v) {
        return "<b>" + v + "</b>";
    };
    $.fn.gtw_e_type_selector = function (opts) {
        var icons     = new $GTW.UI_Icon_Map (opts && opts ["icon_map"] || {});
        var selectors = $.extend
            ( { aid       : "[name=__attribute_selector_for__]"
              }
            , icons.selectors
            , opts && opts ["selectors"] || {}
            );
        var options  = $.extend
            ( { treshold  : 1
              }
            , opts || {}
            , { icon_map  : icons
              , selectors : selectors
              }
            );
        var ajax_response;
        var focus_cb = function focus_cb (ev) {
            var S       = options.selectors;
            var target$ = $(ev.delegateTarget);
            var key     = target$.prop ("id");
            var widget;
            var apply_cb = function apply_cb (ev) {
                var but$ = $(ev.delegateTarget);
                var hidden$, response;
                response = widget.data ("completed_response");
                if (response ["value"] && response ["display"]) {
                    hidden$ = target$.siblings
                        ("[name=\"" + key + "\"]").first ();
                    target$
                        .prop ("title", response.display)
                        .val  (response.display);
                    hidden$
                        .val  (response.value);
                    close_cb  (ev);
                    if ("esf_focusee" in options) {
                        options.esf_focusee.focus ();
                    };
                };
                return false;
            };
            var clear_cb = function clear_cb (ev) {
                widget.find (":input").not ("button, .hidden").each
                    ( function () {
                        $(this).val ("");
                      }
                    );
                widget.find (S.apply_button)
                    .button ("option", "disabled", true);
            };
            var close_cb = function close_cb (ev) {
                widget.dialog ("destroy");
            };
            var completed_cb = function completed_cb (inp$, response) {
                close_cb ();
                widget = setup_widget (response);
                widget
                    .data ("completed_response", response)
                    .find (S.apply_button)
                        .button ("option", "disabled", false);
            };
            var get_ccb = function get_ccb (inp$, term, cb, response) {
                var label;
                var l = response.fields - !response.partial; // skip pid
                var v = response.fields - 1;
                var result = [];
                inp$.data ("completer_response", response);
                if (response.completions > 0 && response.fields > 0) {
                    for ( var i = 0, li = response.matches.length, match
                        ; i < li
                        ; i++
                        ) {
                        match = response.matches [i];
                        label = $.map (match.slice (0, l), bwrap).join ("");
                        result.push
                            ( { index : i
                              , label : label
                              , value : match [v]
                              }
                            );
                    };
                };
                cb (result);
            };
            var get_completions = function get_completions (inp$, term, cb) {
                var aid      = widget.find (S.aid).val ();
                var trigger  = inp$.prop ("id");
                var values   = {}, n = 0;
                if (aid) {
                    widget.find (":input").not ("button, .hidden").each
                        ( function () {
                            var i$ = $(this);
                            var k  = i$.prop ("id");
                            var v  = i$.val  ();
                            if (k && v) {
                                values [k] = v;
                                n += 1;
                            };
                          }
                        );
                };
                if (n > 0) {
                    $.gtw_ajax_2json
                        ( { async         : true
                          , data          :
                              { aid       : aid
                              , entity_p  : true
                              , trigger   : trigger
                              , trigger_n : trigger
                              , values    : values
                              }
                          , success       : function (answer, status, xhr) {
                              if (! answer ["error"]) {
                                  get_ccb (inp$, term, cb, answer);
                              } else {
                                  console.error
                                      ("Ajax error", answer, data);
                              };
                            }
                          , url           : options.url.qx_esf_completer
                          }
                        , "Completion"
                        );
                };
            };
            var select_cb = function select_cb (ev, inp$, item) {
                var aid      = widget.find (S.aid).val ();
                var response = inp$.data ("completer_response");
                var trigger  = inp$.prop ("id");
                if (response.partial) {
                    inp$.val (item.value);
                    if (response.matches.length > 1) {
                        setTimeout
                            ( function () {
                                inp$.focus ();
                                inp$.autocomplete ("search");
                              }
                            , 1
                            );
                    } else {
                        inputs$.eq (item.index + 1).focus ();
                    };
                } else {
                    $.gtw_ajax_2json
                        ( { async         : true
                          , data          :
                              { aid       : aid
                              , pid       : item.value
                              }
                          , success       : function (answer, status, xhr) {
                                completed_cb (inp$, answer);
                            }
                          , url           : options.url.qx_esf_completed
                          }
                        , "Completion"
                        );
                }
            };
            var setup_widget = function setup_widget (response) {
                var result = $(response.html)
                    .dialog
                        ( { autoOpen : false
                          , close    : close_cb
                          }
                        );
                var form$ = result.is ("form") ? result : result.find ("form");
                var inputs$ = result.find (":input").not ("button, .hidden");
                result.find  (S.button)
                    .gtw_buttonify (icons, options.buttonify_options);
                result.find  (S.apply_button)
                    .button  ("option", "disabled", true)
                    .click   (apply_cb);
                result.find  (S.cancel_button).click (close_cb);
                result.find  (S.clear_button).click  (clear_cb);
                form$.submit (apply_cb);
                inputs$.each
                    ( function () {
                        var inp$ = $(this);
                        inp$.gtw_autocomplete
                            ( { focus     : function (event, ui) {
                                    return false;
                                }
                              , minLength : options.treshold
                              , select    : function (event, ui) {
                                    select_cb (event, inp$, ui.item);
                                    return false;
                                }
                              , source    : function (req, cb) {
                                    get_completions (inp$, req.term, cb);
                                }
                              }
                            , "html"
                            );
                      }
                    );
                result
                    .dialog ("option", "width", "auto")
                    .dialog ("open")
                    .dialog ("widget")
                        .position
                            ( { my         : "right top"
                              , at         : "right bottom"
                              , of         : target$
                              , collision  : "fit"
                              }
                            );
                inputs$.first ().focus ();
                return result;
            };
            if (!ajax_response) {
                $.gtw_ajax_2json
                    ( { async       : false
                      , data        :
                          { key     : key
                          }
                      , success     : function (response, status) {
                            if (! response ["error"]) {
                                if ("html" in response) {
                                    ajax_response = response;
                                } else {
                                  console.error ("Ajax Error", response);
                                }
                            } else {
                                console.error ("Ajax Error", response);
                            };
                        }
                      , url         : options.url.qx_esf
                      }
                    , "Entity completer"
                    );
            };
            if (ajax_response) {
                widget = setup_widget (ajax_response);
            };
            return false;
        };
        this.each
            ( function () {
                $(this).gtw_hd_input ({ callback : focus_cb });
              }
            );
        return this;
    }
  } (jQuery)
);

// __END__ GTW/jQ/e_type_selector.js
