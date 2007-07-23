# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004-2006 Mag. Christian Tanzer. All rights reserved
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
#    TFL.CDG.Array
#
# Purpose
#    Performance optimization of c_code generation of Array containing structs
#    (without nested structs/arrays)
#
# Revision Dates
#    18-Nov-2006 (MZO) Creation
#    23-Jul-2007 (CED) Activated absolute_import
#    ««revision-date»»···
#--
from __future__ import absolute_import


from   _TFL              import TFL
import _TFL._CDG
import _TFL._SDG._C.Array

from   predicate         import un_nested

class _CDG_Array_ (TFL.SDG.C.Array) :
    """C array declaration"""


    Ancestor             = TFL.SDG.C.Array
    _real_name           = "Array"


    c_format             = "".join \
        ( ( TFL.SDG.C.Array._common_format
          , """%(:front= =%(NL)s%(base_indent)s:.initializers:)s"""
          , ";%(NL)s"
          , """%(:head= :*description:)s"""
          )
        )

    def _setup_initializers \
        (self, init_list, description = None) :
        result   = TFL.SDG.C.Init_Comp (description = description)
        t        = self._struct or self.type
        assert isinstance (t, (TFL.SDG.C.Struct)), (t, type (t))
        Init = t._setup_initializers_for_cdg_array
        result_l = []
        for k, v in enumerate (init_list) :
            result_l.append (Init (v, description = "[%s]" % k))
        result = "{ %s\n  }" % ("\n  , ".join (result_l), )
        return result
    # end def _setup_initializers

# end class _CDG_Array_

Array = _CDG_Array_

if __name__ != "__main__" :
    TFL.CDG._Export ("*")
### __END__ TFL.SDG.C.Array
