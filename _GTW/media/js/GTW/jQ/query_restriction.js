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
//    26-Nov-2011 (CT) Creation continued...
//                     (setup_obj_list, GTW_buttonify, fix_buttons)
//    28-Nov-2011 (CT) Creation continued.... (order_by_cb, ...)
//    29-Nov-2011 (CT) Creation continued..... (order_by...)
//    30-Nov-2011 (CT) Creation continued...... (ev.delegateTarget)
//     5-Dec-2011 (CT) Creation continued....... (s/input/:input/ for selectors)
//     6-Dec-2011 (CT) Creation continued........ (use `gtw_ajax_2json`)
//    ««revision-date»»···
//--

"use strict";

( function ($, undefined) {
    $.fn.gtw_query_restriction = function (qrs, opts) {
        var icon_map  = $.extend
            ( { ADD            : "plusthick"
              , APPLY          : "check"
              , CANCEL         : "closethick"
              , CLEAR          : "trash"
              , FIRST          : "arrowthick-1-n"
              , LAST           : "arrowthick-1-s"
              , NEXT           : "arrowthick-1-e"
              , PREV           : "arrowthick-1-w"
              }
            , opts && opts ["icon_map"] || {}
            );
        var selectors = $.extend
            ( { add_button            : "button[name=ADD]"
              , apply_button          : "button[name=APPLY]"
              , ascending             : ".asc"
              , button                : "button[name]"
              , attr_filter_container : "tr"
              , attr_filter_disabler  : "td.disabler"
              , attr_filter_label     : "td.name label"
              , attr_filter_op        : "td.op a.button"
              , attr_filter_value     : "td :input.value"
              , attr_filter_ui_value  : "td :input.ui-value"
              , attrs_container       : "table.attrs"
              , cancel_button         : "button[name=CANCEL]"
              , clear_button          : "button[name=CLEAR]"
              , descending            : ".desc"
              , disabled_button       : "button[class=disabled]"
              , head_line             : "h1.headline"
              , limit                 : ":input[name=limit]"
              , object_container      : "table.Object-List"
              , offset                : ":input[name=offset]"
              , order_by_criteria     : "ul.criteria"
              , order_by_criterion    : "li"
              , order_by_direction    : ".direction"
              , order_by_disabler     : ".disabler"
              , order_by_display      : ":input.value.display[id=QR-order_by]"
              , order_by_proto        : "ul.prototype li"
              , order_by_value        : ":input.value.hidden[name=order_by]"
              , submit                : "[type=submit]"
              }
            , opts && opts ["selectors"] || {}
            );
        var options  = $.extend
            ( { asc_class             : "ui-icon-triangle-1-s"
              , desc_class            : "ui-icon-triangle-1-n"
              , sortable_class        : "ui-icon-arrowthick-2-n-s"
              }
            , opts || {}
            , { icon_map  : icon_map
              , selectors : selectors
              }
            );
        var qr$    = $(this);
        var body$  = $("body").last ();
        var af_map = {}, ob_widget$;
        var attr_filters =
            ( function () {
                var result = [];
                var name_sep = new RegExp (qrs.name_sep, "g");
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
                        f.order_by_key = f.key.replace (name_sep, ".");
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
                        v                = qrs.op_map [k];
                        v.key            = k;
                        result [v.sym]   = v;
                        result [v.label] = v;
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
            var target$ = $(ev.delegateTarget);
            var choice  = target$.data ("choice");
            var afs$    = $(selectors.attr_filter_container, qr$);
            var head$   = afs$.filter
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
                dis$.attr ("title", options.enabler_title)
                    .find (".button")
                        .addClass    ("ui-icon-plusthick")
                        .removeClass ("ui-icon-minusthick");
            } else {
                value$.removeProp ("disabled").focus ();
                dis$.attr ("title", options.disabler_title)
                    .find (".button")
                        .addClass    ("ui-icon-minusthick")
                        .removeClass ("ui-icon-plusthick");
            };
        };
        var fix_buttons = function fix_buttons (buttons) {
            var name, sel, value, old$, new$;
            for (name in buttons) {
                if (buttons.hasOwnProperty (name)) {
                    value = buttons [name];
                    sel   = selectors.add_button.replace ("ADD", name);
                    old$  = $(sel);
                    new$  = $(value);
                    old$.replaceWith (new$);
                };
            };
            $(selectors.button).gtw_buttonify
                (icon_map, options.buttonify_options);
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
            var but$ = $(ev.delegateTarget);
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
            var target$ = $(ev.delegateTarget);
            var menu$   = target$.closest (".cmd-menu");
            target$.data ("callback") (ev);
            menu$.hide ();
        };
        var new_attr_filter = function new_attr_filter (choice) {
            var S = selectors;
            var op  = op_map_by_sym ["=="] ; // last-op ???
            var key = choice.key + qrs.op_sep + op.key;
            var ajx = false;
            if (! ("attr_filter_html" in choice)) {
                $.gtw_ajax_2json
                    ( { async       : false
                      , data        :
                          { key     : key
                          }
                      , success     : function (response, status) {
                            if (! response ["error"]) {
                                if ("html" in response) {
                                  choice.attr_filter_html = $(response.html);
                                  choice.attr_filter_html
                                      .find (selectors.attr_filter_disabler)
                                          .each (setup_disabler);
                                  ajx = true;
                                } else {
                                  console.error ("Ajax Error", response);
                                }
                            } else {
                                console.error ("Ajax Error", response);
                            };
                        }
                      , url         : options.qx_af_html_url
                      }
                    , "Attribute filter"
                    );
                if (!ajx) {
                  return;
                };
            };
            var result = choice.attr_filter_html
                .clone (true)
                .data  ("choice", choice);
            update_attr_filter_op (result, op, key);
            $(S.attr_filter_op, result).each (setup_op_button);
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
            var target$ = $(ev.delegateTarget);
            var choice  = target$.data ("choice");
            var but$    = target$.data ("but$");
            var afc$    = but$.closest (S.attr_filter_container);
            var name    = value$.attr  ("name");
            var prefix  = name.split   (qrs.op_sep) [0];
            var key     = prefix + qrs.op_sep + choice.key;
            update_attr_filter_op (afc$, op, key);
        };
        var order_by =
            { cb              :
                { add_criterion : function add_criterion (ev) {
                      var S       = selectors;
                      var target$ = $(ev.delegateTarget);
                      var choice  = target$.data ("choice").label;
                      var c$      = order_by.new_criterion (choice);
                      var but$    = ob_widget$.find (S.add_button);
                      var menu$   = but$.data ("menu$").element;
                      ob_widget$.find (S.order_by_criteria).append (c$);
                      order_by.toggle_criteria (menu$, choice, "addClass");
                      ob_widget$.find (S.apply_button).focus ();
                  }
                , apply       : function apply (ev) {
                      var S     = selectors;
                      var crit$ = ob_widget$.find
                          (S.order_by_criteria + " " + S.order_by_criterion);
                      var displays = [], values = [];
                      crit$.each
                          ( function () {
                                var c$ = $(this);
                                var v$ = c$.find ("b");
                                if (! c$.hasClass ("disabled")) {
                                    var dir$  = c$.find (S.order_by_direction);
                                    var label = v$.html ();
                                    if (label) {
                                        var desc  = dir$.hasClass
                                            (options.desc_class);
                                        var sign  = desc ? "-" : "";
                                        var af    = af_map [label];
                                        displays.push (sign + label);
                                        values.push   (sign + af.order_by_key);
                                    };
                                };
                            }
                          )
                      $(S.order_by_display).val (displays.join (", "));
                      $(S.order_by_value)  .val (values.join   (", "));
                      order_by.cb.close ();
                      qr$.find (S.apply_button).focus ();
                  }
                , clear       : function clear (ev, ui) {
                      var S = selectors;
                      var but$    = ob_widget$.find (S.add_button);
                      var menu$   = but$.data ("menu$").element;
                      ob_widget$.find (S.order_by_criteria).empty ();
                      menu$.find ("a.button").removeClass ("ui-state-disabled");
                  }
                , close       : function close (ev) {
                      ob_widget$.dialog ("close");
                      order_by.cb.clear ();
                  }
                , dir         : function dir (ev) {
                      var S        = selectors;
                      var target$  = $(ev.target);
                      var crit$    = target$.closest (S.order_by_criterion);
                      var dir$     = crit$.find (S.order_by_direction);
                      order_by.toggle_dir (dir$);
                  }
                , disabler    : function disabler (ev) {
                      var S        = selectors;
                      var target$  = $(ev.target);
                      var crit$    = target$.closest (S.order_by_criterion);
                      var disabled = crit$.hasClass ("disabled");
                      var but$     = ob_widget$.find (S.add_button);
                      var menu$    = but$.data ("menu$").element;
                      var choice   = crit$.find ("b").html ();
                      if (! disabled) {
                          crit$.addClass ("disabled");
                          target$
                              .attr ("title", options.enabler_title)
                              .addClass    ("ui-icon-plusthick")
                              .removeClass ("ui-icon-minusthick");
                          order_by.toggle_criteria
                              (menu$, choice, "removeClass");
                      } else {
                          crit$.removeClass ("disabled");
                          target$
                              .attr ("title", options.disabler_title)
                              .addClass    ("ui-icon-minusthick")
                              .removeClass ("ui-icon-plusthick");
                          order_by.toggle_criteria
                              (menu$, choice, "addClass");
                      };
                      return false;
                  }
                , open        : function open (ev) {
                      var S       = selectors;
                      var target$ = $(ev.delegateTarget);
                      var li$     = target$.closest ("li");
                      var hidden$ = li$.find (selectors.order_by_value).last ();
                      var width   = qr$.width ();
                      var dialog;
                      if (ob_widget$ == null) {
                          ob_widget$ = order_by.setup_widget (target$);
                      };
                      order_by.cb.clear ();
                      order_by.prefill  (target$.val ().split (","));
                      ob_widget$
                          .dialog ("option", "width", width * 0.75)
                          .dialog ("open")
                          .dialog ("widget")
                              .position
                                  ( { my         : "top"
                                    , at         : "bottom"
                                    , of         : target$
                                    , collision  : "none"
                                    }
                                  );
                  }
                }
            , new_criterion     : function new_criterion (label, desc) {
                  var S      = selectors;
                  var result = ob_widget$.find (S.order_by_proto).clone (true);
                  var dir$;
                  result.find ("b").html (label);
                  if (desc) {
                      dir$ = result.find (S.order_by_direction);
                      order_by.toggle_dir (dir$);
                  };
                  return result;
              }
            , prefill           : function prefill (choices) {
                  var S       = selectors;
                  var crits$  = ob_widget$.find (S.order_by_criteria);
                  var but$    = ob_widget$.find (S.add_button);
                  var menu$   = but$.data ("menu$").element;
                  var c$, desc;
                  for (var i = 0, li = choices.length, choice; i < li; i++) {
                      choice = $.trim (choices [i]);
                      if (choice.length) {
                          desc = false;
                          if (choice [0] === "-") {
                              desc = true;
                              choice = choice.slice (1);
                          }
                          c$ = order_by.new_criterion (choice, desc);
                          crits$.append (c$);
                          order_by.toggle_criteria (menu$, choice, "addClass");
                      };
                  };
              }
            , setup             : function setup () {
                  var li$ = $(this).closest ("li");
                  li$.hd_input ({ callback : order_by.cb.open });
              }
            , setup_widget      : function setup_widget (but$) {
                  var S      = selectors;
                  var obf$   = options.order_by_form_html;
                  var result = obf$.dialog
                      ( { autoOpen : false
                        , title    : obf$.attr ("title")
                        }
                      );
                  result.find (S.order_by_proto)
                      .append
                          ( $("<a href=\"#\">")
                              .addClass
                                  ("button ui-icon " + options.sortable_class)
                              .css ("float", "right")

                          )
                      .attr ("title", options.order_by_sortable_title);
                  result.find (S.order_by_criteria).sortable
                      ( { close       : order_by.cb.clear
                        , distance    : 5
                        , placeholder : "ui-state-highlight"
                        }
                      );
                  result.find (S.button)
                      .gtw_buttonify (icon_map, options.buttonify_options);
                  result.find (S.add_button)
                      .each
                          ( function () {
                              var but$ = $(this);
                              attach_menu
                                ( but$
                                , new_menu
                                    ( but$
                                    , attr_filters, order_by.cb.add_criterion
                                    )
                                );
                            }
                          );
                  result.find (S.apply_button).click  (order_by.cb.apply);
                  result.find (S.cancel_button).click (order_by.cb.close);
                  result.find (S.clear_button).click  (order_by.cb.clear);
                  result.find (S.order_by_direction)
                      .addClass ("ui-icon " + options.asc_class)
                      .attr     ("title", options.order_by_asc_title);
                  result.find (S.order_by_disabler)
                      .addClass ("ui-icon ui-icon-minusthick")
                      .attr     ("title", options.disabler_title)
                      .click    (order_by.cb.disabler);
                  result.delegate
                      (S.order_by_criterion, "click", order_by.cb.dir);
                  return result;
              }
            , toggle_criteria   : function toggle_criteria (menu$, choice, toggler) {
                  var cl = choice.length;
                  menu$.find ("a.button").each
                      ( function () {
                          var a$ = $(this);
                          var label      = a$.html ();
                          var label_head = label.slice (0, cl);
                          var label_sep  = label [cl];
                          var match =
                              (  (cl <= label.length)
                              && (!label_sep)
                              || (label_sep === "/")
                              );
                          if (match && (choice === label_head)) {
                              a$ [toggler] ("ui-state-disabled");
                          };
                        }
                      );
              }
            , toggle_dir        : function toggle_dir (dir$) {
                  var old_class, new_class, title;
                  if (dir$.hasClass (options.asc_class)) {
                      old_class = options.asc_class;
                      new_class = options.desc_class;
                      title     = options.order_by_desc_title;
                  } else {
                      old_class = options.desc_class;
                      new_class = options.asc_class;
                      title     = options.order_by_asc_title;
                  };
                  dir$.removeClass (old_class)
                      .addClass    (new_class)
                      .attr        ("title", title);
              }
            };
        var setup_disabler = function setup_disabler () {
            var dis$ = $(this);
            dis$.append ($("<a class=\"button ui-icon ui-icon-minusthick\">"))
                .attr   ("title", options.disabler_title);
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
            if ("buttons" in response) {
                fix_buttons (response.buttons);
            };
            if ("setup_obj_list" in options) {
                options.setup_obj_list ();
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
            return false;
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
        var update_attr_filter_op = function update_attr_filter_op (afc$, op, key) {
            var S = selectors;
            $(S.attr_filter_label, afc$).attr ("for", key);
            $(S.attr_filter_value, afc$)
                .not (".hidden")
                    .attr ("id", key)
                    .end ()
                .not (".display")
                    .attr ("name", key);
            $(S.attr_filter_op,    afc$)
                .html (op.label || op.sym)
                .attr ("title", op.desc);
        };
        $(document)
            .bind ("click.menuhide", hide_menu_cb)
            .bind ("keyup.menuhide", hide_menu_cb);
        $(selectors.button).gtw_buttonify (icon_map, options.buttonify_options);
        $(selectors.add_button, qr$)
            .each
                ( function () {
                    var but$ = $(this);
                    attach_menu
                      (but$, new_menu (but$, attr_filters, add_attr_filter_cb));
                  }
                );
        $(selectors.attr_filter_op).each (setup_op_button);
        $(selectors.attr_filter_disabler).each (setup_disabler);
        $(selectors.attrs_container)
            .delegate (selectors.attr_filter_disabler, "click", disabler_cb);
        $(selectors.order_by_display).each (order_by.setup);
        qr$.delegate (selectors.submit, "click", submit_cb);
        return this;
    }
  } (jQuery)
);

// __END__ GTW/jQ/query_restriction.js
