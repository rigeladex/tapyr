# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006-2009 Martin Glück. All rights reserved
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
#    Some useful classes
#
# Revision Dates
#    18-Sep-2007 (MG) Creation
#    18-Nov-2007 (MG) `IntegerLimitField` : `get_internal_type` added
#    15-Dec-2007 (MG) Missing import added
#     4-Apr-2008 (MG) `additional_user_attrs` added
#     9-May-2008 (MG) `_Permisson_Mixin_` factored
#     1-Jul-2008 (CT) `M_Model` and `Model` added
#    26-Feb-2009 (CT) `Model._before_save` added
#    27-Feb-2009 (CT) `M_Model._setup_attr` added and used
#    19-May-2009 (CT) `IntegerLimitField` removed
#                     (use `DJO.M_Field.Integer` instead)
#    28-May-2009 (CT) Legacy `M_User_Create_Mod` removed
#    ««revision-date»»···
#--

from   _TFL                               import TFL
import _TFL._Meta.M_Class
import _TFL.Record

from   _DJO                               import DJO

from   django.db                          import models as DM
from   django.contrib.auth.models         import User
import django.db.models.base as DBM
import datetime
from   django.utils.translation           import gettext_lazy as _

class M_Model (TFL.Meta.M_Class, DM.Model.__class__) :
    """Meta class for models with support for `.__super` and `_real_name`."""

    def __init__ (cls, name, bases, dict) :
        cls.__m_super.__init__ (name, bases, dict)
        cls._setup_attr        (cls)
    # end def __init__

    @classmethod
    def _setup_attr (meta, cls) :
        ### this is defined as a class method of the meta class so that it
        ### can be called for `cls` that don't use M_Model as meta class
        cls._Field = map = TFL.Record ()
        for f in cls._meta.fields :
            map [f.name] = f
    # end def _setup_attr

# end class M_Model

class _DJO_Model_ (DM.Model) :

    __metaclass__ = M_Model
    _real_name    = "Model"

    class Meta :
        abstract       = True
    # end class Meta

    def _before_save (self, request, ** kw) :
        pass
    # end def _before_save

Model = _DJO_Model_ # end class

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

if __name__ != "__main__" :
    DJO._Export ("*")
### __END__ DJO.Models
