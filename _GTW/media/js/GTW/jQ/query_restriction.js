// Copyright (C) 2011-2012 Mag. Christian Tanzer All rights reserved
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
//    24-Nov-2011 (CT) Creation continued (disabler_cb, submit_cb)
//    26-Nov-2011 (CT) Creation continued
//                     (setup_obj_list, GTW_buttonify, fix_buttons)
//    28-Nov-2011 (CT) Creation continued (order_by_cb, ...)
//    29-Nov-2011 (CT) Creation continued (order_by...)
//    30-Nov-2011 (CT) Creation continued (ev.delegateTarget)
//     5-Dec-2011 (CT) Creation continued (s/input/:input/ for selectors)
//     6-Dec-2011 (CT) Creation continued (use `gtw_ajax_2json`
//                     [qx_af_html_url, qx_obf_url],
//                     `active_menu_but_class`, `adjust_op_menu`)
//     7-Dec-2011 (CT) Creation continued (`response.callbacks`)
//     7-Dec-2011 (CT) Creation continued (reorganize `options`)
//    12-Dec-2011 (CT) Creation continued (start `setup_completer`)
//    13-Dec-2011 (CT) Creation continued (continue `setup_completer`)
//    15-Dec-2011 (CT) Creation continued (use `$GTW.UI_Icon_Map`,
//                     `.toggleClass`)
//    16-Dec-2011 (CT) Creation continued (factor e_type_selector.js)
//    22-Dec-2011 (CT) s/children/attrs/ (in `attr_filters`)
//    16-Jan-2012 (CT) Creation continued (`attr_select`)
//    17-Jan-2012 (CT) Creation continued (add `focus` to `op_select_cb`)
//    ««revision-date»»···
//--

"use strict";

