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
#    «text»···
#
# Revision Dates
#    18-Jan-2010 (MG) Creation
#    ««revision-date»»···
#--

from   _MOM               import MOM
import _MOM._Attr.Type

from   _TFL                                 import TFL
import _TFL._Meta.Object

from   _GTW                                 import GTW
import _GTW._Form._Form_
import _GTW._Form._MOM.Field_Group_Description

MOM.Attr.A_Attr_Type.widget = "html/field.jnj, string"

class M_Instance (TFL.Meta.Object.__class__) :
    """Meta class for MOM object forms"""

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        if cls.et_man :
            et_man                = cls.et_man
            cls.fields_for_et_man = TFL.defaultdict (list)
            cls.Roles             = []
            for fg in cls.field_groups :
                if isinstance (fg, GTW.Form.Field_Group) :
                    for f in fg.fields :
                        cls.fields_for_et_man [f.et_man].append (f)
            if issubclass (et_man._etype, MOM.Link) :
                ### handle the link role's before the link itself
                scope             = et_man.home_scope
                cls.Roles         = \
                    [   (r.name, getattr (scope, r.role_type.type_name))
                    for r in et_man.Roles
                    ]
    # end def __init__

    def New (cls, et_man, * field_group_descriptions, ** kw) :
        field_groups  = []
        suffix        = et_man.type_base_name
        if "suffix" in kw :
            suffix    = "__".join ((kw.pop ("suffix"), suffix))
        added_fields  = set ()
        if not field_group_descriptions :
            field_group_descriptions = \
                (GTW.Form.MOM.Field_Group_Description (), )
        for fgd in field_group_descriptions :
            field_groups.extend (fgd (et_man, added_fields))
        return cls.__m_super.New \
            ( suffix
            , field_groups = field_groups
            , et_man       = et_man
            , ** kw
            )
    # end def New

# end class M_Instance

class _Instance_ (GTW.Form._Form_) :
    """Base class for the real form and the `nested` from."""

    __metaclass__ = M_Instance
    et_man        = None

    def __init__ (self, instance = None, prefix = None, parent = None) :
        self.__super.__init__ (instance)
        self.instance_for_et_man = {self.et_man : instance}
        scope                    = self.et_man.home_scope
        for role_name, et_man in self.Roles :
            self.instance_for_et_man [et_man] = getattr \
                (instance, role_name, None)
        self.prefix              = prefix
        ### make copies of the inline groups to allow caching of inline forms
        self.inline_groups       = []
        for i, fg in enumerate (self.field_groups) :
            if isinstance (fg, GTW.Form.MOM.Inline) :
                self.field_groups [i] = new_fg = fg.clone (self)
                self.inline_groups.append (new_fg)
        self.parent              = parent
    # end def __init__

    def _get_raw (self, field) :
        return field.get_raw (self.instance_for_et_man [field.et_man])
    # end def _get_raw

    def __call__ (self, request_data) :
        ### XXX does not feel to be the correct place to make this conversion
        if not isinstance (request_data, GTW.Tornado.Request_Data) :
            request_data  = GTW.Tornado.Request_Data (request_data)
        self.request_data = request_data
        errors            = []
        roles             = []
        for role_name, et_man in self.Roles :
            if self.parent and et_man is self.parent.et_man :
                instance  = self.parent.instance
            else :
                instance  = self._create_or_update (et_man, None, errors)
            roles.append (instance and instance.epk_raw)
        self.instance     = self._create_or_update (self.et_man, roles, errors)
        error_count       = 0 ### XXX
        for ig in self.inline_groups :
            error_count  += ig (request_data)
        return error_count
    # end def __call__

    def _create_or_update (self, et_man, roles, errors) :
        roles         = roles or ()
        has_substance = len (roles)
        raw_attrs     = {}
        instance      = self.instance_for_et_man [et_man]
        for f in self.fields_for_et_man [et_man] :
            value              = self.get_raw (f)
            raw_attrs [f.name] = value
            has_substance     += bool \
                (self.get_id (f) in self.request_data and value)
        if has_substance :
            ### at least on attribute is filled out
            try :
                raw_attrs ["on_error"] = errors.append
                if instance :
                    roles = dict \
                        ((ak.name, t) for (ak, r) in zip (et_man.Roles, roles))
                    instance.set     (on_error = errors.append, ** roles)
                    instance.set_raw (** raw_attrs)
                else :
                    instance = et_man (raw = True, * roles, ** raw_attrs)
            except Exception, exc:
                errors.append (exc)
        return instance
    # end def _create_or_update

# end class _Instance_

if __name__ != "__main__" :
    GTW.Form.MOM._Export ("*")
### __END__ GTW.Form.MOM._Instance_
