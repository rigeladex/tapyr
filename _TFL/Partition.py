# -*- coding: iso-8859-1 -*-
# Copyright (C) 2007  Andreas Baumgartner <baumgartner@tttech.com>
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
#    Partition
#
# Purpose
#    calculates a partitioning into 2 containers for a list of blocks,
#    so that the overhead is minimized
#
# Revision Dates
#    25-May-2007 (ABA) Creation
#    25-May-2007 (ABA) adapt to Coding Guidelines
#    ««revision-date»»···
#--

from _TFL import TFL

def partition (blocks) :
    if not blocks :
        return (0, 0)
    blocks.sort ()
    last = blocks [-1]
    segment2_mb_size = last
    area_old = 1 * (last - blocks [0])
    segment1_mb_size = blocks [0]
    i = 1
    while i < len (blocks) :
        area = (i + 1) * (last - blocks [i])
        if area > area_old :
            segment1_mb_size = blocks [i]
            area_old = area
        i += 1
    return (segment1_mb_size, segment2_mb_size)
# end def _partition

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.Black_Hole
