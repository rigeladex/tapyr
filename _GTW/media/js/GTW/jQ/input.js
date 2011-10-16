//-*- coding: iso-8859-1 -*-
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
//    GTW/jQ/input.js
//
// Purpose
//    jQuery plugin for improving input elements
//
//
// Revision Dates
//    12-Jan-2011 (CT) Creation
//    26-Jan-2011 (CT) Style change
//    16-Oct-2011 (MG) Handling of placeholder for `password` changed
//    ««revision-date»»···
//--

"use strict";

( function ($) {
    $.fn.gtw_input_placeholders = function (opts) {
        var options  = $.extend
            ( { overlay_type : "b"
              , p_class      : "placeholden"
              }
            , opts || {}
            );
        var pop_placeholder = function (target$, placeholder) {
            if (target$.val () == placeholder) {
                target$.val ("").removeClass (options.p_class);
            };
        };
        this
            .each
                ( function (n) {
                    var target$ = $(this);
                    var placeholder = target$.attr ("placeholder");
                    if (placeholder) {
                        if (target$.attr ("type") != "password") {
                            target$
                                .focus
                                    ( function (ev) {
                                        pop_placeholder (target$, placeholder);
                                      }
                                    )
                                .blur
                                    ( function (ev) {
                                        var v = target$.val ();
                                        if (v == "" || v == placeholder) {
                                            target$
                                                .val      (placeholder)
                                                .addClass (options.p_class);
                                        };
                                      }
                                    )
                                .blur ();
                        } else {
                            var overlay$ =
                                $( '<input type="text" value="'
                                 + ' class="_placeholder_"''
                                 + placeholder
                                 + '"/>'
                                 );
                            overlay$
                                .insertBefore (target$)
                                .addClass     (options.p_class)
                                .css
                                    ( { height   : target$.css ("height")
                                      , width    : target$.css ("width")
                                      }
                                    )
                                .focus
                                    ( function (ev) {
                                        target$.show  ().focus ();
                                        overlay$.hide ();
                                      }
                                    );
                            target$
                                .blur
                                    ( function (ev) {
                                        var v = target$.val ();
                                        if (v == "" || v == placeholder) {
                                            target$.hide  ();
                                            overlay$.show ();
                                        };
                                      }
                                    )
                                .blur ();
                        };
                    };
                  }
                )
            .parents ("form")
                .submit (
                    function () {
                        $("._placeholder_").hide ();
                        $("[placeholder]", this)
                            .each (
                                function () {
                                    var target$ = $(this);
                                    pop_placeholder
                                        (target$, target$.attr ("placeholder"));
                                }
                            )
                    }
                );
        return this;
    };
  }
) (jQuery);

// __END__ GTW/jQ/input.js
