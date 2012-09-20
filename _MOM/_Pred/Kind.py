# -*- coding: iso-8859-15 -*-
# Copyright (C) 2009-2012 Mag. Christian Tanzer. All rights reserved
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
#    MOM.Pred.Kind
#
# Purpose
#    Provide property classes for various predicate kinds
#
# Revision Dates
#    24-Sep-2009 (CT) Creation (factored from TOM.Pred.Kind)
#    25-Feb-2010 (CT) `check_pred_p` added (honoring `check_always`)
#    11-Mar-2010 (CT) `check_pred_p` removed (was a Bad Idea (tm))
#     2-Sep-2010 (CT) `Region` added
#    27-Apr-2012 (CT) Add `Region` to last paragraph of `__doc__`
#    12-Sep-2012 (CT) Add `__init__` argument `e_type`
#    ««revision-date»»···
#--

from   _TFL                  import TFL
from   _MOM                  import MOM

import _TFL._Meta.Property

import _MOM._Pred
import _MOM._Prop.Kind

class Kind (MOM.Prop.Kind) :
    """Root class of predicate kinds to used as properties for essential
       predicates of the MOM meta object model.
    """

    kind                  = None ### override in descendents
    pred                  = None
    prop                  = TFL.Meta.Alias_Property ("pred")
    Table                 = dict ()

    def __init__ (self, pred_type, e_type) :
        self.__super.__init__ (pred_type, e_type)
        self.attrs = set      (pred_type.attributes + pred_type.attr_none)
    # end def __init__

    def get_attr_value (self, obj, attr) :
        return getattr (obj, attr, None)
    # end def get_attr_value

    def check_predicate (self, obj, attr_dict = {}) :
        return self.pred (self, obj, attr_dict)
    # end def check_predicate

    _del = None
    _get = check_predicate
    _set = None

# end class Kind

class Object (Kind) :
    """Predicate kind for object-local invariant.

       Object predicates must be satisfied at all times. They can only refer
       to attributes of a single instance of the essential class or
       association for which the predicate is defined.

       Object predicates are checked whenever the value of one or more
       essential attributes is set or changed.
    """

    kind = "object"

    def __init__ (self, pred_type, e_type) :
        self.__super.__init__ (pred_type, e_type)
        assert "is_used" not in self.pred.guard_attr, \
            ( "System-dependent attribute `is_used` can't be used in guard "
              "of object invariant %s!"
            % self.name
            )
    # end def __init__

    def get_attr_value (self, obj, attr) :
        ### Don't want computed values here because they might
        ### refer to attribute values about to be changed (and thus
        ### trigger spurious predicate violations in `obj.set`)
        ### This is only a problem for object predicates, since they're the
        ### only ones that get automatically evaluated on a set operation
        if obj.raw_attr (attr) is not "" :
            return self.__super.get_attr_value (obj, attr)
    # end def get_attr_value

# end class Object

class Region (Kind) :
    """Predicate kind for region-wide invariant.

       Region predicates can refer to other objects and their predicates and
       must be satisfied before an object can be committed to the database.

       Region predicates are checked by `scope.commit` before attempting to
       actually do the commit. Some backends might move the checks of
       some regional predicates to the database engine, e.g., checks for
       uniqueness constraints.
    """

    kind = "region"

# end class Region

class System (Kind) :
    """Predicate kind for system-wide invariant.

       System predicates can refer to other objects and their predicates and
       must *not* be satisfied at all times.

       Many applications require that all system predicates are satisfied
       before some commands can be performed.
    """

    kind = "system"

# end class System

__doc__ = """
Class `MOM.Pred.Kind`
=====================

.. moduleauthor:: Christian Tanzer <tanzer@swing.co.at>

.. class:: Kind

    `MOM.Pred.Kind` is the root class of a hierarchy of classes defining the
    various kinds of predicates of essential classes. The predicate kind
    controls how a predicate is evaluated. Technically, `Kind` and its
    subclasses define Python `property` types.

    The kind of a concrete predicate is specified as one the properties of
    the :mod:`predicate's type<_MOM._Pred.Type>`. The kind
    class gets instantiated by :class:`~_MOM._Pred.Spec.Spec` which passes
    the `type` to the kind's `__init__`.

    This module provides three kinds of predicates: :class:`Object`,
    :class:`Region`, and :class:`System`. A specific application or
    application domain can define additional kinds of predicates by providing
    additional classes derived from :class:`Kind`.

.. autoclass:: Object
.. autoclass:: Region
.. autoclass:: System

"""

if __name__ != "__main__" :
    MOM.Pred._Export ("*")
### __END__ MOM.Pred.Kind
