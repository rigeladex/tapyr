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
//    23-Nov-2011 (CT) Creation continued (new_attr_filter, ...)
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
        var qr$   = $(this);
        var body$ = $("body").last ();
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
                        if ("children" in f) {
                            add (f.children, f.key, f.label);
                        };
                    };
                };
                add (qrs.filters);
                return result;
              } ()
            );
        var add_cb = function add_cb (ev) {
            var target = $(ev.target);
            var choice = target.data ("choice");
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
        var hide_menu_cb = function hide_menu_cb (ev) {
            var menu$ = $(".drop-menu"), tc;
            if (menu$.is (":visible")) {
                tc = $(ev.target).closest (".drop-menu");
                if (ev.keyCode === $.ui.keyCode.ESCAPE || ! tc.length) {
                    menu$.hide ();
                };
            };
        };
        var new_attr_filter = function new_attr_filter (choice) {
            var S = selectors;
            var key = choice.key + qrs.op_sep + "EQ"; // last-op ???
            // XXX choice.deep ....
            var result = options.attr_filter_html.clone (true);
            result.attr ("title", choice.label);
            $(S.attr_filter_label, result)
                .attr   ("for", key)
                .append (choice.label);
            $(S.attr_filter_op, result)
                .append ("==")   // last-op ???
                .attr ("title", "equal")
                .click  (op_cb); // XXX use 1 `delegate` instead of n `click`
            $(S.attr_filter_value, result)
                .attr ({ id : key, name : key });
            result.data ("choice", choice);
            return result;
        } ;
        var op_cb = function op_cb (ev) {
            console.info ("Op callback", ev);
            // TDB
        } ;
        var setup_menu = function setup_menu (but$, choices, cb) {
            var menu = $("<ul class=\"drop-menu cmd-menu\">");
            for (var i = 0, li = choices.length; i < li; i++) {
                ( function () {
                    var c = choices [i];
                    menu.append
                      ( $("<li>")
                          .append
                              ( $("<a class=\"button\" href=\"#\">")
                                  .append (c.label)
                                  .click
                                      ( function cmd_click (ev) {
                                          cb (ev);
                                          but$.data ("menu$").element.hide ();
                                        }
                                      )
                                  .data   ("choice", c)
                              )
                      );
                  } ()
                );
            }
            but$.click
                  ( function (ev) {
                      var menu = but$.data ("menu$");
                      if (menu.element.is (":visible")) {
                          menu.element.hide ();
                      } else {
                          menu.element.show ()
                              .position
                                ( { my         : "right top"
                                  , at         : "right bottom"
                                  , of         : but$
                                  , collision  : "none"
                                  }
                                )
                              .focus ();
                          if (ev && "stopPropagation" in ev) {
                              ev.stopPropagation ();
                          };
                      };
                    }
                  )
                .data
                  ( "menu$"
                  , menu.menu
                          ( { select    : function (event, ui) {
                                console.info ("Menu selection", event, ui);
                                var cmd$ = $(ui.item);
                                cmd$.trigger ("cmd_menu_do");
                              }
                            }
                          )
                        .appendTo (body$)
                        .css      ({ top: 0, left: 0, position : "absolute" })
                        .hide     ()
                        .zIndex   (but$.zIndex () + 1)
                        .data     ("menu")
                  );
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
                    setup_menu ($(this), attr_filters, add_cb);
                  }
                )
            .removeClass ("disabled");
        return this;
    }
  } (jQuery)
);

// __END__ GTW/jQ/query_restriction.js
