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
//    28-Feb-2011 (CT) `setup_value` revamped
//     1-Mar-2011 (CT) `$anchor_id` setting changed, `packed_values` added
//     2-Mar-2011 (CT) `sid` added to `packed_values`
//     5-Mar-2011 (CT) `Element.changed` added
//     9-Mar-2011 (CT) `Field_Role_Hidden` added
//     9-Mar-2011 (CT) `Element.setup_value` changed
//                     * copy `value.init` to `edit`
//                     * support `Field_Role_Hidden`
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
        , changed : function changed () {
              var i, l, child, has_value;
              has_value =
                  (  (this ["value"]  !== undefined)
                  && (this.value.edit !== undefined)
                  );
              if (has_value && this.value.init !== this.value.edit) {
                  return true;
              }
              if (this ["children"] !== undefined) {
                  for (i = 0, l = this.children.length; i < l; i += 1) {
                      child = this.child (i);
                      if (child.changed ()) {
                          return true;
                      }
                  }
              }
              return false;
          }
        , child : function child (i) {
              return Elements.id_map [this.children [i]];
          }
        , setup_value : function setup_value (root, anchor, roots) {
              var i, l, child;
              var cls = this.constructor;
              var new_anchor = anchor, new_root = root;
              if (this ["value"] !== undefined) {
                  if (cls.is_anchored || cls.is_root) {
                      new_anchor = this;
                      this.value.$id = this.$id;
                      this.value.$child_ids = [];
                      if (this.value ["init"] && ! this.value ["edit"]) {
                          this.value.edit = $GTW.inspect.copy (this.value.init);
                      }
                  }
                  if (  cls.type_name === "Field_Role_Hidden"
                     && ! this.value ["init"]
                     ) {
                      this.value.edit =
                          Elements.id_map [root.$anchor_id].value.edit;
                      this.value.role_id = root.$anchor_id;
                  }
                  if (cls.is_anchored) {
                      if (this.$id !== anchor.$id) {
                          this.value ["$anchor_id"] = anchor.$id;
                      }
                  }
                  if (cls.is_root) {
                      roots.push (this);
                      new_root = this;
                  } else {
                      anchor.value [this.$id] = this.value;
                      anchor.value ["$child_ids"].push (this.$id);
                  }
                  if (this.$id !== anchor.$id) {
                     this.$anchor_id = anchor.$id;
                  }
              }
              if (this ["children"] !== undefined) {
                  for (i = 0, l = this.children.length; i < l; i += 1) {
                      child = this.child (i);
                      if (child) {
                          child.setup_value (new_root, new_anchor, roots);
                      }
                  }
              }
          }
        }
      , { is_anchored : false, is_root : false, type_name : "Element" }
    );
    var Entity = Element.extend (
        {}
      , { is_anchored : true, is_root : true, type_name : "Entity" }
    );
    var Entity_Link = Element.extend (
        {}
      , { is_root : true, type_name : "Entity_Link" }
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
      , { is_anchored : true, type_name : "Field_Composite" }
    );
    var Field_Entity = Element.extend (
        {}
      , { is_anchored : true, type_name : "Field_Entity" }
    );
    var Field_Role_Hidden = Element.extend (
        {}
      , { type_name : "Field_Role_Hidden" }
    );
    var Fieldset = Element.extend (
        {}
      , { type_name : "Fieldset" }
    );
    var Form = Element.extend (
        { init : function init (spec) {
              Elements.root = this;
              this._super      (spec);
              this.setup_value ();
          }
        , get : function get (id) {
              return Elements.id_map [id];
          }
        , packed_values : function packed_values (args) {
              var i, l, child;
              var form     = this;
              var entities = args || form.roots;
              var result   =
                  { $id        : form.$id
                  , sid        : form.value.sid
                  , $child_ids : []
                  };
              for (i = 0, l = entities.length; i < l; i += 1) {
                  child = entities [i];
                  result [child.$id] = child.value;
                  result.$child_ids.push (child.$id);
              }
              return result;
          }
        , setup_value : function setup_value () {
              var i, l, child;
              if (this ["children"] !== undefined) {
                  this.roots = [];
                  for (i = 0, l = this.children.length; i < l; i += 1) {
                      child = this.child (i);
                      child.setup_value (child, child, this.roots);
                  }
              }
          }
        }
      , { type_name : "Form" }
    )
    var get = function get (id) {
        return Elements.id_map [id];
    };
    Elements = new $GTW.Module (
        { create                : create
        , Element               : Element
        , Entity                : Entity
        , Entity_Link           : Entity_Link
        , Entity_List           : Entity_List
        , Field                 : Field
        , Field_Composite       : Field_Composite
        , Field_Entity          : Field_Entity
        , Field_Role_Hidden     : Field_Role_Hidden
        , Fieldset              : Fieldset
        , get                   : get
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
