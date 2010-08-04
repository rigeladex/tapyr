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
#    GTW.Form.MOM._Instance_
#
# Purpose
#    Base class for form's which handle instances
#
# Revision Dates
#    18-Jan-2010 (MG) Creation
#    20-Jan-2010 (MG) Error handling added
#    29-Jan-2010 (MG) Bug fixing
#    30-Jan-2010 (MG) Instance state added, bug fixing continued
#    30-Jan-2010 (MG) Instance state corrected, update roles only if they
#                     have been changed
#     2-Feb-2010 (MG) Collect all `Media`s from the field_group_descriptions
#                     and add the combined Media to the form class
#     2-Feb-2010 (MG) `_get_raw`: pass form to `field.get_raw`
#     2-Feb-2010 (MG) Instance state handling changed (field is now added to
#                     the first field group)
#                     `_create_or_update`: filter hidden field
#                     `hidden_fields` removed
#     3-Feb-2010 (MG) `New`: filter empty field groups
#     3-Feb-2010 (MG) Collect `Media`s of field groups instead of field group
#                     descriptions
#     3-Feb-2010 (MG) `_prepare_form` added
#     3-Feb-2010 (MG) Collect all completers and add the `js_on_ready` to the
#                     Media
#     5-Feb-2010 (MG) Handling of inline forms changed, handling of link
#                     creation changed
#     5-Feb-2010 (MG) Form class setup moved from `New` to `__new__`,
#                     `form_path` added
#     8-Feb-2010 (MG) Directly access the `_etype` of the `et_man` (An_Entity
#                     etype managers work differently)
#                     `__call__?: if `Attribute_Inline` set the
#                     created/modified instance to the main instance
#     9-Feb-2010 (MG) `prefix` added
#    10-Feb-2010 (MG) `form_path` moved from property to `__new__`
#                     `_Instance_.__init__` make a copy of `field_groups`
#                     Support for renaming of instances added
#    16-Feb-2010 (MG) Make `instance_state` empty if instance is None
#    22-Feb-2010 (CT) `Instance.__init__` changed to pass `** kw` to `super`
#    22-Feb-2010 (MG) `_create_instance` factored
#    24-Feb-2010 (MG) `from_name` added and used
#    26-Feb-2010 (MG) Javascript handling changed
#    27-Feb-2010 (MG) `add_internal_fields` changed
#    28-Feb-2010 (MG) `__call__` fixed
#    28-Feb-2010 (MG) `__call__` changed to set attribute inline values only
#                     if the value has not changed (or ortherwise setting a
#                     role of a link to the same object will raise a
#                     name clash error)
#    02-Mar-2010 (MG) `M_Instance.__new__` handle completers on top level forms
#     6-Mar-2010 (MG) Form handling changed
#    10-Mar-2010 (MG) `Instance_State_Field.get_raw` changed to always return
#                     a dict filled with default values even if instance is
#                     `None`
#    11-Mar-2010 (MG) `_create_instance` filter empty raw_values
#     3-May-2010 (MG) New form handling implemented
#     3-May-2010 (MG) Use `e_type.ui_name` instance on `e_type.type_base_name`
#     5-May-2010 (MG) `render_mode_description` added
#    15-May-2010 (MG) `css_class`, `widget`, and `default_render_mode` added
#    19-May-2010 (MG) `_handle_errors` option parameter `field` added
#    20-May-2010 (MG) `next_erroneous_field` added
#    26-May-2010 (MG) Error handling changed
#     1-Jun-2010 (MG) `add_changed_raw` `attrs_in_request_data` counter
#                     added, `has_substance` added
#     1-Jun-2010 (MG) `initial_data` support added
#     9-Jun-2010 (MG) `initial_data` support enhanced
#    22-Jun-2010 (MG) `_create_or_update` special exception handler added to
#                     prevent double recording of invariant errors
#     4-Aug-2010 (MG) Render mode `table` added to `_Instance_`
#    ««revision-date»»···
#--

