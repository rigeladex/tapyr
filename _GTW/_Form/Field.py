# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009-2010 Martin Glueck All rights reserved
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
#    GTW.Form.Field
#
# Purpose
#    A field of a form
#
# Revision Dates
#    30-Dec-2009 (MG) Creation
#    02-Feb-2010 (MG) `get_raw` paremeter form added
#    20-Feb-2010 (MG) Parameter `ui_name` added
#    15-Apr-2010 (MG) `default` method added to allow callable default values
#    ««revision-date»»···
#--
from   _TFL               import TFL
import _TFL._Meta.Object
from   _GTW               import GTW
import _GTW._Form
from   _TFL.I18N          import _T

class _Field_ (TFL.Meta.Object) :
    """Base class for form fields."""

    electric  = False

    def __init__ (self, name, default = u"") :
        self.name      = name
        self._default  = default
    # end def __init__

    def default (self, form, defaults) :
        if callable (self._default) :
            return self._default (form)
        return self._default
    # end def default

    @TFL.Meta.Once_Property
    def Media (self) :
        return self.widget.Media
    # end def Media

# end class _Field_

class Field (_Field_) :
    """A free field which should be part of a HTML form."""

    widget  = GTW.Form.Widget_Spec ("html/field.jnj, string")
    hidden  = False
    choices = ()

    def __init__ (self, name, default = u"", ui_name = None, ** kw) :
        self.__super.__init__ (name, default)
        self.html_name = name
        self.ui_name   = _T (ui_name or name.capitalize ())
        self.__dict__.update (kw)
    # end def __init__

    def get_raw (self, form, defaults) :
        return getattr (form.instance, self.name, self.default (form, defaults))
    # end def get_raw

# end class Field

if __name__ != "__main__" :
    GTW.Form._Export ("_Field_", "Field")
### __END__ GTW.Form.Field
