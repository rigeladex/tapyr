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
#    MOM.Meta.M_Attr_Kind
#
# Purpose
#    Meta class for `MOM.Attr.Kind` properties
#
# Revision Dates
#    22-Oct-2009 (CT) Creation
#    ««revision-date»»···
#--
from   _TFL                  import TFL
from   _MOM                  import MOM

import _MOM._Meta.M_Prop_Kind

class M_Attr_Kind (MOM.Meta.M_Prop_Kind) :
    """Meta class for `MOM.Attr.Kind` properties of MOM meta object model."""

    def __init__ (cls, name, bases, dict) :
        cls.__m_super.__init__ (name, bases, dict)
        cls.kind_name = cls.__name__.replace ("Mixin", "").strip ("_")
    # end def __init__

# end class M_Attr_Kind

if __name__ != "__main__" :
    MOM.Meta._Export ("*")
### __END__ MOM.Meta.M_Attr_Kind
