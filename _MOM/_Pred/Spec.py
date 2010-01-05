# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009-2010 Mag. Christian Tanzer. All rights reserved
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
#    ««revision-date»»···
#--

from   _MOM                  import MOM
from   _TFL                  import TFL

import _MOM._Meta.M_Pred_Spec
import _MOM._Pred.Kind
import _MOM._Pred.Type
import _MOM._Prop.Spec

import _TFL._Meta.Property
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

    def __init__ (self, e_type) :
        self.__super.__init__ (e_type)
        self._attr_map = TFL.defaultdict (list)
        for n, a in e_type.attributes.iteritems () :
            self._setup_attr_checker (e_type, a)
        e_type.predicates = self._prop_dict
    # end def __init__

    def _kind_list_name (self, kind) :
        return "_p_%s" % kind
    # end def _kind_list_name

    def _setup_attr_checker (self, e_type, attr) :
        kind = (MOM.Pred.Object, MOM.Pred.System) [attr.electric]
        stem = "AC_check_%s" % (attr.name, )
        for i, (check, attr_none) in enumerate (attr._checkers ()) :
            name = "%s_%d" % (stem, i)
            checker = self._new_prop \
                ( name      = name
                , kind      = kind
                , prop_type = MOM.Pred.Attribute_Check
                    (name, attr.name, check, attr_none)
                , e_type    = e_type
                )
            self._setup_prop (e_type, name, kind.kind, checker)
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
