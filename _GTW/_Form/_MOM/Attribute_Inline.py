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
#    GTW.Form.MOM.Attribute_Inline
#
# Purpose
#    Handle the creation/modification of an object inside of a other form.
#    The attribute inline will be treated like a `Field` of a form and not
#    like a inline group
#
# Revision Dates
#    15-Apr-2010 (MG) Creation
#     3-May-2010 (MG) `need_change` added and used
#     6-May-2010 (MG) `ui_name` and `visible_field_count` added
#     6-May-2010 (MG) `create_object` change to set the role of the link if
#                     this instance has not changed but the link does not
#                     exist yet (this happens if the role has been
#                     auto-completed)
#     7-May-2010 (MG) `need_change` eliminated, `create_object` changed
#    12-May-2010 (CT) Use `pid`, not `lid`
#    19-May-2010 (MG) `Id_Attribute_Inline_Instance.create_object` added
#     1-Jun-2010 (MG) `initial_data` support added
#     8-Aug-2010 (MG) State handling changed, inline `testing` changed
#    ««revision-date»»···
#--

from   _TFL                                 import TFL
import _TFL._Meta.Once_Property
from   _TFL.predicate                       import all_true
from   _GTW                                 import GTW
import _GTW._Form.Field
import _GTW._Form.Widget_Spec
import _GTW._Form._MOM
import _GTW._Form._MOM.Inline_Instance

class _GTW_Attribute_Inline_ (TFL.Meta.Object) :
    """The `field` instance for attribute inline editing."""

    electric    = False
    _real_name  = "_Attribute_Inline_"

    def __init__ (self, name, form_cls, inline_description, form = None) :
        self.name               = self.html_name = name
        self.form_cls           = form_cls
        self.inline_description = inline_description
        self.form               = form
    # end def __init__

    def create_object (self, parent_form) :
        form = self.form
        parent_form.raw_attr_dict.pop (self.name, None)
        if self.needs_processing :
            form.recursively_run ("create_object", form, reverse = True)
        if (    not form.error_count (form)
           and (   form.instance
               or (form.is_link_role and form.raw_attr_dict)
               )
           ) :
            p_instance = parent_form.instance
            instance   = self.form.instance
            if getattr (p_instance, form.generic_name, None) != instance :
                ### the instance has been created/updated successfully ->
                ### update the raw_attr_dict of the parent
                parent_form.raw_attr_dict [form.generic_name] = \
                    form.get_object_raw (parent_form)
            else :
                parent_form.raw_attr_dict.pop (form.generic_name, None)
        ### do not move the caching up because the `get_object_raw` could
        ### create additional errors
        ec = form.error_count (form)
        if ec or not form.instance :
            ### an error was detected or the instance has not been
            ### created -> delete the values for this attribute from
            ### parent's raw_attr_dict
            parent_form.raw_attr_dict.pop (form.generic_name, None)
        ##parent_form.inline_errors += ec
    # end def create_object

    def clone (self, form) :
        instance     = getattr (form.instance, self.name, None)
        name         = self.name
        if name not in form.initial_data :
            name     = self.attr_kind.name
        initial_data = form.initial_data.get (name, {})
        return self.__class__ \
            ( self.name, self.form_cls, self.inline_description
            , self.form_cls
                ( instance
                , parent       = form
                , prefix       = "__".join ((form.prefix, self.name))
                , initial_data = initial_data
                , test         = form.test
                )
            )
    # end def clone

    def get_raw (self, form, defaults) :
        return self.form.get_object_raw (defaults)
    # end def get_raw

    @TFL.Meta.Once_Property
    def Media (self) :
        try :
           self._setup_javascript ()
           return self.media
        except StandardError, e :
            import pdb; pdb.set_trace ()
            raise
    # end def Media

    @TFL.Meta.Once_Property
    def needs_header (self) :
        return self.inline_description.needs_header \
            or (self.visible_field_count > 1)
    # end def needs_header

    def prepare_request_data (self, form, request_data) :
        self.form.recursively_run \
            ("prepare_request_data", self.form, request_data)
    # end def prepare_request_data

    def _setup_javascript (self) :
        pass
    # end def _setup_javascript

    def set_cooked_attr (self, attr_dict, raw_attr_dict) :
        attr_dict [self.form.generic_name] = self.form.instance
        raw_attr_dict.pop (self.name,              None)
        raw_attr_dict.pop (self.form.generic_name, None)
    # end def set_cooked_attr

    def setup_raw_attr_dict (self, form) :
        self.form.recursively_run ("setup_raw_attr_dict", self.form)
    # end def setup_raw_attr_dict

    @TFL.Meta.Once_Property
    def visible_field_count (self) :
        return len ([f for f in self.form_cls.fields if not f.hidden])
    # end def visible_field_count

    @TFL.Meta.Once_Property
    def ui_name (self) :
        return self.form_cls.et_man.ui_name
    # end def ui_name

    def update_object (self, form) :
        self.form.recursively_run ("update_object", self.form)
    # end def update_object

    def update_raw_attr_dict (self, form) :
        self.form.recursively_run ("update_raw_attr_dict", self.form)
    # end def update_raw_attr_dict

    def __getattr__ (self, name) :
        try :
            return getattr (self.inline_description, name)
        except AttributeError :
            raise AttributeError (name)
    # end def __getattr__

_Attribute_Inline_ = _GTW_Attribute_Inline_# end class

class GTW_An_Attribute_Inline (_Attribute_Inline_) :
    """Inline of an An_Entity."""


    Form_Class       = GTW.Form.MOM.An_Attribute_Inline_Instance
    needs_processing = True
    _real_name       = "An_Attribute_Inline_Instance"

An_Attribute_Inline = GTW_An_Attribute_Inline # end class

class GTW_Id_Attribute_Inline (_Attribute_Inline_) :
    """Inline for a ID_Entity."""

    Form_Class = GTW.Form.MOM.Id_Attribute_Inline_Instance
    _real_name = "Id_Attribute_Inline"

    @TFL.Meta.Once_Property
    def needs_processing (self) :
        state = self.form.state
        pid   = self.form.pid
        if state == "U" :
            ### this from handles an instance which should be unlinked
            ### because we handle an attribute inline we cannot destroy the
            ### object but just unlink it from the parent object
            self.form.instance = None
            return False
        if pid and not self.form.test :
            ### the client side provided information which object should be
            ### linked -> let's get this object by it's pid and set it in the
            ### form
            self.form.instance = self.form.et_man.pid_query (self.form.pid)
        return True
    # end def needs_processing

    def _setup_javascript (self) :
        if self.form_cls.completer :
            self.form_cls.completer.attach (self.form_cls, self.link_name)
            GTW.Form.Javascript.Attribute_Inline \
                (self.form_cls, self, ** self.javascript_options)
    # end def _setup_javascript

Id_Attribute_Inline = GTW_Id_Attribute_Inline # end class

if __name__ != "__main__" :
    GTW.Form.MOM._Export ("*", "_Attribute_Inline_")
### __END__ GTW.Form.MOM.Attribute_Inline
