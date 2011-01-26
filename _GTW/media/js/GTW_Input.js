//-*- coding: iso-8859-1 -*-
// Copyright (C) 2011 Mag. Christian Tanzer All rights reserved
// Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
// ****************************************************************************
// This file is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This file is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Affero General Public License for more details.
//
// You should have received a copy of the GNU Affero General Public License
// along with this file. If not, see <http://www.gnu.org/licenses/>.
// ****************************************************************************
//
//++
// Name
//    GTW_Input
//
// Purpose
//    jQuery plugin for improving input elements
//
//
// Revision Dates
//    12-Jan-2011 (CT) Creation
//    26-Jan-2011 (CT) Style change
//    ««revision-date»»···
//--

( function ($) {
    $.fn.gtw_input_placeholders = function (options) {
        var options  = $.extend
            ( { overlay_type : "b"
              , p_class      : "placeholden"
              }
            , options || {}
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
                                $( "<"  + options.overlay_type + ">"
                                 + placeholder
                                 + "</" + options.overlay_type + ">"
                                 );
                            overlay$
                                .insertBefore (target$)
                                .css
                                    ( { height   : target$.css ("height")
                                      , position : "absolute"
                                      , width    : target$.css ("width")
                                      }
                                    )
                                .addClass (options.p_class)
                                .click
                                    ( function (ev) {
                                        overlay$.hide ();
                                        target$.focus ();
                                      }
                                    )
                                .hide ();
                            target$
                                .focus
                                    ( function (ev) { overlay$.hide (); })
                                .blur
                                    ( function (ev) {
                                        var v = target$.val ();
                                        if (v == "" || v == placeholder) {
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
                .submit
                    ( function () {
                        $("[placeholder]", this)
                            .each
                                ( function () {
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

// __END__ GTW_Input.js
