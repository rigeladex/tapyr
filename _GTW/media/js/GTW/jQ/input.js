//-*- coding: utf-8 -*-
// Copyright (C) 2011-2014 Mag. Christian Tanzer All rights reserved
// Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
// #*** <License> ************************************************************#
// This software is licensed under the terms of the BSD 3-Clause License
// <http://www.c-tanzer.at/license/bsd_3c.html>.
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
//    11-Jul-2014 (CT) Move `"use strict"` into closure
//    ««revision-date»»···
//--

( function ($) {
    "use strict";

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
                                 +  placeholder + '"'
                                 + ' class="_placeholder_"'
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
                                    )
                                .hide ();
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
