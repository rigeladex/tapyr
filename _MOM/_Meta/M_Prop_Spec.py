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
#    MOM.Meta.M_Prop_Spec
#
# Purpose
#    Root meta class for for attribute-spec and predicate-spec metaclasses
#
# Revision Dates
#    29-Sep-2009 (CT) Creation (factored from TOM.Meta.M_Prop_Spec)
#    ««revision-date»»···
#--

from   _MOM                import MOM
from   _TFL                import TFL

import _TFL._Meta.M_Class
import _MOM._Meta.M_Prop_Type

class M_Prop_Spec (TFL.Meta.M_Class) :
    """Root meta class for for attribute-spec and predicate-spec metaclasses.
    """

    def m_setup_names (cls) :
        dict       = cls.__dict__
        _names     = {}
        _own_names = {}
        setattr (cls, "_names",     _names)
        setattr (cls, "_own_names", _own_names)
        for b in reversed (cls.__bases__) :
            _names.update (getattr (b, "_names", {}))
        for n, v in dict.iteritems () :
            if n.startswith ("_") and n.endswith ("_") :
                continue
            if isinstance (v, MOM.Meta.M_Prop_Type) :
                _names [n] = _own_names [n] = v
            elif v is None :
                _names [n] = _own_names [n] = None
            elif n in _names :
                raise cls._m_inconsistent_prop (n, v, _names, dict)
    # end def m_setup_names

# end class M_Prop_Spec

__doc__ = """
Class `MOM.Meta.M_Prop_Spec`
============================

.. moduleauthor:: Christian Tanzer <tanzer@swing.co.at>

.. class:: M_Prop_Spec

    `MOM.Meta.M_Prop_Spec` provides the meta machinery for defining
    :class:`attribute<_MOM._Meta.M_Attr_Spec.M_Attr_Spec>` and
    :class:`predicate<_MOM._Meta.M_Pred_Spec.M_Pred_Spec>` specifications.

    `M_Prop_Spec` gathers all class attributes of the `Spec` which are
    derived from the :class:`base property
    type<_MOM._Meta.M_Prop_Type.M_Prop_Type>` and puts them into the class
    attributes mapping property names to property values:

    .. attribute:: _names

      Dictionary with all locally defined *and* all inherited properties.

    .. attribute:: _own_names

      Dictionary with all locally defined properties.

    Setting a class variable to `None` in a derived `Spec` will remove the
    property from the `Spec`.
"""

if __name__ != "__main__" :
    MOM.Meta._Export ("*")
### __END__ MOM.Meta.M_Prop_Spec
