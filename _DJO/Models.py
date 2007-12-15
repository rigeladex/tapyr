# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006-2007 Martin Glück. All rights reserved
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
#    DJO.Models
#
# Purpose
#    Some usefull classes
#
# Revision Dates
#    18-Sep-2007 (MGL) Creation
#    18-Nov-2007 (MG) ` IntegerLimitField` : `get_internal_type` added
#    15-Dec-2007 (MG) Missing import added
#    ««revision-date»»···
#--

from   django.db                          import models as DM
from   django.contrib.auth.models         import User
import django.db.models.base as DBM
import datetime
from   django.utils.translation           import gettext_lazy as _

class M_User_Create_Mod (DBM.ModelBase) :
    """Meta class which add's the created_by/at and modified_by/at fields."""

    def __new__ (cls, name, bases, attrs) :
        if not name.startswith ("_") :
            user_prefix = attrs.pop ("user_prefix", "")
            if user_prefix :
                user_prefix = "%s_" % (user_prefix, )
            for base_name, verbose, rel, default in \
                    ( ( "created",  "Created",       "creator"
                      , datetime.datetime.now
                      )
                    , ( "modified", "Last modified", "modifier"
                      , None
                      )
                    ) :
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
        return super (M_User_Create_Mod, cls).__new__ (cls, name, bases, attrs)
    # end def __new__

# end class M_User_Create_Mod

class _User_Create_Mod_ (object) :
    """Automatically add cerated and modified fields to the model."""

    __metaclass__ = M_User_Create_Mod

    def save (self, user = None) :
        if user :
            if self.pk is None :
                self.created_by = user
            self.modified_by    = user
            self.modified_at    = datetime.datetime.now ()
        return super (_User_Create_Mod_, self).save ()
    # end def save

# end class _User_Create_Mod_

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
    from _DJO import DJO
    DJO._Export ("*")
### __END__ DJO.Models
