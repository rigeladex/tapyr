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
//     6-Feb-2011 (CT) Creation continued...
//    24-Feb-2011 (CT) Creation continued....
//    28-Feb-2011 (CT) Creation continued.....
//                     `setup_value` revamped
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
        , child : function child (i) {
            return Elements.id_map [this.children [i]];
          }
        , setup_value : function setup_value (root, anchor) {
              var i, l, child, has_value;
              var new_anchor = anchor, new_root = root;
              has_value = this ["value"] !== undefined;
              if (has_value) {
                  if (this.constructor.is_anchor) {
                      new_anchor = this;
                      this.value.$id = this.$id;
                  }
                  if (this.constructor.is_root) {
                      new_root   = this;
                      this.value ["$anchor_id"] = anchor.$id;
                  } else {
                      anchor.value [this.$id] = this.value;
                  }
              }
              if (this ["children"] !== undefined) {
                  for (i = 0, l = this.children.length; i < l; i += 1) {
                      child = this.child (i);
                      child.setup_value (new_root, new_anchor);
                  }
              }
          }
        }
      , { is_anchor : false, is_root : false, type_name : "Element" }
    );
    var Entity = Element.extend (
        {}
      , { is_anchor : true, is_root : true, type_name : "Entity" }
    );
    var Entity_Link = Element.extend (
        {}
      , { is_anchor : true, is_root : true, type_name : "Entity_Link" }
    );
    var Entity_List = Element.extend (
        {}
      , { type_name : "Entity_List" }
    );
    var Field = Element.extend (
        {}
      , { type_name : "Field" }
    );
    var Field_Composite = Element.extend (
        {}
      , { is_anchor : true, type_name : "Field_Composite" }
    );
    var Field_Entity = Element.extend (
        {}
      , { is_anchor : true, type_name : "Field_Entity" }
    );
    var Fieldset = Element.extend (
        {}
      , { type_name : "Fieldset" }
    );
    var Form = Element.extend (
        { init : function init (spec) {
              this._super      (spec);
              this.setup_value ();
          }
        , setup_value : function setup_value () {
              var i, l, child;
              if (this ["children"] !== undefined) {
                  for (i = 0, l = this.children.length; i < l; i += 1) {
                      child = this.child (i);
                      child.setup_value (child, child);
                  }
              }
          }
        }
      , { type_name : "Form" }
    )
    Elements = new $GTW.Module (
        { create                : create
        , Element               : Element
        , Entity                : Entity
        , Entity_Link           : Entity_Link
        , Entity_List           : Entity_List
        , Field                 : Field
        , Field_Composite       : Field_Composite
        , Field_Entity          : Field_Entity
        , Fieldset              : Fieldset
        , id_map                : {}
        }
    );
    $GTW.AFS = new $GTW.Module (
        { Elements              : Elements
        , Form                  : Form
        }
    );
  } ()
);

// __END__ GTW/AFS/Elements.js
