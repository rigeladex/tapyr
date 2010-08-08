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
#     4-May-2010 (CT) `Collection_Inline._linked_instances` changed to not
#                     return `None`
#    06-May-2010 (MG) `s/_linked_instances/linked_instances/g`
#    12-May-2010 (MG) `setup_javascript` changed
#    12-May-2010 (CT) Use `pid`, not `lid`
#    13-May-2010 (MG) UI-Display editing style continued
#    19-May-2010 (MG) `test` added
#    26-May-2010 (MG) Error handling changed
#    28-May-2010 (MG) Support nexted attributes for `ui_display_attrs`
#    28-May-2010 (MG) s/ui_display_attrs/list_display/g
#                     s/ui_display/list_display_values/
#    28-May-2010 (MG) `list_display_values` fixed
#     1-Jun-2010 (MG) `initial_data` support added
#    24-Jun-2010 (MG) `setup_javascript` changed to support callables in
#                     `javascript_options`
#     3-Aug-2010 (MG) `initial_pid_and_state` changed to handle `role_names`
#                     correctly
#     8-Aug-2010 (MG) State handling changed, inline `testing` changed
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
import  operator

class Link_Inline (TFL.Meta.Object) :
    """Handling of all link-forms as a field group of a form.."""

    request_data = dict ()
    ### if different form `None` only the form with the number set will be
    ### evaluated

    restrict_to  = None

    def __init__ (self, inline_description, form_cls, owner = None) :
        self.name               = form_cls.et_man._etype.type_base_name
        self.inline_description = inline_description
        self.form_cls           = form_cls
        self.owner              = owner
        self.test               = owner and owner.test
        if owner :
            self.prefix         = "__".join ((owner.prefix, self.name))
            self.prefix_pat     = "%s-M%%s" % (self.prefix, )
            self._initial_pids  = set ()
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

    @TFL.Meta.Once_Property
    def form_count (self) :
        count         = 0
        try :
            value     = self.request_data [self.range_field_name]
            count     = int (value.split (":") [1])
        except KeyError :
            owner     = self.owner
            if owner.instance :
                count = self.min_empty + self.linked_instances.count ()
        return min \
            (self.max_count, max (self.min_count, self.min_required, count))
    # end def form_count

    @TFL.Meta.Once_Property
    def forms (self) :
        owner          = self.owner
        et_man         = self.form_cls.et_man
        used_instances = dict ()
        if self.restrict_to is None :
            count      = self.form_count
            no_offset  = 0
        else :
            count      = 1
            no_offset  = self.restrict_to
        form_cls       = self.form_cls
        prototype      = self.owner.prototype
        pid_pat        = "__".join ((self.prefix_pat, "_pid_"))
        result         = []
        ### find the links currently linked to the owner
        if owner.instance :
            instances = dict ((str (i.pid), i) for i in self.linked_instances)
        else :
            instances = dict ()
        ### find the links which are actively requested by forms
        for no in xrange (count) :
            pid = self.request_data.get (pid_pat % no, ":").split (":") [0]
            if pid :
                used_instances [pid] = instances.pop (pid, None)
        instances    = sorted (instances.values ())
        initial_data = owner.initial_data.get (self.own_role_name, {})
        for no in xrange (count) :
            pid = self.request_data.get (pid_pat % no, ":").split (":") [0]
            ### assign the correct link to the form or assign a free link
            if pid in used_instances :
                instance = used_instances [pid]
            elif instances :
                instance = instances.pop (0)
            else :
                instance = None
            result.append \
                (  form_cls
                      ( instance     = instance
                      , prefix       = self.prefix_pat % (no + no_offset)
                      , form_number  = no + no_offset
                      , inline       = self
                      , prototype    = prototype
                      , parent       = self.owner
                      , initial_data = initial_data
                      , test         = owner.test
                      )
                )
        return result
    # end def forms

    @TFL.Meta.Once_Property
    def linked_instances (self) :
        if self.owner.instance :
            et_man = self.form_cls.et_man
            return et_man.query \
                ( sort_key = et_man.sorted_by
                , ** {self.own_role_name : self.owner.instance}
                )
        return TFL.Q_Result (())
    # end def linked_instances

    def initial_pid_and_state (self, link, no) :
        if not self.test and link.pid and link not in self._initial_pids :
            self._initial_pids.add (link)
            pid_name_pat   = "%s%%s___pid_"   % (self.prefix_pat % no, )
            state_name_pat = "%s%%s___state_" % (self.prefix_pat % no, )
            result         = []
            attr_spec      = [""]
            attr_spec.extend (self.role_names)
            for attr in attr_spec :
                obj       = link
                css_class = "mom-link"
                if attr :
                    obj       = getattr (obj, attr)
                    attr      = "__%s" % (attr, )
                    css_class = "mom-obj"
                result.extend \
                    ( ( (obj.pid, pid_name_pat   % (attr, ), css_class)
                      , ("",      state_name_pat % (attr, ), css_class)
                      )
                    )
            return result
        return ()
    # end def initial_pid_and_state

    @TFL.Meta.Once_Property
    def Media (self) :
        return GTW.Media.from_list \
            ([m for m in (self.media, self.form_cls.Media) if m])
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

    def setup_javascript (self, parent_form) :
        if self.render_mode == "popup" :
            cls = GTW.Form.Javascript.Link_Inline_UI_Display
        else :
            cls = GTW.Form.Javascript.Link_Inline
        jso = dict ()
        for k, v in self.javascript_options.iteritems () :
            if callable (v) :
                v = v (self)
            jso [k] = v
        cls (self.form_cls, self, ** jso)
    # end def setup_javascript

    def create_object (self, form) :
        ### add checks for min/max
        if getattr (GTW.Form.MOM._Instance_, "BREAK", False) :
            import pdb; pdb.set_trace ()
        for lform in self.forms :
            lform.recursively_run \
                ("create_object", lform, reverse = True)
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

    def list_display_values (self, link) :
        etype = self.form_cls.et_man._etype
        for attr in self.inline_description.list_display :
            try :
                value = operator.attrgetter (attr) (link)
            except AttributeError :
                print attr, link
                raise
            if hasattr (value, "ui_display") :
                yield value.ui_display
            else :
                obj = link
                oet = etype
                while "." in attr :
                    kind_name, attr = attr.split (".")
                    oet             = getattr (etype, kind_name).Class
                    obj             = getattr (link,  kind_name)
                kind = getattr     (oet, attr)
                yield kind.get_raw (obj)
    # end def list_display_values

    def update_object (self, form) :
        for lform in self.forms :
            lform.recursively_run ("update_object", lform)
    # end def update_object

    def update_raw_attr_dict (self, form) :
        for lform in self.forms :
            lform.recursively_run ("update_raw_attr_dict", lform)
    # end def update_raw_attr_dict

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
            if lform.instance :
                raw_values.append (lform.get_object_raw ({}))
        ### import pdb; pdb.set_trace ()
    # end def create_object

    @TFL.Meta.Once_Property
    def linked_instances (self) :
        return TFL.Q_Result \
            (getattr (self.owner.instance, self.link_name) or ())
    # end def linked_instances

    @TFL.Meta.Once_Property
    def forms (self) :
        owner          = self.owner
        et_man         = self.form_cls.et_man
        count          = self.form_count
        form_cls       = self.form_cls
        prototype      = self.owner.prototype
        result         = []
        instances      = self.linked_instances.all ()
        for no in xrange (count) :
            if instances :
                instance = instances.pop (0)
            else :
                instance = None
            result.append \
                (  form_cls
                      ( instance  = instance
                      , prefix    = self.prefix_pat % no
                      , prototype = prototype
                      , parent    = self.owner
                      )
                )
        return result
    # end def forms

    def setup_javascript (self, parent_form) :
        GTW.Form.Javascript.Link_Inline \
            (self.form_cls, self, ** self.javascript_options)
    # end def setup_javascript

# end class Collection_Inline

if __name__ != "__main__" :
    GTW.Form.MOM._Export ("*")
### __END__ GTW.Form.MOM.Inline
