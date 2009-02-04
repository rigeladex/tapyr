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
#    ««revision-date»»···
#--

from   _DJO                        import DJO
from   _TFL                        import TFL

from   _DJO.Models                 import _User_Create_Mod_

import _TFL.Decorator
import _TFL._Meta.M_Class

from   django.utils.datastructures import SortedDict
from   django.http                 import HttpResponseRedirect
from   django.utils.html           import escape
from   django.utils.encoding       import smart_unicode, force_unicode
from   django.utils.safestring     import mark_safe
from   django.core.urlresolvers    import reverse
from   django.db.models.base       import Model
from   django.db.models.manager    import Manager
from   django                      import forms
from   django.forms.forms          import BoundField
from   django.forms.models         import BaseModelForm, ModelForm
from   django.utils.translation    import gettext_lazy as _
import copy

class _Form_Output_ (TFL.Meta.Object) :

    @classmethod
    def add_field (cls, bound_field, field_html, label, bf_errors) :
        raise NotImplementedError
    # end def add_field

    @classmethod
    def add_hidden_fields (cls, html) :
        raise NotImplementedError
    # end def add_hidden_fields

    @classmethod
    def add_hidden_field_errors (cls, errors) :
        raise NotImplementedError
    # end def add_hidden_field_errors

    @classmethod
    def add_fieldless_errors (cls, errors) :
        raise NotImplementedError
    # end def add_fieldless_errors

    @classmethod
    def html (cls, form) :
        cls.top_errors                 = form.non_field_errors ()
        cls.output, cls.hidden_fields = [], []
        for name, field in form.fields.items () :
            bf        = BoundField (form, field, name)
            # Escape and cache in local variable.
            bf_errors = form.error_class \
                (escape (error) for error in bf.errors)
            if bf.is_hidden:
                cls.add_hidden_field_errors (name, bf_errors)
                cls.hidden_fields.append    (unicode (bf))
            else:
                if bf.label :
                    label = escape (force_unicode (bf.label))
                    # Only add the suffix if the label does not end in
                    # punctuation.
                    if form.label_suffix :
                        if label [-1] not in ':?.!' :
                            label += form.label_suffix
                    label = bf.label_tag (label) or ''
                else:
                    label = ''
                cls.add_field \
                    (bf, unicode (bf)
                    , force_unicode (label), force_unicode (bf_errors)
                    )
        cls.add_fieldless_errors (cls.top_errors)
        cls.add_hidden_fields    (u"".join (cls.hidden_fields))
        return mark_safe (u"\n".join (cls.output))
    # end def __call__

# end class _Form_Output_

class _Definition_List_ (_Form_Output_) :

    @classmethod
    def add_field (cls, bound_field, field_html, label, bf_errors) :
        cls.output.extend \
            (["<dt>%s</dt>" % (label, ), "<dd>%s</dd>" % (field_html, )])
        field = bound_field.field
        if field.help_text :
            cls.output.append \
                ("<dd>%s</dd>" % (force_unicode (field.help_text)))
        if bf_errors :
            cls.output.append \
                ('<dd class="form_errors">%s</dd>' % (bf_errors, ))
    # end def add_field

    @classmethod
    def add_hidden_fields (cls, html) :
        if cls.output :
            cls.output [-1] = \
                "%s%s</dd>" % (cls.output [-1] [:-len ("</dd>")] , html)
        else :
            cls.output.append (html)
    # end def add_hidden_fields

    @classmethod
    def add_hidden_field_errors (cls, name, errors) :
        cls.top_errors.extend \
            ( [ "(Hidden field %s) %s"
                % (name, force_unicode (e)) for e in errors
              ]
            )
    # end def add_hidden_field_errors

    @classmethod
    def add_fieldless_errors (cls, errors) :
        if errors :
            cls.output [0:0] = \
                [ '<dt class="form_errors">%s</dt>' % (_("Errors"), )
                , '<dd class="form_errors">%s</dd>' % (errors, )
                ]
    # end def add_fieldless_errors

# end class _Definition_List_

