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
#    MOM.Meta.M_Pred_Type
#
# Purpose
#    Meta classes for MOM.Pred.Type classes
#
# Revision Dates
#     1-Oct-2009 (CT) Creation (factored from TOM.Meta.M_Pred_Type)
#    16-Apr-2012 (CT) Fix stylo
#    ««revision-date»»···
#--

from   _MOM                import MOM
from   _TFL                import TFL

import _MOM._Meta.M_Prop_Type

class M_Pred_Type (MOM.Meta.M_Prop_Type) :
    """Meta class for :mod:`~_MOM._Pred.Type` classes.

       `M_Pred_Type` sets several class attributes needed by
       :class:`~_MOM._Pred.Kind.Kind`.

       `M_Pred_Type` converts all properties listed in `_force_tuple` from
       strings to tuples.
    """

    _force_tuple = \
        ( "attributes"
        , "attr_none"
        , "bvar_attr"
        , "guard_attr"
        , "parameters"
        )

    def __new__ (meta, name, bases, dict) :
        for a in meta._force_tuple :
            if a in dict and isinstance (dict [a], (str, unicode)) :
                dict [a] = (dict [a], )
        return super (M_Pred_Type, meta).__new__ \
            (meta, name, bases, dict)
    # end def __new__

# end class M_Pred_Type

class M_Pred_Type_Condition (M_Pred_Type) :
    """Meta class for :class:`~_MOM._Pred.Type.Condition`

       `M_Pred_Type_Condition` compiles `assertion` into `assert_code` and
       `guard` into `guard_code`.
    """

    def __init__ (cls, name, bases, dict) :
        cls.__m_super.__init__ (name, bases, dict)
        ### We must compile here even if `cls.assert_code` already exists.
        ### Otherwise overriding `assertion` would not work.
        ass = cls.assertion
        if ass:
            setattr (cls, "assert_code", compile (ass, ass, "eval"))
        guard = cls.guard
        if guard :
            if not getattr (cls, "guard_attr", None) :
                setattr (cls, "guard_attr", (guard, ))
            setattr (cls, "guard_code", compile (guard, guard, "eval"))
    # end def __init__

    def __str__  (cls) :
        return "%s : `%s'" % (cls.name, cls.assertion)
    # end def __str__

    def __repr__ (cls) :
        return '%s (%r, "%s", %r)' % \
            ( cls.__class__.__name__
            , cls.attributes
            , cls.assertion
            , cls.parameters
            )
    # end def __repr__

# end class M_Pred_Type_Condition

class M_Pred_Type_Quantifier (M_Pred_Type) :
    """Meta class for quantifier predicates.

       `M_Pred_Type_Quantifier` compiles several class attributes into code
       objects:

       .. attribute:: assert_code

         Compiled from `bvar` and `assertion`.

       .. attribute:: guard_code

         Compiled from `guard`, if any.

       .. attribute:: seq_code

         Compiled from `seq`

       .. attribute:: attr_code

         Compiled from `bvar` and `bvar_attr`, if any.
    """

    ### `this=this' is needed to make the object containing the quantifier
    ### visible inside the `lambda' evaluating the quantifier's `assertion'
    quantifier_fmt = "map (lambda %s, this=this : %s, seq)"

    def __init__ (cls, name, bases, dict) :
        cls.__m_super.__init__ (name, bases, dict)
        if cls.bvar and cls.assertion :
            quantifier = cls.quantifier_fmt % (cls.bvar, cls.assertion)
            setattr \
                ( cls, "assert_code"
                , compile (quantifier, quantifier, "eval")
                )
        guard = cls.guard
        if guard :
            if not getattr (cls, "guard_attr", None) :
                setattr (cls, "guard_attr", (guard, ))
            setattr (cls, "guard_code", compile (guard, guard, "eval"))
        if isinstance (cls.seq, basestring) :
            setattr (cls, "seq_code", compile (cls.seq, cls.seq, "eval"))
        if cls.bvar and cls.bvar_attr :
            one_element_code = \
                ( "'''%s''' %% (%s)"
                % ( "\n".join (("  %-10s : %%4s" % bv) for bv in cls.bvar_attr)
                  , ", ".join (cls.bvar_attr)
                  )
                )
            attr_code = \
                ( "map (lambda %s, this = this : (%s), seq)"
                % (cls.bvar, one_element_code)
                )
            setattr (cls, "attr_code", compile (attr_code, attr_code, "eval"))
    # end def __init__

    def __str__  (cls) :
        return "%s" % (cls.name, )
    # end def __str__

    def __repr__ (cls) :
        return '%s (%r, "%s", %r, %r)' % \
            ( cls.__class__.__name__
            , cls.bvar
            , cls.assertion
            , cls.seq
            , cls.description
            )
    # end def __repr__

# end class M_Pred_Type_Quantifier

class M_Pred_Type_N_Quantifier (M_Pred_Type_Quantifier) :
    """Meta class for :class:`~_MOM._Pred.Type.N_Quant`"""

    def __init__ (cls, name, bases, dict) :
        cls.__m_super.__init__ (name, bases, dict)
        if cls.lower_limit is not None and cls.upper_limit is None :
            setattr (cls, "upper_limit", cls.lower_limit)
    # end def __init__

# end class M_Pred_Type_N_Quantifier

class M_Pred_Type_U_Quantifier (M_Pred_Type_Quantifier) :
    """Meta class for :class:`~_MOM._Pred.Type.U_Quant`"""

    ### `this=this' is needed to make the object containing the quantifier
    ### visible inside the `lambda' evaluating the quantifier's `assertion'
    quantifier_fmt = "map (lambda %s, this=this : not (%s), seq)"

# end class M_Pred_Type_U_Quantifier

__doc__ = """
Class `MOM.Meta.M_Pred_Type`
============================

.. moduleauthor:: Christian Tanzer <tanzer@swing.co.at>

.. autoclass:: M_Pred_Type
.. autoclass:: M_Pred_Type_Condition
.. autoclass:: M_Pred_Type_Quantifier
.. autoclass:: M_Pred_Type_N_Quantifier
.. autoclass:: M_Pred_Type_U_Quantifier

"""

if __name__ != "__main__" :
    MOM.Meta._Export ("*")
### __END__ MOM.Meta.M_Pred_Type
