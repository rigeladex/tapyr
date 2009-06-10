# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005-2009 Martin Glück. All rights reserved
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
#    DJO.Forms
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
#    ««revision-date»»···
#--

from   _DJO                        import DJO
from   _TFL                        import TFL

import _TFL.Decorator
import _TFL._Meta.M_Class
import _TFL.NO_List
from   _TFL.predicate              import all_true

import _DJO.Formset_Description
import _DJO.Formset

from    django.forms                    import BaseForm, BaseModelForm
from    django.forms.util               import ErrorList
from    django.forms                    import models
from    django.db.models.fields.related import RelatedField

django_model_to_dict = models.model_to_dict

@TFL.Add_New_Method (BaseModelForm)
@TFL.Contextmanager
def object_to_save (self, commit=True) :
    """Context manager for saving an object created from a form"""
    obj = self.save (commit = False)
    try :
        yield obj
    finally :
        if commit :
            obj.save      ()
            self.save_m2m ()
# end def object_to_save

class M_Model_Form (TFL.Meta.M_Class) :
    """Meta class for forms based on a django model."""

    def __new__ (cls, name, bases, attrs) :
        base_fields      = TFL.NO_List ()
        model            = attrs.get ("model", None)
        used_fields      = set ()
        unbound_formsets = attrs ["unbound_formsets"] = []
        for fsd in attrs.get ("formset_descriptions", ()) :
            for formset in fsd (model, used_fields) :
                unbound_formsets.append (formset)
                base_fields.extend      (formset)
        _meta                  = attrs.get ("_meta", None)
        if _meta :
            _meta.fields = [f.name for f in base_fields]
        attrs ["base_fields"]  = base_fields
        return super (M_Model_Form, cls).__new__ \
            (cls, name, bases, attrs)
    # end def __new__

    def New (cls, model, * formset_descriptions, ** kw) :
        class Meta :
            exclude = ()
        Meta.model  = model

        if not formset_descriptions :
            formset_descriptions = \
               (DJO.Formset_Description (model = model), )
        return super (M_Model_Form, cls).New \
            ( model.__name__
            , model                 = model
            , formset_descriptions = formset_descriptions
            , _meta                 = Meta
            , ** kw
            )
    # end def New

# end class M_Model_Form

def model_to_dict (instance, fields = None, exclude = None) :
    _F = getattr (instance, "_F", None)
    if _F is not None :
        ### XXX don't know if we need this, depends on how ManyToManyField
        ### will be implemented
        from django.db.models.fields.related import ManyToManyField
        ### we build the data dict in a different way
        data = {}
        exclude = (exclude or ())
        for fn in fields or [f.name for f in _F if f.editable] :
            if fn in exclude :
                continue
            f = _F [fn]
            if isinstance (f, ManyToManyField):
                # If the object doesn't have a primry key yet, just use an empty
                # list for its m2m fields. Calling f.value_from_object will
                # raise an exception.
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
        return django_model_to_dict (instance, fields, exclude)
# end def model_to_dict
models.model_to_dict = model_to_dict

class _DJO_Model_Form_ (BaseModelForm) :
    """Base class for all form's which derive there fields from a Django
       model.

       BaseForm expect's a class attribute called `base_fields` which is a
       sorted dict containing django field instances.
    """

    __metaclass__ = M_Model_Form
    _real_name    = "Model_Form"
    _djo_clean    = None

    def __init__ (self, * args, ** kw) :
        ### super call must be before creating the bound formset's in order
        ### to have the `instance` member setup correctly
        self.__super.__init__ (* args, ** kw)
        self.formsets     = []
        self.nested_forms = []
        for ufs in self.unbound_formsets :
            bfs = ufs (self)
            self.formsets.append (bfs)
            if isinstance (bfs, DJO.Bound_Nested_Form_Formset) :
                self.nested_forms.append (bfs)
    # end def __init__

    def clean (self) :
        result = self.__super.clean ()
        if callable (self._djo_clean) :
            result = self._djo_clean (result)
        return result
    # end def clean

    def full_clean (self) :
        if not self.is_bound: # Stop further processing.
            return
        for bfs in self.nested_forms :
            bfs.full_clean ()
        self.__super.full_clean ()
    # end def full_clean

    def is_valid (self) :
        return (    all_true (nf.is_valid () for nf in self.nested_forms)
               and self.__super.is_valid ()
               )
    # end def is_valid

    def save (self, commit = True) :
        from django.db import models

        instance     = self.instance
        _F           = instance._F
        if self.errors :
            raise ValueError\
                ( "The %s could not be %s because the data didn't "
                  "validate."
                % ( instance._meta.object_name
                  , "created" if not instance.pk else "changed"
                  )
                )
        cleaned_data        = self.cleaned_data
        file_field_defers   = []
        self.related_defers = []
        for ff in self.fields :
            df    = _F [ff.name]
            # Defer saving file-type fields until after the other fields, so a
            # callable upload_to can use the values from other fields.
            if isinstance (df, models.FileField):
                file_field_defers.append (dj)
            elif isinstance (df, RelatedField) :
                ### related fields can only be `saved` after the main object
                ### has been saved, so we defer them
                self.related_defers.append (df)
            else:
                df.save_form_data (instance, cleaned_data [df.name])

        for df in file_field_defers :
            df.save_form_data (instance, cleaned_data [df.name])
        if commit :
            instance.save ()
            self.save_m2m ()
        return instance
    # end def save

    def save_m2m (self) :
        for df in self.related_defers :
            df.save_form_data (self.instance, self.cleaned_data [df.name])
        self.related_defers = []
        for nf in self.nested_forms :
            nf.save_and_assign (self.instance)
    # end def save_m2m

Model_Form = _DJO_Model_Form_ # end class

if __name__ != "__main__" :
    DJO._Export ("*")
### __END__ DJO.Forms