from   _MOM               import MOM
import _MOM._Attr.Type

from   _TFL                                 import TFL
import _TFL._Meta.Object
from   _TFL.predicate                       import undotted_dict
from   _GTW                                 import GTW
import _GTW._Form._Form_
import _GTW._Form.Field
import _GTW._Form.Widget_Spec
import _GTW._Form._MOM.Inline

import  base64
import  cPickle
import  itertools

class Instance_State_Field (GTW.Form.Field) :
    """Saves the state of the object to edit before the user made changes"""

    hidden   = True
    electric = True

    widget = GTW.Form.Widget_Spec ("html/field.jnj, hidden")

    def get_raw (self, form, defaults = {}) :
        state = {}
        for n, f in form.fields.iteritems () :
            if not f.electric :
                state [n] = defaults.get (form.get_id (f), u"")
        return base64.b64encode (cPickle.dumps (state))
    # end def get_raw

    def decode (self, data) :
        if data :
            return cPickle.loads (base64.b64decode (data))
        return {}
    # end def decode

# end class  Instance_State_Field

class M_Instance (GTW.Form._Form_.__class__) :
    """Meta class for MOM object forms"""

    field_attrs = dict ()

    def __new__ (mcls, name, bases, dct) :
        et_man                   = dct.get ("et_man", None)
        field_group_descriptions = dct.pop ("field_group_descriptions", ())
        form_name                = dct.pop \
            ("form_name", getattr (et_man, "ui_name", None))
        result = super (M_Instance, mcls).__new__ (mcls, name, bases, dct)
        if et_man :
            ### parent must be set during form class creation
            parent               = result.parent
            if parent :
                form_name        = "__".join ((parent.form_name, form_name))
            result.form_name     = form_name
            result.sub_forms     = sub_forms = {}
            field_groups         = []
            medias               = []
            added_fields         = set (result.ignore_fields)
            if not field_group_descriptions :
                ### XXX try to get the default field group descriptions for this
                ### et-man from somewhere
                field_group_descriptions = \
                    (GTW.Form.MOM.Field_Group_Description (), )
            ### make the first pass through all fields groups to resolve the
            ### callable field spec
            for fgd in field_group_descriptions :
                fgd (True, et_man, added_fields, parent = result)
            ### now, make the second pass through the field groups
            for fgd in field_group_descriptions :
                fgs = [   fg
                      for fg in fgd
                          (False, et_man, added_fields, parent = result) if fg
                      ]
                field_groups.extend (fgs)
                for fg in fgs :
                    media = fg.Media
                    if media :
                        medias.append (media)
                    inline_form = getattr (fg, "form_cls", None)
                    if inline_form :
                        sub_forms [inline_form.et_man.ui_name] = \
                            inline_form
                    else :
                        for f in fg.fields :
                            inline_form = getattr (f, "form_cls", None)
                            if inline_form :
                                sub_forms [f.link_name] = inline_form
                    fg.setup_javascript (result)
            result.add_internal_fields (et_man)
            js_on_ready          = ()
            if not parent :
                js_on_ready      = result.javascript.js_on_ready
            result.Media         = GTW.Media.from_list \
                (medias, js_on_ready = js_on_ready)
            result.field_groups  = field_groups
            result.fields        = result._setup_fields (field_groups)
        return result
    # end def __new__

    def add_internal_fields (cls, et_man) :
        ### we add the instance state field
        cls.instance_state_field = Instance_State_Field \
            ("instance_state", et_man = et_man)
        cls.hidden_fields.append (cls.instance_state_field)
    # end def add_internal_fields

    @TFL.Meta.Once_Property
    def completer (cls) :
        return GTW.Form.Javascript.Multi_Completer ()
    # end def completer

    def New (cls, et_man, * field_group_descriptions, ** kw) :
        suffix        = et_man._etype.type_base_name
        if "suffix" in kw :
            suffix    = "__".join ((kw.pop ("suffix"), suffix))
        return cls.__m_super.New \
            ( suffix
            , field_group_descriptions = field_group_descriptions
            , et_man                   = et_man
            , ** kw
            )
    # end def New

