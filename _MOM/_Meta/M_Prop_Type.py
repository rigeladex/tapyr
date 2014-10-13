# -*- coding: utf-8 -*-
# Copyright (C) 2009-2014 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package _MOM.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    MOM.Meta.M_Prop_Type
#
# Purpose
#    Base meta class for metaclasses for MOM.Attr.Type and MOM.Pred.Type
#
# Revision Dates
#    28-Sep-2009 (CT) Creation  (factored from TOM.Meta.M_Prop_Type)
#     5-Jan-2010 (CT) Use `TFL._Meta.M_Auto_Combine` as base class
#    12-Sep-2012 (CT) Add `dyn_doc_p`
#     4-Jun-2013 (CT) Try to take start value of `dyn_doc_p` from `dct`
#    14-Jun-2013 (CT) Change `dyn_doc_p` to dict
#    14-Jun-2013 (CT) Use `_doc_properties` in `__init__`, not literal in
#                     `__new__`  to normalize indent, update `dyn_doc_p`
#    10-Mar-2014 (CT) Improve grep-ability of `dyn_doc_p` update
#    10-Mar-2014 (CT) Factor `_i_rank` in here
#    26-Mar-2014 (CT) Add guard against double quotes in `_doc_properties`
#    ««revision-date»»···
#--

from   _MOM                import MOM
from   _TFL                import TFL

import _MOM._Meta
import _TFL._Meta.M_Auto_Combine
import _TFL.normalized_indent

class M_Prop_Type (TFL.Meta.M_Auto_Combine) :
    """Root of metaclasses for MOM.Attr.Type and MOM.Pred.Type"""

    count = 0

    def __new__ (meta, name, bases, dct) :
        doc = dct.get ("__doc__")
        if not doc :
            if "__doc__" in dct :
                del dct ["__doc__"]
        elif "description" not in dct :
            dct ["description"] = doc
        dct ["name"] = name
        return meta.__mc_super.__new__ (meta, name, bases, dct)
    # end def __new__

    def __init__ (cls, name, bases, dct) :
        M_Prop_Type.count += 1
        cls._i_rank        = M_Prop_Type.count
        cls.__m_super.__init__ (name, bases, dct)
        cls.dyn_doc_p = dyn_doc_p = dict (getattr (cls, "dyn_doc_p", {}))
        for n in cls._doc_properties :
            v = dct.get (n)
            if v :
                v = TFL.normalized_indent (v)
                setattr (cls, n, v)
                if "%(" in v :
                    dyn_doc_p [n] = v
                if '"' in v :
                    ### Double quotes in _doc_properties break generated HTML
                    ### like::
                    ###     """<input title="%s" ···>""" % (v, )
                    raise TypeError \
                        ( "Property `%s` of %s must not contain double quotes"
                        % (n, cls)
                        )
        if not cls.__doc__ :
            cls.__doc__ = cls.description
    # end def __init__

# end class M_Prop_Type

__doc__ = """
Class `MOM.Meta.M_Prop_Type`
============================

.. moduleauthor:: Christian Tanzer <tanzer@swing.co.at>

.. class:: M_Prop_Type

    `MOM.Meta.M_Prop_Type` provides the meta machinery for defining
    :class:`attribute<_MOM._Meta.M_Attr_Type.Root>` and
    :class:`predicate<_MOM._Meta.M_Pred_Type.M_Pred_Type>` types.

    `M_Prop_Type` adds the class attributes:

    .. attribute:: name

      The name of the property.

    `M_Prop_Type` normalizes the `__doc__`, `description` and `explanation`
    attributes:

    * It removes an empty `__doc__` attribute to allow inheritance (by
      default, each Python class gets an empty `__doc__` attribute if the
      class definition doesn't contain an explicit docstring).

    * It sets `description` to the value of `__doc__`, if the class
      definition contains an explicit docstring.

    * It normalizes the indentation of `description` and `explanation` by
      calling `TFL.normalized_indent`.

"""

if __name__ != "__main__" :
    MOM.Meta._Export ("*")
### __END__ MOM.Meta.M_Prop_Type