class _Table_ (_Form_Output_) :

    @classmethod
    def add_field (cls, bound_field, field_html, label, bf_errors) :
        field = bound_field.field
        cls.output.append ("<tr>")
        cls.output.append ("<td>%s</td>" % (label, ))
        cls.output.append ("<td>")
        cls.output.append (field_html)
        if field.help_text :
            cls.output.append (force_unicode (field.help_text))
        if bf_errors :
            cls.output.append (bf_errors)
        cls.output.append ("</td>")
        cls.output.append ("</tr>")
    # end def add_field

    @classmethod
    def add_hidden_fields (cls, html) :
        cls.output.append (html)
    # end def add_hidden_fields

    @classmethod
    def add_hidden_field_errors (cls, name, errors) :
        cls.top_errors.extend \
            ( [ "(Hidden field %s) %s"
                % (name, force_unicode (e)) for e in errors
              ]
            )
    # end def add_hidden_field_errors

    @classmethod
    def add_fieldless_errors (cls, errors) :
        if errors :
            cls.output [0:0] = \
                ['<span class="form_errors">%s</span>' % (errors, )]
    # end def add_fieldless_errors

# end class _Table_

class _Markup_Less_ (_Form_Output_) :

    @classmethod
    def add_field (cls, bound_field, field_html, label, bf_errors) :
        field_tags = ["<span>"]
        field      = bound_field.field
        if field.help_text :
            field_tags.append (force_unicode (field.help_text))
        if bf_errors :
            field_tags.append \
                ('<span class="form_errors">%s/span>' % (bf_errors, ))
        field_tags.extend ((field_html, "</span>"))
        cls.output.append (label)
        cls.output.extend (field_tags)
    # end def add_field

    @classmethod
    def add_hidden_fields (cls, html) :
        cls.output.append (html)
    # end def add_hidden_fields

    @classmethod
    def add_hidden_field_errors (cls, name, errors) :
        cls.top_errors.extend \
            ( [ "(Hidden field %s) %s"
                % (name, force_unicode (e)) for e in errors
              ]
            )
    # end def add_hidden_field_errors

    @classmethod
    def add_fieldless_errors (cls, errors) :
        if errors :
            cls.output [0:0] = \
                ['<span class="form_errors">%s</span>' % (errors, )]
    # end def add_fieldless_errors

# end class _Markup_Less_

class SortedDictFromList (SortedDict):
    "A dictionary that keeps its keys in the order in which they're inserted."
    # This is different than django.utils.datastructures.SortedDict, because
    # this takes a list/tuple as the argument to __init__().

    def __init__(self, data = None):
        if data is None :
            data = []
        self.keyOrder = [ d [0] for d in data]
        dict.__init__ (self, dict (data))
    # end def __init__

    def copy (self):
        return SortedDictFromList \
            ([(k, copy.deepcopy (v)) for k, v in self.iteritems ()])
    # end def copy

# end class SortedDictFromList

class M_Fields_From_Model (TFL.Meta.M_Class) :
    """Meta class for form class creation."""

    def __new__ (cls, name, bases, attrs) :
        model             = attrs.get ("model",          None)
        model_field_names = attrs.pop ("model_fields",   ())
        field_order       = attrs.pop ("field_order",    model_field_names)
        field_override    = attrs.pop ("field_override", {})
        model_field_names = set (model_field_names)
        fields            = dict \
            ( (field_name, attrs.pop (field_name))
                for field_name, obj in attrs.items () ## we pop items from
                                                      ## the dict -> no iter
                  if isinstance (obj, forms.Field)
            )
        if model_field_names and model :
            model_fields = model._meta.fields + model._meta.many_to_many
            fields.update \
                ( (f.name, field_override.get (f.name, None) or f.formfield ())
                    for f in model_fields if f.name in model_field_names
                )
        set_after_save = set (attrs.get ("set_after_save", ()))
        sorted_fields  = [(fn, fields.pop (fn)) for fn in field_order]
        sorted_fields.extend \
            ( (fn, f) for (fn, f) in sorted
                ( fields.iteritems ()
                , key = lambda (fn, f) : f.creation_counter
                )
            )
        if not "set_before_save" in attrs :
            attrs ["set_before_save"] = set \
                (fn for fn, f in sorted_fields if not fn in set_after_save)
        attrs ["set_after_save"] = set_after_save
        attrs ["base_fields"]    = SortedDictFromList (sorted_fields)
        return super (M_Fields_From_Model, cls).__new__ \
            (cls, name, bases, attrs)
    # end def __new__

# end class M_Fields_From_Model

