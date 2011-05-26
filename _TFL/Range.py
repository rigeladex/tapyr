# -*- coding: iso-8859-15 -*-
# Copyright (C) 2001-2009 Mag. Christian Tanzer. All rights reserved
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
#    TFL.Range
#
# Purpose
#    Implement range generator
#
#    Idea blatantly stolen from a posting by "Andrew Dalke" <dalke@acm.org>
#    in comp.lang.python on Wed, 9 May 2001 12:20:56 -0600,
#    Message-id: <9dc1se$tdn$1@nntp9.atl.mindspring.net>
#    References: <mailman.989424256.5933.python-list@python.org>
#
# Revision Dates
#    10-May-2001 (CT) Creation
#    21-Feb-2002 (CT) `Range_` renamed to `_Range_`
#    28-Sep-2004 (CT) Use `isinstance` instead of type comparison
#    11-Nov-2009 (CT) Use `slice` instead of `types.SliceType`
#    ««revision-date»»···
#--

from _TFL import TFL

class _Range_ :
    """Range generator: takes integers and slices as arguments to
       `[]' and returns a list of indices as specified by the arguments.

       For instance,

       >>> Range [1]
       [0]
       >>> Range [5]
       [0, 1, 2, 3, 4]
       >>> Range [4:8]
       [4, 5, 6, 7]
       >>> Range [4:8:2]
       [4, 6]
       >>> Range [1:3, 7:9]
       [1, 2, 7, 8]
       >>> Range [0:10:2, 10:100:10]
       [0, 2, 4, 6, 8, 10, 20, 30, 40, 50, 60, 70, 80, 90]
    """

    def __getitem__ (self, indices) :
        if not isinstance (indices, (list, tuple)) :
            indices = (indices, )
        result = []
        for i in indices :
            if isinstance (i, slice) :
                result.extend (range (i.start, i.stop, i.step or 1))
            else :
                result.extend (range (i))
        return result
    # end def __getitem__

# end class _Range_

Range = _Range_ ()

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.Range
