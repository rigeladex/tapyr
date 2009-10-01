# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
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
#    MOM.Sequence_Number
#
# Purpose
#    Model sequence numbers of ordered links of associations of
#    MOM meta object model
#
# Revision Dates
#     1-Oct-2009 (CT) Creation (factored from `TOM.Sequence_Number`)
#    ««revision-date»»···
#--

from   _MOM                  import MOM
from   _TFL                  import TFL

import _MOM.Entity

_Ancestor_Essence = MOM.Entity

class Sequence_Number (_Ancestor_Essence) :
    """Model sequence number of link in ordered association."""

    is_partial    = False

    class _Attributes (_Ancestor_Essence._Attributes) :

        class seq_nr (A_Int) :
            """Sequence number of a link in an ordered association."""

            kind = Attr.Primary

        # end class seq_nr

    # end class _Attributes

    def __add__ (self, rhs) :
        return self.seq_nr + getattr (rhs, "seq_nr", rhs)
    # end def

    def __sub__ (self, rhs) :
        return self.seq_nr - getattr (rhs, "seq_nr", rhs)
    # end def __sub__

    __radd__ = __add__
    __rsub__ = __sub__

# end class Sequence_Number

if __name__ != "__main__" :
    MOM._Export ("Sequence_Number")
### __END__ MOM.Sequence_Number