class Form (forms.BaseForm) :
    """Base class for all forms."""

    __metaclass__ = M_Fields_From_Model

    def __init__ (self, request, ** kw) :
        self.REQUEST = request
        add_files    = kw.pop ("add_files", False)
        instance     = self.INSTANCE = kw.pop ("instance",  None)
        setup        = kw.pop ("setup",     {})
        data         = files = None
        self.is_post = request.method == "POST"
        if self.is_post :
            data = request.POST
        elif instance :
            initial = {}
            for attr in self.base_fields.iterkeys () :
                value = getattr (instance, attr, None)
                if value is not None :
                    if isinstance (value, Manager) :
                        value = [o.pk for o in value.all ()]
                    elif isinstance (value, Model) :
                        value = value.pk
                    initial [attr] = value
            kw.setdefault ("initial", {}).update (initial)
        if add_files :
            files = request.FILES
        if "redirect_to" in kw :
            self.redirect_to = Reverse_Redirect (* kw.pop ("redirect_to"))
        super (Form, self).__init__ (data = data, files = files, ** kw)
        self._setup_fields (** setup)
    # end def __init__

    def process_request (self, ** kw) :
        if self.is_post and self.is_valid () :
            return self.save (** kw)
        return False
    # end def process_request

    def _setup_fields (self) :
        pass
    # end def _setup_fields

    def save (self, ** kw) :
        instance             = self.INSTANCE
        request              = self.REQUEST
        cd                   = self.cleaned_data
        created              = instance is None
        if not instance :
            instance         = self.model ()
        save_kw              = kw.pop ("save", {})
        if isinstance (instance, _User_Create_Mod_) :
            save_kw ["user"] = request.user
        for field in self.set_before_save :
            setattr (instance, field, cd [field])
        for n, v in kw.get ("set_before_save", {}).iteritems () :
            setattr (instance, n, v)
        if created :
            instance.save (** save_kw)
        for field in self.set_after_save :
            setattr (instance, field, cd [field])
        for n, v in kw.get ("set_after_save", {}).iteritems () :
            setattr (instance, n, v)
        instance.save (** save_kw)
        return self._save_successfull (** kw)
    # end def save

    def _save_successfull (self, ** kw) :
        if hasattr (self, "redirect_to") :
            return self.redirect_to (self.REQUEST, self.INSTANCE, ** kw)
        return False
    # end def _save_successfull

    def __nonzero__ (self) :
        return bool (self.INSTANCE)
    # end def __nonzero__

    def as_plain (self) :
        return _Markup_Less_.html (self)
    # end def as_plan

    def as_dl (self) :
        ##import pdb; pdb.set_trace ()
        return _Definition_List_.html (self)
    # end def as_dl

    def as_table (self) :
        return _Table_.html (self)
    # end def as_dl

# end class Form

class Redirect (TFL.Meta.Object) :
    """Redirect to a static URL"""

    def __init__ (self, url, anchor = None) :
        self.url    = url
        self.anchor = anchor
    # end def __init__

    def __call__ (self, * args, ** kw) :
        url = [self._url ()]
        if self.anchor :
            url.append (self.anchor)
        return HttpResponseRedirect ("#".join (url))
    # end def __call__

    def _url (self, url) :
        return self.url
    # end def _url

# end class Redirect

class Reverse_Redirect (Redirect) :
    """Redirect to a named url pattern"""

    def __init__ (self, url_pattern_name, * args, ** kw) :
        self.url_pattern_name = url_pattern_name
        self.anchor           = kw.pop ("anchor", None)
        self.args             = args
        self.kw               = kw
    # end def __init__

    def _url (self) :
        return reverse \
            (self.url_pattern_name, args = self.args, kwargs = self.kw)
    # end def _url

# end class Reverse_Redirect

class FileNameInput (forms.widgets.FileInput) :

    def value_from_datadict (self, data, files, name) :
        return data.get (name, None)
    # end def value_from_datadict

# end class FileNameField

@TFL.Add_New_Method (BaseModelForm)
@TFL.Contextmanager
def object_to_save (self, commit=True) :
    """Context manager for saving an object created from a form"""
    obj = self.save (commit=False)
    try :
        yield obj
    finally :
        if commit :
            obj.save      ()
            self.save_m2m ()
# end def object_to_save

class M_Model_Form (TFL.Meta.M_Class, ModelForm.__class__) :
    """Meta class for model forms with support for `.__super` and
       `_real_name`.
    """
# end class M_Model

class _DJO_Model_Form_ (ModelForm) :

    __metaclass__ = M_Model_Form
    _real_name    = "Model_Form"
    _djo_clean    = None

    def clean (self) :
        result = self.__super.clean ()
        if callable (self._djo_clean) :
            result = self._djo_clean (result)
        return result
    # end def clean

Model_Form = _DJO_Model_Form_ # end class

if __name__ != "__main__" :
    DJO._Export ("*")
### __END__ DJO.Forms
