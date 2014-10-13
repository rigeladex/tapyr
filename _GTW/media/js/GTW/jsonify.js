// Copyright (C) 2011-2014 Mag. Christian Tanzer All rights reserved
// Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
// #*** <License> ************************************************************#
// This software is licensed under the terms of the BSD 3-Clause License
// <http://www.c-tanzer.at/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    GTW_jsonify
//
// Purpose
//    Jsonify function for GTW
//
// Revision Dates
//    26-Jan-2011 (CT) Creation
//    31-May-2011 (MG) Missing `var` added
//    11-Jul-2014 (CT) Move `"use strict"` into closure
//    ««revision-date»»···
//--

( function () {
    "use strict";

    var json_char_map =
        { "\\" : "\\\\", "\"" : "\\\""
        , "\b" : "\\b",  "\f" : "\\f", "\n" : "\\n", "\r" : "\\r", "\t" : "\\t"
        };
    var jsonify  = function jsonify (thing) {
        var i, l, k, t, v, name;
        var rs = [];
        switch (typeof thing) {
            case "boolean" :
                return thing.toString ();
            case "number" :
                return isFinite (thing) ? thing.toString () : "null";
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
                    }
                }
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
                    }
                    rs.push (v);
                }
                return '"' + rs.join ("") + '"';
            default :
                return "null";
        }
    };
    $GTW.update ({ jsonify : jsonify });
  } ()
);

// __END__ GTW_jsonify.js
