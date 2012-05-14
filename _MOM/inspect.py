# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package MOM.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    MOM.inspect
#
# Purpose
#    Provide functions for introspection of MOM meta object model
#
# Revision Dates
#    14-May-2012 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM import MOM
from   _TFL import TFL

def show_children (T, bi = "  ", level = 0, seen = None) :
    """Display tree of children of essential type `T`."""
    if seen is None :
        seen = set ()
    print ("%s%s" % (bi * level, T.type_name))
    l1 = level + 1
    for c in sorted (T.children.itervalues (), key = TFL.Getter.i_rank) :
        if c not in seen :
            show_children (c, bi, l1, seen)
            seen.add (c)
# end def show_children

if __name__ != "__main__" :
    MOM._Export_Module ()
### __END__ MOM.inspect
