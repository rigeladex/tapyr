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
//    24-Feb-2012 (CT) Change `get_completions` to handle `n == 0` correctly
//     7-Mar-2012 (CT) Factor `ET_Selector` and `ET_Selector_HD`
//     7-Mar-2012 (CT) Add `ET_Selector_AFS`, refactor as necessary
//     8-Mar-2012 (CT) Fix bugs in `ET_Selector_AFS`, `ET_Selector_HD`
//     8-Mar-2012 (CT) Add `options.completer_position` and `.dialog_position`
//    ««revision-date»»···
//--

"use strict";

( function ($, undefined) {
    var bwrap = function bwrap (v) {
        return "<b>" + v + "</b>";
    };
    var default_position =
        { my         : "right top"
        , at         : "right bottom"
        , collision  : "fit"
        };
    var ET_Selector = $GTW.Class.extend (
        { defaults              :
            { completer_position  : default_position
            , dialog_position     : default_position
            , icon_map            : {}
            , selectors           :
                { aid             : "[name=__attribute_selector_for__]"
                }
            , treshold            : 1
            }
        , init                  : function init (opts) {
              var icon_map = $.extend
                  ( {}
                  , this.defaults.icon_map
                  , opts && opts ["icon_map"] || {}
                  );
              var completer_position, dialog_position;
              this.icons = new $GTW.UI_Icon_Map (icon_map);
              this.selectors = $.extend
                  ( {}
                  , this.defaults.selectors
                  , this.icons.selectors
                  , opts && opts ["selectors"] || {}
                  );
              completer_position = $.extend
                  ( {}
                  , this.defaults.completer_position
                  , opts && opts ["completer_position"] || {}
                  );
              dialog_position = $.extend
                  ( {}
                  , this.defaults.dialog_position
                  , opts && opts ["dialog_position"] || {}
                  );
              this.options = $.extend
                  ( {}
                  , this.defaults
                  , opts || {}
                  , { icon_map           : this.icons
                    , completer_position : completer_position
                    , dialog_position    : dialog_position
                    , selectors          : this.selectors
                    }
                  );
              this.ajax_response = undefined;
              this.widget        = undefined;
          }
        , activate_cb           : function activate_cb (ev) {
              var self = (ev && "data" in ev) ? ev.data || this : this;
              self.target$  = $(ev.delegateTarget);
              self.esf_data = self.get_esf_data (ev, self.target$);
              if (! self.ajax_response) {
                  $.gtw_ajax_2json
                      ( { async       : false
                        , data        : self.esf_data
                        , success     : function (response, status) {
                              if (! response ["error"]) {
                                  if ("html" in response) {
                                      self.ajax_response = response;
                                      self.widget        = self.setup_widget
                                          (response);
                                  } else {
                                    console.error ("Ajax Error", response);
                                  }
                              } else {
                                  console.error ("Ajax Error", response);
                              };
                          }
                        , url         : self.options.url.qx_esf
                        }
                      , "Entity completer"
                      );
              } else {
                  self.widget = self.setup_widget (self.ajax_response);
              };
              return false;
          }
        , apply_cb              : function apply_cb (ev) {
              var self = (ev && "data" in ev) ? ev.data || this : this;
              var response = self.widget.data ("completed_response");
              if (response ["value"] && response ["display"]) {
                  self._apply_cb_inner (ev, response);
              };
              self.close_cb  (ev);
              if ("esf_focusee" in self.options) {
                  self.options.esf_focusee.focus ();
              };
              return false;
          }
        , clear_cb              : function clear_cb (ev) {
              var self = (ev && "data" in ev) ? ev.data || this : this;
              var S    = self.options.selectors;
              self.widget.find (":input").not ("button, .hidden").each
                  ( function () {
                      $(this).val ("");
                    }
                  );
              self.widget.find (S.apply_button)
                  .button ("option", "disabled", true);
          }
        , close_cb              : function close_cb (ev) {
              var self = (ev && "data" in ev) ? ev.data || this : this;
              self.widget.dialog ("destroy");
          }
        , completed_cb          : function completed_cb (inp$, response) {
              var S = this.options.selectors;
              this.close_cb ();
              this.widget = this.setup_widget (response);
              this.widget
                  .data ("completed_response", response)
                  .find (S.apply_button)
                      .button ("option", "disabled", false);
          }
        , get_ccb               : function get_ccb (inp$, term, cb, response) {
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
          }
        , get_completions       : function get_completions (inp$, term, cb) {
              var self     = this;
              var S        = self.options.selectors;
              var trigger  = inp$.prop ("id");
              var values   = {}, n = 0;
              self.completion_data = self.get_completion_data ();
              if (self.completion_data.key) {
                  self.widget.find (":input").not ("button, .hidden").each
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
                        , data          : $.extend
                            ( { entity_p  : true
                              , trigger   : trigger
                              , trigger_n : trigger
                              , values    : values
                              }
                            , self.completion_data
                            )
                        , success       : function (answer, status, xhr) {
                            if (! answer ["error"]) {
                                self.get_ccb (inp$, term, cb, answer);
                            } else {
                                console.error ("Ajax error", answer, data);
                            };
                          }
                        , url           : self.options.url.qx_esf_completer
                        }
                      , "Completion"
                      );
              } else {
                  cb ([]);
              };
          }
        , select_cb             : function select_cb (ev, inp$, item) {
              var self     = this;
              var S        = self.options.selectors;
              var response = inp$.data ("completer_response");
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
                      self.inputs$.eq (item.index + 1).focus ();
                  };
              } else {
                  $.gtw_ajax_2json
                      ( { async         : true
                        , data          : $.extend
                            ( { pid     : item.value
                              }
                            , self.completion_data
                            )
                        , success       : function (answer, status, xhr) {
                              self.completed_cb (inp$, answer);
                          }
                        , url           : self.options.url.qx_esf_completed
                        }
                      , "Completion"
                      );
              };
          }
        , setup_widget          : function setup_widget (response) {
              var self    = this;
              var options = self.options;
              var S       = options.selectors;
              var result  = $(response.html)
                  .dialog
                      ( { autoOpen : false
                        , close    : self.close_cb
                        }
                      );
              var form$   = result.is ("form") ? result : result.find ("form");
              this.inputs$ = result.find (":input").not ("button, .hidden");
              result.find  (S.button)
                  .gtw_buttonify (self.icons, options.buttonify_options);
              result.find  (S.apply_button)
                  .button  ("option", "disabled", true)
                  .click   (self, self.apply_cb);
              result.find  (S.cancel_button).click (self, self.close_cb);
              result.find  (S.clear_button).click  (self, self.clear_cb);
              form$.submit (self, self.apply_cb);
              this.inputs$.each
                  ( function () {
                      var inp$ = $(this);
                      inp$.gtw_autocomplete
                          ( { focus     : function (event, ui) {
                                  return false;
                              }
                            , minLength : options.treshold
                            , position  : options.completer_position
                            , select    : function (event, ui) {
                                  self.select_cb (event, inp$, ui.item);
                                  return false;
                              }
                            , source    : function (req, cb) {
                                  self.get_completions (inp$, req.term, cb);
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
                          ( $.extend
                              ( {}
                              , options.dialog_position
                              , { of : self.target$ }
                              )
                          );
              this.inputs$.first ().focus ();
              return result;
          }
        }
    );
    var ET_Selector_AFS = ET_Selector.extend (
        { get_completion_data   : function get_completion_data () {
              var opts = this.options;
              var aid$ = this.widget.find (opts.selectors.aid);
              var result =
                  { key : aid$.val ()
                  , etn : opts.afs.anchor.type_name // aid$.prop ("title")
                  };
              return result;
          }
        , get_esf_data          : function get_esf_data (ev, target$) {
              var opts = this.options;
              var result =
                  { fid     : opts.afs.elem.anchor_id
                  , trigger : opts.afs.fid
                  };
              return result;
          }
        , _apply_cb_inner       : function (ev, response) {
              this.options.afs.apply_cb (response.display, response.value);
          }
        }
    );
    var ET_Selector_HD = ET_Selector.extend (
        { get_completion_data   : function get_completion_data () {
              var aid$ = this.widget.find (this.options.selectors.aid);
              return { key : aid$.val () };
          }
        , get_esf_data          : function get_esf_data (ev, target$) {
              return { key : target$.prop ("id") };
          }
        , _apply_cb_inner       : function (ev, response) {
              var hidden$ = this.target$.siblings
                  ("[name=\"" + this.esf_data.key + "\"]").first ();
              this.target$
                  .prop ("title", response.display).val (response.display);
              hidden$.val (response.value);
          }
        }
    );
    $.fn.gtw_e_type_selector_afs = function (opts) {
        this.each
            ( function () {
                var selector = new ET_Selector_AFS (opts);
                $(this).data ("selector_afs", selector);
              }
            );
        return this;
    };
    $.fn.gtw_e_type_selector_hd = function (opts) {
        this.each
            ( function () {
                var selector = new ET_Selector_HD (opts);
                $(this).gtw_hd_input
                    ({callback : function (ev) { selector.activate_cb (ev); }});
              }
            );
        return this;
    };
  } (jQuery)
);

// __END__ GTW/jQ/e_type_selector.js
