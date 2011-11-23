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
//    qGTW/jQ/uery_restriction.js
//
// Purpose
//    jQuery plugin for a query restriction form
//
// Revision Dates
//    22-Nov-2011 (CT) Creation
//    23-Nov-2011 (CT) Creation continued (new_attr_filter, op_map_by_sym, ...)
//    ««revision-date»»···
//--

"use strict";

( function ($, undefined) {
    $.fn.gtw_query_restriction = function (qrs, opts) {
        var selectors = $.extend
            ( { add_button            : "button[name=ADD]"
              , attrs_container       : "table.attrs"
              , attr_filter_container : "tr"
              , attr_filter_label     : "td.name label"
              , attr_filter_op        : "td.op a.button"
              , attr_filter_value     : "td.value input"
              , disabled_button       : "button[class=disabled]"
              , order_by_ui           : "input.ui-value[name=order_by]"
              , order_by_value        : "input.hidden[name=order_by]"
              , submit                : "[type=submit]"
              }
            , opts && opts ["selectors"] || {}
            );
        var options  = $.extend
            ( {}
            , opts || {}
            , { selectors : selectors }
            );
        var qr$    = $(this);
        var body$  = $("body").last ();
        var af_map = {};
        var attr_filters =
            ( function () {
                var result = [];
                var add = function add (filters, prefix, ui_prefix) {
                    for (var i = 0, li = filters.length, f; i < li; i++) {
                        f = filters [i];
                        if (prefix) {
                            f.key   = prefix    + qrs.name_sep + f.name;
                            f.label = ui_prefix + qrs.ui_sep   + f.ui_name;
                        } else {
                            f.key   = f.name;
                            f.label = f.ui_name;
                        };
                        result.push (f);
                        af_map [f.label] = f;
                        if ("children" in f) {
                            add (f.children, f.key, f.label);
                        };
                    };
                };
                add (qrs.filters);
                return result;
              } ()
            );
        var op_map_by_sym =
            ( function () {
                var result = {}, k, v;
                for (k in qrs.op_map) {
                    if (qrs.op_map.hasOwnProperty (k)) {
                        v              = qrs.op_map [k];
                        v.key          = k;
                        v.label        = v.sym;
                        result [v.sym] = v;
                    };
                };
                return result;
              } ()
            );
        var sig_map =
            ( function () {
                var result = {}, k, v;
                for (k in qrs.sig_map) {
                    if (qrs.sig_map.hasOwnProperty (k)) {
                        v = qrs.sig_map [k];
                        result [k] = $.map
                            ( v
                            , function (value) {
                                return qrs.op_map [value];
                              }
                            );
                    };
                };
                return result;
              } ()
            );
        var add_attr_filter_cb = function add_attr_filter_cb (ev) {
            var target$ = $(ev.target);
            var choice = target$.data ("choice");
            var afs$   = $(selectors.attr_filter_container, qr$);
            var head$  = afs$.filter
                ( function () {
                    return $(this).attr ("title") <= choice.label;
                  }
                );
            var nf$ = new_attr_filter (choice);
            if (head$.length) {
                head$.last ().after  (nf$);
            } else if (afs$.length) {
                afs$.first ().before (nf$);
            } else {
                $(selectors.attrs_container).append (nf$);
            };
            nf$.find (selectors.attr_filter_value).focus ();
        };
        var attach_menu = function attach_menu (but$, menu) {
            but$.click (menu_click_cb)
                .data  ("menu$", menu);
        };
        var hide_menu_cb = function hide_menu_cb (ev) {
            var menu$ = $(".drop-menu"), tc;
            if (menu$.is (":visible")) {
                tc = $(ev.target).closest (".drop-menu");
                if (ev.keyCode === $.ui.keyCode.ESCAPE || ! tc.length) {
                    menu$.hide ();
                };
            };
        };
        var menu_click_cb = function menu_click_cb (ev) {
            var but$ = $(ev.target);
            var menu = but$.data ("menu$");
            if (menu.element.is (":visible")) {
                menu.element.hide ();
            } else {
                menu.element
                    .show ()
                    .position
                      ( { my         : "right top"
                        , at         : "right bottom"
                        , of         : but$
                        , collision  : "none"
                        }
                      )
                    .zIndex (but$.zIndex () + 1)
                    .focus  ();
                if (ev && "stopPropagation" in ev) {
                    ev.stopPropagation ();
                };
            };
        };
        var menu_select_cb = function menu_select_cb (ev) {
            var target$ = $(ev.target);
            var menu$   = target$.closest (".cmd-menu");
            target$.data ("callback") (ev);
            menu$.hide ();
        };
        var new_attr_filter = function new_attr_filter (choice) {
            var S = selectors;
            var op  = op_map_by_sym ["=="] ; // last-op ???
            var key = choice.key + qrs.op_sep + op.key;
            // XXX choice.deep ....
            var result = options.attr_filter_html.clone (true);
            result.attr ("title", choice.label);
            $(S.attr_filter_label, result)
                .attr   ("for", key)
                .append (choice.label);
            $(S.attr_filter_op, result)
                .append (op.sym)
                .attr   ("title", op.desc)
                .each   (setup_op_button);
            $(S.attr_filter_value, result)
                .attr ({ id : key, name : key });
            result.data ("choice", choice);
            return result;
        };
        var new_menu = function new_menu (but$, choices, cb) {
            var menu = $("<ul class=\"drop-menu cmd-menu\">"), result;
            for (var i = 0, li = choices.length; i < li; i++) {
                ( function () {
                    var c = choices [i];
                    menu.append
                      ( $("<li>")
                          .append
                              ( $("<a class=\"button\" href=\"#\">")
                                  .append (c.label)
                                  .click  (menu_select_cb)
                                  .data
                                      ( { but$   : but$
                                        , callback : cb
                                        , choice : c
                                        }
                                      )
                              )
                      );
                  } ()
                );
            };
            result = menu
                .menu     ({})
                .appendTo (body$)
                .css      ({ top: 0, left: 0, position : "absolute" })
                .hide     ()
                .data     ("menu");
            return result;
        };
        var op_select_cb = function op_cb (ev) {
            var S = selectors;
            var target$ = $(ev.target);
            var choice  = target$.data  ("choice");
            var but$    = target$.data  ("but$");
            var afc$    = but$.closest (selectors.attr_filter_container);
            var label$  = $(S.attr_filter_label, afc$);
            var op$     = $(S.attr_filter_op,    afc$);
            var value$  = $(S.attr_filter_value, afc$);
            var name    = value$.attr ("name");
            var prefix  = name.split (qrs.op_sep) [0];
            var key     = prefix + qrs.op_sep + choice.key;
            label$.attr ("for", key);
            op$ .html   (choice.label)
                .attr   ("title", choice.desc);
            value$.attr ({ id : key, name : key});
        };
        var setup_op_button = function setup_op_button () {
            var but$ = $(this);
            var afc$ = but$.closest (selectors.attr_filter_container);
            var afs  = af_map  [afc$.attr ("title")];
            var ops  = sig_map [afs.sig_key];
            attach_menu (but$, new_menu (but$, ops, op_select_cb));
        };
        var tr_selector = function tr_selector (label) {
            var head = selectors.attr_filter_container, tail;
            if (label.length) {
                tail = "[title^='"+label+"']";
            } else {
                tail = "[title]";
            };
            return head + tail;
        };
        $(document)
            .bind ("click.menuhide", hide_menu_cb)
            .bind ("keyup.menuhide", hide_menu_cb);
        $(selectors.add_button)
            .each
                ( function () {
                    var but$ = $(this);
                    attach_menu
                      (but$, new_menu (but$, attr_filters, add_attr_filter_cb));
                  }
                )
            .removeClass ("disabled");
        $(selectors.attr_filter_op).each (setup_op_button);
        return this;
    }
  } (jQuery)
);

// __END__ GTW/jQ/query_restriction.js
