# -*- coding: iso-8859-15 -*-
# Copyright (C) 2009 Martin Glück. All rights reserved
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
#    DJO.Field_Description
#
# Purpose
#    Container to hold information about fields (in forms or models)
#
# Revision Dates
#     6-Jun-2009 (MG) Factored from `Formset_Description.py`
#    12-Aug-2009 (CT) `__repr__` added
#    ««revision-date»»···
#--

from   _TFL               import TFL
import _TFL._Meta.Object
from   _DJO               import DJO

class Field_Description (TFL.Meta.Object) :
    """Description of how a field should be rendered in a form (set)"""

    def __init__ (self, name, ** kw) :
        self.name = name
        self.__dict__.update (kw)
    # end def __init__

    def __repr__ (self) :
        return "<Field_Description %s>" % (self.name, )
    # end def __repr__

    def __str__ (self) :
        return self.name
    # end def __str__

# end class Field_Description

if __name__ != "__main__" :
    DJO._Export ("*")
### __END__ DJO.Field_Description
