# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006-2008 Martin Glück. All rights reserved
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
#    DJO.Models
#
# Purpose
#    Some usefull classes
#
# Revision Dates
#    18-Sep-2007 (MG) Creation
#    18-Nov-2007 (MG) `IntegerLimitField` : `get_internal_type` added
#    15-Dec-2007 (MG) Missing import added
#     4-Apr-2008 (MG) `additional_user_attrs` added
#     9-May-2008 (MG) `_Permisson_Mixin_` factored
#     1-Jul-2008 (CT) `M_Model` and `Model` added
#    ««revision-date»»···
#--

from   _TFL                               import TFL
import _TFL._Meta.M_Class

from   _DJO                               import DJO

from   django.db                          import models as DM
from   django.contrib.auth.models         import User
import django.db.models.base as DBM
import datetime
from   django.utils.translation           import gettext_lazy as _

class M_Model (TFL.Meta.M_Class, DM.Model.__class__) :
    """Meta class for models with support for `.__super` and `_real_name`."""
# end class M_Model

class _DJO_Model_ (DM.Model) :

    __metaclass__ = M_Model
    _real_name    = "Model"

    class Meta :
        abstract       = True
    # end class Meta

Model = _DJO_Model_ # end class

class M_User_Create_Mod (DBM.ModelBase) :
    """Meta class which add's the created_by/at and modified_by/at fields."""

    def __new__ (cls, name, bases, attrs) :
        if not name.startswith ("_") :
            auto_user_attrs       = [], []
            user_prefix           = attrs.pop ("user_prefix", "")
            additional_user_attrs = attrs.pop ("additional_user_attrs", ())
            if user_prefix :
                user_prefix = "%s_" % (user_prefix, )
            for base_name, verbose, rel, default in \
                    ( ( "created",  "Created",       "creator"
                      , datetime.datetime.now
                      )
                    , ( "modified", "Last modified", "modifier"
                      , None
                      )
                    ) + additional_user_attrs :
                attrs ["%s_by" % (base_name, )] = DM.ForeignKey \
                    ( User
                    , verbose_name = _("%s by" % (verbose, ))
                    , related_name = "%s%s" % (user_prefix, rel)
                    , null         = default is None
                    )
                attrs ["%s_at" % (base_name, )] = DM.DateTimeField \
                    ( _("%s at" % (verbose, ))
                    , default      = default
                    , null         = default is None
                    )
                auto_user_attrs [0].append \
                    (("%s_by" % (base_name, ), default is None))
                if not default :
                    auto_user_attrs [1].append ("%s_at" % (base_name, ))
            attrs ["auto_user_attrs"] = auto_user_attrs
        return super (M_User_Create_Mod, cls).__new__ (cls, name, bases, attrs)
    # end def __new__

# end class M_User_Create_Mod

class _Permisson_Mixin_ (object) :
    """Add the `add_allowed`, `change_allowed`, and `delete_allowed` methods to
       models.
    """

    @classmethod
    def _user_has_permission (cls, request_or_user, * permissions) :
        user = request_or_user
        if not isinstance (user, User) :
            user = request_or_user.user
        for p in permissions :
            if not user.has_perm (".".join ((cls._meta.app_label, p))) :
                return False
        ### if no permissions where speficied we return False
        return bool (permissions)
    # end def _user_has_permission

    @classmethod
    def add_allowed (cls, request_or_user) :
        meta = cls._meta
        return cls._user_has_permission \
            (request_or_user, "add_%s" % (meta.object_name.lower (), ))
    # end def add_allowed

    def delete_allowed (self, request_or_user) :
        meta = self._meta
        return self._user_has_permission \
            (request_or_user, "delete_%s" % (meta.object_name.lower (), ))
    # end def delete_allowed

    def change_allowed (self, request_or_user) :
        meta = self._meta
        return self._user_has_permission \
            (request_or_user, "change_%s" % (meta.object_name.lower (), )
            )
    # end def change_allowed

# end class _Permisson_Mixin_

class _User_Create_Mod_ (_Permisson_Mixin_) :
    """Automatically add cerated and modified fields to the model."""

    __metaclass__ = M_User_Create_Mod

    def delete_allowed (self, request_or_user) :
        user = request_or_user
        if not isinstance (user, User) :
            user = request_or_user.user
        if self.created_by == user :
            return True
        return super (_User_Create_Mod_, self).delete_allowed (user)
    # end def delete_allowed

    def change_allowed (self, request_or_user) :
        user = request_or_user
        if not isinstance (user, User) :
            user = request_or_user.user
        if self.created_by == user :
            return True
        return super (_User_Create_Mod_, self).change_allowed (user)
    # end def change_allowed

    def save (self, user = None) :
        if user :
            if self.pk is None :
                self.created_by = user
            self.modified_by    = user
            self.modified_at    = datetime.datetime.now ()
        return super (_User_Create_Mod_, self).save ()
    # end def save

# end class _User_Create_Mod_

DM._Permisson_Mixin_ = _Permisson_Mixin_
DM._User_Create_Mod_ = _User_Create_Mod_

### some common fields
class IntegerLimitField (DM.IntegerField) :
    """Just add min/max values to the default integer field"""

    def __init__ (self, * args, ** kw) :
        self.min_value = kw.pop ("min_value", None)
        self.max_value = kw.pop ("max_value", None)
        super (IntegerLimitField, self).__init__ (* args, ** kw)
    # end def __init__

    def formfield (self, * args, ** kw) :
        if self.min_value is not None :
            kw ["min_value"] = self.min_value
        if self.max_value is not None :
            kw ["max_value"] = self.max_value
        return super (IntegerLimitField, self).formfield (* args, ** kw)
    # end def formfield

    def get_internal_type(self):
        return "IntegerField"
    # end def get_internal_type

# end class IntegerLimitField

DM.IntegerLimitField = IntegerLimitField

if __name__ != "__main__" :
    DJO._Export ("*")
### __END__ DJO.Models
