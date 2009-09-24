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
#    MOM.Attr.Spec
#
# Purpose
#    Attribute specification for essential entities of the MOM meta object model
#
# Revision Dates
#    24-Sep-2009 (CT) Creation (factored from TOM.Attr.Spec)
#    ««revision-date»»···
#--

from   _TFL                  import TFL
from   _MOM                  import MOM

import _TFL._Meta.M_Class
import _TFL._Meta.Property

import _MOM._Attr.Type
import _MOM._Attr.Kind

if __name__ != "__main__" :
    MOM.Attr._Export ("*")
### __END__ MOM.Attr.Spec
