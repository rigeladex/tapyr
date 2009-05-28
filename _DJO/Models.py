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

if __name__ != "__main__" :
    DJO._Export ("*")
### __END__ DJO.Models
