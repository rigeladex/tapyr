# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.cluster
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
#    Apply_All
#
# Purpose
#    Class transparently applying method calls to a set of objects
#
# Revision Dates
#    20-Feb-2005 (CT) Creation
#    23-Jul-2007 (CED) Activated absolute_import
#    ««revision-date»»···
#--
from __future__ import absolute_import


from   _TFL              import TFL
import _TFL._Meta.Object

class Apply_All (TFL.Meta.Object) :
    """Class transparently applying method calls to a set of objects.

       >>> l1  = range (5)
       >>> l2  = ["f", "b", "c", "a"]
       >>> all = Apply_All (l1, l2)
       >>> all._reveivers
       ([0, 1, 2, 3, 4], ['f', 'b', 'c', 'a'])
       >>> all.sort ()
       >>> all._reveivers
       ([0, 1, 2, 3, 4], ['a', 'b', 'c', 'f'])
       >>> all.count ("a")
       [0, 1]
       >>> all.reverse ()
       >>> all._reveivers
       ([4, 3, 2, 1, 0], ['f', 'c', 'b', 'a'])
       >>> all.pop ()
       [0, 'a']
       >>> all._reveivers
       ([4, 3, 2, 1], ['f', 'c', 'b'])
    """

    def __init__ (self, * receivers) :
        self._reveivers = receivers
    # end def __init__

    def _apply (self, name, * args, ** kw) :
        result = []
        for r in self._reveivers :
            f = getattr (r, name)
            r = f (* args, ** kw)
            if r is not None :
                result.append (r)
        return result or None
    # end def _apply

    def __getattr__ (self, name) :
        return lambda * args, ** kw : self._apply (name, * args, ** kw)
    # end def __getattr__

# end class Apply_All

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ Apply_All
