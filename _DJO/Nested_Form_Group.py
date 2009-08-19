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
#    15-Jul-2009 (CT) `Nested_Form_Count` changed to keep reference to
#                     `Bound_Nested_Form_Group` instead of `count_spec`
#    12-Aug-2009 (CT) `Nested_Form_Count.__init__` changed to add hidden
#                     fields `id` and `_delete_`
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

    def __init__ (self, bnfg) :
        self.bnfg    = bnfg
        self.name    = "%s-count" % (bnfg.name, )
        self._widget = HiddenInput ()
    # end def __init__

    @property
    def value (self) :
        return self.bnfg.count_spec
    # end def value

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
        instance       = form.instance
        no             = 0
        pf             = self.Name
        self.prototype = self.form_class \
            (prefix = "%s-MP" % pf, empty_permitted = True)
        if instance.pk :
            rel_instances = tuple (getattr (instance, self.name).all ())
        else :
            rel_instances = ()
        self.object_count = Nested_Form_Count (self)
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
                    , prefix          = "%s-M%s" % (pf, no)
                    , empty_permitted =
                        (rel_inst is None) and (no >= min_required)
                    )
                )
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
        self.__super.__init__ (model, nfgd)
        self.field_name = name   = str (nfgd.field)
        self.related_model       = model._F [name].rel.to
        self.Name                = self.related_model.__name__.lower ()
        Form_Type                = getattr (self, "Form", DJO.Model_Form)
        Form_Mixins              = getattr (self, "Form_Mixins", ())
        kw                       = dict    (head_mixins = Form_Mixins)
        field_group_descriptions = getattr \
            ( self, "field_group_descriptions"
            , (DJO.Auto_Field_Group_Description (model = model), )
            )
        assert len (field_group_descriptions) == 1
        fgd = field_group_descriptions [0]
        if not any (getattr (f, "name", f) == "id" for f in fgd.fields) :
            fgd.fields += (DJO.Field_Description ("id", widget = HiddenInput), )
        self.form_class = fc = Form_Type.New \
            (self.related_model, * field_group_descriptions, ** kw)
        from django.forms import BooleanField
        ufg = fc.unbound_field_groups [0]
        hfs = BooleanField (widget = HiddenInput, initial = 0)
        hfs.name = "_state_"
        ufg.fields.append (hfs)
        if self.completer :
            self.Media = DJO.Media \
                (js_on_ready = self.completer.js_on_ready (self))
    # end def __init__

# end class Nested_Form_Group

if __name__ != "__main__" :
    DJO._Export ("*")
### __END__ DJO.Nested_Form_Group
