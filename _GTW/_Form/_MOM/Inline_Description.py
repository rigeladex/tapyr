# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.Form.MOM.
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
#    GTW.Form.MOM.Inline_Description
#
# Purpose
#    Description of the behaviour of an inline editing
#
# Revision Dates
#    19-Jan-2010 (MG) Creation
#    ««revision-date»»···
#--

from   _TFL                                 import TFL
import _TFL._Meta.Object

from   _GTW                                 import GTW
import _GTW._Form._MOM.Inline
import _GTW._Form._MOM.Inline_Instance

class Inline_Description (TFL.Meta.Object) :
    """A Inline_Description `form` inside a real form."""

    widget    = "html/form.jnj, inline"
    css_class = "inline-object"

    completer    = None
    max_count    = 256 ### seems to be more than enough for a web-app
                       ### and sys.maxint on a 64 bit is machine way to much
    min_count    = 1
    min_empty    = 0
    min_required = 0

    def __init__ ( self, et_man, own_role_name
                 , * field_group_descriptions
                 , ** kw
                 ) :
        self.__dict__.update (kw)
        self.e_type_name              = getattr (et_man, "type_name", et_man)
        self.own_role_name            = own_role_name
        self.field_group_descriptions = field_group_descriptions
    # end def __init__

    def __call__ (self, et_man, added_fields, ** kw) :
        scope             = et_man.home_scope
        inline_form       = GTW.Form.MOM.Inline_Instance.New \
            ( getattr (scope, self.e_type_name)
            , * self.field_group_descriptions
            , suffix      = et_man.type_base_name
            )
        return (GTW.Form.MOM.Inline (self, inline_form), )
    # end def __call__

# end class Inline_Description

if __name__ != "__main__" :
    GTW.Form.MOM._Export ("*")
### __END__ GTW.Form.MOM.Inline_Description
