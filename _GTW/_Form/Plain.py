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
#    GTW.Form.Plain
#
# Purpose
#    Handling of HTMl forms
#
# Revision Dates
#    30-Dec-2009 (MG) Creation
#    ««revision-date»»···
#--
from   _GTW               import GTW
import _GTW._Form._Field_Group_
import _GTW._Form.Field_Group
import  itertools

class Plain (GTW.Form._Field_Group_) :
    """Handling of plain HTML forms with user constricted field groups."""

    method       = "POST"
    parent       = None
    request_data = {}
    postfix      = None

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

    def get_id (self, field) :
        if self.postfix :
            return "_".join ((field.name, self.postfix))
        return field.name
    # end def get_id

# end class Plain

if __name__ != "__main__" :
    GTW.Form._Export ("*")
### __END__ GTW.Form.Plain
