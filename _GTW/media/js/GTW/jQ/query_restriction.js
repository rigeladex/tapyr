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
//    GTW/jQ/uery_restriction.js
//
// Purpose
//    jQuery plugin for a query restriction form
//
// Revision Dates
//    22-Nov-2011 (CT) Creation
//    23-Nov-2011 (CT) Creation continued (new_attr_filter, op_map_by_sym, ...)
//    24-Nov-2011 (CT) Creation continued.. (disabler_cb, submit_cb)
//    25-Nov-2011 (CT) Creation continued... (options.postifier)
//    ««revision-date»»···
//--

"use strict";

( function ($, undefined) {
    $.fn.gtw_query_restriction = function (qrs, opts) {
        var selectors = $.extend
            ( { add_button            : "button[name=ADD]"
              , attr_filter_container : "tr"
              , attr_filter_disabler  : "td.disabler"
              , attr_filter_label     : "td.name label"
              , attr_filter_op        : "td.op a.button"
              , attr_filter_value     : "td input.value"
              , attr_filter_ui_value  : "td input.ui-value"
              , attrs_container       : "table.attrs"
              , disabled_button       : "button[class=disabled]"
              , head_line             : "h1.headline"
              , limit                 : "input[name=limit]"
              , object_container      : "table.Object-List"
              , offset                : "input[name=offset]"
              , order_by_ui           : "input.ui-value[name=order_by]"
              , order_by_value        : "input.value[name=order_by]"
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
        var disabler_cb = function disabler_cb (ev) {
            var S = selectors;
            var afc$     = $(ev.target).closest (S.attr_filter_container);
            var dis$     = $(S.attr_filter_disabler, afc$);
            var value$   = $(S.attr_filter_value, afc$);
            var disabled = value$.prop ("disabled");
            if (! disabled) {
                value$.prop ("disabled", true);
                dis$.attr ("title", options.attr_filter_enabler_title)
                    .find (".button")
                        .addClass    ("ui-icon-plusthick")
                        .removeClass ("ui-icon-minusthick");
            } else {
                value$.removeProp ("disabled").focus ();
                dis$.attr ("title", options.attr_filter_disabler_title)
                    .find (".button")
                        .addClass    ("ui-icon-minusthick")
                        .removeClass ("ui-icon-plusthick");
            };
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
                hide_menu_cb (ev);
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
        var setup_disabler = function setup_disabler () {
            var dis$ = $(this);
            dis$.append ($("<a class=\"button ui-icon ui-icon-minusthick\">"))
                .attr   ("title", options.attr_filter_disabler_title);
        };
        var setup_op_button = function setup_op_button () {
            var but$ = $(this);
            var afc$ = but$.closest (selectors.attr_filter_container);
            var afs  = af_map  [afc$.attr ("title")];
            var ops  = sig_map [afs.sig_key];
            attach_menu (but$, new_menu (but$, ops, op_select_cb));
        };
        var submit_ajax_cb = function submit_ajax_cb (response) {
            var S = selectors;
            var of$ = $(S.offset);
            if ("object_container" in response) {
                $(S.object_container).last ().replaceWith
                    (response.object_container);
            };
            if ("head_line" in response) {
                $(S.head_line).html (response.head_line);
            };
            if ("limit" in response) {
                $(S.limit).val (response.limit);
            };
            if ("offset" in response) {
                $(S.offset).val (response.offset);
            };
            if ("postifier" in options) {
                options.postifier ();
            };
            $GTW.push_history (qr$.attr ("action") + "?" + qr$.serialize ());
        };
        var submit_cb = function submit_cb (ev) {
            var S = selectors;
            var target$ = $(ev.target);
            var form$   = target$.closest ($("form"));
            var args    = form$.serialize ()
                + "&" + this.name + "=" + this.value;
            $.getJSON (form$.attr ("action"), args, submit_ajax_cb);
            if (ev && ev.preventDefault) {
                ev.preventDefault ();
            };
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
        $(selectors.attr_filter_disabler).each (setup_disabler);
        options.attr_filter_html.find
            (selectors.attr_filter_disabler).each (setup_disabler);
        $(selectors.attrs_container)
            .delegate (selectors.attr_filter_disabler, "click", disabler_cb);
        qr$.delegate  (selectors.submit, "click", submit_cb);
        return this;
    }
  } (jQuery)
);

// __END__ GTW/jQ/query_restriction.js
