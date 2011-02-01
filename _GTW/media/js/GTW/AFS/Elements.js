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
//    GTW/AFS/Elements.js
//
// Purpose
//    Elements for AJAX-enhanced forms
//
// Revision Dates
//    28-Jan-2011 (CT) Creation
//    30-Jan-2011 (CT) Creation continued
//    31-Jan-2011 (CT) Creation continued..
//    ««revision-date»»···
//--

( function () {
    var Elements;
    var create = function create (spec) {
        var Type, type_name = spec ["type"];
        if (type_name !== undefined) {
            Type = Elements [type_name];
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
            if (elem !== undefined && elem ["$id"] !== undefined) {
                result.push (elem.$id);
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
              if (this ["$id"] !== undefined) {
                  Elements.id_map [this.$id] = this;
              }
          }
        , setup_value : function setup_value (value) {
              var i, l, v, child, $id;
              this.value = value;
              if (this ["children"] !== undefined) {
                  for (i = 0, l = this.children.length; i < l; i += 1) {
                      child = Elements.id_map [this.children [i]];
                      $id   = child ["$id"];
                      if ($id !== undefined) {
                          v = value [$id];
                          if (v !== undefined) {
                              child.setup_value (v);
                          }
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
    Elements = new $GTW.Module (
        { create   : create
        , Element  : Element
        , Entity   : Entity
        , Field    : Field
        , Fieldset : Fieldset
        , id_map   : {}
        }
    );
    $GTW.AFS = new $GTW.Module (
        { Elements : Elements
        , Form     : Form
        }
    );
  } ()
);

// __END__ GTW/AFS/Elements.js
