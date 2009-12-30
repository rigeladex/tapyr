# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Martin Glueck All rights reserved
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
#    GTW.Field_Group
#
# Purpose
#    A group of field which are part of a form
#
# Revision Dates
#    30-Dec-2009 (MG) Creation
#    ««revision-date»»···
#--
from   _TFL               import TFL
import _TFL._Meta.Object
import _TFL.NO_List
from   _GTW               import GTW
import _GTW.Field
import _GTW._Field_Group_

class Field_Group (GTW._Field_Group_) :
    """A group of field's which are part of a form."""

    widget = "form.jnj, field_group_div_seq"

    def __init__ (self, parent, * fields, ** kw) :
        self.parent       = parent
        self.fields       = TFL.NO_List (fields)
    # end def __init__

    def __iter__ (self) :
        return iter (self.fields)
    # end def __iter__

    @property
    def instance (self) :
        return self.parent.instance
    # end def instance

# end class Field_Group


if __name__ != "__main__" :
    GTW._Export ("*")
### __END__ GTW.Field_Group
