# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 Mag. Christian Tanzer. All rights reserved
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
#    TFL.SDG.C._Scope_
#
# Purpose
#    Model scope-like elements in the code in a C file
#
# Revision Dates
#    27-Jul-2004 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL              import TFL
import _TFL._SDG._C.Node

class _Scope_ (TFL.SDG.C.Node) :
    """Root class for all scope-like C document nodes"""

    Ancestor             = TFL.SDG.C.Node
    init_arg_defaults    = dict \
        ( explanation    = ""
        )

    _autoconvert         = dict \
        ( explanation    =
              lambda s, k, v : s._convert_c_comment (k, v, eol = False)
        )

    children_group_names = \
        ( Ancestor.Head, Ancestor.Body, Ancestor.Tail, Ancestor.Decl)

    explanation_level    = Ancestor.description_level + 2

    def insert (self, child, index = None, delta = 0, cgi = None) :
        """Insert `child' to `self.children' at position `index'
           (`index is None' means append)
           (None means append).
        """
        for c in self._convert_c_stmt (child) :
            if cgi is not None :
                c.cgi = cgi
            self.__super.insert (c, index, delta)
    # end def insert

    def insert_head (self, child, index = None, delta = 0) :
        ### just for backward compatibility
        ### don't use for new code
        self.insert (child, index, delta, cgi = self.Head)
    # end def insert_head

    def insert_tail (self, child, index = None, delta = 0) :
        ### just for backward compatibility
        ### don't use for new code
        self.insert (child, index, delta, cgi = self.Tail)
    # end def insert_tail

# end class _Scope_

if __name__ != "__main__" :
    TFL.SDG.C._Export ("_Scope_")
### __END__ TFL.SDG.C._Scope_
