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
#    «text»···
#
# Revision Dates
#    29-May-2009 (MG) Creation
#    29-May-2009 (MG) `_setup_fields` corrected, order if initialization fixed
#    02-Jun-2009 (MG) `exclude`and `used_fields` added
#     2-Jun-2009 (MG) `model`no longer a property, `setup_fields` is not an API
#     2-Jun-2009 (MG) `setup_fields`: Parameter `used_fields` added, support
#                     for wildcard field * added
#     2-Jun-2009 (MG) `Field_Description` added
#    ««revision-date»»···
#--

from   _TFL               import TFL
import _TFL._Meta.Object
from   _DJO               import DJO

class Field_Description (TFL.Meta.Object) :
    """Desciption of how a field should be rendered in a form (set)"""

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

    defaults = dict (template = "model_admin_change_table.html")

    def __init__ (self, * fields, ** kw) :
        self.template = kw.pop ("template", self.defaults ["template"])
        self.exclude  = set (kw.pop ("exclude", ()))
        self._field_descriptions = fields
        self.model               = kw.pop ("model", None)
        if self.model :
            self.setup_fields ()
    # end def __init__

    def setup_fields (self, used_fields = set ()) :
        model        = self.model
        _F           = model._F
        exclude      = self.exclude
        self._fields = []
        _fields      = self._field_descriptions
        if (   (len (self._field_descriptions) == 1)
           and (self._field_descriptions [0]   == "*")
           ) :
            _fields = None
            exclude = used_fields.copy ()
            exclude.update             (self.exclude)
        for fd in _fields or [f.name for f in _F if f.editable] :
            name     = str (fd)
            if name in exclude :
                continue
            dj_field              = _F [name]
            kw                    = dict (widget = getattr (fd, "widget", None))
            form_field_class      = getattr (fd, "form_flield_class", None)
            if form_field_class is not None :
                ### the default form class is set as default of the
                ### constructor. therefore only pass the argument if really
                ### required
                kw ["form_class"] = form_field_class
            fo_field              = dj_field.formfield (** kw)
            if fo_field :
                ### we need to set the name for the form-field because we
                ### need to use the TFL.NO_list to keep the order but a
                ### NO_List needs a `name`
                fo_field.name = dj_field.name
                self._fields.append (fo_field)
                used_fields.add (name)
        return self._fields
    # end def setup_fields

    def __iter__ (self) :
        from django.forms.forms import BoundField

        for field in self._fields :
            yield BoundField (self.form, field, field.name)
    # end def __iter__

# end class Form_Set_Description

if __name__ != "__main__" :
    DJO._Export ("*")
### __END__ DJO.Form_Set_Description
