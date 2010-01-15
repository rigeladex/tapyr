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
#    GTW.Form.MOM.Instance
#
# Purpose
#    A form which creates/changes a MOM entity
#
# Revision Dates
#    30-Dec-2009 (MG) Creation
#    ««revision-date»»···
#--
from   _TFL               import TFL
import _TFL._Meta.Object

from   _MOM               import MOM
import _MOM.Entity
import _MOM._Attr.Type

from   _GTW               import GTW
import _GTW._Form._MOM
import _GTW._Form.Plain

import  itertools

class Field_Group_Description (TFL.Meta.Object) :
    """A field group which derives it's fields from an MOM.Entity"""

    def __init__ (self, e_type, * fields) :
        self.e_type             = e_type
        self.fields             = list (fields or ("*", ))
        self._contains_wildcard = "*" in self.fields
    # end def __init__

    def field_groups (self, parent, added_fields = None, ** kw) :
        if added_fields is None :
            added_fields = set ()
        e_type           = self.e_type
        if self._contains_wildcard :
            if len (self.fields) == 1 :
                return itertools.chain \
                    (* (   self.__class__
                             (e_type, * (ak.name for ak in attrs)
                             ).field_groups (parent, added_fields, ** kw)
                       for attrs in (e_type.primary, e_type.user_attr)
                       )
                    )
            else :
                self._contains_wildcard = False
                wildcard_pos            = self.fields.index ("*")
                field_names             = set (self.fields)
                missing_fields          = \
                    [   ak.name
                    for ak in sorted
                       ( itertools.chain (e_type.primary, e_type.user_attr)
                       , key = lambda ak : ak.rank
                       )
                        if ak.name not in field_names
                    ]
                self.fields [wildcard_pos : wildcard_pos + 1] = missing_fields
                added_fields.update (self.fields)
        else :
                added_fields.update (self.fields)
        return \
            ( GTW.Form.Field_Group
                ( parent
                , * [getattr (e_type, an) for an in self.fields]
                , ** kw
                )
            ,
            )
    # end def field_groups

# end class Field_Group_Description

class Instance (GTW.Form.Plain) :
    """A form to create/edit MOM entities."""

    def __init__ ( self, action, e_type_or_instance
                 ,  * field_group_descriptions
                 , ** kw
                 ) :
        e_type   = e_type_or_instance
        instance = e_type_or_instance
        if isinstance (e_type_or_instance, MOM.Entity) :
            e_type   = instance.__class__
        else :
            instance = None
        self.e_type  = e_type
        if not field_group_descriptions :
            field_group_descriptions = \
                (GTW.Form.MOM.Field_Group_Description (e_type), )
        self.__super.__init__ \
            (action, instance, * field_group_descriptions, ** kw)
    # end def __init__

    def __call__ (self, request_data) :
        self.request_data = request_data
    # end def __call__

# end class Instance

MOM.Attr.A_Attr_Type.widget = "html/field.jnj, string"

if __name__ != "__main__" :
    GTW.Form.MOM._Export ("*")
### __END__ GTW.Form.MOM.Instance
