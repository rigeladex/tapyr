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
#    DJO.Formset_Description
#
# Purpose
#    Classes to describe formsets
#
# Revision Dates
#    29-May-2009 (MG) Creation
#    29-May-2009 (MG) `_setup_fields` corrected, order if initialization fixed
#    02-Jun-2009 (MG) `exclude`and `used_fields` added
#     2-Jun-2009 (MG) `model`no longer a property, `setup_fields` is not an API
#     2-Jun-2009 (MG) `setup_fields`: Parameter `used_fields` added, support
#                     for wildcard field * added
#     2-Jun-2009 (MG) `Field_Description` added
#     4-Jun-2009 (MG) Reorganized: `Formset` and `Bound_Formset` factored
#                     out of `Formset_Description`
#     5-Jun-2009 (MG) `Formset.__init__` honor `required` of field
#                     description
#     6-Jun-2009 (MG) `s/Form_Set/Formset/g`
#     6-Jun-2009 (MG) `Field_Description` factored into own module
#     6-Jun-2009 (MG) `Formset` and `Bound_Formset` factored into own module
#    10-Jun-2009 (MG) `Nested_Form_Description` and friends added
#    ««revision-date»»···
#--

from   _TFL               import TFL
import _TFL._Meta.Object
from   _DJO               import DJO
import _DJO.Field_Description
from    copy              import copy
import  sys

class Nested_Form_Description (DJO.Field_Description) :
    """Specfies that instead of rendering a field as a widget a nested form
       should be rendered
    """

    min_count = 1
    max_count = sys.maxint
    min_empty = 1

# end class Nested_Form_Description

class Formset_Description (TFL.Meta.Object) :
    """Describes a part of a form used to create/edit a Django model"""

    template = None
    model    = None

    def __init__ (self, * fields, ** kw) :
        self.exclude  = set (kw.pop ("exclude", ()))
        self.fields   = fields
        self.__dict__.update (kw)
    # end def __init__

    def copy (self, fields = (), exclude = ()) :
        result         = copy (self)
        result.fields  = fields
        result.exclude = set (exclude)
        return result
    # end def copy

    def __call__ (self, model = None, used_fields = set ()) :
        result            = []
        exclude           = self.exclude
        fields            = self.fields
        if (len (fields) == 1) and (fields [0]   == "*") :
            fields        = None
            exclude       = used_fields.copy ()
            exclude.update                   (self.exclude)
        fields            = fields or [f.name for f in model._F if f.editable]
        self.fields       = []
        self.exclude      = set ()
        nested_form_index = []
        for idx, fd in enumerate (fields) :
            name     = str (fd)
            if name in exclude :
                continue
            self.fields.append (fd)
            used_fields.add    (name)
            if isinstance (fd, Nested_Form_Description) :
                nested_form_index.append (idx)
        model = model or self.model
        if nested_form_index :
            current_idx = 0
            for nested_idx in nested_form_index :
                if nested_idx > 0 :
                    fsd = self.copy (self.fields [current_idx : nested_idx])
                    result.append (DJO.Formset (model, fsd))
                result.append \
                    (DJO.Nested_Form_Formset (model, self.fields [nested_idx]))
                current_idx = nested_idx + 1
            rem_fields = self.fields [current_idx : ]
            if rem_fields :
                fsd = self.copy (rem_fields)
                result.append (DJO.Formset (model, fsd))
        else :
            result.append (DJO.Formset (model, self))
        return result
    # end def __call__

# end class Formset_Description

if __name__ != "__main__" :
    DJO._Export ("*")
### __END__ DJO.Formset_Description
