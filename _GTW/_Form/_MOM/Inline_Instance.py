# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg. martin@mangari.org
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
#    Inline_Instance
#
# Purpose
#    «text»···
#
# Revision Dates
#    19-Jan-2010 (MG) Creation
#    ««revision-date»»···
#--

from   _GTW                                 import GTW
import _GTW._Form._MOM
import _GTW._Form._MOM._Instance_

class Inline_Instance (GTW.Form.MOM._Instance_) :
    """A form which is embedded in a `Instance` form."""

    widget        = "html/form.jnj, field_groups"

# end class Inline_Instance

if __name__ != "__main__" :
    GTW.Form.MOM._Export ("*")

### __END__ GTW.Form.MOM.Inline_Instance
