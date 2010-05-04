# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.Form.MOM.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    GTW.Form.MOM.Inline
#
# Purpose
#    Add a `Inline` object to a form
#
# Revision Dates
#    18-Jan-2010 (MG) Creation
#    20-Jan-2010 (MG) Error handling added (includig checking of
#                     `min_required` and `max_count`)
#     2-Feb-2010 (MG) `form_count` added
#     2-Feb-2010 (MG) `prototype_form` added
#     3-Feb-2010 (MG) `Media` property moved in here
#     3-Feb-2010 (MG) `range_field_name` added and used to check how many
#                     forms have be sent by the browser
#     3-Feb-2010 (MG) `name` added
#     5-Feb-2010 (MG) `Attribute_Inline` and `Link_Inline` factored
#     5-Feb-2010 (MG) `_Inline_.Media` handle media for completers
#     8-Feb-2010 (MG) Directly access the `_etype` of the `et_man` (An_Entity
#                     etype managers work differently)
#    10-Feb-2010 (MG) Property `instances` removed (legacy)
#                     `froms` and `form_count` moved into subclasses
#                     Support for inline level JS on ready code added
#                     Form field prefix handling changed
#    11-Feb-2010 (MG) class `Instances` renamed to `Instance_Collection`,
#                     Changed handling of instance to form assignment (to
#                     make sure that each posted form gets assing the correct
#                     instance)
#    26-Feb-2010 (MG) Javascript handling changed
#     6-Mar-2010 (MG) `Attribute_Inline` streamlined
#    11-Mar-2010 (MG) `An_Attribute_Inline/Id_Attribute_Inline` added
#     3-May-2010 (MG) New form handling implemented
#    ««revision-date»»···
#--

from   _TFL                                 import TFL
from   _TFL.predicate                       import paired
import _TFL.Caller
import _TFL._Meta.Object
import _TFL._Meta.Once_Property

from   _GTW                                 import GTW
import _GTW._Form.Field_Error
import _GTW._Form._MOM

class Link_Inline (TFL.Meta.Object) :
    """Handling of all link-forms as a field group of a form.."""

    request_data = dict ()

    def __init__ ( self, inline_description, form_cls, owner = None) :
        self.name               = form_cls.et_man._etype.type_base_name
        self.inline_description = inline_description
        self.form_cls           = form_cls
        self.owner              = owner
        if owner :
            self.prefix         = "__".join ((owner.prefix, self.name))
        self.errors             = GTW.Form.Error_List ()
        max_count               = getattr (form_cls.et_man, "max_count", None)
        if max_count :
            self.max_count      = max_count
    # end def __init__

    def clone (self, form) :
        return self.__class__ \
            (self.inline_description, self.form_cls, owner = form)
    # end def clone

    def defaults (self, form, instance, defaults = {}) :
        pass
    # end def defaults

    def get_errors (self) :
        return self.errors
    # end def get_errors

    @TFL.Meta.Once_Property
    def _linked_instances (self) :
        return self.form_cls.et_man.query \
            (** {self.own_role_name : self.owner.instance})
    # end def _linked_instances

    @TFL.Meta.Once_Property
    def Media (self) :
        return GTW.Media.from_list \
            ([m for m in (self.widget.Media, self.form_cls.Media) if m])
    # end def Media

    @TFL.Meta.Once_Property
    def prototype_form (self) :
        iform_cls     = self.form_cls
        et_man        = iform_cls.et_man
        owner         = self.owner
        prefix        = "%s-MP" % (self.prefix, )
        return iform_cls \
            (None, prefix = prefix, parent = owner, prototype = True)
    # end def prototype_form

    @TFL.Meta.Once_Property
    def range_field_name (self) :
        return "%s-m2m-range" % (self.form_cls.et_man._etype.type_base_name, )
    # end def range_field_name

    @TFL.Meta.Once_Property
    def form_count (self) :
        count         = 0
        try :
            value     = self.request_data [self.range_field_name]
            count     = int (value.split (":") [1])
        except KeyError :
            owner     = self.owner
            if owner.instance :
                count = self.min_empty + self._linked_instances.count ()
        return min \
            (self.max_count, max (self.min_count, self.min_required, count))
    # end def form_count

    @TFL.Meta.Once_Property
    def forms (self) :
        owner          = self.owner
        et_man         = self.form_cls.et_man
        used_instances = dict ()
        count          = self.form_count
        form_cls       = self.form_cls
        prototype      = self.owner.prototype
        prefix_pat     = "%s-M%%d" % (self.prefix, )
        lid_pat        = "__".join ((prefix_pat, "_lid_a_state_"))
        result         = []
        ### find the links currently linked to the owner
        if owner.instance :
            instances = dict ((i.lid, i) for i in self._linked_instances)
        else :
            instances = dict ()
        ### find the links which are actively requested by forms
        for no in xrange (count) :
            lid = self.request_data.get (lid_pat % no, ":").split (":") [0]
            if lid :
                used_instances [lid] = instances.pop (lid, None)
        instances = sorted (instances.values ())
        for no in xrange (count) :
            lid = self.request_data.get (lid_pat % no, ":").split (":") [0]
            ### assign the correct link to the form or assign a free link
            if lid in used_instances :
                instance = used_instances [lid]
            elif instances :
                instance = instances.pop (0)
            else :
                instance = None
            result.append \
                (  form_cls
                      ( instance  = instance
                      , prefix    = prefix_pat % no
                      , prototype = prototype
                      , parent    = self.owner
                      )
                )
        return result
    # end def forms

    def setup_javascript (self, parent_form) :
        GTW.Form.Javascript.Link_Inline (self.form_cls, self)
    # end def setup_javascript

    def create_object (self, form) :
        ### add checks for min/max
        for lform in self.forms :
            lform.recursively_run \
                ("create_object", lform, reverse = True)
            form.inline_errors += lform.error_count
    # end def create_object

    def prepare_request_data (self, form, request_data) :
        self.request_data = request_data
        for lform in self.forms :
            lform.recursively_run \
                ("prepare_request_data", lform, request_data)
    # end def prepare_request_data

    def setup_raw_attr_dict (self, form) :
        for lform in self.forms :
            lform.recursively_run ("setup_raw_attr_dict", lform)
    # end def setup_raw_attr_dict

    def update_object (self, form) :
        for lform in self.forms :
            lform.recursively_run ("update_object", lform)
    # end def setup_raw_attr_dict

    def update_raw_attr_dict (self, form) :
        for lform in self.forms :
            lform.recursively_run ("update_raw_attr_dict", lform)
    # end def setup_raw_attr_dict

    def __getattr__ (self, name) :
        try :
            result = getattr (self.inline_description, name)
        except AttributeError :
            raise AttributeError (name)
        setattr (self, name, result)
        return result
    # end def __getattr__

