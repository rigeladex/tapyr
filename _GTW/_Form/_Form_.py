# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.Form.
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
#    GTW.Form._Form_
#
# Purpose
#    Base class for forms
#
# Revision Dates
#    19-Jan-2010 (MG) Creation
#    20-Jan-2010 (MG) `get_id` allow string as parameter as well
#     5-Feb-2010 (MG) `M_Form` added
#    10-Feb-2010 (MG) `prefix_sub` added
#    10-Feb-2010 (MG) `get_raw`: As soon as we have `request_data` use the
#                     values from there or empty string (empty strings are
#                     not part of the request data!)
#    22-Feb-2010 (CT) `kw` added
#    26-Feb-2010 (MG) Javascript handling added
#    26-Feb-2010 (MG) `is_checked` added
#    27-Feb-2010 (MG) `M_Form.__new__` added to introduce `hidden_fields`
#     4-Mar-2010 (MG) `error_code` and `Not_Assigned` added
#     4-Mar-2010 (MG) `Hidden_Fields_List` added and used
#     6-Mar-2010 (MG) Error handling changed
#     3-May-2010 (MG) New form handling implemented
#     6-May-2010 (MG) `fgs_need_header` added
#    20-May-2010 (MG) `next_erroneous_field` and `errors_of_field_group` added
#    20-May-2010 (MG) `get_errors` changed to support inline forms
#    26-May-2010 (MG) Error handling changed
#    27-May-2010 (MG) `Form_Errors._order` changed
#     1-Jun-2010 (MG) `get_raw` `default` parameter added
#    29-Jun-2010 (MG) `_Form_.inline_fields` added
#    ««revision-date»»···
#--

from   _TFL               import TFL
import _TFL.I18N
import _TFL._Meta.Object
import _TFL._Meta.Once_Property
import _TFL.defaultdict
import _TFL.Record

from   _GTW              import GTW
import _GTW._Form.Field_Error
import _GTW._Form.Javascript
import _GTW._Form.Widget_Spec

GTW.Form.Widget_Spec.field_error      = "html/form.jnj, field_error"
GTW.Form.Widget_Spec.non_field_errors = "html/form.jnj, field_error"
GTW.Form.Widget_Spec.field_label      = "html/form.jnj, field_label"
GTW.Form.Widget_Spec.fg_tr_head       = "html/form.jnj, fg_tr_head"
GTW.Form.Widget_Spec.fg_tr_body       = "html/form.jnj, fg_tr_body"
GTW.Form.Widget_Spec.th_onion         = "html/form.jnj, th_onion"
GTW.Form.Widget_Spec.td_onion         = "html/form.jnj, td_onion"

GTW.Form.Widget_Spec.field_seq        = "html/form.jnj, field_seq"

class Hidden_Fields_List (object) :
    """A kind of list which handles the hidden fields of a form instance to
       support exactly one iteration over the fields
    """

    def __init__ (self, fields) :
        self.fields = fields
    # end def __init__

    def __nonzero__ (self) :
        return bool (self.fields)
    # end def __nonzero__

    def __iter__ (self) :
        fields, self.fields = self.fields, []
        for f in fields :
            yield f
    # end def __iter__

# end class Hidden_Fields_List

