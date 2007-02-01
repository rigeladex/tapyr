# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005-2007 TTTech Computertechnik AG. All rights reserved
# Schönbrunnerstraße 7, A--1040 Wien, Austria. office@tttech.com
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
#    TFL.CDG.Type_Packer
#
# Purpose
#    Classes for handling the alignement and padding of C data types.
#
# Revision Dates
#    27-Jul-2006 (CED) Creation
#     9-Jan-2007 (MZO) [21197] `gap_byte_positions` added
#     1-Feb-2007 (CED) Additional packers added
#    ««revision-date»»···
#--

from   _TFL                           import TFL
import _TFL._Meta.Object
from   _TFL.predicate                 import *

import struct

class _Type_Packer_ (TFL.Meta.Object) :

    markers = ("@", "=", "<", ">", "!")

    def __init__ (self, pure_format, cpu_gran) :
        self.pure_format        = pure_format
        self.cpu_gran           = cpu_gran
        self.gap_byte_positions = {}
        self.packed_format      = self._pack      (pure_format)
        self.alignment          = self._alignment (self.packed_format)
    # end def __init__

    def _alignment (self, format) :
        return max \
            (self._align_atom (a) for a in self._atoms (format))
    # end def _alignment

    def _atoms (self, format) :
        current = []
        for c in format :
            if c in self.markers :
                continue
            current.append (c)
            if not c.isdigit () :
                yield "".join (current)
                current = []
    # def _atoms

    def _pack (self, format) :
        result    = []
        offset    = 0
        max_align = 1
        self.gap_byte_positions = {}
        for atom in self._atoms (format) :
            size  = struct.calcsize  (atom)
            align = self._align_atom (atom)
            if align > max_align :
                max_align = align
            gap   = rounded_up (offset, align) - offset
            if gap :
                self.gap_byte_positions [offset] = gap
                result.append ("%dx" % gap)
            result.append (atom)
            offset += (gap + size)
        gap   = rounded_up (offset, max_align) - offset
        if gap :
            self.gap_byte_positions [offset] = gap
            result.append ("%dx" % gap)
        return "".join (result)
    # def _pack

# end class _Type_Packer_

class _Padding_Type_Packer_ (_Type_Packer_) :
    """Packs types (especially structs) using padding bytes.
    """

    def _align_atom (self, atom) :
        type_format = atom [-1]
        size        = struct.calcsize (type_format)
        return size
    # end def _align_atom

# end class _Padding_Type_Packer_

class GCC_Like_Type_Packer (_Padding_Type_Packer_) :
    """Packs types like the GCC
      (and most other compilers) does by default.
    """

    def _align_atom (self, atom) :
        result = self.__super._align_atom (atom)
        return min (result, self.cpu_gran)
    # end def _align_atom

# end class GCC_Like_Type_Packer

class MSVC_Like_Type_Packer (_Padding_Type_Packer_) :
    """Packs types like the Microsoft Visual C compiler does by default"""
# end class MSVC_Like_Type_Packer

class Dense_Type_Packer (_Type_Packer_) :
    """Packs types without padding"""

    def _align_atom (self, atom) :
        return 1
    # end def _align_atom

# end class Dense_Type_Packer

### XXX More packers to follow ....

Active_Type_Packer = GCC_Like_Type_Packer

if __name__ != "__main__" :
    import _TFL._CDG
    TFL.CDG._Export ("*", "Active_Type_Packer")
### __END__ TFL.CDG.Type_Packer
