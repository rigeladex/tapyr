# -*- coding: iso-8859-1 -*-
# Copyright (C) 2007-2009 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin.glueck@gmail.com
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
#    DJO.Model_Form
#
# Purpose
#    Simplify form handling with the newforms django library
#
# Revision Dates
#     3-Nov-2007 (MG) Creation
#    14-Dec-2007 (CT) Moved into package DJO
#     2-Jan-2008 (MG) Sort order of non model fields changed
#    10-Jan-2008 (MG) Support `anchors` in the `*Redirect` classes
#    30-Jun-2008 (CT) `object_to_save` added to `BaseModelForm`
#    15-Jul-2008 (CT) `Model_Form` added
#     3-Oct-2008 (CT) Optional argument `commit` added to `object_to_save`
#     3-Oct-2008 (CT) s/django.newforms/django.forms/g
#     4-Feb-2009 (CT) Derive from `TFL.Meta.Object` instead of `object` and
#                     `TFL.Meta.M_Class` instead of `type`
#    28-May-2009 (CT) Legacy removed
#    29-May-2009 (MG) `M_Model_Form` filled with life
#    29-May-2009 (MG) `M_Model_Form` filled with life continued
#     2-Jun-2009 (MG) `Model_Form.save` added
#     2-Jun-2009 (MG) `model_to_dict` added
#     2-Jun-2009 (MG) Support for wildcard field spec (`*`) added. Problem in
#                     `Model_Form.save` fixed
#    02-Jun-2009 (MG) Cleanup of `New`
#     4-Jun-2009 (MG) `**kw` added to `M_Model_Form.New`
#     4-Jun-2009 (MG) Use new `Formset` and `Bound_Formset` class
#     5-Jun-2009 (MG) Update `_meta.fields` based on the form set descriptions
#     6-Jun-2009 (MG) `s/Form_Set/Formset/g`
#    10-Jun-2009 (MG) Support for netsed forms added
#    11-Jun-2009 (CT) Module renamed from Forms to Model_Form
#    11-Jun-2009 (CT) Use `Override_Method` to change `models.model_to_dict`
#    11-Jun-2009 (CT) Use `cls.__m_super` instead of `super (..., cls)`
#    11-Jun-2009 (CT) `Model_Form.__init__` changed to expect `request`
#                     instead of `* args`
#    12-Jun-2009 (CT) `object_to_save` removed
#    12-Jun-2009 (CT) `clean` and `_djo_clean` removed
#    12-Jun-2009 (CT) `_before_commit` added to, `commit` argument removed
#                     from, `save`
#    12-Jun-2009 (CT) `Model_Form_Mixin`, `Creator_Form_Mixin`, and
#                     `Kind_Name_Form_Mixin` added
#    15-Jun-2009 (MG) `Model_Form.__init__` changed so that only some
#                     attributes are passed to the django form ancestor
#    15-Jun-2009 (MG) `Model_Form_Mixin` cannot inherit from
#                     `TFL.Meta.Object`
#    17-Jun-2009 (MG) `Model_Form.__init__` handle `empty_permitted`
#                     `Model_Form.save` only save the instance if the form
#                     tries to change anything, moved saving of nested form's
#                     into `save` method
#    19-Jun-2009 (MG) Support data argumnet for Model_Form as well as request
#                     Pass `used_fields` to `groups` method
#    19-Jun-2009 (MG) `s/nested_forms/forms/g`
#    14-Jul-2009 (CT) `Media` added
#    20-Aug-2009 (CT) `form_map` added to `Model_Form`
#    ««revision-date»»···
#--

from   _DJO                        import DJO
from   _TFL                        import TFL

import _TFL.Decorator
import _TFL._Meta.M_Class
import _TFL._Meta.Object
import _TFL.NO_List

from   _TFL._Meta.Once_Property    import Once_Property
from   _TFL.predicate              import all_true

import _DJO.Field_Group_Description

from    django.forms                    import BaseForm, BaseModelForm
from    django.forms.util               import ErrorList
from    django.forms                    import models
from    django.db.models.fields.related import RelatedField
from    django.db.models                import FileField

class M_Model_Form (TFL.Meta.M_Class) :
    """Meta class for forms based on a django model."""

    def __new__ (cls, name, bases, attrs) :
        base_fields          = TFL.NO_List ()
        model                = attrs.get ("model", None)
        used_fields          = set ()
        unbound_field_groups = attrs ["unbound_field_groups"] = []
        for fgd in attrs.get ("field_group_descriptions", ()) :
            for grp in fgd.groups (model, used_fields) :
                field_group = grp           (model, used_fields)
                unbound_field_groups.append (field_group)
                base_fields.extend          (field_group)
        _meta = attrs.get ("_meta", None)
        if _meta :
            _meta.fields = [f.name for f in base_fields]
        attrs ["base_fields"]  = base_fields
        return super (M_Model_Form, cls).__new__ \
            (cls, name, bases, attrs)
    # end def __new__

    def New (cls, model, * field_group_descriptions, ** kw) :
        class Meta :
            exclude = ()
        Meta.model  = model
        if not field_group_descriptions :
            field_group_descriptions = \
               (DJO.Auto_Field_Group_Description (model = model), )
        return cls.__m_super.New \
            ( model.__name__
            , model                    = model
            , field_group_descriptions = field_group_descriptions
            , _meta                    = Meta
            , ** kw
            )
    # end def New

