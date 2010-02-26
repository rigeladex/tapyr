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

class Instance_Collection (object) :

    def __init__ (self, et_man, instances, lids_used = set ()) :
        self.et_man     = et_man
        self.instances  = tuple (i for i in instances if i is not None)
        self._by_lid    = dict \
            ((getattr (i, "lid", ""), i) for i in self.instances)
        self._unused    = \
            [i for (lid, i) in self._by_lid.iteritems ()
               if lid not in lids_used
            ]
    # end def __init__

    def instance_for_lid (self, lid = "") :
        instance = self._by_lid.get (lid)
        if not instance :
            if lid :
                et_man             = self.et_man
                pid                = et_man.pid_from_lid         (lid)
                self._by_lid [lid] = instance = et_man.pid_query (pid)
                assert instance not in self._unused
            else :
                try :
                    instance = self._unused.pop (0)
                except IndexError :
                    instance = None
        return instance
    # end def instance_for_lid

# end class Instance_Collection

class _Inline_ (TFL.Meta.Object) :
    """A Inline `form` inside a real form."""

    def __init__ ( self, inline_description, form_cls, parent = None) :
        self.inline_description = inline_description
        self.form_cls           = form_cls
        self.parent             = parent
        self.errors             = GTW.Form.Error_List ()
        self.name               = form_cls.et_man._etype.type_base_name
    # end def __init__

    def clone (self, parent) :
        return self.__class__ (self.inline_description, self.form_cls, parent)
    # end def clone

    def get_errors (self) :
        return self.errors
    # end def get_errors

    @TFL.Meta.Once_Property
    def Media (self) :
        self._setup_javascript ()
        return GTW.Media.from_list \
            ([m for m in (self.widget.Media, self.form_cls.Media) if m])
    # end def Media

    @TFL.Meta.Once_Property
    def prototype_form (self) :
        iform_cls     = self.form_cls
        et_man        = iform_cls.et_man
        parent        = self.parent
        return iform_cls \
            (None, prefix_sub = "-MP", parent = parent, prototype = True)
    # end def prototype_form

    def _setup_javascript (self) :
        pass
    # end def _setup_javascript

    def __call__ (self, request_data) :
        return sum (ifo (request_data) for ifo in self.forms)
    # end def __call__

    def __getattr__ (self, name) :
        result = getattr (self.inline_description, name)
        setattr (self, name, result)
        return result
    # end def __getattr__

# end class _Inline_

class Attribute_Inline (_Inline_) :
    """An inline group handling an attribute which refers to a MOM.Entity"""

    form_count = 1

    @TFL.Meta.Once_Property
    def error_count (self) :
        return self.forms [0].error_count
    # end def error_count

    @TFL.Meta.Once_Property
    def forms (self) :
        return \
            [ self.form_cls
                ( prefix_sub = self.parent.prefix_sub
                , parent     = self
                , prototype  = self.parent.prototype
                )
            ]
    # end def forms

    @TFL.Meta.Once_Property
    def instance (self) :
        return self.forms [0].instance
    # end def instance

    def _setup_javascript (self) :
        if self.completer :
            self.completer.attach               (self.form_cls)
            parent_form = self.form_cls.parent_form
            if issubclass (parent_form, GTW.Form.MOM.Instance) :
                GTW.Form.Javascipt.Attribute_Inline (self.form_cls, self)
    # end def _setup_javascript

    @TFL.Meta.Once_Property
    def Instances (self) :
        return Instance_Collection \
            ( self.form_cls.et_man
            , (getattr (self.parent.instance, self.link_name, None), )
            )
    # end def Instances

# end class Attribute_Inline

class Link_Inline (_Inline_) :
    """An inline group handling a MOM.Link"""

    @TFL.Meta.Once_Property
    def range_field_name (self) :
        return "%s-m2m-range" % (self.form_cls.et_man._etype.type_base_name, )
    # end def range_field_name

    @TFL.Meta.Once_Property
    def Instances (self) :
        parent = self.parent
        et_man = self.form_cls.et_man
        if parent.instance :
            instances = et_man.query (** {self.own_role_name : parent.instance})
        else :
            instances = ()
        return Instance_Collection \
            (et_man, instances, set (f.lid for f in self.forms))
    # end def Instances

    @TFL.Meta.Once_Property
    def form_count (self) :
        count         = 0
        parent        = self.parent
        try :
            value     = parent.request_data [self.range_field_name]
            count     = int (value.split (":") [1])
        except KeyError :
            if parent.instance :
                count = self.min_empty + self.form_cls.et_man.query \
                    (** {self.own_role_name : parent.instance}).count ()
        return min \
            (self.max_count, max (self.min_count, self.min_required, count))
    # end def form_count

    @TFL.Meta.Once_Property
    def forms (self) :
        form_cls  = self.form_cls
        prototype = self.parent.prototype
        return \
            [   form_cls
                  ( prefix_sub = "-M%s" % (no if not prototype else "P", )
                  , parent     = self
                  , prototype  = prototype
                  )
            for no in xrange (self.form_count)
            ]
    # end def forms

    def _setup_javascript (self) :
        GTW.Form.Javascipt.Link_Inline (self.form_cls, self)
    # end def _setup_javascript

    def __call__ (self, request_data) :
        error_count   = self.__super.__call__ (request_data)
        correct_forms = []
        if not error_count :
            correct_forms = \
                [ ifo for ifo in self.forms
                    if ifo.instance and not ifo.error_count
                ]
        correct_forms_count = len (correct_forms)
        if correct_forms_count < self.min_required :
            self.errors.append \
                (u"At least %(min)d inline instances are required"
                  "(%(current)d)"
                % dict (current = correct_forms_count, min = self.min_required)
                )
            error_count += 1
        if correct_forms_count > self.max_count :
            self.errors.append \
                ( u"More that %(max)d instance specified (%(current)d)"
                % dict (current = correct_forms_count, max = self.max_count)
                )
            error_count += 1
        return error_count
    # end def __call__

# end class Link_Inline

if __name__ != "__main__" :
    GTW.Form.MOM._Export ("*", "_Inline_")
### __END__ GTW.Form.MOM.Inline
