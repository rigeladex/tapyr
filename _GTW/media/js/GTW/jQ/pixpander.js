//-*- coding: iso-8859-1 -*-
// Copyright (C) 2010-2011 Mag. Christian Tanzer All rights reserved
// Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
// #*** <License> ************************************************************#
// This software is licensed under the terms of either the
// MIT License or the GNU Affero General Public License (AGPL) Version 3.
// http://www.c-tanzer.at/license/mit_or_agpl.html
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
//    ««revision-date»»···
//--

( function ($) {
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
                    img$.attr (
                      { src   : url
                      , style : style
                      }
                    );
                    if (wd) {
                      img$.css ({ width : wd });
                    }
                    options.x_class && img$.toggleClass (options.x_class);
                    if (event && event.preventDefault) {
                        event.preventDefault ();
                    };
                };
                img$.toggle
                    ( function (ev) { show (ev, src, sty); }
                    , function (ev) { show (ev, a.attr ("href"), "", wd); }
                    );
            }
        );
        return this;
    };
  }
) (jQuery);

// __END__ GTW_pixpander.js
