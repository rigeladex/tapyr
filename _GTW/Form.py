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
#    GTW.Form
#
# Purpose
#    Handling of HTMl forms
#
# Revision Dates
#    30-Dec-2009 (MG) Creation
#    ««revision-date»»···
#--
from   _GTW               import GTW
import _GTW._Field_Group_
import _GTW.Field_Group
import  itertools

class Form (GTW._Field_Group_) :
    """Handling of HTML forms"""

    method       = "POST"
    parent       = None
    request_data = {}

    def __init__ ( self, action, instance
                 , *  field_group_descriptions
                 , ** kw
                 ) :
        self.action       = action
        self.instance     = instance
        self.__dict__.update (kw)
        self.field_groups = []
        added_fields      = set ()
        for fgd in field_group_descriptions :
            fgs = fgd.field_groups (self, added_fields)
            self.field_groups.extend (fgs)
    # end def __init__

    def __iter__ (self) :
        return iter (self.field_groups)
    # end def __iter__

# end class Form

if __name__ != "__main__" :
    GTW._Export ("*")
### __END__ GTW.Form
