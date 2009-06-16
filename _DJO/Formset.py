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
#    DJO.Formset
#
# Purpose
#    Handling of formsets within forms
#
# Revision Dates
#     6-Jun-2009 (MG) Creation (factored from Formset_Description)
#    11-Jun-2009 (CT) `Form_Mixins` added to `Nested_Form_Formset`
#    11-Jun-2009 (CT) `Bound_Nested_Form_Formset` adapted to pass `request`
#                     to `nested_form_class`
#    15-Jun-2009 (MG) `Bound_Nested_Form_Formset.__init__` use `request`
#                     instead of passing data and files
#    16-Jun-2009 (MG) Only pass `widget`to formfields if really set
#    ««revision-date»»···
#--

from   _TFL                  import TFL
import _TFL._Meta.Object
from   _TFL.predicate        import all_true
from   _DJO                  import DJO
from    django.forms.widgets import HiddenInput

class Bound_Formset (TFL.Meta.Object) :
    """A formset bound to an instance of a Form"""

    def __init__ (self, formset, form) :
        self.formset = formset
        self.form    = form
    # end def __init__

    def __getattr__ (self, name) :
        return getattr (self.formset, name)
    # end def __getattr__

    def __iter__ (self) :
        from django.forms.forms import BoundField

        for field in self.formset.fields :
            yield BoundField (self.form, field, field.name)
    # end def __iter__

# end class Bound_Formset

class Nested_Form_Count (object) :

    def __init__ (self, name, value) :
        self.name    = "%s-count" % (name, )
        self.value   = value
        self._widget = HiddenInput ()
    # end def __init__

    def __unicode__ (self) :
        return self._widget.render \
            (self.name, self.value, attrs = dict (id = "id_%s" % (self.name, )))
    # end def __unicode__

# end class Nested_Form_Count

class Bound_Nested_Form_Formset (Bound_Formset) :
    """A formset which should display a nested form instead of some fields."""

    def __init__ (self, formset, form) :
        self.__super.__init__ (formset, form)
        self.nested_forms = nested_forms = []
        instance          = form.instance
        no                = 0
        self.object_count = Nested_Form_Count (self.name, self.count_spec)
        if instance.pk :
            rel_instances = tuple (getattr (instance, self.name).all ())
        else :
            rel_instances = ()
        if form.is_bound :
            count_spec    = form.data [self.object_count.name]
            count         = int (count_spec.split (":") [0])
        form_count = min \
            ( self.max_count
            , max (self.min_count, len (rel_instances) + self.min_empty)
            )
        for no, rel_inst in enumerate \
                (rel_instances + (None, ) * (form_count - len (rel_instances))):
            nested_forms.append \
                ( self.nested_form_class
                    ( request  = self.form.request
                    , instance = rel_inst
                    , prefix   = "M%d" % (no, )
                    )
                )
    # end def __init__

    @property
    def count_spec (self) :
        return ":".join \
            (   str (n)
            for n in (len (self.nested_forms), self.min_count, self.max_count)
            )
    # end def count_spec

    def save_and_assign (self, instance) :
        setattr (instance, self.name, [nf.save () for nf in self.nested_forms])
    # end def save_and_assign

    def full_clean (self) :
        for nf in self.nested_forms :
            nf.full_clean ()
    # end def full_clean

    def is_valid (self) :
        return all_true (nf.is_valid () for nf in self.nested_forms)
    # end def is_valid

# end class Bound_Nested_Form_Formset

class _Formset_ (TFL.Meta.Object) :
    """Base class for formset's"""

    Bound_Formset = Bound_Formset

    def __init__ (self, model, fsd = None) :
        self.model                = model
        self.formset_description = fsd or DJO.Formset_Description ()
        self.fields               = []
    # end def __init__

    def __call__ (self, form) :
        return self.Bound_Formset (self, form)
    # end def __call__

    def __getattr__ (self, name) :
        return getattr (self.formset_description, name)
    # end def __getattr__

    def __iter__ (self) :
        return iter (self.fields)
    # end def __iter__

# end class _Formset_

class Formset (_Formset_) :
    """A Formset binds a form set description to an model."""

    def __init__ (self, model, fsd = None) :
        self.__super.__init__ (model, fsd)
        _F                        = model._F
        for fd in fsd.fields or [f.name for f in _F if f.editable] :
            name = str (fd)
            if name in fsd.exclude :
                continue
            dj_field          = _F [name]
            kw                = dict ()
            form_field_class  = getattr (fd, "form_flield_class", None)
            ### the following attribues must not be passed to `formfield` is
            ### they have not been specified in the field definition to
            ### ensure the proper default
            for attr in "form_class", "required", "widget":
                value = getattr (fd, attr, None)
                if value is not None :
                    kw [attr] = value
            fo_field          = dj_field.formfield (** kw)
            if fo_field :
                ### we need to set the name for the form-field because we
                ### need to use the TFL.NO_list to keep the order but a
                ### NO_List needs a `name`
                fo_field.name = dj_field.name
                self.fields.append (fo_field)
    # end def __init__

# end class Formset

class Nested_Form_Formset (_Formset_) :
    """Render a nested form instead of a form field"""

    template      = "nested_model_form.html"
    Bound_Formset = Bound_Nested_Form_Formset

    def __init__ (self, model, related_field) :
        self.__super.__init__ (model, related_field)
        related_model          = model._F [related_field.name].rel.to
        Form_Type              = getattr (self, "Form", DJO.Model_Form)
        Form_Mixins            = getattr (self, "Form_Mixins", ())
        formset_descriptions   = getattr (self, "formset_descriptions", ())
        kw                     = dict    (head_mixins = Form_Mixins)
        self.nested_form_class = Form_Type.New \
            (related_model, * formset_descriptions, ** kw)
    # end def __init__

# end class Nested_Form_Formset

if __name__ != "__main__" :
    DJO._Export ("*")
### __END__ DJO.Formset