( function ($, undefined) {
    $.fn.gtw_query_restriction = function (qrs, opts) {
        var icons     = new $GTW.UI_Icon_Map (opts && opts ["icon_map"] || {});
        var selectors = $.extend
            ( { ascending                : ".asc"
              , attr_filter_container    : "tr"
              , attr_filter_disabler     : "td.disabler"
              , attr_filter_label        : "td.name label"
              , attr_filter_op           : "td.op a.button"
              , attr_filter_value        : "td :input.value"
              , attr_filter_value_entity : "td.value.Entity"
              , attrs_container          : "table.attrs"
              , descending               : ".desc"
              , disabled_button          : "button[class=disabled]"
              , disabler                 : ".disabler"
              , head_line                : "h1.headline"
              , limit                    : ":input[name=limit]"
              , object_container         : "table.Object-List"
              , offset                   : ":input[name=offset]"
              , order_by_criteria        : "ul.attributes"
              , order_by_criterion       : "li"
              , order_by_direction       : ".direction"
              , order_by_display         : ":input.value.display[id=QR-order_by]"
              , order_by_value           : ":input.value.hidden[name=order_by]"
              , prototype                : "ul.prototype li"
              , select_attr_attributes   : "ul.attributes"
              , select_attr_item         : "li"
              , select_attr_value        : ":input.value.hidden[name=fields]"
              , submit                   : "[type=submit]"
              }
            , icons.selectors
            , opts && opts ["selectors"] || {}
            );
        var ui_class = $.extend
            ( { active_menu_button    : "active-menu-button"
              , disable               : icons.ui_class ["DISABLE"]
              , enable                : icons.ui_class ["ENABLE"]
              , sort_asc              : icons.ui_class ["SORT_ASC"]
              , sort_desc             : icons.ui_class ["SORT_DESC"]
              }
            , opts && opts ["ui_class"] || {}
            );
        var options  = $.extend
            ( { treshold  : 0
              }
            , opts || {}
            , { icon_map  : icons
              , selectors : selectors
              , ui_class  : ui_class
              }
            );
        var qr$    = $(this);
        var body$  = $("body").last ();
        var af_map = {};
        var as_widget$, ob_widget$;
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
                        f.q_name          = f.key.replace (name_sep, ".");
                        f.ops_selected    = [];
                        af_map [f.label]  = f;
                        af_map [f.q_name] = f;
                        result.push (f);
                        if ("attrs" in f) {
                            add (f.attrs, f.key, f.label);
                        };
                    };
                };
                add (qrs.filters);
                return result;
              } ()
            );
        var op_map_by_sym =
            ( function () {
                var result = {}, k, v, label;
                for (k in qrs.op_map) {
                    if (qrs.op_map.hasOwnProperty (k)) {
                        v              = qrs.op_map [k];
                        v.key          = k;
                        // if label contains stuff like `&ge;` we need to
                        // run it through `html` because we'll later want
                        // to look up `but$.html ()` in `op_map_by_sym`
                        label          = $("<a>").append (v.label).html ();
                        result [v.sym] = v;
                        result [label] = v;
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
            var S       = options.selectors;
            var target$ = $(ev.delegateTarget);
            var choice  = target$.data ("choice");
            var afs$    = $(S.attr_filter_container, qr$);
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
                $(S.attrs_container).append (nf$);
            };
            $(S.attr_filter_value, nf$).focus ();
            setup_esf (nf$);
        };
        var adjust_op_menu = function adjust_op_menu (afs) {
            var menu$ = afs.ops_menu$;
            menu$.element.find ("a.button").each
                ( function () {
                    var a$    = $(this);
                    var label = a$.html ();
                    var map   = afs.ops_selected;
                    var op    = op_map_by_sym [label];
                    a$.toggleClass ("ui-state-disabled", !! map [op.sym]);
                  }
                );
        };
        var attach_menu = function attach_menu (but$, menu) {
            but$.click (menu_click_cb)
                .data  ("menu$", menu);
        };
        var attr_select =
            { cb              :
                { add         : function add (ev) {
                      var S       = options.selectors;
                      var target$ = $(ev.delegateTarget);
                      var choice  = target$.data ("choice").label;
                      var c$      = attr_select.new_attr (choice);
                      var but$    = as_widget$.find (S.add_button);
                      var menu$   = but$.data ("menu$").element;
                      as_widget$.find    (S.select_attr_attributes).append (c$);
                      attr_select.toggle (menu$, choice, true);
                      as_widget$.find    (S.apply_button).focus ();
                  }
                , apply       : function apply (ev) {
                      var S      = options.selectors;
                      var attrs$ = as_widget$.find
                          (S.select_attr_attributes + " " + S.select_attr_item);
                      var values = [];
                      attrs$.each
                          ( function () {
                                var a$ = $(this);
                                var v$ = a$.find ("b");
                                if (! a$.hasClass ("disabled")) {
                                    var label = v$.html ();
                                    if (label) {
                                        var af = af_map [label];
                                        values.push (af.q_name);
                                    };
                                };
                            }
                          )
                      $(S.select_attr_value).val (values.join   (", "));
                      attr_select.cb.close ();
                      qr$.find (S.apply_button).focus ();
                  }
                , clear       : function clear (ev, ui) {
                      var S = options.selectors;
                      var but$    = as_widget$.find (S.add_button);
                      var menu$   = but$.data ("menu$").element;
                      as_widget$.find (S.select_attr_attributes).empty ();
                      menu$.find ("a.button").removeClass ("ui-state-disabled");
                  }
                , close       : function close (ev) {
                      as_widget$.dialog ("close");
                      attr_select.cb.clear ();
                  }
                , disabler    : function disabler (ev) {
                      var S        = options.selectors;
                      var target$  = $(ev.target);
                      var attr$    = target$.closest (S.select_attr_item);
                      var disabled = attr$.hasClass  ("disabled");
                      var but$     = as_widget$.find (S.add_button);
                      var menu$    = but$.data ("menu$").element;
                      var choice   = attr$.find ("b").html ();
                      var title    = disabled ?
                          options.title.disabler : options.title.enabler;
                      attr$.toggleClass ("disabled", !disabled);
                      target$
                          .attr        ("title", title)
                          .toggleClass (options.ui_class.enable,  !disabled)
                          .toggleClass (options.ui_class.disable,  disabled);
                      attr_select.toggle (menu$, choice, disabled);
                      return false;
                  }
                , open        : function open (ev) {
                      var S       = options.selectors;
                      var target$ = $(ev.delegateTarget);
                      var li$     = target$.closest ("li");
                      var value$  = $(S.select_attr_value);
                      var val     = value$.val ();
                      var width   = qr$.width  ();
                      var dialog;
                      if (as_widget$ == null) {
                          as_widget$ = attr_select.setup_widget (target$);
                      };
                      attr_select.cb.clear ();
                      attr_select.prefill  (val ? val.split (",") : []);
                      as_widget$
                          .dialog ("option", "width", "auto")
                          .dialog ("open")
                          .dialog ("widget")
                              .position
                                  ( { my         : "top"
                                    , at         : "bottom"
                                    , of         : target$
                                    , collision  : "fit"
                                    }
                                  );
                  }
                }
            , new_attr          : function new_attr (label) {
                  var S      = options.selectors;
                  var result = as_widget$.find (S.prototype).clone (true);
                  var dir$;
                  result.find ("b").html (label);
                  return result;
              }
            , prefill           : function prefill (choices) {
                  var S       = options.selectors;
                  var attrs$  = as_widget$.find (S.select_attr_attributes);
                  var but$    = as_widget$.find (S.add_button);
                  var menu$   = but$.data ("menu$").element;
                  var af, a$;
                  for (var i = 0, li = choices.length, choice; i < li; i++) {
                      choice = $.trim (choices [i]);
                      if (choice.length) {
                          af = af_map [choice];
                          a$ = attr_select.new_attr (af.label);
                          attrs$.append (a$);
                          attr_select.toggle (menu$, choice, true);
                      };
                  };
              }
            , setup             : function setup () {
                  $(this).click (attr_select.cb.open);
              }
            , setup_widget      : function setup_widget (but$) {
                  var S      = options.selectors;
                  var saf$   = options ["select_attr_form_html"];
                  var result;
                  if (! saf$) {
                      $.gtw_ajax_2json
                          ( { async       : false
                            , success     : function (response, status) {
                                if (! response ["error"]) {
                                    if ("html" in response) {
                                        saf$ = $(response.html);
                                        options.select_attr_form_html = saf$;
                                    } else {
                                        console.error ("Ajax Error", response);
                                    };
                                } else {
                                  console.error ("Ajax Error", response);
                                }
                              }
                            , url         : options.url.qx_asf
                            }
                          );
                      if (! saf$) {
                          return;
                      };
                  };
                  result = saf$.dialog
                      ( { autoOpen : false
                        , title    : saf$.attr ("title")
                        }
                      );
                  result.find (S.prototype)
                      .attr ("title", options.title.select_attr_sortable);
                  result.find (S.select_attr_attributes).sortable
                      ( { close       : attr_select.cb.clear
                        , distance    : 5
                        , placeholder : "ui-state-highlight"
                        }
                      );
                  result.find (S.button)
                      .gtw_buttonify (icons, options.buttonify_options);
                  result.find (S.add_button)
                      .each
                          ( function () {
                              var but$ = $(this);
                              attach_menu
                                ( but$
                                , new_menu (attr_filters, attr_select.cb.add)
                                );
                            }
                          );
                  result.find (S.apply_button).click  (attr_select.cb.apply);
                  result.find (S.cancel_button).click (attr_select.cb.close);
                  result.find (S.clear_button).click  (attr_select.cb.clear);
                  result.find (S.disabler)
                      .addClass ("ui-icon " + options.ui_class.disable)
                      .attr     ("title", options.title.disabler)
                      .click    (attr_select.cb.disabler);
                  return result;
              }
            , toggle         : function toggle (menu$, choice, state) {
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
                              a$.toggleClass ("ui-state-disabled", state);
                          };
                        }
                      );
              }
            };
        var disabler_cb = function disabler_cb (ev) {
            var S        = options.selectors;
            var afc$     = $(ev.target).closest (S.attr_filter_container);
            var dis$     = $(S.attr_filter_disabler, afc$);
            var but$     = dis$.find (".button");
            var val$     = $(S.attr_filter_value, afc$);
            var disabled = val$.prop ("disabled");
            var title    = disabled ?
                options.title.disabler : options.title.enabler;
            afc$.toggleClass ("ui-state-disabled",     !disabled);
            but$.toggleClass (options.ui_class.enable, !disabled)
                .toggleClass (options.ui_class.disable, disabled);
            dis$.attr    ("title", title);
            val$.prop    ("disabled", !disabled);
            return false;
        };
        var fix_buttons = function fix_buttons (buttons) {
            var S = options.selectors;
            var name, sel, value, old$, new$;
            for (name in buttons) {
                if (buttons.hasOwnProperty (name)) {
                    value = buttons [name];
                    sel   = S.add_button.replace ("ADD", name);
                    old$  = $(sel);
                    new$  = $(value);
                    old$.replaceWith (new$);
                };
            };
            $(S.button).gtw_buttonify (icons, options.buttonify_options);
        };
        var hide_menu_cb = function hide_menu_cb (ev) {
            var menu$ = $(".drop-menu"), tc;
            if (menu$.is (":visible")) {
                tc = $(ev.target).closest (".drop-menu");
                if (ev.keyCode === $.ui.keyCode.ESCAPE || ! tc.length) {
                    menu$.hide ();
                    $("." + options.ui_class.active_menu_button)
                        .removeClass (options.ui_class.active_menu_button);
                };
            };
        };
        var menu_click_cb = function menu_click_cb (ev) {
            var but$ = $(ev.delegateTarget);
            var menu = but$.data ("menu$");
            var opts = menu.element.data ("options");
            if (menu.element.is (":visible")) {
                menu.element.hide ();
                but$.removeClass (options.ui_class.active_menu_button);
            } else {
                hide_menu_cb (ev); // hide other open menus, if any
                if (opts && "open" in opts) {
                    opts.open (ev, menu);
                };
                menu.element
                    .show ()
                    .position
                      ( { my         : "right top"
                        , at         : "right bottom"
                        , of         : but$
                        , collision  : "fit"
                        }
                      )
                    .zIndex (but$.zIndex () + 1)
                    .focus  ();
                but$.addClass (options.ui_class.active_menu_button);
                if (ev && "stopPropagation" in ev) {
                    ev.stopPropagation ();
                };
            };
        };
        var menu_select_cb = function menu_select_cb (ev) {
            var target$ = $(ev.delegateTarget);
            var menu$   = target$.closest (".cmd-menu");
            target$.data ("callback") (ev);
            $("."+options.ui_class.active_menu_button)
                .removeClass (options.ui_class.active_menu_button);
            menu$.hide ();
        };
        var new_attr_filter = function new_attr_filter (choice) {
            var S = options.selectors;
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
                                      .find (S.attr_filter_disabler)
                                          .each (setup_disabler);
                                  ajx = true;
                                } else {
                                  console.error ("Ajax Error", response);
                                }
                            } else {
                                console.error ("Ajax Error", response);
                            };
                        }
                      , url         : options.url.qx_af_html
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
        var new_menu = function new_menu (choices, cb, options) {
            var menu = $("<ul class=\"drop-menu cmd-menu\">"), result;
            menu.data ({ options : options });
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
                                      ( { callback : cb
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
        var op_select_cb = function op_select_cb (ev) {
            var S       = options.selectors;
            var target$ = $(ev.delegateTarget);
            var choice  = target$.data ("choice");
            var but$    = $("."+options.ui_class.active_menu_button).first ();
            var afc$    = but$.closest (S.attr_filter_container);
            var val$  = $(S.attr_filter_value, afc$);
            var name    = val$.attr ("name");
            var prefix  = name.split  (qrs.op_sep) [0];
            var key     = prefix + qrs.op_sep + choice.key;
            update_attr_filter_op (afc$, choice, key);
            setTimeout
                ( function () {
                    $(S.attr_filter_value, afc$).focus ();
                  }
                , 1
                );
        };
        var order_by =
            { cb              :
                { add_criterion : function add_criterion (ev) {
                      var S       = options.selectors;
                      var target$ = $(ev.delegateTarget);
                      var choice  = target$.data ("choice").label;
                      var c$      = order_by.new_criterion (choice);
                      var but$    = ob_widget$.find (S.add_button);
                      var menu$   = but$.data ("menu$").element;
                      ob_widget$.find (S.order_by_criteria).append (c$);
                      order_by.toggle_criteria (menu$, choice, true);
                      ob_widget$.find (S.apply_button).focus ();
                  }
                , apply       : function apply (ev) {
                      var S     = options.selectors;
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
                                            (options.ui_class.sort_desc);
                                        var sign  = desc ? "-" : "";
                                        var af    = af_map [label];
                                        displays.push (sign + label);
                                        values.push   (sign + af.q_name);
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
                      var S = options.selectors;
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
                      var S        = options.selectors;
                      var target$  = $(ev.target);
                      var crit$    = target$.closest (S.order_by_criterion);
                      var dir$     = crit$.find (S.order_by_direction);
                      order_by.toggle_dir (dir$);
                  }
                , disabler    : function disabler (ev) {
                      var S        = options.selectors;
                      var target$  = $(ev.target);
                      var crit$    = target$.closest (S.order_by_criterion);
                      var disabled = crit$.hasClass ("disabled");
                      var but$     = ob_widget$.find (S.add_button);
                      var menu$    = but$.data ("menu$").element;
                      var choice   = crit$.find ("b").html ();
                      var title    = disabled ?
                          options.title.disabler : options.title.enabler;
                      crit$.toggleClass ("disabled", !disabled);
                      target$
                          .attr        ("title", title)
                          .toggleClass (options.ui_class.enable,  !disabled)
                          .toggleClass (options.ui_class.disable,  disabled);
                      order_by.toggle_criteria (menu$, choice, disabled);
                      return false;
                  }
                , open        : function open (ev) {
                      var S       = options.selectors;
                      var target$ = $(ev.delegateTarget);
                      var li$     = target$.closest ("li");
                      var width   = qr$.width ();
                      var dialog;
                      if (ob_widget$ == null) {
                          ob_widget$ = order_by.setup_widget (target$);
                      };
                      order_by.cb.clear ();
                      order_by.prefill  (target$.val ().split (","));
                      ob_widget$
                          .dialog ("option", "width", "auto")
                          .dialog ("open")
                          .dialog ("widget")
                              .position
                                  ( { my         : "top"
                                    , at         : "bottom"
                                    , of         : target$
                                    , collision  : "fit"
                                    }
                                  );
                  }
                }
            , new_criterion     : function new_criterion (label, desc) {
                  var S      = options.selectors;
                  var result = ob_widget$.find (S.prototype).clone (true);
                  var dir$;
                  result.find ("b").html (label);
                  if (desc) {
                      dir$ = result.find (S.order_by_direction);
                      order_by.toggle_dir (dir$);
                  };
                  return result;
              }
            , prefill           : function prefill (choices) {
                  var S       = options.selectors;
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
                          order_by.toggle_criteria (menu$, choice, true);
                      };
                  };
              }
            , setup             : function setup () {
                  var li$ = $(this).closest ("li");
                  li$.gtw_hd_input ({ callback : order_by.cb.open });
              }
            , setup_widget      : function setup_widget (but$) {
                  var S      = options.selectors;
                  var obf$   = options ["order_by_form_html"];
                  var result;
                  if (! obf$) {
                      $.gtw_ajax_2json
                          ( { async       : false
                            , success     : function (response, status) {
                                if (! response ["error"]) {
                                    if ("html" in response) {
                                        obf$ = $(response.html);
                                        options.order_by_form_html = obf$;
                                    } else {
                                        console.error ("Ajax Error", response);
                                    };
                                } else {
                                  console.error ("Ajax Error", response);
                                }
                              }
                            , url         : options.url.qx_obf
                            }
                          );
                      if (! obf$) {
                          return;
                      };
                  };
                  result = obf$.dialog
                      ( { autoOpen : false
                        , title    : obf$.attr ("title")
                        }
                      );
                  result.find (S.prototype)
                      .attr ("title", options.title.order_by_sortable);
                  result.find (S.order_by_criteria).sortable
                      ( { close       : order_by.cb.clear
                        , distance    : 5
                        , placeholder : "ui-state-highlight"
                        }
                      );
                  result.find (S.button)
                      .gtw_buttonify (icons, options.buttonify_options);
                  result.find (S.add_button)
                      .each
                          ( function () {
                              var but$ = $(this);
                              attach_menu
                                ( but$
                                , new_menu
                                    (attr_filters, order_by.cb.add_criterion)
                                );
                            }
                          );
                  result.find (S.apply_button).click  (order_by.cb.apply);
                  result.find (S.cancel_button).click (order_by.cb.close);
                  result.find (S.clear_button).click  (order_by.cb.clear);
                  result.find (S.order_by_direction)
                      .addClass ("ui-icon " + options.ui_class.sort_asc)
                      .attr     ("title", options.title.order_by_asc);
                  result.find (S.disabler)
                      .addClass ("ui-icon " + options.ui_class.disable)
                      .attr     ("title", options.title.disabler)
                      .click    (order_by.cb.disabler);
                  result.delegate
                      (S.order_by_criterion, "click", order_by.cb.dir);
                  return result;
              }
            , toggle_criteria   : function toggle_criteria (menu$, choice, state) {
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
                              a$.toggleClass ("ui-state-disabled", state);
                          };
                        }
                      );
              }
            , toggle_dir        : function toggle_dir (dir$) {
                  var asc   = dir$.hasClass (options.ui_class.sort_asc);
                  var title = asc ?
                      options.title.order_by_desc : options.title.order_by_asc;
                  dir$.toggleClass (options.ui_class.sort_asc, !asc)
                      .toggleClass (options.ui_class.sort_desc, asc)
                      .attr        ("title", title);
              }
            };
        var setup_disabler = function setup_disabler () {
            var dis$ = $(this);
            dis$.append
                    ( $("<a class=\"button\" name=\"DISABLE\">")
                        .gtw_iconify (icons)
                    )
                .attr   ("title", options.title.disabler);
        };
        var setup_esf = function setup_esf (cntxt) {
            var S = options.selectors;
            $(S.attr_filter_value_entity, cntxt).gtw_e_type_selector (options);
        };
        var setup_op_button = function setup_op_button () {
            var but$   = $(this);
            var afc$   = but$.closest (options.selectors.attr_filter_container);
            var afs    = af_map [afc$.attr ("title")];
            var label  = but$.html ();
            var op     = op_map_by_sym [label];
            if (! ("ops_menu$" in afs)) {
                afs.ops_menu$ = new_menu
                    ( sig_map [afs.sig_key]
                    , op_select_cb
                    , { open : function (ev, menu) {
                            adjust_op_menu (afs);
                        }
                      }
                    );
            };
            attach_menu (but$, afs.ops_menu$);
            afs.ops_selected [op.sym] = true;
        };
        var submit_ajax_cb = function submit_ajax_cb (response) {
            var S = options.selectors;
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
            if ("callbacks" in response) {
                for ( var i = 0, li = response.callbacks.length, cb, cbn
                    ; i < li
                    ; i++
                    ) {
                    cbn = response.callbacks [i];
                    cb  = options.callback [cbn];
                    if (cb) {
                        cb ();
                    };
                };
            };
            $GTW.push_history (qr$.attr ("action") + "?" + qr$.serialize ());
        };
        var submit_cb = function submit_cb (ev) {
            var S = options.selectors;
            var target$ = $(ev.target);
            var form$   = target$.closest ($("form"));
            var args    = form$.serialize ()
                + "&" + this.name + "=" + this.value;
            $.getJSON (form$.attr ("action"), args, submit_ajax_cb);
            return false;
        };
        var tr_selector = function tr_selector (label) {
            var head = options.selectors.attr_filter_container, tail;
            if (label.length) {
                tail = "[title^='"+label+"']";
            } else {
                tail = "[title]";
            };
            return head + tail;
        };
        var update_attr_filter_op = function update_attr_filter_op (afc$, op, key) {
            var S    = options.selectors;
            var afs  = af_map  [afc$.attr ("title")];
            var but$ = $(S.attr_filter_op, afc$);
            var oop  = op_map_by_sym [but$.html ()];
            if (oop) {
                afs.ops_selected [oop.sym] = false;
            };
            $(S.attr_filter_label, afc$).attr ("for", key);
            $(S.attr_filter_value, afc$)
                .not (".hidden")
                    .prop ("id", key)
                    .end ()
                .not (".display")
                    .prop ("name", key);
            $(S.attr_filter_op,    afc$)
                .attr ("title", op.desc)
                .html (op.label);
            afs.ops_selected [op.sym] = true;
        };
        options.esf_focusee = qr$.find (selectors.apply_button);
        $(document).bind ("click.menuhide keyup.menuhide", hide_menu_cb);
        $(selectors.button).gtw_buttonify (icons, options.buttonify_options);
        $(selectors.add_button, qr$)
            .each
                ( function () {
                    attach_menu
                        ($(this), new_menu (attr_filters, add_attr_filter_cb));
                  }
                );
        $(selectors.attr_filter_op).each (setup_op_button);
        $(selectors.attr_filter_disabler).each (setup_disabler);
        setup_esf ();
        $(selectors.attrs_container)
            .delegate (selectors.attr_filter_disabler, "click", disabler_cb);
        $(selectors.order_by_display).each (order_by.setup);
        $(selectors.config_button).each    (attr_select.setup);
        qr$.delegate (selectors.submit, "click", submit_cb);
        return this;
    }
  } (jQuery)
);

// __END__ GTW/jQ/query_restriction.js
