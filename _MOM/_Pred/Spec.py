# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
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
#    ««revision-date»»···
#--

from   _MOM                  import MOM
from   _TFL                  import TFL

import _MOM._Meta.M_Pred_Spec
import _MOM._Pred.Kind
import _MOM._Pred.Type
import _MOM._Prop.Spec

import _TFL._Meta.Property

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
        for n, a in e_type.attributes.iteritems () :
            if a.is_primary :
                self._setup_attr_checker_1 \
                    ( e_type
                    , a
                    , "AC_check_%s_not_empty" % (a.name, )
                    , MOM.Pred.Object
                    , "value is not None and value != ''"
                    , (a.name, )
                    )
            if a.check and (a.kind != "outer") :
                self._setup_attr_checker (e_type, a)
        e_type.predicates = self._prop_dict
    # end def __init__

    def _kind_list_name (self, kind) :
        return "_p_%s" % kind
    # end def _kind_list_name

    def _setup_attr_checker (self, e_type, attr) :
        kind = (MOM.Pred.Object, MOM.Pred.System) [attr.electric]
        for i, check in enumerate (attr.check) :
            self._setup_attr_checker_1 \
                (e_type, attr, "AC_check_%s_%d" % (attr.name, i), kind, check)
    # end def _setup_attr_checker

    def _setup_attr_checker_1 (self, e_type, attr, name, kind, check, attr_none = ()) :
        checker = self._new_prop \
            ( name      = name
            , kind      = kind
            , prop_type = MOM.Pred.Attribute_Check
                (name, attr.name, check, attr_none)
            , e_type    = e_type
            )
        self._setup_prop (e_type, name, kind.kind, checker)
    # end def _setup_attr_checker_1

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
