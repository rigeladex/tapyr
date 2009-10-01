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
#    ««revision-date»»···
#--

from   _MOM                import MOM
from   _TFL                import TFL

import _MOM._Meta.M_Prop_Type

class M_Attr_Type (MOM.Meta.M_Prop_Type) :
    """Meta class for MOM.Attr.Type classes."""

    count = 0

    def __init__ (cls, name, bases, dict) :
        cls.__m_super.__init__ (name, bases, dict)
        M_Attr_Type.count += 1
        if not name.startswith (("_A_", "A_")) :
            cls.ckd_name = "__%s"     % (cls.name, )
            cls.raw_name = "__raw_%s" % (cls.name, )
    # end def __init__

# end class M_Attr_Type

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

    def __init__ (cls, name, bases, dict) :
        cls.__m_super.__init__ (name, bases, dict)
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
.. autoclass:: M_Attr_Type_Unit

"""

if __name__ != "__main__" :
    MOM.Meta._Export ("*")
### __END__ MOM.Meta.M_Attr_Type
