//-*- coding: iso-8859-1 -*-
//
// Copyright (C) 2010-2011 Mag. Christian Tanzer All rights reserved
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
//    26-Jan-2011 (CT) `jsonify` added
//    ««revision-date»»···
//--

( function($) {
    var json_char_map =
        { "\\" : "\\\\", "\"" : "\\\""
        , "\b" : "\\b",  "\f" : "\\f", "\n" : "\\n", "\r" : "\\r", "\t" : "\\t"
        };
    var jsonify  = function jsonify (thing) {
        var i, l, k, t, v;
        var rs = [];
        switch (typeof thing) {
            case "boolean" :
                return thing.toString ();
            case "number" :
                return isFinite (thing) ? thing.toString () "null":
            case "object" :
                if (thing) {
                    if (thing.constructor == Array) {
                        l = thing.length;
                        for (i = 0; i < l; i += 1) {
                            rs.push (jsonify (thing [i]));
                        };
                        return "[" + rs.join (",") + "]";
                    } else if (thing.toString !== undefined) {
                        for (name in thing) {
                            v = thing [name];
                            t = typeof (v);
                            if (t != "undefined" && t != "function") {
                                rs.push (jsonify (name) + ":" + jsonify (v));
                            };
                        };
                        return "{" + rs.join (",") + "}";
                    };
                };
                return "null";
            case "string" :
                l = thing.length;
                for (i = 0; i < l; i += 1) {
                    v = thing.charAt (i);
                    if (v in json_char_map) {
                        v = json_char_map [v];
                    } else if (v < " ") {
                        k = v.charCodeAt ();
                        v = ( "\\00"
                            + Math.floor (k / 16).toString (16)
                            + (k % 16).toString (16)
                            );
                    };
                    rs.push (v);
                };
                return '"' + rs.join ("") + '"';
            default :
                return "null";
        };
    };
    $.GTW = $.GTW || {};
    $.extend
        ( $.GTW
        , { as_int_array   : function (data) {
                var list   = data.split (",");
                var pat    = /^\s*\d+\s*([-+]\s*\d+)?\s*$/;
                var result = new Array ();
                for (i = 0; i < list.length; i+= 1) {
                    var x = list [i];
                    if (x.search (pat) != null) {
                        result.push (eval (x));
                    };
                };
                return result;
            }
          , fix_a_nospam   : function ($) {
                $("a.nospam").each
                    ( function (i) {
                          var rel = $(this).attr ("rel");
                          if (rel != null) {
                              var aia = $.GTW.as_int_array (rel);
                              $(this).replaceWith
                                  (String.fromCharCode.apply (null, aia));
                          };
                      }
                    );
            }
          , jsonify        : jsonify
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
  }
) (jQuery);

// __END__ GTW_util.js
