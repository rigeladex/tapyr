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
#    ««revision-date»»···
#--

from   _TFL               import TFL
import _TFL._Meta.Object
from   _DJO               import DJO

class Form_Set_Description (TFL.Meta.Object) :
    """Describes a part of a form used to create/edit a Django model"""

    defaults = dict (template = "")

    def __init__ (self, * fields, ** kw) :
        self.template = kw.pop ("template", self.defaults ["template"])
        self._field_descriptions = fields
        self.model               = kw.pop ("model", None)
    # end def __init__

    def _set_model (self, model) :
        self._model = model
        if model :
            self._setup_fields ()
    # end def _set_model

    def model (self) :
        return self._model
    # end def model

    model = property (model, _set_model)

    def _setup_fields (self) :
        model        = self._model
        _F           = model._F
        self._fields = []
        for fd in    self._field_descriptions \
                 or [f.name for f in _F if f.editable] :
            dj_field = _F [getattr (fd, "name", fd)]
            fo_field = dj_field.formfield ()
            if fo_field :
                ### we need to set the name for the form-field becasue we
                ### need to use the TFL.NO_list to keep the order but a
                ### NO_List needs a `name`
                fo_field.name = dj_field.name
                self._fields.append (fo_field)
    # end def _setup_fields

# end class Form_Set_Description

if __name__ != "__main__" :
    DJO._Export ("*")
### __END__ DJO.Form_Set_Description
