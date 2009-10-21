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
#    MOM.Meta.M_Prop_Type
#
# Purpose
#    «text»···
#
# Revision Dates
#    28-Sep-2009 (CT) Creation  (factored from TOM.Meta.M_Prop_Type)
#    ««revision-date»»···
#--

from   _MOM                import MOM
from   _TFL                import TFL

import _MOM._Meta
import _TFL._Meta.M_Class
import _TFL.normalized_indent

class M_Prop_Type (TFL.Meta.M_Class_SW) :
    """Root of metaclasses for MOM.Attr.Type and MOM.Pred.Type"""

    def __new__ (meta, name, bases, dct) :
        doc = dct.get ("__doc__")
        if not doc :
            if "__doc__" in dct :
                del dct ["__doc__"]
        elif "description" not in dct :
            dct ["description"] = doc
        for n in "description", "explanation", "syntax":
            if n in dct :
                dct [n] = TFL.normalized_indent (dct [n])
        dct ["name"]         = name
        return super (M_Prop_Type, meta).__new__ (meta, name, bases, dct)
    # end def __new__

    def __init__ (cls, name, bases, dict) :
        cls.__m_super.__init__ (name, bases, dict)
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
    :class:`attribute<_MOM._Meta.M_Attr_Type.M_Attr_Type>` and
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
