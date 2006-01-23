# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006 TTTech Computertechnik AG. All rights reserved
# Schönbrunnerstraße 7, A--1040 Wien, Austria. office@tttech.com
#
#++
# Name
#    TFL.CDG.Bin_Block
#
# Purpose
#    Defines class for generation of Bin Blocks
#
# Revision Dates
#    23-Jan-2006 (CED) Creation
#    ««revision-date»»···
#--
#

from     _TFL                  import TFL
import   _TFL._CDG
import   _TFL._Meta.Object

class Bin_Block (TFL.Meta.Object) :

    def __init__ (self, byte_order, root) :
        self.__super.__init__ ()
        self.byte_order  = byte_order
        self.root        = root
        self._binheader  = root.packed (byte_order)
        self._offset     = len (self._binheader)
        self._binbuffer  = []
        self._offset_map = {}
    # def __init__

    def add (self, structs) :
        if not isinstance (structs, (tuple, list)) :
            structs = (structs, )
        for s in structs :
            bin   = s.packed (self.byte_order)
            align = s.alignment
            miss  = align - (self._offset % align)
            if 0 < miss < align :
                fill = struct.pack ("%dx" % miss)
            else :
                fill = ""
            self._binbuffer.append (fill)
            self._binbuffer.append (bin)
            self._offset += len (fill)
            off_name = s.__class__.offset_field_name
            if off_name not in self._offset_map :
                self._offset_map [off_name] = self._offset
                setattr (self.root, off_name, self._offset)
            self._offset += len (bin)
    # def add

    def __str__ (self) :
        ### We have to re-pack the root struct, cause the offset field values
        ### have changed during adding
        buffer = "".join (self._binbuffer)
        self.root.total_size = len (self._binheader) + len (buffer)
        self._binheader      = self.root.packed (self.byte_order)
        return "%s%s" % (self._binheader, buffer)
    # def __str__

# class Bin_Block

if __name__ != "__main__" :
    TFL.CDG._Export ("*")

### __END__ TFL.CDG.File
