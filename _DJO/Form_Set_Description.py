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
#    DJO.Form_Set_Description
#
# Purpose
#    Classes to describe form set's and the handling for fromset in forms
#
# Revision Dates
#    29-May-2009 (MG) Creation
#    29-May-2009 (MG) `_setup_fields` corrected, order if initialization fixed
#    02-Jun-2009 (MG) `exclude`and `used_fields` added
#     2-Jun-2009 (MG) `model`no longer a property, `setup_fields` is not an API
#     2-Jun-2009 (MG) `setup_fields`: Parameter `used_fields` added, support
#                     for wildcard field * added
#     2-Jun-2009 (MG) `Field_Description` added
#     4-Jun-2009 (MG) Reorganized: `Form_Set` and `Bound_Form_Set` factored
#                     out of `Form_Set_Description`
#     5-Jun-2009 (MG) `Form_Set.__init__` honor `required` of field
#                     description
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

    def __str__ (self) :
        return self.name
    # end def __str__

# end class Field_Description

class Form_Set_Description (TFL.Meta.Object) :
    """Describes a part of a form used to create/edit a Django model"""

    template = None

    def __init__ (self, * fields, ** kw) :
        self.exclude  = set (kw.pop ("exclude", ()))
        self.fields   = fields
        self.__dict__.update (kw)
    # end def __init__

    def __call__ (self, model = None, used_fields = set ()) :
        return DJO.Form_Set (model or self.model, self, used_fields)
    # end def __call__

# end class Form_Set_Description

class Form_Set (TFL.Meta.Object) :
    """A Form_Set binds a form set description to an model."""

    def __init__ (self, model, fsd = None, used_fields = ()) :
        self.model                = model
        self.form_set_description = fsd
        _F                        = model._F
        if not fsd :
            fsd                   = DJO.Field_Description ()
        exclude                   = fsd.exclude
        self.fields               = []
        fields                    = fsd.fields
        if (   (len (fields) == 1)
           and (fields [0]   == "*")
           ) :
            fields  = None
            exclude = used_fields.copy ()
            exclude.update             (fsd.exclude)
        for fd in fields or [f.name for f in _F if f.editable] :
            name     = str (fd)
            if name in exclude :
                continue
            dj_field              = _F [name]
            kw                    = dict (widget = getattr (fd, "widget", None))
            form_field_class      = getattr (fd, "form_flield_class", None)
            ### the following attribues must not be passed to `formfield` is
            ### they have not been specified in the field definition to
            ### ensure the proper default
            for attr in "form_class", "required" :
                value = getattr (fd, attr, None)
                if value is not None :
                    kw [attr]     = value
            fo_field              = dj_field.formfield (** kw)
            if fo_field :
                ### we need to set the name for the form-field because we
                ### need to use the TFL.NO_list to keep the order but a
                ### NO_List needs a `name`
                fo_field.name = dj_field.name
                self.fields.append (fo_field)
                used_fields.add (name)
    # end def __init__

    def __call__ (self, form) :
        return DJO.Bound_Form_Set (self, form)
    # end def __call__

    def __getattr__ (self, name) :
        return getattr (self.form_set_description, name)
    # end def __getattr__

    def __iter__ (self) :
        return iter (self.fields)
    # end def __iter__

# end class Form_Set

class Bound_Form_Set (TFL.Meta.Object) :
    """A formset bound to an instance of a Form"""

    def __init__ (self, form_set, form) :
        self.form_set = form_set
        self.form     = form
    # end def __init__

    def __getattr__ (self, name) :
        return getattr (self.form_set, name)
    # end def __getattr__

    def __iter__ (self) :
        from django.forms.forms import BoundField

        for field in self.form_set.fields :
            yield BoundField (self.form, field, field.name)
    # end def __iter__

# end class Bound_Form_Set

if __name__ != "__main__" :
    DJO._Export ("*")
### __END__ DJO.Form_Set_Description
