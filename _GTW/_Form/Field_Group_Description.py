# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009-2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
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
#    GTW.Form.Field_Group_Description
#
# Purpose
#    Abstract definition of a field group
#
# Revision Dates
#    30-Dec-2009 (MG) Creation
#    ««revision-date»»···
#--
from   _TFL               import TFL
import _TFL._Meta.Object
from   _GTW               import GTW
import _GTW._Form

class Field_Group_Description (TFL.Meta.Object) :
    """Abstract definition of a field group."""

    def __init__ (self, * fields, ** kw) :
        self.fields = fields
        self.__dict__.update (kw)
    # end def __init__

# end class Field_Group_Description

if __name__ != "__main__" :
    GTW.Form._Export ("*")
### __END__ GTW.Form.Field_Group_Description