# end class M_Instance

class _Instance_ (GTW.Form._Form_) :
    """Base class for the form's handling any kind of MOM instances."""

    __metaclass__           = M_Instance
    et_man                  = None
    prototype               = False
    ignore_fields           = ()
    _create_update_executed = False
    raw_attr_dict           = {}
    initial_data            = {}

    css_class               = "Object-Editor"
    widget                  = GTW.Form.Widget_Spec ("html/form.jnj, object")

    default_render_mode     = "div_seq"

    render_mode_description = GTW.Form.Render_Mode_Description \
        ( div_seq = GTW.Form.Widget_Spec
              ( object     = "html/rform.jnj, object"
              , aid_object = "html/rform.jnj, aid_object"
              )
        , table   = GTW.Form.Widget_Spec
              ( object     = "html/rform.jnj, object"
              , aid_object = "html/rform.jnj, aid_object"
              )
        )

    ### a standard form always creates the instance new and does not reuse an
    ### existing instance
    state            = "N"

    def __init__ ( self
                 , instance     = None
                 , parent       = None
                 , prefix       = None
                 , initial_data = {}
                 , ** kw
                 ) :
        if not prefix :
            prefix                   = self.et_man.ui_name
        self.initial_data            = undotted_dict \
            (dict (self.initial_data, ** initial_data))
        self.__super.__init__ (instance, prefix = prefix, ** kw)
        scope                        = self.et_man.home_scope
        self.parent                  = parent
        ### make a copies of the inline fields/groups to allow caching of the
        ### inline forms
        for src, src_list_class, iln, iln_cls in \
            ( ( "fields"
              , TFL.NO_List
              , "inline_fields"
              , GTW.Form.MOM._Attribute_Inline_
              )
            , ( "field_groups"
              , list
              , "inline_groups"
              , GTW.Form.MOM.Link_Inline
              )
            ):
            new_src_list                 = src_list_class ()
            iln_list                     = []
            for e in getattr (self, src) :
                if isinstance (e, iln_cls) :
                    e = e.clone     (self)
                    iln_list.append (e)
                new_src_list.append (e)
            setattr (self, src, new_src_list)
            setattr (self, iln, iln_list)
    # end def __init__

    def add_changed_raw (self, dict, field) :
        if isinstance (field, basestring) :
            field = self.fields [field]
        raw       = self.get_raw            (field, None)
        if raw is None :
            raw   = u""
        else :
            self.attrs_in_request_data += 1
        old       = self.instance_state.get (field.name, u"")
        if raw != old :
            dict [field.name] = raw
    # end def add_changed_raw

    def _create_instance (self, on_error) :
        if not self.instance or self.state == "r" :
            ### a new instance should be created starting from scratch or
            ### from a rename -> we have to fill in at least all primaries
            for attr_kind in self.et_man._etype.primary :
                n             = attr_kind.attr.name
                if n not in self.raw_attr_dict :
                    raw_value = attr_kind.get_raw (self.instance)
                    if 1 or raw_value :
                        self.raw_attr_dict [n] = raw_value
        return self.et_man \
            (raw = True, on_error = on_error, ** self.raw_attr_dict)
    # end def _create_instance

    def create_object (self, form) :
        self._create_or_update (False)
    # end def _create_object

    def _create_or_update (self, force_create = False) :
        if (  (not self._create_update_executed and self.raw_attr_dict)
           or (   not self.instance
              and not self.error_count
              and self.request_data
              and force_create
              )
           ) :
            ###    at least on attribute is filled out
            ### or the creation is forced on a post request if the instance
            ###    has not been created so far.
            self._create_update_executed = True
            instance                     = self.instance
            errors = []
            try :
                if instance and self.state != "r" :
                    instance.set_raw \
                        (on_error = errors.append, ** self.raw_attr_dict)
                else :
                    self.instance = self._create_instance \
                        (on_error = errors.append)
            except MOM.Error.Invariant_Errors :
                ### since we pass an on_error hanlder an ` Invariant_Errors`
                ### exception can only be raise in case of propblems with
                ### mandatory attributes in which case the errors are already
                ### stored in the `errors` list and therefore don't need to
                ### be handled again
                pass
            except Exception, exc:
                if __debug__ :
                    import traceback
                    traceback.print_exc ()
                errors.append   (exc)
            self._handle_errors (errors)
        return self.instance
    # end def _create_or_update

    def get_object_raw (self, defaults = {}) :
        instance = self._create_or_update (True)
        return getattr (instance, "epk_raw", ())
    # end def get_object_raw

    @TFL.Meta.Once_Property
    def has_substance (self) :
        return self.request_data and self.attrs_in_request_data > 0
    # end def has_substance

    def _handle_errors (self, error_list, field = None) :
        for error_or_list in error_list :
            error_list = (error_or_list, )
            if isinstance (error_or_list, MOM.Error.Invariant_Errors) :
                error_list = error_or_list.args [0]
            for error in error_list :
                field      = None
                attributes = list (getattr (error, "attributes", ()))
                attr       = getattr       (error, "attribute",  field)
                if attr :
                    attributes.append (attr)
                for attr in attributes :
                    try :
                        field = self.fields [attr]
                    except KeyError :
                        import pdb; pdb.set_trace ()
                    break
                self.errors.add (self, field, error)
    # end def _handle_errors

    @TFL.Meta.Once_Property
    def instance_state (self) :
        if self.request_data :
            state = self.request_data.get \
                (self.get_id (self.instance_state_field))
        else :
            state = self.instance_state_field.get_raw (self)
        return self.instance_state_field.decode (state)
    # end def instance_state

    def prepare_request_data (self, form, request_data) :
        self.request_data = request_data
    # end def prepare_request_data

    def setup_raw_attr_dict (self, form) :
        self.attrs_in_request_data = 0
        self.raw_attr_dict         = dict ()
        for f in (f for f in self.fields if not f.electric) :
            self.add_changed_raw (self.raw_attr_dict, f)
    # end def setup_raw_attr_dict

    def recursively_run (self, method_name, * args, ** kw) :
        lists   = [self], self.inline_groups, self.inline_fields
        if kw.pop ("reverse", False) :
            lists = reversed (lists)
        for obj in itertools.chain (* lists) :
            getattr (obj, method_name) (* args, ** kw)
    # end def recursively_run

    def update_object (self, form) :
        pass
    # end def update_object

    def update_raw_attr_dict (self, form) :
        pass
    # end def update_raw_attr_dict

    def __call__ (self, request_data) :
        ### first, we give each form_group the chance of adding/changing
        ### the request data
        self.recursively_run ("prepare_request_data", self, request_data)
        ### now we build the attr_dict for this form and for all forms in
        ### the inline groups based on the request_data
        self.recursively_run ("setup_raw_attr_dict", self)
        ### Once the raw attr dict for all forms are created let's give the
        ### fields and field groups a change to update the raw attr dict
        self.recursively_run ("update_raw_attr_dict", self)
        ### it's time to actually create the object based on the raw
        ### attr dict
        self.recursively_run ("create_object",        self, reverse = True)
        ### once the object are created the field groups get one final
        ### chance to update the created object
        self.recursively_run ("update_object",        self)
        return self.error_count ()
    # end def __call__

# end class _Instance_

if __name__ != "__main__" :
    GTW.Form.MOM._Export ("*")
### __END__ GTW.Form.MOM._Instance_
