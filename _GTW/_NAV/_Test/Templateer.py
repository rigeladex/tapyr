# -*- coding: utf-8 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.NAV.Test.
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
#    GTW.NAV.Test.Templateer
#
# Purpose
#    A faked templateer for testing
#
# Revision Dates
#    19-Feb-2010 (MG) Creation
#    ««revision-date»»···
#--

from   _TFL                  import TFL
import _TFL._Meta.Object

from   _GTW                  import GTW
import _GTW._NAV._Test

Context = dict

def render (template, context) :
    return template, context
# end def render

if __name__ != "__main__" :
    GTW.NAV.Test._Export ("*")
### __END__ GTW.NAV.Test.Templateer


