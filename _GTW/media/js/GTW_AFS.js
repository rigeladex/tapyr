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
//    28-Jan-2011 (CT) Creation
//    30-Jan-2011 (CT) Creation continued
//    ««revision-date»»···
//--

( function () {
    var AFS;
    var create = function create (spec) {
        var Type, type_name = spec ["type"];
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
            if (elem !== undefined && elem ["_id"] !== undefined) {
                result.push (elem._id);
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
              if (this ["_id"] !== undefined) {
                  AFS.id_map [this._id] = this;
              }
          }
        , setup_value : function setup_value (value) {
              var id = value ["_id"], n, v, elem;
              if (id !== undefined && id === this ["_id"]) {
                  this.value = value;
              }
              for (n in value) {
                  if (value.hasOwnProperty (n) && n [0] !== "_") {
                      v = value [n];
                      if (v ["_id"] !== undefined) {
                          elem = AFS.id_map [v._id];
                          elem.setup_value (v);
                      }
                  }
              }
          }
        }
      , { type_name : "Element" }
    );
    var Entity = Element.extend (
        {}
      , { type_name : "Entity" }
    );
    var Field = Element.extend (
        {}
      , { type_name : "Field" }
    );
    var Fieldset = Element.extend (
        {}
      , { type_name : "Fieldset" }
    );
    var Form = Element.extend (
        { init : function init (spec, value) {
              this._super      (spec);
              this.setup_value (value);
          }
        }
      , { type_name : "Form" }
    )
    $GTW.AFS = AFS = new $GTW.Module (
        { create   : create
        , Element  : Element
        , Entity   : Entity
        , Field    : Field
        , Fieldset : Fieldset
        , Form     : Form
        , id_map   : {}
        }
    );
  } ()
);

// __END__ GTW_AFS.js
