# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005-2009 Martin Gl�ck. All rights reserved
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
#    28-May-2009 (CT) Legacy removed
#    ��revision-date�����
#--

from   _DJO                        import DJO
from   _TFL                        import TFL

import _TFL.Decorator
import _TFL._Meta.M_Class

from   django.forms.models         import BaseModelForm, ModelForm

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
