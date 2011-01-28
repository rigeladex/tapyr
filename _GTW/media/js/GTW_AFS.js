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
//    GTW_AFS
//
// Purpose
//    jQuery plugin for AJAX-enhanced forms
//
// Revision Dates
//    18-Jan-2011 (CT) Creation
//    ««revision-date»»···
//--

( function () {
    var AFS;
    var create = function create (spec) {
        var Type, type_name = spec ["type_name"];
        if (type_name !== undefined) {
            Type = AFS [type_name];
            if (Type !== undefined) {
                return new Type (spec);
            }
        }
        return spec;
    };
    var create_list = function create_list (elems) {
        var elem, i, l = elems.length, result = [];
        for (i = 0; i < l; i += 1) {
            elem = create (elems [i]);
            if (elem !== undefined) {
                result.push (elem);
            }
        }
        return result;
    };
    var Element = $GTW.Class.extend (
        { init : function init (spec) {
              var name, value;
              for (name in spec) {
                  if (spec.hasOwnProperty (name)) {
                      value = spec [name]
                      if (name === "children") {
                          value = create_list (value);
                      }
                      this [name] = value;
                  }
              }
              if (this.id !== undefined) {
                  AFS.id_map [this.id] = this;
              }
          }
        }
      , { type_name : "Element" }
    );
    $GTW.AFS = AFS = new $GTW.Module (
        { create   : create
        , Element  : Element
        , id_map   : {}
        }
    );
  } ()
);

// __END__ GTW_AFS.js
