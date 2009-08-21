# -*- coding: iso-8859-1 -*-
# Copyright (C) 2007-2009 Martin Glück. All rights reserved
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
#    DJO.Nested_Model_Form
#
# Purpose
#    Base class for model forms which are nested inside other model forms.
#
# Revision Dates
#    21-Aug-2009 (MG) Creation
#    ««revision-date»»···
#--

from   _DJO                         import DJO
from   _TFL                         import TFL

import _DJO.Field_Group_Description
import _DJO.Model_Form
from    django.forms.widgets        import HiddenInput
from    django.forms                import BooleanField

class M_Nested_Model_Form (DJO.Model_Form.__class__) :
    """Meta class which adds some special fields needed for handling the
       nesting
    """

    pk_name          = "id"
    state_field_name = "_state_"

    def __new__ (meta, name, bases, dict) :
        pk   = meta.pk_name
        field_group_descriptions = dict.get ("field_group_descriptions", ())
        if field_group_descriptions :
            assert len (field_group_descriptions) == 1
            fgd = field_group_descriptions [0]
            if not any (getattr (f, "name", f) == pk for f in fgd.fields) :
                fgd.fields += \
                   (DJO.Field_Description (pk, widget = HiddenInput), )
        result = super (M_Nested_Model_Form, meta).__new__ \
            (meta, name, bases, dict)
        if field_group_descriptions :
            ufg      = result.unbound_field_groups [0]
            hfs      = BooleanField (widget = HiddenInput, initial = 0)
            hfs.name = meta.state_field_name
            ufg.fields.append (hfs)
        return result
    # end def __new__

# end class M_Nested_Model_Form

class Nested_Model_Form (DJO.Model_Form) :
    """Base class for nested model forms"""

    __metaclass__ = M_Nested_Model_Form

    def save (self) :
        import pdb; pdb.set_trace ()
        print self.data.get ("%s-%s" % \
            (self.prefix, self.__class__.state_field_name))
        return self.__super.save ()
    # end def save

# end class Nested_Model_Form

if __name__ != "__main__" :
    DJO._Export ("*")
### __END__ DJO.Nested_Model_Form
