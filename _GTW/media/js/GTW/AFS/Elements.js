//-*- coding: iso-8859-1 -*-
// Copyright (C) 2011-2012 Mag. Christian Tanzer All rights reserved
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
//    10-Mar-2011 (CT) `Element._setup_value` factored out of `.setup_value`
//                     (using dynamic binding instead of `if` statements)
//     1-Apr-2011 (CT) `Element.id_suffix` added
//     1-Apr-2011 (CT) `Entity_List.max_child_idx` and `.new_child_idx` added
//     5-Apr-2011 (CT) `Element.remove` added
//    13-Apr-2011 (CT) `Element.new_child_idx` added (empty)
//    27-May-2011 (CT) `Field_Role_Hidden._setup_value` changed to set
//                     `value.edit` unconditionally
//    27-May-2011 (CT) `Entity_List.setup_value` redefined to set `anchor_id`
//                     and `root_id`
//     7-Jul-2011 (CT) `field_name_map` added
//    25-Jul-2011 (CT) `get_value` added
//    12-Sep-2011 (CT) `Field_Composite._setup_value` changed to update
//                     `anchor.field_name_map`
//     7-Oct-2011 (CT) Guard added to `Element._setup_value`
//    10-Oct-2011 (CT) `_clear_value` added to `Field` and `Field_Entity`
//    20-Oct-2011 (CT) `_clear_value` added to `Entity_Link`
//    16-Feb-2012 (CT) Factor `add` in `packed_values`, support `role_id` there
//    17-Feb-2012 (CT) Add `callback_map` to module `GTW.AFS`
//    17-Feb-2012 (CT) Add and use `Element._setup_callbacks`
//    ««revision-date»»···
//--

"use strict";