class M_Form (TFL.Meta.Object.__class__) :
    """Meta class for forms."""

    parent = None

    def __new__ (mcls, name, bases, dct) :
        result = super (M_Form, mcls).__new__ (mcls, name, bases, dct)
        result.hidden_fields = []
        return result
    # end def __new__

    def _setup_fields (cls, field_groups) :
        result          = TFL.NO_List ()
        fgs_need_header = False
        for fg in (  fg for fg in field_groups
                  if isinstance (fg, GTW.Form.Field_Group)
                  ) :
            result.update (fg.fields)
            fgs_need_header |= sum (f.needs_header for f in fg.fields) > 0
        result.extend (cls.hidden_fields)
        cls.fgs_need_header = fgs_need_header
        return result
    # end def _setup_fields

    def form_and_completer (cls, path) :
        ### Return the form class and the complter object for the `path`
        ### where path is a list of names specifing the way done from the top
        ### level form to the completer
        form_cls  = cls
        completer = None
        path      = path [0].split ("__")
        while path :
            if path [0] in form_cls.sub_forms :
                form_cls = form_cls.sub_forms [path.pop (0)]
            else :
                break
        completer = getattr (form_cls, "completer", None)
        while path :
            completer = getattr (completer, path.pop (0), None)
        if completer :
            return form_cls, completer
        return None, None
    # end def form_and_completer

    @TFL.Meta.Once_Property
    def form_path_css (cls) :
        return "__".join (getattr (cls, "form_path", "").split ("/"))
    # end def form_path_css

    @TFL.Meta.Once_Property
    def javascript (cls) :
        ### if we are the top level form -> create a new javascript object
        if not cls.parent :
            return GTW.Form.Javascript.Form (cls)
        ### since we have a parent return the javascript object for this form
        return cls.parent.javascript
    # end def javascript

# end class M_Form

class Form_Errors (dict) :
    """A dict object which preserves the order."""

    __metaclass__ = TFL.Meta.M_Class

    def __init__ (self, root) :
        self.__super.__init__ ()
        self.root            = root
        self._no_more_errors = False
    # end def __init__

    def add (self, form, field, error) :
        if form not in self :
            self [form] = TFL.defaultdict (GTW.Form.Error_List)
        if isinstance (field, basestring) :
            field = form.fields.get (field, field)
        self [form] [field].append (error)
    # end def add

    def for_field (self, field) :
        for ed in self.itervalues () :
            if field in ed :
                return ed [field]
        return GTW.Form.Error_List ()
    # end def for_field

    def next_field (self, field) :
        result    = None, None
        if self._no_more_errors or not self._order :
            return result
        form      = getattr (self, "_current_form", self._order [0])
        if field :
            try :
                index = form.fields.index (field)
            except ValueError :
                ### force moving to the next form
                index = len (form.fields)
        else :
            index = -2
        for i in xrange (index + 1, len (form.fields)) :
            if i < 0 :
                field = None
            else :
                field = form.fields [i]
            if self.count (form, field) :
                field  = field or form.fields [0]
                result = field, form.get_id (field)
                break
        while not result [0] and not self._no_more_errors :
            ### no more error's in this form
            form = self._next_form (form)
            if form :
                result = self.next_field (None)
            else :
                self._no_more_errors = True
        self._current_form = form
        return result
    # end def next_field

    def _next_form (self, form) :
        index = self._order.index (form) + 1
        if index < len (self._order) :
            self._current_form = self._order [index]
            return self._current_form
    # end def _next_form

    @TFL.Meta.Once_Property
    def _order (self) :
        result = TFL.Ordered_Set ()
        self._form_order (result, self.root)
        return result
    # end def _order

    def _form_order (self, order, root) :
        order.append (root)
        for fg in root.field_groups :
            if not isinstance (fg, GTW.Form.MOM.Link_Inline) :
                for fi in root.fields_of_field_group (fg) :
                    form = getattr (fi, "form", None)
                    if form :
                        self._form_order (order, form)
            else :
                for form in fg.forms :
                    self._form_order (order, form)
    # end def _form_order

    def _errors_of_form (self, form = None, field = False, transitive = True) :
        if form is None :
            forms = self.iterkeys ()
        else :
            forms = (form, )
        for fo in forms :
            ed     = self.get (fo, TFL.defaultdict (GTW.Form.Error_List))
            fields = (field, )
            if field is False :
                fields = [None]
                fields.extend (fo.fields)
            for f in fields :
                if f in ed :
                    yield f, ed [f]
            if transitive :
                for ifi in fo.inline_fields :
                    for fi, el in self._errors_of_form (ifi.form, field, True) :
                        yield fi, el
    # end def _fields_of_form

    def of_form (self, form, field = False) :
        result = GTW.Form.Error_List ()
        for fi, el in self._errors_of_form (form, field, True) :
            result.add (el)
        return result
    # end def of_form

    def fields_of_form (self, form = None, field = False) :
        result = []
        for fi, el in self._fields_of_form (form, field, True) :
            result.append (fi)
        return result
    # end def fields_of_form

    def count (self, form = None, field = False) :
        result = 0
        for fi, el in self._errors_of_form (form, field, True) :
            result += len (el)
        return result
    # end def count

