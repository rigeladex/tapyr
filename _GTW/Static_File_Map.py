# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.
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
#    GTW.Static_File_Map
#
# Purpose
#    Map a directory to a prefix
#
# Revision Dates
#    22-Feb-2010 (MG) Creation
#    23-Feb-2010 (CT) s/exists/get/; Instance `static_file_map` added
#    ««revision-date»»···
#--

from   _GTW                     import GTW

from   _TFL                     import TFL
import _TFL._Meta.Object

import  os

class Static_File_Map (TFL.Meta.Object) :
    """A mapping of a prefix to a directory on the disk."""

    def __init__ (self, prefix, directory) :
        if prefix and not prefix.endswith ("/") :
            prefix    += "/"
        self.prefix    = prefix
        self.directory = directory
    # end def __init__

    def get (self, path) :
        if not path.startswith (self.prefix) :
            return None
        abspath = os.path.abspath \
            (os.path.join (self.directory, path.replace (self.prefix, "")))
        if os.path.isfile (abspath) :
            return abspath
    # end def get

# end class Static_File_Map

static_file_map = Static_File_Map \
    ("GTW", os.path.join (os.path.dirname (__file__), "media"))

if __name__ != "__main__" :
    GTW._Export ("*")
### __END__ GTW.Static_File_Map
