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
#    DJO.Nested_Form_Group
#
# Purpose
#    Used to specify how a many 2 many realtion should be rendered as an
#    inline form.
#
# Revision Dates
#    19-Jun-2009 (MG) Creation
#    19-Jun-2009 (MG) `s/nested_forms/forms/g`
#     9-Jul-2009 (MG) `Nested_Form_Count.__unicode__`: class added
#     9-Jul-2009 (MG) `Nested_Form_Group`: bug related to `object_count` fixed
#     9-Jul-2009 (MG) On post, use count from post data
#    ««revision-date»»···
#--

from   _TFL                         import TFL
import _TFL._Meta.Object
from   _DJO                         import DJO
import _DJO.Field_Group_Description
import _DJO.Field_Group
from   _TFL.predicate               import all_true
from    django.forms.widgets        import HiddenInput

class Nested_Form_Count (object) :

    def __init__ (self, name, value) :
        self.name    = "%s-count" % (name, )
        self.value   = value
        self._widget = HiddenInput ()
    # end def __init__

    def __unicode__ (self) :
        return self._widget.render \
            ( self.name, self.value
            , attrs =
                { "id"    : "id_%s" % (self.name, )
                , "class" : "many-2-many-range"
                }
            )
    # end def __unicode__

# end class Nested_Form_Count

class Bound_Nested_Form_Group (DJO.Bound_Field_Group) :
    """A field_group which should display a nested form instead of some fields."""

    def __init__ (self, field_group, form) :
        self.__super.__init__ (field_group, form)
        self.forms     = forms = []
        prefix         = "%s-M%%s" % (self.form_class.model.__name__.lower (), )
        self.prototype = self.form_class \
            (prefix = prefix % "P", empty_permitted = True)
        instance          = form.instance
        no                = 0
        if instance.pk :
            rel_instances = tuple (getattr (instance, self.name).all ())
        else :
            rel_instances = ()
        self.object_count = Nested_Form_Count (self.name, self.count_spec)
        count             = 0
        if form.is_bound :
            count_spec    = form.data [self.object_count.name]
            try :
                count     = int (count_spec.split (":") [1])
            except :
                count     = self.min_required
        min_required      = self.min_required
        form_count        = min \
            ( self.max_count
            , max
                ( self.min_count
                , len (rel_instances) + self.min_empty
                , min_required
                , count
                )
            )
        for no, rel_inst in enumerate \
                (rel_instances + (None, ) * (form_count - len (rel_instances))):
            forms.append \
                ( self.form_class
                    ( request         = self.form.request
                    , instance        = rel_inst
                    , prefix          = prefix % (no, )
                    , empty_permitted =
                        (rel_inst is None) and (no >= min_required)
                    )
                )
        self.object_count.value = self.count_spec
    # end def __init__

    @property
    def count_spec (self) :
        return ":".join \
            (   str (n)
            for n in (self.min_count, len (self.forms), self.max_count)
            )
    # end def count_spec

    def save_and_assign (self, instance) :
        rel_instances = [nf.save () for nf in self.forms]
        setattr (instance, self.name, [i for i in rel_instances if i.pk])
    # end def save_and_assign

    def full_clean (self) :
        for nf in self.forms :
            nf.full_clean ()
    # end def full_clean

    def is_valid (self) :
        return all_true (nf.is_valid () for nf in self.forms)
    # end def is_valid

# end class Bound_Nested_Form_Group

class Nested_Form_Group (DJO._Field_Group_) :
    """Render a nested form instead of a form field"""

    Bound_Field_Group = Bound_Nested_Form_Group

    def __init__ (self, model, nfgd, used_fields = set ()) :
        name                     = str (nfgd.field)
        self.__super.__init__ (model, nfgd)
        related_model            = model._F [name].rel.to
        Form_Type                = getattr (self, "Form", DJO.Model_Form)
        Form_Mixins              = getattr (self, "Form_Mixins", ())
        field_group_descriptions = getattr (self, "field_group_descriptions", ())
        kw                       = dict    (head_mixins = Form_Mixins)
        self.form_class          = Form_Type.New \
            (related_model, * field_group_descriptions, ** kw)
    # end def __init__

# end class Nested_Form_Field_Group

if __name__ != "__main__" :
    DJO._Export ("*")
### __END__ DJO.Nested_Form_Group
