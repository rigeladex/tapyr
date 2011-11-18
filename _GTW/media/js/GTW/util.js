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
//    GTW_util
//
// Purpose
//    Utility javascript functions for GTW
//
// Revision Dates
//     3-Aug-2010 (CT) Creation (`as_int_array`)
//     4-Aug-2010 (CT) `fix_a_nospam` added (factored from GTW.jQuery)
//    10-Oct-2010 (CT) `GTW_Externalize` added
//    19-Nov-2010 (CT) `push_history` added
//    20-Jan-2011 (CT) Rename functions `GTW_Externalize` to `gtw_externalize`
//    26-Jan-2011 (CT) Style change
//     5-Apr-2011 (CT) `Array.prototype.indexOf` defined, if necessary
//    14-Oct-2011 (MG) Missing `var` added to `as_int_array`
//    ««revision-date»»···
//--

"use strict";

( function ($) {
    $GTW.update
        ( { as_int_array   : function (data) {
                var list   = data.split (",");
                var pat    = /^\s*\d+\s*([-+]\s*\d+)?\s*$/;
                var result = new Array ();
                for (var i = 0; i < list.length; i+= 1) {
                    var x = list [i];
                    if (x.search (pat) != null) {
                        result.push (eval (x));
                    };
                };
                return result;
            }
          , fix_a_nospam   : function ($) {
                $("a.nospam").each (
                    function () {
                        var rel = $(this).attr ("rel");
                        if (rel != null) {
                            var aia = $GTW.as_int_array (rel);
                            $(this).replaceWith
                                (String.fromCharCode.apply (null, aia));
                        };
                    }
                );
            }
          , push_history   : function (url, title, state) {
                if (Modernizr.history) {
                    window.history.pushState (state, title, url);
                };
                /* else { XXX ??? } */
            }
          }
        );
    $.fn.gtw_externalize = function () {
        this.click
            ( function (event) {
                  window.open (this.href).focus ();
                  if (event && event.preventDefault) {
                      event.preventDefault ();
                  }
              }
            ).addClass ("external");
        return this;
    };
    if (! Array.prototype.indexOf) {
        Array.prototype.indexOf = function indexOf (elem, start) {
            var len = this.length;
            if (start === undefined) {
                start = 0;
            } else {
                start = (start > 0) ? Math.floor (start) : Math.ceil (start);
                if (start < 0) {
                    start += len;
                    if (start < 0) {
                        start = 0;
                    }
                }
            }
            for (var i = start; i < len; i++) {
                if (i in this && this [i] === elem) {
                    return i;
                }
            }
            return -1;
        };
    }
  }
) (jQuery);

// __END__ GTW_util.js
