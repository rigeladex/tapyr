# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.Form.
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
#    GTW.Form.Widget_Spec
#
# Purpose
#    Specification of widget to be used to render a form, field-group, or field
#
# Revision Dates
#    13-Jan-2010 (CT) Creation
#     2-Feb-2010 (MG) `Media` added
#     5-Feb-2010 (MG) Allow a `Widget_Spec` instance as `default`
#    ««revision-date»»···
#--

from   _GTW                               import GTW
from   _TFL                               import TFL

import _TFL._Meta.Object
import _GTW._Form

class Widget_Spec (TFL.Meta.Object) :
    """Specification of a widget to be used to render a form, field-group, or
       field.
    """

    default = None
    Media   = None

    def __init__ (self, default, ** kw) :
        if isinstance (default, self.__class__) :
            self.__dict__.update (default.__dict__)
        else :
            assert default and isinstance (default, basestring)
            self.default = default
        self.Media   = kw.pop ("Media", self.Media)
        self.__dict__.update (kw)
    # end def __init__

    def __getattr__ (self, name) :
        return self.default
    # end def __getattr__

    def __str__ (self) :
        return self.default
    # end def __str__

# end class Widget_Spec

if __name__ != "__main__" :
    GTW.Form._Export ("*")
### __END__ GTW.Form.Widget_Spec
