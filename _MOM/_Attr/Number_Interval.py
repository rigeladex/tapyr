# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package MOM.Attr.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    MOM.Attr.Number_Interval
#
# Purpose
#    Factory for composite attribute types modelling an interval of numbers
#
# Revision Dates
#    28-Mar-2012 (CT) Creation (factored from un-DRY `Float_Interval`)
#    29-Mar-2012 (CT) Add `__module__` to `__class__` calls
#    29-Mar-2012 (CT) Rename `new_interval_attr_type` to `make`, add doctest
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   __future__            import unicode_literals

from   _MOM.import_MOM       import *
from   _MOM.import_MOM       import _A_Composite_, _A_Number_

import _TFL.Caller

_Ancestor_Essence = MOM.An_Entity

class _Interval_ (_Ancestor_Essence) :
    """Model an interval (lower, upper)."""

    ui_display_sep = " - "

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class lower (_A_Number_) :
            """Lower bound of interval."""

            kind               = Attr.Necessary

        # end class lower

        class upper (_A_Number_) :
            """Upper bound of interval."""

            kind               = Attr.Necessary

        # end class upper

        class center (_A_Number_) :
            """Center of interval."""

            kind               = Attr.Query
            query              = (Q.lower + Q.upper) * 0.5
            auto_up_depends    = ("lower", "upper")

        # end class center

        class length (_A_Number_) :
            """Length of interval."""

            kind               = Attr.Query
            query              = Q.upper - Q.lower
            auto_up_depends    = ("lower", "upper")

        # end class length

    # end class _Attributes

    class _Predicates (_Ancestor_Essence._Predicates) :

        _Ancestor = _Ancestor_Essence._Predicates

        class is_valid (Pred.Condition) :
            """The upper bound must be greater than the lower bound."""

            kind               = Pred.Object
            assertion          = "lower < upper"
            attributes         = ("lower", "upper")

        # end class is_valid

    # end class _Predicates

# end class _Interval_

def make (bounds_type, name = None) :
    """Make a new composite type and a new attribute type for `bounds_type`.

    >>> Int_Interval, A_Int_Interval = MOM.Attr.Number_Interval.make (A_Int)
    >>> Int_Interval
    <class 'MOM.Int_Interval' [Spec Essence]>
    >>> Int_Interval._Attributes.lower.mro () [:2]
    [<class 'Number_Interval.lower'>, <class '_MOM._Attr.Type.A_Int'>]
    >>> Int_Interval._Attributes.lower.P_Type
    <type 'int'>

    >>> Float_Interval._Attributes.lower.mro () [:2]
    [<class 'Number_Interval.lower'>, <class '_MOM._Attr.Type.A_Float'>]
    >>> Float_Interval._Attributes.lower.P_Type
    <type 'float'>

    >>> Frequency_Interval._Attributes.lower.mro () [:2]
    [<class 'Number_Interval.lower'>, <class '_MOM._Attr.Type.A_Freqency'>]
    >>> Frequency_Interval._Attributes.lower.P_Type
    <type 'float'>

    """
    if name is None and bounds_type.__name__.startswith ("A_") :
        name = bounds_type.__name__ [2:]
    def new_attr (_Attr, attr_name, module) :
        ancestor = getattr (_Attr, attr_name)
        return ancestor.__class__ \
            (attr_name, (bounds_type, ancestor), dict (__module__ = module))
    cls_name    = "%s_Interval" % (name, )
    module      = TFL.Caller.globals () ["__name__"]
    _Attributes = _Interval_._Attributes.__class__ \
        ( "_Attributes"
        , (_Interval_._Attributes, )
        , dict
            (  (n, new_attr (_Interval_._Attributes, n, module))
            for n in ("lower", "upper", "center", "length")
            )
        )
    Interval_Type =  _Interval_.__class__ \
        ( cls_name, (_Interval_, )
        , dict
            ( _Attributes = _Attributes
            , __doc__ = "Model an interval of %s values (lower, upper)."
                % (name.lower (), )
            , __module__ = module
            )
        )
    A_Interval_Type = _A_Composite_.__class__ \
        ( "A_%s" % (cls_name, ), (_A_Composite_, )
        , dict
            ( P_Type  = Interval_Type
            , typ     = cls_name
            , __doc__ =
                ( "Models an attribute holding a interval of %s "
                  "values (lower, upper)"
                % (name.lower (), )
                )
            , __module__ = module
            )
        )
    return Interval_Type, A_Interval_Type
# end def make

Float_Interval,     A_Float_Interval     = make (A_Float)
Frequency_Interval, A_Frequency_Interval = make (A_Freqency)

__all__ = tuple \
    (  k for (k, v) in globals ().iteritems ()
    if isinstance (v, MOM.Meta.M_Attr_Type) and not v.__name__ == "_Interval_"
    )

if __name__ != "__main__" :
    MOM.Attr._Export ("*")
    MOM.Attr._Export_Module ()
### __END__ MOM.Attr.Number_Interval
