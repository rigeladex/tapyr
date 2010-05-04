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
#    GTW.Form.MOM.Instance
#
# Purpose
#    A form which creates or changes a MOM object
#
# Revision Dates
#    18-Jan-2010 (MG) Creation
#    29-Jan-2010 (MG) Use `Widget_Spec` instead of plain text
#    22-Feb-2010 (CT) `Instance.__init__` changed to pass `** kw` to `super`
#    ««revision-date»»···
#--

from   _MOM               import MOM

from   _TFL                                 import TFL
import _TFL._Meta.Object
import _TFL.defaultdict
import _GTW._Form.Field_Error

from   _GTW                                 import GTW
import _GTW._Form._MOM
import _GTW._Form._MOM._Instance_

class Instance (GTW.Form.MOM._Instance_) :
    """A form which creates or changes a MOM object.

       Instance of this class are always the top level form and can never be
       used as inlines.
    """

    css_class     = "Object-Editor"
    widget        = "html/form.jnj, object"

    def __init__ (self, action, instance = None, ** kw) :
        self.action = action
        self.__super.__init__ (instance, ** kw)
    # end def __init__

# end class Instance

if __name__ != "__main__" :
    GTW.Form.MOM._Export ("*")
### __END__ GTW.Form.MOM.Instance