# end class M_Model_Form

@TFL.Override_Method (models)
def model_to_dict (instance, fields = None, exclude = None) :
    _F = getattr (instance, "_F", None)
    if _F is not None :
        from django.db.models.fields.related import ManyToManyField
        ### we build the data dict in a different way
        data = {}
        exclude = (exclude or ())
        for fn in fields or [f.name for f in _F if f.editable] :
            if fn in exclude :
                continue
            f = _F [fn]
            if isinstance (f, ManyToManyField):
                # If the object doesn't have a primary key yet, just use an
                # empty list for its m2m fields.
                # Calling f.value_from_object will raise an exception.
                if instance.pk is None:
                    data [f.name] = []
                else:
                    # MultipleChoiceWidget needs a list of pks, not object
                    # instances.
                    data [f.name] = \
                         [obj.pk for obj in f.value_from_object (instance)]
            else:
                data [f.name] = f.value_from_object (instance)
        return data
    else :
        return model_to_dict.orig (instance, fields, exclude)
# end def model_to_dict

class _DJO_Model_Form_ (BaseModelForm) :
    """Base class for all form's which derive there fields from a Django
       model.

       BaseForm expect's a class attribute called `base_fields` which is a
       sorted dict containing django field instances.
    """

    __metaclass__ = M_Model_Form
    _real_name    = "Model_Form"

    def __init__ (self, request = None, instance = None, prefix = None, ** kw) :
        ### super call must be before creating the bound field_group's in order
        ### to have the `instance` member setup correctly
        form_kw = dict (empty_permitted = kw.pop ("empty_permitted", False))
        if request :
            form_kw ["data"] = request.POST
        if "data" in kw :
            form_kw ["data"] = kw.pop ("data")
        self.__super.__init__ (instance = instance, prefix = prefix, ** form_kw)
        self.request      = request
        self.field_groups = []
        self.forms        = []
        self.form_map     = {}
        for ufs in self.unbound_field_groups :
            bfs = ufs (self)
            self.field_groups.append (bfs)
            if isinstance (bfs, DJO.Bound_Nested_Form_Group) :
                self.forms.append (bfs)
                self.form_map [bfs.name] = bfs
    # end def __init__

    def full_clean (self) :
        if self.is_bound:
            for bfs in self.forms :
                bfs.full_clean ()
            self.__super.full_clean ()
    # end def full_clean

    def is_valid (self) :
        return (   self.__super.is_valid ()
               and all_true (nf.is_valid () for nf in self.forms)
               )
    # end def is_valid

    @Once_Property
    def Media (self) :
        medias = [fg.Media for fg in self.field_groups if fg.Media]
        if medias :
            result = DJO.Media (children = medias)
            return result
    # end def Media

    def save (self) :
        instance = self.instance
        _F       = instance._F
        if self.errors :
            raise ValueError\
                ( "The %s could not be %s because the data didn't "
                  "validate."
                % ( instance._meta.object_name
                  , "created" if not instance.pk else "changed"
                  )
                )
        if self.has_changed () :
            cleaned_data        = self.cleaned_data
            file_field_defers   = []
            self.related_defers = []
            for ff in self.fields :
                df = _F [ff.name]
                # Defer saving file-type fields until after the other fields, so a
                # callable upload_to can use the values from other fields.
                if isinstance (df, FileField):
                    file_field_defers.append (dj)
                elif isinstance (df, RelatedField) :
                    ### related fields can only be `saved` after the main object
                    ### has been saved, so we defer them
                    self.related_defers.append (df)
                else:
                    df.save_form_data (instance, cleaned_data [df.name])
            for df in file_field_defers :
                df.save_form_data (instance, cleaned_data [df.name])
            self._before_commit (instance)
            instance.save ()
            self.save_m2m ()
        for nf in self.forms :
            nf.save_and_assign (self.instance)
        return instance
    # end def save

    def save_m2m (self) :
        for df in self.related_defers :
            df.save_form_data (self.instance, self.cleaned_data [df.name])
        self.related_defers = []
    # end def save_m2m

    def _before_commit (self, instance) :
        return instance
    # end def _before_commit

Model_Form = _DJO_Model_Form_ # end class

class Model_Form_Mixin (object) :

    __metaclass__ = M_Model_Form

# end class Model_Form_Mixin

class Creator_Form_Mixin (Model_Form_Mixin) :
    """Model_Form mixin dealing with models with `creator`."""

    def _before_commit (self, instance) :
        if not instance.creator :
            request = self.request
            if request.user.is_authenticated () :
                instance.creator = request.user
        return self.__super._before_commit (instance)
    # end def _before_commit

# end class Creator_Form_Mixin

class Kind_Name_Form_Mixin (Model_Form_Mixin) :
    """Model_Form mixin dealing with models with `kind_name`."""

    kind_name       = None

    def __init__ (self, request = None, instance = None, ** kw) :
        self.kind_name = kw.pop ("kind_name", None)
        self.__super.__init__ (request = request, instance = instance, ** kw)
    # end def __init__

    def _before_commit (self, instance) :
        instance.kind = instance._F.kind.choice_to_code (self.kind_name)
        return self.__super._before_commit (instance)
    # end def _before_commit

# end class Kind_Name_Form_Mixin

if __name__ != "__main__" :
    DJO._Export ("*")
### __END__ DJO.Model_Form
