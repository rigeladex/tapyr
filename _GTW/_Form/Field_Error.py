# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
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
#    GTW.Form.Field_Error
#
# Purpose
#    Classes for error handling for forms
#
# Revision Dates
#    15-Jan-2010 (MG) Creation
#    ««revision-date»»···
#--

from   _TFL                    import TFL
import _TFL._Meta.Object

from   _GTW                    import GTW
import _GTW._Form

class Error_List (list, TFL.Meta.Object) :
    """A list of errors."""

    widget = "html/field_error.jnj, error_list"

    def add (self, error) :
        if isinstance (error, (list, tuple, self.__class__)) :
            self.extend (error)
        else :
            self.append (error)
        return error
    # end def add

# end class Error_List

if __name__ != "__main__" :
    GTW.Form._Export ("*")
### __END__ GTW.Form.Field_Error
