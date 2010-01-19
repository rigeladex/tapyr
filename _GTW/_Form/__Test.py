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
#    GTW.Form.__Test
#
# Purpose
#    Simple test for plain forms
#
# Revision Dates
#    19-Jan-2010 (MG) Creation
#    ««revision-date»»···
#--

from   _GTW._Form                         import Form
import _GTW._Form.Auth

form = Form.Auth.Login (None, "/login.html")
#import pdb; pdb.set_trace ()
print form (dict (username = "user1", password = "passwd1"))
### __END__ GTW.Form.__Test


