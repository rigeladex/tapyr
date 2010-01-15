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
from   _TFL               import TFL
import _TFL.I18N
import _TFL._Meta.Once_Property

from   _GTW               import GTW
import _GTW._Form._Field_Group_
import _GTW._Form.Field_Group

class Plain (GTW.Form._Field_Group_) :
    """Handling of plain HTML forms with user constricted field groups."""

    method       = "POST"
    parent       = None
    postfix      = None

    def __init__ ( self, action, instance
                 , *  field_group_descriptions
                 , ** kw
                 ) :
        self.__super.__init__ ()
        self.request_data = {}
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

    def __call__ (self, request_data, errors = (), field_errors = {}) :
        self.request_data.update (request_data)
        self.errors.add          (errors)
        for k, v in field_errors.iteritems () :
            self.field_errors [k].add (v)
        return len (self.errors) + len (self.field_errors)
    # end def __call__

    def get_field ( self, field_name
                  , field_errors = None
                  , error_text   = None
                  , as_list      = False
                  ) :
        value = self.request_data.get (field_name, None)
        if not value and field_errors is not None :
            error_text = error_text or TFL.I18N._T \
                    (u"Field `%(field)s` is required")
            field_errors [field_name].append \
                (error_text % dict (field = field_name))
        if value and not as_list :
            return value [0]
        return value
    # end def get_field

# end class Plain

if __name__ != "__main__" :
    GTW.Form._Export ("*")
### __END__ GTW.Form.Plain
