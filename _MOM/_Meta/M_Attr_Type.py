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
#    MOM.Meta.M_Attr_Type
#
# Purpose
#    Meta classes for MOM.Attr.Type classes
#
# Revision Dates
#    28-Sep-2009 (CT) Creation (factored from TOM.Meta.M_Attr_Type)
#    29-Sep-2009 (CT) `ckd_name` and `raw_name` added
#     7-Oct-2009 (CT) `M_Attr_Type_Named_Value` added
#     7-Oct-2009 (CT) `M_Attr_Type.__init__` changed to add `syntax`
#     9-Oct-2009 (CT) Handling of `default` and `raw_default` added
#    ««revision-date»»···
#--

from   _MOM                import MOM
from   _TFL                import TFL

import _MOM._Meta.M_Prop_Type

import _TFL._Meta.Once_Property

class M_Attr_Type (MOM.Meta.M_Prop_Type) :
    """Meta class for MOM.Attr.Type classes."""

    count = 0

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        M_Attr_Type.count += 1
        if not name.startswith (("_A_", "A_")) :
            cls.ckd_name = "__%s"     % (cls.name, )
            cls.raw_name = "__raw_%s" % (cls.name, )
        if not hasattr (cls, "syntax") :
            if not name.startswith (("_A_", "A_Attr_Type")) :
                ### Adding `syntax` here (instead of as a class attribute in
                ### `A_Attr_Type`) allows descendent meta classes to define a
                ### meta property for `syntax` (which would be hidden by the
                ### class attribute)
                cls.syntax = ""
        raw_default = dct.get ("raw_default")
        if raw_default :
            assert not cls.default, \
                ( "Can't specify both raw default and %s "
                  "and cooked default %s for %s"
                % (raw_default, cls.default, cls)
                )
            if cls.symbolic_ref_pat.match (raw_default) :
                cls._symbolic_default = True
            ### Can't precompute `default` from `raw_default`
        if cls.default is not None and not cls.raw_default :
            ### Precompute `raw_default` from `default`
            cls.raw_default = cls.as_string (cls.default)
    # end def __init__

# end class M_Attr_Type

class M_Attr_Type_Link_Role (M_Attr_Type) :
    """Meta class for MOM.Attr.A_Link_Role classes."""

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        if cls.role_type and dct.get ("role_name") is None :
            cls.role_name = cls.role_type.type_base_name.lower ()
    # end def __init__

# end class M_Attr_Type_Link_Role

class M_Attr_Type_Named_Value (M_Attr_Type) :
    """Meta class for MOM.Attr.A_Named_Value classes.

       `M_Attr_Type_Named_Value` adds Once_Property for `Elbat` (reverse
       mapping) for `Table` and for `syntax`, if these aren't defined by the
       descendent of `A_Named_Value`.
    """

    @TFL.Meta.Once_Property
    def Elbat (cls) :
        """Reversed mapping for `cls.Table`. Requires that `Table` is a
           unique mapping.
        """
        result = {None : ""}
        for i, v in cls.Table.iteritems () :
            if v in result :
                raise TypeError \
                    ( "Non-unique mapping for %s: "
                      "\n"
                      "    keys %r and %r both map to value '%s'."
                      "\n"
                      "Please specify reverse mapping `Elbat` manually."
                    % (cls, i, result [v], v)
                    )
            result [v] = i
        return result
    # end def Elbat

    @TFL.Meta.Once_Property
    def syntax (cls) :
        return \
            ( "The following string values are accepted as valid "
              "%s values: %s"
            % (cls.typ, ", ".join (sorted (cls.Table.iterkeys ())))
            )
    # end def syntax

# end class M_Attr_Type_Named_Value

class M_Attr_Type_Unit (M_Attr_Type) :
    """Meta class for MOM.Attr._A_Unit_ classes.

       `M_Attr_Type_Unit` defines the class attributes:

       .. attribute:: _default_unit

         The unit to be used if the user doesn't specify an explicit unit for
         the value of an attribute of this type.

       .. attribute:: syntax

         A description of the syntax for the attribute including the possible
         units and the default unit and the values of the optional class
         attributes `_syntax_spec_head` and `_syntax_spec_tail`, if defined
         in the class specifying the attribute type.
    """

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        if name != "_A_Unit_" :
            ud = getattr (cls, "_unit_dict",    None)
            if ud :
                for n, v in ud.iteritems () :
                    if v == 1.0 :
                        du = n
                        setattr (cls, "_default_unit", du)
                        break
                else :
                    du = None
                if du and ud [du] == 1.0 :
                    syntax = "\n".join \
                        ( [s for s in
                              ( getattr (cls, "_syntax_spec_head", "")
                              , "The default unit is %s. If you specify "
                                "another unit, it must be separated from "
                                "the number by at least one space."
                                "\n"
                                "You can use the following units: %s."
                                % (du, ", ".join (sorted (ud.iterkeys ())))
                              , getattr (cls, "_syntax_spec_tail", "")
                              ) if s
                          ]
                        )
                    setattr (cls, "syntax", syntax)
                elif __debug__ :
                    print \
                        ( "Attribute type %s doesn't specify a `_default_unit`"
                          "with value 1.0 in `_unit_dict`"
                        ) % name
            elif __debug__ :
                if not ud :
                    print \
                        ( "Attribute type %s doesn't specify a _unit_dict"
                        ) % name
    # end def __init__

# end class M_Attr_Type_Unit

__doc__ = """
Class `MOM.Meta.M_Attr_Type`
============================

.. moduleauthor:: Christian Tanzer <tanzer@swing.co.at>

.. autoclass:: M_Attr_Type
.. autoclass:: M_Attr_Type_Named_Value
.. autoclass:: M_Attr_Type_Unit

"""

if __name__ != "__main__" :
    MOM.Meta._Export ("*")
### __END__ MOM.Meta.M_Attr_Type
