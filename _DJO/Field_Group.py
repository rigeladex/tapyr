# -*- coding: iso-8859-1 -*-
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
#    DJO.Field_Group
#
# Purpose
#    Handling of field_groups within forms
#
# Revision Dates
#     6-Jun-2009 (MG) Creation (factored from Field_Group_Description)
#    11-Jun-2009 (CT) `Form_Mixins` added to `Nested_Form_Field_Group`
#    11-Jun-2009 (CT) `Bound_Nested_Form_Field_Group` adapted to pass `request`
#                     to `nested_form_class`
#    15-Jun-2009 (MG) `Bound_Nested_Form_Field_Group.__init__` use `request`
#                     instead of passing data and files
#    16-Jun-2009 (MG) Only pass `widget`to formfields if really set
#    17-Jun-2009 (MG) `Bound_Nested_Form_Field_Group.__init__` pass
#                     `empty_permitted` to form to allow empty forms
#                     `save_and_assign` only set instances which have a
#                     primary key (are saved to the database)
#    18-Jun-2009 (CT) `Bound_Nested_Form_Field_Group.__init__` changed to
#                     consider `min_required` for `form_count`
#    19-Jun-2009 (MG) Nested parts factored into `Nested_Form_Group`
#    29-Jul-2009 (CT) Once_Property `Bound_Field` factored
#    ««revision-date»»···
#--

from   _TFL                          import TFL
import _TFL._Meta.Object
from   _TFL._Meta.Once_Property      import Once_Property
from   _TFL.predicate                import all_true
from   _DJO                          import DJO
import _DJO.Field_Group_Description

class Bound_Field_Group (TFL.Meta.Object) :
    """A field_group bound to an instance of a Form"""

    def __init__ (self, field_group, form) :
        self.field_group = field_group
        self.form        = form
    # end def __init__

    @Once_Property
    def Bound_Field (self) :
        from django.forms.forms import BoundField
        return BoundField
    # end def Bound_Field

    def __getattr__ (self, name) :
        return getattr (self.field_group, name)
    # end def __getattr__

    def __iter__ (self) :
        BF = self.Bound_Field
        for field in self.field_group.fields :
            yield BF (self.form, field, field.name)
    # end def __iter__

# end class Bound_Field_Group

class _Field_Group_ (TFL.Meta.Object) :
    """Base class for field_group's"""

    Bound_Field_Group = Bound_Field_Group

    def __init__ (self, model, fgd = None) :
        self.model                   = model
        self.field_group_description = fgd or DJO.Field_Group_Description ()
        self.fields                  = []
    # end def __init__

    def __call__ (self, form) :
        return self.Bound_Field_Group (self, form)
    # end def __call__

    def __getattr__ (self, name) :
        return getattr (self.field_group_description, name)
    # end def __getattr__

    def __iter__ (self) :
        return iter (self.fields)
    # end def __iter__

# end class _Field_Group_

class Field_Group (_Field_Group_) :
    """A Field_Group binds a form set description to an model."""

    def __init__ (self, model, fgd = None, used_fields = set ()) :
        self.__super.__init__ (model, fgd)
        _F = model._F
        for fd in fgd.fields or [f.name for f in _F if f.editable] :
            name = str (fd)
            if name in fgd.exclude :
                continue
            used_fields.add (name)
            dj_field          = _F [name]
            kw                = dict ()
            form_field_class  = getattr (fd, "form_field_class", None)
            ### the following attribues must not be passed to `formfield` if
            ### they have not been specified in the field definition to
            ### ensure the proper default
            for attr in "form_class", "required", "widget":
                value = getattr (fd, attr, None)
                if value is not None :
                    kw [attr] = value
            fo_field  = dj_field.formfield (** kw)
            if fo_field :
                ### we need to set the name for the form-field because we
                ### need to use the TFL.NO_list to keep the order but a
                ### NO_List needs a `name`
                fo_field.name = dj_field.name
                self.fields.append (fo_field)
    # end def __init__

# end class Field_Group

if __name__ != "__main__" :
    DJO._Export ("*", "_Field_Group_")
### __END__ DJO.Field_Group