# end class Form_Errors

class _Form_ (TFL.Meta.Object) :
    """Base class for forms"""

    prefix        = ""
    __metaclass__ = M_Form
    instance      = None
    inline_fields = ()

    def __init__ (self, instance = None, prefix = "", ** kw) :
        if instance is not None :
            self.instance  = instance
        self.prefix        = prefix
        self.request_data  = {}
        self.hidden_fields = Hidden_Fields_List (self.hidden_fields)
        self.kw            = TFL.Record (** kw)
    # end def __init__

    @TFL.Meta.Once_Property
    def errors (self) :
        if not self.parent :
            return Form_Errors (self)
        return self.parent.errors
    # end def errors

    def error_count (self, form = None, field = False) :
        return self.errors.count (form, field)
    # end def error_count

    def fields_with_errors_of_field_group (self, fg, transitive = False) :
        result = []
        if self.errors :
            for fi in self.fields_of_field_group (fg) :
                if self.errors.count (self, None) :
                    result.append (None)
                if self.errors.count (self, fi) :
                    result.append (fi)
                if transitive :
                    form = getattr (fi, "form", None)
                    for fg in getattr (form, "field_groups", ()) :
                        result.extend \
                            (form.fields_with_errors_of_field_group (fg, True))
        return result
    # end def errors_of_field_group

    def fields_of_field_group (self, fg) :
        for f in fg.fields :
            yield self.fields [f.name]
    # end def fields_of_field_group

    def form_defaults (self) :
        defaults = {}
        for f in self.fields :
            defaults [self.get_id (f)] = f.get_raw (self, defaults)
        ### allow the field groups the change the defaults afer the
        ### fields-default have been set
        for fg in self.field_groups :
            fg.defaults (self, self.instance, defaults)
        return defaults
    # end def form_defaults

    def get_errors (self, field = None) :
        if isinstance (field, basestring) :
            field = self.fields [field]
        if field :
            result = self.errors.for_field (field)
        else :
            result = self.errors.of_form  (self, None)
        return result
    # end def get_errors

    def get_id (self, field) :
        if isinstance (field, basestring) :
            field = self.fields [field]
        if self.prefix :
            return "__".join ((self.prefix, field.html_name))
        return field.html_name
    # end def get_id

    def get_raw (self, field, default = u"") :
        return self.raw_values.get (self.get_id (field), default)
    # end def get_raw

    def is_checked (self, field) :
        result = dict (value = "yes")
        if isinstance (field, basestring) :
            field = self.fields [field]
        if field.get_cooked (self) :
            result ["checked"] = "checked"
        return result
    # end def is_chained

    no_more_errors = object ()

    def next_erroneous_field (self, current = None) :
        return self.errors.next_field (current)
    # end def next_erroneous_field

    @TFL.Meta.Once_Property
    def raw_values (self) :
        if self.request_data :
            return self.request_data
        ### since we don't have any request data the raw values are actually
        ### the default values.
        ### A seperate method is used to make overloading much easier
        return self.form_defaults ()
    # end def raw_values

# end class _Form_

if __name__ != "__main__" :
    GTW.Form._Export ("*")
### __END__ GTW.Form._Form_
