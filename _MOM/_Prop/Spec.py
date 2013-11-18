# -*- coding: utf-8 -*-
# Copyright (C) 2009-2013 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package _MOM.
#
# This module is free software; you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this library. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    MOM.Prop.Spec
#
# Purpose
#    Base class for attribute and predicate specification
#
# Revision Dates
#    30-Sep-2009 (CT) Creation (factored from TOM.Property_Spec)
#     6-Oct-2009 (CT) `_create_properties` changed to include inherited
#                     properties into `_prop_dict` and `_prop_kind`
#     6-Oct-2009 (CT) `setattr` call moved from `_setup_prop` to `_add_prop`
#    13-Oct-2009 (CT) Bug fixes
#    21-Oct-2009 (CT) `_setup_attr_checker_1` factored and used to add a
#                     checker for primary attributes not being empty
#    22-Oct-2009 (CT) `_effective_prop_kind_mixins` factored
#    22-Oct-2009 (CT) Use `kind_name`
#     4-Feb-2010 (CT) Argument `e_type` added to `_effective_prop_kind_mixins`
#    26-May-2010 (CT) `__init__` changed to copy `_own_names` and `_names`
#                     from (essential) class to (app-type specific) instance
#    14-Oct-2010 (CT) `Kind_Mixins` added as `Spec` variable
#    22-Dec-2011 (CT) Change `_effective_prop_kind` to set `kind` to `kind.kind`
#    12-Sep-2012 (CT) Add `e_type` to `kind.__init__`
#    29-Jan-2013 (CT) Factor `_sort_properties`
#    11-Mar-2013 (CT) Add `fix_doc`
#     3-Jun-2013 (CT) Assign `_prop_dict` to attribute named by `_prop_map_name`
#     3-Jun-2013 (CT) Change argument of `fix_doc` from `e_type` to `et_scope`
#     6-Jun-2013 (CT) Use `prop.assign`, not `setattr`, to assign to `e_type`
#    ««revision-date»»···
#--

from   _MOM                  import MOM
from   _TFL                  import TFL
from   _TFL.pyk              import pyk

import _MOM._Meta.M_Prop_Spec
import _MOM._Prop

import _TFL._Meta.Object
import _TFL.Sorted_By

import itertools

class _Prop_Spec_ (TFL.Meta.Object) :
    """Base class for attribute and predicate specification."""

    __metaclass__       = MOM.Meta.M_Prop_Spec
    _real_name          = "Spec"
    _lists_to_combine   = ("Kind_Mixins", )

    Kind_Mixins         = ()

    _prop_dict_cls      = dict
    _mixed_kinds        = dict ()

    def __init__ (self, e_type) :
        self._own_names  = dict  (self._own_names) ### class to instance
        self._names      = dict  (self._names)     ### class to instance
        self._create_prop_dict  (e_type)
        self._create_properties (e_type)
        self._sort_properties   (e_type)
        setattr (e_type, self._prop_map_name, self._prop_dict)
    # end def __init__

    def fix_doc (self, et_scope) :
        for p in self._prop_dict.itervalues () :
            p.prop.fix_doc (et_scope)
            if p.prop.description :
                p.__doc__ = p.prop.description
    # end def fix_doc

    def _add_prop (self, e_type, name, prop_type) :
        kind = self._effective_prop_kind (name, prop_type, e_type)
        prop = None
        if kind is not None :
            prop = self._new_prop (name, kind, prop_type, e_type)
            self._setup_prop      (e_type, name, kind.kind, prop)
        prop.assign (e_type, name)
        return prop
    # end def _add_prop

    def _create_prop_dict (self, e_type) :
        self._prop_dict = self._prop_dict_cls ()
        self._prop_kind = dict ((k, []) for k in self._Prop_Pkg.Kind.Table)
        for n, v in self._prop_kind.iteritems () :
            setattr (e_type, self._kind_list_name (n), v)
    # end def _create_prop_dict

    def _create_properties (self, e_type) :
        for n, prop_type in self._own_names.iteritems () :
            if prop_type is not None :
                self._add_prop (e_type, n, prop_type)
        base_props = {}
        for b in e_type.__bases__ [::-1] :
            bps = getattr (b, self._prop_map_name, {})
            base_props.update (bps)
        for n, prop_type in self._names.iteritems () :
            if n not in self._prop_dict :
                ### Inherited property: include in `_prop_dict` and `_prop_kind`
                prop = base_props.get (n)
                if prop is not None :
                    self._setup_prop (e_type, n, prop.kind, prop)
    # end def _create_properties

    def _effective_prop_kind (self, name, prop_type, e_type) :
        kind = result = getattr (prop_type, "kind", None)
        kind_mixins   = self._effective_prop_kind_mixins \
            (name, kind, prop_type, e_type)
        if kind is not None and kind_mixins :
            kinds = tuple (kind_mixins) + (kind, )
            try :
                result = self._mixed_kinds [kinds]
            except KeyError :
                result = self._mixed_kinds [kinds] = kind.__class__ \
                    ( "__".join (k.kind_name for k in reversed (kinds))
                    , kinds
                    , dict
                        ( __module__ = kind.__module__
                        , kind       = kind.kind
                        )
                    )
        return result
    # end def _effective_prop_kind

    def _effective_prop_kind_mixins (self, name, kind, prop_type, e_type) :
        return tuple (getattr (prop_type, "Kind_Mixins", ())) + self.Kind_Mixins
    # end def _effective_prop_kind_mixins

    def _kind_list_name (self, kind) :
        return kind
    # end def _kind_list_name

    def _new_prop (self, name, kind, prop_type, e_type) :
        return kind (prop_type, e_type)
    # end def _new_prop

    def _setup_prop (self, e_type, name, kind, prop) :
        self._prop_dict [name] = prop
        self._prop_kind [kind].append (prop)
    # end def _setup_prop

    def _sort_properties (self, e_type) :
        for pk in self._prop_kind.itervalues () :
            pk.sort (key = TFL.Sorted_By ("rank", "name"))
    # end def _sort_properties

Spec = _Prop_Spec_ # end class

if __name__ != "__main__" :
    MOM.Prop._Export ("*")
### __END__ MOM.Prop.Spec
