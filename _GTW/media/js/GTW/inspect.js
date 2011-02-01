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
//    GTW_inspect
//
// Purpose
//    Provide functions to inspect Javascript objects
//
// Revision Dates
//    28-Jan-2011 (CT) Creation
//    ««revision-date»»···
//--

( function () {
    var inspect;
    var blanks =
    "                                                                         ";
    $GTW.inspect = inspect = new $GTW.Module (
        { filter_function  : function filter_function (name, obj) {
              return typeof (obj [name]) === "function";
          }
        , filter_not_function : function filter_not_function (name, obj) {
              return typeof (obj [name]) !== "function";
          }
        , filter_object : function filter_object (name, obj) {
              return typeof (obj [name]) === "object";
          }
        , filter_own : function filter_own (name, obj) {
              return obj.hasOwnProperty (name);
          }
        , key_cmp : function key_cmp (l, r) {
              if (typeof l === "string") { l = l.toLowerCase (); }
              if (typeof r === "string") { r = r.toLowerCase (); }
              if      (l <   r) { return -1; }
              else if (l === r) { return  0; }
              else              { return +1; }
          }
        , keys : function keys (obj, filter) {
              var result = [];
              if (filter === undefined) {
                  filter = inspect.filter_own;
              }
              for (name in obj) {
                  if (filter (name, obj)) {
                      result.push (name);
                  }
              }
              return result;
          }
        , items : function items (obj, filter) {
              var result = [];
              if (filter === undefined) {
                  filter = inspect.filter_own;
              }
              for (name in obj) {
                  if (filter (name, obj)) {
                      result.push ([name, obj [name]]);
                  }
              }
              return result;
          }
        , show   : function show (obj, filter, level) {
              var i, l, name, r, regexp, value;
              var result = [];
              var lev    = level || 0;
              var indent = blanks.slice (0, 4 * lev);
              var names  = inspect.keys (obj, filter).sort (inspect.key_cmp);
              for (i = 0, l = names.length; i < l; i += 1) {
                  name  = names [i];
                  value = obj   [name];
                  switch (typeof value) {
                      case "function" :
                          value  = value.toString ();
                          regexp = new RegExp ("function +" + name + " *\\(");
                          if (value.match (regexp)) {
                              r = indent + value;
                          } else {
                              r = indent + name + " : " + value;
                          }
                          r = r.split ("\n") [0].replace (/ *\{ *$/, "");
                          break;
                      case "object" :
                          result.push (indent + name + " :");
                          r = inspect.show (value, filter, lev + 1); ;
                          break;
                      case "string" :
                          r = indent + name + " = \"" + value + "\"";
                          break;
                      default :
                          r = indent + name + " = " + value;
                  }
                  result.push (r);
              }
              return result.join ("\n");
          }
        , values : function values (obj, filter) {
              var result = [];
              if (filter === undefined) {
                  filter = inspect.filter_own;
              }
              for (name in obj) {
                  if (filter (name, obj)) {
                      result.push (obj [name]);
                  }
              }
              return result;
          }
        }
    );
  } ()
);

// __END__ GTW_inspect.js
