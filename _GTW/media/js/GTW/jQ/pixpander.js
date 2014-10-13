//-*- coding: utf-8 -*-
// Copyright (C) 2010-2014 Mag. Christian Tanzer All rights reserved
// Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
// #*** <License> ************************************************************#
// This software is licensed under the terms of the BSD 3-Clause License
// <http://www.c-tanzer.at/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    GTW_pixpander
//
// Purpose
//    jQuery plugin for expanding linked images in place
//
//
// Revision Dates
//    18-Oct-2010 (CT) Creation
//    20-Jan-2011 (CT) Rename function `GTW_pixpander` to `gtw_pixpander`
//    26-Jan-2011 (CT) Style change
//     5-Apr-2011 (CT) Changed to restore `width`
//     1-Jun-2011 (CT) Bug fixed
//    30-Nov-2011 (CT) Use `return false` instead of .`preventDefault`
//    11-Jul-2014 (CT) Move `"use strict"` into closure
//    ««revision-date»»···
//--

( function ($) {
    "use strict";

    $.fn.gtw_pixpander = function (options) {
        options = $.extend
            ( { x_class     : "pixpanded"
              }
            , options || {}
            );
        $(this).each (
            function () {
                var img  = this;
                var img$ = $(img);
                var a    = img$.closest ("a");
                var src  = img.src;
                var sty  = img.style;
                var wd   = img$.css ("width")
                var show = function (event, url, style, wd) {
                    img$
                        .attr ({ src : url, style : style })
                        .css  ({ width : wd ? wd : "auto" })
                        ;
                    options.x_class && img$.toggleClass (options.x_class);
                    return false;
                };
                img$.toggle
                    ( function (ev) { return show (ev, a.attr ("href"), ""); }
                    , function (ev) { return show (ev, src, sty, wd); }
                    );
            }
        );
        return this;
    };
  }
) (jQuery);

// __END__ GTW_pixpander.js
