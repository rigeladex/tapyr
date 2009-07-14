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
#    DJO.Field_Group_Description
#
# Purpose
#    Classes to describe field_groups
#
# Revision Dates
#    29-May-2009 (MG) Creation
#    29-May-2009 (MG) `_setup_fields` corrected, order if initialization fixed
#    02-Jun-2009 (MG) `exclude`and `used_fields` added
#     2-Jun-2009 (MG) `model`no longer a property, `setup_fields` is not an API
#     2-Jun-2009 (MG) `setup_fields`: Parameter `used_fields` added, support
#                     for wildcard field * added
#     2-Jun-2009 (MG) `Field_Description` added
#     4-Jun-2009 (MG) Reorganized: `Field_Group` and `Bound_Field_Group` factored
#                     out of `Field_Group_Description`
#     5-Jun-2009 (MG) `Field_Group.__init__` honor `required` of field
#                     description
#     6-Jun-2009 (MG) `s/Form_Set/Field_Group/g`
#     6-Jun-2009 (MG) `Field_Description` factored into own module
#     6-Jun-2009 (MG) `Field_Group` and `Bound_Field_Group` factored into own module
#    10-Jun-2009 (MG) `Nested_Form_Description` and friends added
#    11-Jun-2009 (CT) `name` and `_` added to `Field_Group_Description`
#    15-Jun-2009 (MG) `Field_Group_Description.__class__`: fixed problem if two
#                     `Nested_Form_Description` are neighbors
#    17-Jun-2009 (MG) `Nested_Form_Description.min_required` added
#    19-Jun-2009 (MG) `Auto_Field_Group_Description.groups` implemented
#    14-Jul-2009 (CT) `Media` added
#    14-Jul-2009 (CT) Use `Template` instance instead of literal string
#    ««revision-date»»···
#--

from   _TFL               import TFL
import _TFL._Meta.Object
from   _DJO               import DJO
import _DJO.Field_Description
import _DJO.Field_Group
import _DJO.Nested_Form_Group
import _DJO.Template
import _DJO._Apps.Base

import  sys

class _Field_Group_Description_ (TFL.Meta.Object) :
    """Base class for field group descriotions"""

    template = None
    model    = None

    _        = TFL.Record ()

    def __init__ (self, ** kw) :
        name = kw.pop ("name", None)
        if name :
            if name in self._ :
                raise NameError, name
            setattr (self._, name, self)
        self.exclude  = set (kw.pop ("exclude", ()))
        self.__dict__.update (kw)
    # end def __init__

    def groups (self, model, used_fields) :
        return [self]
    # end def groups

    @property
    def Media (self) :
        return getattr (self.template, "Media")
    # end def Media

# end class _Field_Group_Description_

class Field_Group_Description (_Field_Group_Description_) :
    """Describes a part of a form used to create/edit a Django model"""

    def __init__ (self, * fields, ** kw) :
        self.__super.__init__ (** kw)
        self.fields = fields
    # end def __init__

    def __call__ (self, model = None, used_fields = set ()) :
        return DJO.Field_Group (model, self, used_fields)
    # end def __call__


# end class Field_Group_Description

class Auto_Field_Group_Description (_Field_Group_Description_) :
    """A field group which creates field groups automatically"""

    field_descriptions = ()

    def groups (self, model, used_fields) :
        result         = []
        _F             = model._F
        exclude        = self.exclude.copy ()
        exclude.update (used_fields)
        field_override = dict ((f.name, f) for f in self.field_descriptions)
        normal_fields  = []
        for name in [f.name for f in _F if f.editable] :
            fd       = field_override.get (name, name)
            if name in exclude :
                continue
            if getattr (fd, "nested", False) :
                if normal_fields :
                    result.append \
                        (DJO.Field_Group_Description (* normal_fields))
                normal_fields = []
                result.append (DJO.Nested_Form_Group (name))
            else :
                normal_fields.append (fd)
        if normal_fields :
            result.append (DJO.Field_Group_Description (* normal_fields))
        return result
    # end def groups

# end class Auto_Field_Group_Description

class Nested_Form_Group_Description (_Field_Group_Description_) :
    """Description of an inline for an may 2 many relation"""

    template     = DJO.Template ["nested_model_form.html"]
    min_count    = 1
    max_count    = sys.maxint
    min_empty    = 1
    min_required = 0

    def __init__ (self, field, field_group_descriptions, ** kw) :
        self.field                    = field
        self.name                     = str (field)
        self.field_group_descriptions = \
            field_group_descriptions or DJO.Auto_Field_Group_Description ()
        self.__super.__init__ (** kw)
    # end def __init__

    def __call__ (self, model = None, used_fields = set ()) :
        return DJO.Nested_Form_Group (model, self, used_fields)
    # end def __call__

# end class Nested_Form_Group_Description
if __name__ != "__main__" :
    DJO._Export ("*")
### __END__ DJO.Field_Group_Description