( function () {
    var Elements;
    var id_suffix_pat = /\d+$/;
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
                      } else if (name === "js_callbacks") {
                          this._setup_callbacks (value);
                      };
                      this [name] = value;
                  };
              };
              if (this ["$id"] !== undefined) {
                  Elements.id_map [this.$id] = this;
              };
          }
        , changed : function changed () {
              var i, l, child, has_value;
              has_value =
                  (  (this ["value"]  !== undefined)
                  && (this.value.edit !== undefined)
                  );
              if (has_value && this.value.init !== this.value.edit) {
                  // XXX `this.value.init !== this.value.edit` doesn't work
                  //     for objects
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
        , get_value : function get_value () {
              if ("value" in this) {
                  if ("edit" in this.value) {
                      return this.value.edit;
                  } else {
                      return this.value.init;
                  };
              };
              return undefined;
          }
        , id_suffix : function id_suffix () {
              var match = this.$id.match (id_suffix_pat);
              if (match !== null) {
                  return Number (match [0]);
              }
              return 65535;
          }
        , new_child_idx : function new_child_idx () {
              return null;
          }
        , remove : function remove () {
              var anchor = $GTW.AFS.Elements.get (this.anchor_id);
              var id     = this.$id;
              var i, l, child, k;
              if (this ["children"] !== undefined) {
                  for (i = 0, l = this.children.length; i < l; i += 1) {
                      child = this.child (i);
                      if (child) {
                          child.remove ();
                      }
                  }
              }
              if (anchor) {
                  delete anchor.value [id];
                  k = anchor.value ["$child_ids"].indexOf (id);
                  if (k >= 0) {
                      anchor.value ["$child_ids"].splice (k, 1);
                  }
              }
              k = Elements.root.roots.indexOf (this);
              if (k >= 0) {
                  Elements.root.roots.splice (k, 1);
              }
              delete Elements.id_map [id];
          }
        , setup_value : function setup_value (kw) {
              var i, l, child;
              var new_kw =
                  {anchor : kw.anchor, root : kw.root, roots : kw.roots};
              if (this ["value"] !== undefined) {
                  this._setup_value (kw, new_kw);
                  if (this.$id !== kw.anchor.$id) {
                      this.anchor_id = kw.anchor.$id;
                  }
              }
              if (this ["children"] !== undefined) {
                  for (i = 0, l = this.children.length; i < l; i += 1) {
                      child = this.child (i);
                      if (child) {
                          child.setup_value (new_kw);
                      }
                  }
              }
          }
        , _setup_callbacks : function _setup_callbacks (js_callbacks) {
              var cb_map = GTW.AFS.callback_map;
              for (var i = 0, li = js_callbacks.length, cb_spec; i < li; i++) {
                  cb_spec = js_callbacks [i];
                  if (cb_spec.cb_name in cb_map) {
                      cb_spec ["callback"] = cb_map [cb_spec.cb_name];
                  } else {
                      console.error ("Unkown callback referenced by", cb_spec);
                  };
              };
          }
        , _setup_value : function _setup_value (kw, new_kw) {
              if (this.$id !== kw.anchor.$id) {
                  var value = kw.anchor.value;
                  var k;
                  value [this.$id] = this.value;
                  // XXX inefficient !!!
                  k = value ["$child_ids"].indexOf (this.$id);
                  if (k < 0) {
                      value ["$child_ids"].push (this.$id);
                  }
              }
          }
        , _sv_anchored_or_root : function _sv_anchored_or_root (kw, new_kw) {
              new_kw.anchor = this;
              this.field_name_map = {};
              this.value.$id = this.$id;
              this.value.$child_ids = [];
              if (this.value ["init"] && ! this.value ["edit"]) {
                  this.value.edit = $GTW.inspect.copy (this.value.init);
              }
          }
        , _sv_anchored : function _sv_anchored (kw, new_kw) {
              if (this.$id !== kw.anchor.$id) {
                  this.value ["anchor_id"] = kw.anchor.$id;
              }
          }
        , _sv_root : function _sv_root (kw, new_kw) {
              this.root_id = kw.root.$id;
              kw.roots.push (this);
              new_kw.root = this;
          }
        }
      , { type_name : "Element" }
    );
    var Entity = Element.extend (
        { _setup_value : function _setup_value (kw, new_kw) {
              this._sv_anchored_or_root (kw, new_kw);
              this._sv_anchored         (kw, new_kw);
              this._sv_root             (kw, new_kw);
          }
        }
      , { type_name : "Entity" }
    );
    var Entity_Link = Element.extend (
        { _clear_value : function _clear_value () {
              this.value.edit.pid = null;
              this.value.edit.cid = null;
          }
        , _setup_value : function _setup_value (kw, new_kw) {
              this._sv_anchored_or_root (kw, new_kw);
              this._sv_root             (kw, new_kw);
          }
        }
      , { type_name : "Entity_Link" }
    );
    var Entity_List = Element.extend (
        { init : function init (spec) {
              var max_child_idx = -1;
              this._super (spec);
              if (this ["children"] !== undefined) {
                  for (var i = 0, li = this.children.length, child; i < li; i++) {
                      child = this.child (i);
                      max_child_idx = Math.max (max_child_idx, child.id_suffix ());
                  }
              }
              this.max_child_idx = max_child_idx;
          }
        , new_child_idx : function new_child_idx () {
              this.max_child_idx += 1; ;
              return this.max_child_idx;
          }
        , setup_value : function setup_value (kw) {
              this._super (kw);
              this.anchor_id = kw.anchor.$id;
              this.root_id   = kw.root.$id;
          }
        }
      , { type_name : "Entity_List" }
    );
    var Field = Element.extend (
        { _clear_value : function _clear_value () {
              this.value.edit = "";
          }
        , _setup_value : function _setup_value (kw, new_kw) {
              if (! this.value ["init"]) {
                  this.value.init = "";
              }
              this._super (kw, new_kw);
              kw.anchor.field_name_map [this.name] = this.$id;
          }
        }
      , { type_name : "Field" }
    );
    var Field_Composite = Element.extend (
        { _setup_value : function _setup_value (kw, new_kw) {
              this._sv_anchored_or_root (kw, new_kw);
              this._sv_anchored         (kw, new_kw);
              this._super               (kw, new_kw);
              kw.anchor.field_name_map [this.name] = this.$id;
          }
        }
      , { type_name : "Field_Composite" }
    );
    var Field_Entity = Element.extend (
        { _clear_value : function _clear_value () {
              this.value.edit.pid = null;
              this.value.edit.cid = null;
          }
        , _setup_value : function _setup_value (kw, new_kw) {
              this._sv_anchored_or_root (kw, new_kw);
              this._sv_anchored         (kw, new_kw);
              this._super               (kw, new_kw);
              kw.anchor.field_name_map [this.name] = this.$id;
          }
        }
      , { type_name : "Field_Entity" }
    );
    var Field_Role_Hidden = Element.extend (
        { _setup_value : function _setup_value (kw, new_kw) {
              var raid           = kw.root.anchor_id;
              this.value.role_id = raid;
              this.value.edit    = Elements.id_map [raid].value.edit;
              this._super (kw, new_kw);
              kw.anchor.field_name_map [this.name] = this.$id;
          }
        }
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
        , packed_values : function packed_values () {
              var i, l;
              var form     = this;
              var entities = arguments.length > 0 ? arguments : form.roots;
              var result   =
                  { $id        : form.$id
                  , sid        : form.value.sid
                  , $child_ids : []
                  };
              var add = function add (elem, result) {
                  var r;
                  result [elem.$id] = elem.value;
                  result.$child_ids.push (elem.$id);
                  if ("role_id" in elem.value) {
                      r = get (elem.value.role_id);
                      if (r) {
                          add (r, result);
                      };
                  };
              };
              for (i = 0, l = entities.length; i < l; i += 1) {
                  add (entities [i], result);
              }
              return result;
          }
        , setup_value : function setup_value () {
              var i, l, child;
              if (this ["children"] !== undefined) {
                  this.roots = [];
                  for (i = 0, l = this.children.length; i < l; i += 1) {
                      child = this.child (i);
                      child.setup_value
                          ({anchor : child, root : child, roots : this.roots});
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
        , callback_map          : {}
        }
    );
  } ()
);

// __END__ GTW/AFS/Elements.js
