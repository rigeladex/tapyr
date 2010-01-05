# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package _MOM.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
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
#    ««revision-date»»···
#--

from   _MOM                  import MOM
from   _TFL                  import TFL

import _MOM._Meta.M_Prop_Spec
import _MOM._Prop

import _TFL._Meta.Object
import _TFL.Sorted_By

class _Prop_Spec_ (TFL.Meta.Object) :
    """Base class for attribute and predicate specification."""

    __metaclass__  = MOM.Meta.M_Prop_Spec
    _real_name     = "Spec"
    _prop_dict_cls = dict

    _mixed_kinds   = dict ()

    def __init__ (self, e_type) :
        self._create_prop_dict  (e_type)
        self._create_properties (e_type)
    # end def __init__

    def _add_prop (self, e_type, name, prop_type) :
        kind = self._effective_prop_kind (name, prop_type)
        prop = None
        if kind is not None :
            prop = self._new_prop (name, kind, prop_type, e_type)
            self._setup_prop      (e_type, name, kind.kind, prop)
        setattr (e_type, name, prop)
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
        for n, prop_type in self._names.iteritems () :
            if n not in self._prop_dict :
                ### Inherited property: include in `_prop_dict` and `_prop_kind`
                prop = getattr (e_type, n, None)
                if prop is not None :
                    self._setup_prop (e_type, n, prop.kind, prop)
        for pk in self._prop_kind.itervalues () :
            pk.sort (key = TFL.Sorted_By ("rank", "name"))
    # end def _create_properties

    def _effective_prop_kind (self, name, prop_type) :
        kind = result = getattr (prop_type, "kind", None)
        kind_mixins   = self._effective_prop_kind_mixins \
            (name, kind, prop_type)
        if kind is not None and kind_mixins :
            kinds = tuple (kind_mixins) + (kind, )
            try :
                result = self._mixed_kinds [kinds]
            except KeyError :
                result = self._mixed_kinds [kinds] = kind.__class__ \
                    ( "__".join (k.kind_name for k in reversed (kinds))
                    , kinds
                    , dict (__module__ = kind.__module__)
                    )
        return result
    # end def _effective_prop_kind

    def _effective_prop_kind_mixins (self, name, kind, prop_type) :
        return tuple (getattr (prop_type, "Kind_Mixins", ()))
    # end def _effective_prop_kind_mixins

    def _kind_list_name (self, kind) :
        return kind
    # end def _kind_list_name

    def _new_prop (self, name, kind, prop_type, e_type) :
        return kind (prop_type)
    # end def _new_prop

    def _setup_prop (self, e_type, name, kind, prop) :
        self._prop_dict [name] = prop
        self._prop_kind [kind].append (prop)
    # end def _setup_prop

Spec = _Prop_Spec_ # end class

if __name__ != "__main__" :
    MOM.Prop._Export ("*")
### __END__ MOM.Prop.Spec
