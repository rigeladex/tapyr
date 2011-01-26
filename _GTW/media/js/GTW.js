//-*- coding: iso-8859-1 -*-
// Copyright (C) 2011 Mag. Christian Tanzer All rights reserved
// Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
// ****************************************************************************
// This file is part of the library GTW.
//
// This file is free software; you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation; either version 2 of the License, or
// (at your option) any later version.
//
// This file is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this file. If not, see <http://www.gnu.org/licenses/>.
// ****************************************************************************
//
//++
// Name
//    GTW
//
// Purpose
//    Provide a javascript class based on ideas of
//        http://dean.edwards.name/weblog/2006/03/base/
//    and
//        http://ejohn.org/blog/simple-javascript-inheritance/
//
//
// Revision Dates
//    25-Jan-2011 (CT) Creation
//    26-Jan-2011 (CT) `update_proto` factored, `update` added
//    ««revision-date»»···
//--

( function () {
    var Class        = function Class () {};
    var making_proto = false;
    var super_re     = /\bthis\._super\b/;
    var super_test   =
        ( super_re.test ((function () { this._super; }))
        ? function (v) { return super_re.test (v); }
        : function (v) { return true; }
        );
    var update_proto = function (dict, proto, base) {
        for (name in dict) {
            if (dict.hasOwnProperty (name)) {
                var d_value = dict [name];
                var b_value = base [name];
                var super_caller =
                    (  (typeof d_value == "function")
                    && (typeof b_value == "function")
                    && super_test (d_value)
                    );
                proto [name] =
                    ( super_caller
                    ? ( function (d_value, b_value) { // freeze closure values
                            return function () {
                                var result, saved_super = this._super;
                                try {
                                    this._super = b_value;
                                    result = d_value.apply (this, arguments);
                                } finally {
                                    this._super = saved_super;
                                };
                                return result;
                            };
                        }
                      ) (d_value, b_value)
                    : d_value
                    );
            };
        };
    };
    Class.extend = function (dict) {
        var base     = this.prototype;
        making_proto = true; // don't run `init` in `this.constructor`
        var proto    = new this ();
        making_proto = false;
        var result   = proto.constructor = function () {
            if (this === window) {
                throw new TypeError ("Needs to be called with new");
            };
            if (! making_proto && this.init) {
                this.init.apply (this, arguments);
                this.update = function (dict) {
                    update_proto.call (this, dict, this, {});
                    return this;
                };
            };
        };
        result.prototype = proto;
        result.extend    = this.extend;
        result.update    = this.update;
        update_proto.call (this, dict, proto, base);
        return result;
    };
    Class.update = function (dict) {
        update_proto.call (this, dict, this, this.prototype);
        return this;
    };
    $GTW = Class.extend ({}).update ({ Class : Class });
  }
) ();

/*

Field = $GTW.Class.extend ({ init : function (name, title) { this.name = name; this.title = title; }, show : function () { return (this.name + ": " + this.title); } });
P_Field = Field.extend ({ show : function () { return this._super () + " but more powerful!"; } });
P_Field.prototype instanceof Field
f = new Field ("a", "b")
pf = new P_Field ("gqu", "foo")
!(f instanceof P_Field) && ( f instanceof Field) && ( f instanceof Object)
(pf instanceof P_Field) && (pf instanceof Field) && (pf instanceof Object)

*/

// __END__ GTW.js
