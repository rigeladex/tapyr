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
#    MOM.Pred.Spec
#
# Purpose
#    Predicate specification for essential entities of the MOM meta object model
#
# Revision Dates
#     1-Oct-2009 (CT) Creation (factored from TOM.Pred.Spec)
#    25-Nov-2009 (CT) `_attr_map` added
#     5-Jan-2010 (CT) `_setup_attr_checker` and `__init__` refactored to use
#                     `attr._checkers` instead of home-grown code
#     4-Feb-2010 (CT) Argument `e_type` added to `_checkers`
#     8-Nov-2011 (CT) Remove `attr_none` from `_setup_attr_checker`
#    12-Aug-2012 (CT) Add `MOM.Pred.Unique.New_Pred`
#    29-Jan-2013 (CT) Change prefix in `_kind_list_name` to `P_` (was `_p_`)
#    29-Jan-2013 (CT) Fix `MOM.Pred.Unique.New_Pred`
#    29-Jan-2013 (CT) Move predicate creation to redefined `_create_properties`
#    29-Jan-2013 (CT) Add `uniqueness_dbw` and `uniqueness_ems`
#    31-May-2013 (CT) Factor `_prop_map_name`
#    ««revision-date»»···
#--

from   _MOM                  import MOM
from   _TFL                  import TFL

import _MOM._Meta.M_Pred_Spec
import _MOM._Pred.Kind
import _MOM._Pred.Type
import _MOM._Prop.Spec

import _TFL._Meta.Property
import _TFL._Meta.Once_Property
import _TFL.defaultdict

class Spec (MOM.Prop.Spec) :
    """Predicate specification for MOM entities (objects and links).

       A :class:`~_MOM.Entity.Entity` class contains a descendent of `Spec`
       with declarations for all predicates (which are descendents of
       MOM.Pred._Condition_) provided by that class.

       :class:`MOM.Meta.M_E_Type<_MOM._Meta.M_Entity.M_E_Type>` instantiates
       the `Spec`: this results in the assignment of all predicate properties
       to the `E_Type`.
    """

    __metaclass__   = MOM.Meta.M_Pred_Spec

    _Prop_Pkg       = MOM.Pred
    _Prop_Spec_Name = "_Predicates"
    _prop_dict      = TFL.Meta.Alias_Property ("_pred_dict")
    _prop_kind      = TFL.Meta.Alias_Property ("_pred_kind")
    _prop_map_name  = "predicates"

    @TFL.Meta.Once_Property
    def uniqueness_dbw (self) :
        """Uniqueness predicates checked by `DBW`"""
        return list (u for u in self.uniqueness if not u.ems_check)
    # end def uniqueness_dbw

    @TFL.Meta.Once_Property
    def uniqueness_ems (self) :
        """Uniqueness predicates checked by `EMS`"""
        return list (u for u in self.uniqueness if u.ems_check)
    # end def uniqueness_ems

    def __init__ (self, e_type) :
        self.__super.__init__ (e_type)
        self._attr_map    = TFL.defaultdict (list)
        self.uniqueness   = e_type.P_uniqueness
    # end def __init__

    def _create_properties (self, e_type) :
        self.__super._create_properties (e_type)
        for n, a in e_type.attributes.iteritems () :
            self._setup_attr_checker (e_type, a)
        if e_type.epk_sig :
            uniq_epk = MOM.Pred.Unique.New_Pred \
                ( * e_type.epk_sig
                , name_suffix = "epk"
                , rank        = -100
                , __module__  = e_type.__module__
                )
            self._add_prop (e_type, uniq_epk.name, uniq_epk)
    # end def _create_properties

    def _kind_list_name (self, kind) :
        return "P_%s" % kind
    # end def _kind_list_name

    def _setup_attr_checker (self, e_type, attr) :
        kind = (MOM.Pred.Object, MOM.Pred.System) [attr.electric]
        stem = "AC_check_%s" % (attr.name, )
        for i, check in enumerate (attr._checkers (e_type)) :
            if isinstance (check, basestring) :
                name      = "%s_%d" % (stem, i)
                c_kind    = kind
                prop_type = MOM.Pred.Attribute_Check (name, attr.name, check)
            else :
                prop_type = check
                c_kind    = check.kind
                name      = check.name
            if prop_type is not None :
                checker = self._new_prop \
                    ( name      = name
                    , kind      = c_kind
                    , prop_type = prop_type
                    , e_type    = e_type
                    )
                self._setup_prop (e_type, name, c_kind.kind, checker)
            else :
                print e_type, attr, check
    # end def _setup_attr_checker

# end class Spec

__doc__ = """
Class `MOM.Pred.Spec`
=====================

.. moduleauthor:: Christian Tanzer <tanzer@swing.co.at>

.. autoclass:: Spec

"""

if __name__ != "__main__" :
    MOM.Pred._Export ("*")
### __END__ MOM.Pred.Spec