# end class Link_Inline

class Collection_Inline (Link_Inline) :
    """Handle the collection of inlines."""

    def create_object (self, form) :
        ### add checks for min/max
        form.raw_attr_dict [self.link_name] = raw_values = []
        for lform in self.forms :
            lform.recursively_run \
                ("create_object", lform, reverse = True)
            form.inline_errors += lform.error_count
            if lform.instance :
                raw_values.append (lform.get_object_raw ({}))
        ### import pdb; pdb.set_trace ()
    # end def create_object

    @TFL.Meta.Once_Property
    def _linked_instances (self) :
        return TFL.Q_Result (getattr (self.owner.instance, self.link_name))
    # end def _linked_instances

    @TFL.Meta.Once_Property
    def forms (self) :
        owner          = self.owner
        et_man         = self.form_cls.et_man
        count          = self.form_count
        form_cls       = self.form_cls
        prototype      = self.owner.prototype
        prefix_pat     = "%s-M%%d" % (self.prefix, )
        result         = []
        instances = self._linked_instances.all ()
        for no in xrange (count) :
            if instances :
                instance = instances.pop (0)
            else :
                instance = None
            result.append \
                (  form_cls
                      ( instance  = instance
                      , prefix    = prefix_pat % no
                      , prototype = prototype
                      , parent    = self.owner
                      )
                )
        return result
    # end def forms

    def setup_javascript (self, parent_form) :
        GTW.Form.Javascript.Link_Inline (self.form_cls, self)
    # end def setup_javascript

# end class Collection_Inline

class _X_Attribute_Inline_ (object) :
    """An inline group handling an attribute which refers to a MOM.Entity"""

    def _setup_javascript (self) :
        if self.completer :
            self.completer.attach               (self.form_cls)
            parent_form = self.form_cls.parent_form
            if issubclass (parent_form, GTW.Form.MOM.Instance) :
                GTW.Form.Javascript.Attribute_Inline (self.form_cls, self)
    # end def _setup_javascript

# end class _X_Attribute_Inline_


if __name__ != "__main__" :
    GTW.Form.MOM._Export ("*")
### __END__ GTW.Form.MOM.Inline
