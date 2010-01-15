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
#    GTW.Form._Field_Group_
#
# Purpose
#    Base class for field groups and forms
#
# Revision Dates
#    30-Dec-2009 (MG) Creation
#    ««revision-date»»···
#--
from   _TFL               import TFL
import _TFL._Meta.Object
import _TFL.NO_List
import _TFL.defaultdict

from   _GTW               import GTW
import _GTW._Form.Field
import _GTW._Form.Field_Error

class _Field_Group_ (TFL.Meta.Object) :
    """A group of field's which are part of a form."""

    def __init__ ( self) :
        self.field_errors = TFL.defaultdict     (GTW.Form.Error_List)
        self.errors       = GTW.Form.Error_List ()
    # end def __init__

    def get_errors (self, field = None) :
        if field :
            if not isinstance (field, basestring) :
                field = field.name
            return self.field_errors [field]
        ### return all errors which not related to a special field
        return self.errors
    # end def get_errors

    def get_raw (self, field) :
        if isinstance (field, basestring) :
            field = self.fields [field]
        return self.request_data.get (field.name, field.get_raw (self.instance))
    # end def get_raw

    @TFL.Meta.Once_Property
    def request_data (self) :
        if self.parent :
            return self.parent.request_data
        self.request_data
    # end def request_data

# end class _Field_Group_


if __name__ != "__main__" :
    GTW.Form._Export ("*")
### __END__ GTW.Form._Field_Group_
