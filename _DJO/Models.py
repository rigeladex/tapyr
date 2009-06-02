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
#    Provide a (shiny new) subclass of django.db.models.base.Model
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
#    28-May-2009 (CT) Legacies `_Permisson_Mixin_` and `_User_Create_Mod_`
#                     removed, too (doh!)
#    28-May-2009 (CT) `__init__` and `save `redefined to handle
#                     `_save_callbacks`
#    29-May-2009 (CT) `__init__` fixed (needs to call `__super.__init__`)
#    29-May-2009 (CT) `assimilate` added
#    30-May-2009 (CT) `M_Model.__new__`, `_handle_foreign_keys`, and
#                     `_setup_opt_proxy_field` added
#     1-Jun-2009 (CT) `_handle_foreign_keys` and `_setup_opt_proxy_field` fixed
#     1-Jun-2009 (CT) Support for `real_name` added
#     1-Jun-2009 (CT) `_handle_foreign_keys` changed to add `_<name>_owned`
#                     fields for One_to_One fields
#     1-Jun-2009 (MG) `_save_callbacks` changed to dict
#     2-Jun-2009 (MG) `_<name>_owned`: cannot have `null = True` (at least on
#                     sqlite)
#     2-Jun-2009 (MG) `delete` added
#    ««revision-date»»···
#--

from   _TFL                               import TFL
import _TFL._Meta.M_Class
import _TFL.Record

from   _DJO                               import DJO
import _DJO.Model_Field_Man
import _DJO.Model_Field                   as     MF

import datetime

from   django.db                          import models as DM
from   django.contrib.auth.models         import User
import django.db.models.base as DBM
from   django.utils.translation           import gettext_lazy as _

class M_Model (TFL.Meta.M_Class, DM.Model.__class__) :
    """Meta class for models with support for `.__super` and `_real_name`."""

    def __new__ (meta, name, bases, dct) :
        meta._handle_foreign_keys (name, bases, dct)
        return super (M_Model, meta).__new__ (meta, name, bases, dct)
    # end def __new__

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        cls._setup_attr        (cls)
    # end def __init__

    @classmethod
    def assimilate (meta, cls) :
        """Assimilate a django model class that doesn't use `M_Model` as meta
           class.
        """
        meta._setup_attr (cls)
        cls._F.finalize  ()
    # end def assimilate

    @classmethod
    def _handle_foreign_keys (meta, name, bases, dct) :
        for k, f in list (dct.iteritems ()) :
            if isinstance (f, MF.One_to_One) :
                ko = "_%s_owned" % k
                dct [ko] = MF.Boolean \
                    (ko, blank = True, editable = False)
            elif isinstance (f, MF.Foreign_Key) :
                if isinstance (f.rel.to, basestring) :
                    if f.opt_proxy_args :
                        raise TypeError \
                            ( "Cannot setup opt_proxy_args for symbolic "
                              "Foreign_Key %s for model %s"
                            % (k, name)
                            )
                else :
                    ledom = f.rel.to
                    for a in f.opt_proxy_args :
                        if a not in dct :
                            ### Can't rely on `dleif._F` yet, unfortunately
                            dleif = ledom._meta.get_field (a)
                            meta._setup_opt_proxy_field \
                                (a, k, ledom, dleif, dct)
    # end def _handle_foreign_keys

    @classmethod
    def _setup_attr (meta, cls) :
        ### this is defined as a class method of the meta class so that it
        ### can be called for `cls` that don't use M_Model as meta class
        cls._F = DJO.Model_Field_Man (cls)
    # end def _setup_attr

    @classmethod
    def _setup_opt_proxy_field (meta, a, k, ledom, dleif, dct) :
        ckw   = dict (dleif._creation_kw, blank = True, real_name = a)
        b     = "_%s" % a
        field = dct [b] = dleif.__class__ (** ckw)
        def _get (this) :
            result = getattr (this, b)
            if result == field.Null :
                l = getattr (this, k, None)
                if l is not None :
                    result = getattr (l, a)
            return result
        def _set (this, value) :
            setattr (this, b, value)
        def _del (this) :
            setattr (this, b, field.Null)
        dct [a] = property (_get, _set, _del, dleif.help_text)
    # end def _setup_opt_proxy_field

# end class M_Model

class _DJO_Model_ (DM.Model) :

    __metaclass__ = M_Model
    _real_name    = "Model"

    class Meta :
        abstract       = True
    # end class Meta

    def __init__ (self, * args, ** kw) :
        self._save_callbacks = {}
        self.__super.__init__ (* args, ** kw)
    # end def __init__

    def delete (self) :
        for f in self._F.Own_O2O :
            ### if this object was created automatically we should delete it
            ### automatically as well
            if getattr (self, "_%s_owned" % (f.name, )) :
                getattr (self, f.name).delete ()
        self.__super.delete ()
    # end def delete

    def save (self, * args, ** kw) :
        try :
            for sc in self._save_callbacks.itervalues () :
                sc ()
        finally :
            self._save_callbacks.clear ()
        self.__super.save (* args, ** kw)
    # end def save

    def _before_save (self, request, ** kw) :
        pass
    # end def _before_save

Model = _DJO_Model_ # end class

if __name__ != "__main__" :
    DJO._Export ("*")
### __END__ DJO.Models
