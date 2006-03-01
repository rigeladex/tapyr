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
#     6-Feb-2006 (CED) Creation continued .
#    15-Feb-2006 (MZO) added import of `struct`
#    22-Feb-2006 (MZO) refactored from `SIT.Conf.Bin_Block_Creator`
#    23-Feb-2006 (CED) Use `rounded_up` instead of home-grown code
#     1-Mar-2006 (CED) Added function declarations to h-file
#    ««revision-date»»···
#--
#

from     _TFL                  import TFL
import   _TFL._CDG
import   _TFL._SDG._C
import   _TFL._Meta.Object
from     _TFL.predicate        import *
import  struct

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
            bin     = s.packed (self.byte_order)
            align   = s.alignment
            gap     = rounded_up (self._offset, align) - self._offset
            if gap :
                fill = struct.pack ("%dx" % gap)
            else :
                fill = ""
            self._binbuffer.append (fill)
            self._binbuffer.append (bin)
            self._offset += gap
            off_name = s.__class__.offset_field_name
            if off_name not in self._offset_map :
                self._offset_map [off_name] = self._offset
                setattr (self.root, off_name, self._offset)
            self._offset += len (bin)
    # def add

    def add_blob (self, blob, offset_name) :
        buffer = "".join (self._binbuffer)
        offset = len (self._binheader) + len (buffer)
        setattr (self.root, offset_name, offset)
        self._binbuffer.append (blob)
    # end def add_blob

    def __str__ (self) :
        ### We have to re-pack the root struct, cause the offset field values
        ### have changed during adding
        buffer = "".join (self._binbuffer)
        self.root.total_size = len (self._binheader) + len (buffer)
        self._binheader      = self.root.packed (self.byte_order)
        return "%s%s" % (self._binheader, buffer)
    # def __str__

# class Bin_Block

class Bin_Block_Creator (TFL.Meta.Object) :

    def __init__ (self, name, scope, gauge) :
        self.name   = name
        self.scope  = scope
        self.gauge  = gauge
    # def __init__

    def __call__ \
        (self, byte_order, meta_struct, config_struct, * args, ** kw) :
        return self.create_bin_block \
            ( meta_struct
            , config_struct (self.scope, * args,  ** kw)
            , byte_order
            )
    # end def __call__

    def additional_blobs (self, bin_block) :
        pass
    # end def additional_blobs

    def additional_defines (self, C, h_file) :
        pass
    # end def additional_defines

    def create_api \
        ( self, filename, meta_struct, config_struct, table_struct
        , main_name, C, c_file = None, h_file = None
        ) :
        self.additional_defines (C, h_file)
        self.create_c_code \
            ( meta_struct, config_struct, table_struct, C
            , c_file, h_file, main_name
            )
        return (c_file, h_file)
    # end def create_api

    def create_bin_block (self, meta_struct, root, byte_order) :
        bblock = TFL.CDG.Bin_Block    (byte_order.name, root)
        for c in meta_struct.uses_global_buffers :
            if root.__class__ is c :
                assert len (c.extension) == 1
                continue
            bblock.add (c.extension)
        self.additional_blobs (bblock)
        return bblock
    # def create_bin_block

    def create_c_code \
        ( self, meta_struct, root, ptr_table, C, c_file, h_file
        , main = "root"
        ) :
        h_file.add (C.App_Include ("ptypes.h"))
        for c in meta_struct.needs_struct :
            h_file.add \
                (c.as_forward_typedef (const = c.const, scope = h_file.scope))
        meta_struct.define_access_macros (C, h_file, main)
        for sf in meta_struct.needs_typedef :
            h_file.add (sf.as_typedef (scope = h_file.scope))
        for c in meta_struct.needs_struct :
            h_file.add (c.as_c_code (scope = h_file.scope, standalone = 1))
        c_file.add (C.App_Include (h_file.inc_name))
        self._aquire_bin_buffer  \
            (meta_struct, root, ptr_table, h_file, c_file, C)
        self._release_bin_buffer \
            (meta_struct, root, ptr_table, h_file, c_file, C)
    # def create_c_code

    def _aquire_bin_buffer \
        (self, meta_struct, root_table, ptr_table, h_file, c_file, C) :
        table  = ptr_table.type_name
        root   = root_table.type_name
        h_file.add \
            ( C.Fct_Decl
                ( "%s *" % table
                , "aquire_bin_buffer"
                , "const ubyte1 * bin_buffer"
                , scope = h_file.scope
                )
            )
        func   = C.Function \
            ( "%s *" % table
            , "aquire_bin_buffer"
            , "const ubyte1 * bin_buffer"
            , scope = c_file.scope
            )
        func.add \
            ( C.Var
                ( "%s *" % root
                , "desc"
                , "(%s *) bin_buffer" % root
                )
            )
        func.add \
            ( C.Var
                ( "struct _%s *" % table
                , "result"
                , "(struct _%s *) malloc (sizeof (%s))" % (table, table)
                )
            )
        blk  = C.Stmt_Group ()
        blk2 = C.Stmt_Group ()
        func.add (C.If ("result", blk))
        func.add (C.Statement ("return result"))
        blk.add \
            ( C.Statement
               ("result->bin_buffer = (ubyte1 *) malloc (desc->total_size)")
            )
        blk.add  (C.If ("! result->bin_buffer", blk2))
        blk.add \
            ( C.Statement
               ("memcpy (result->bin_buffer, bin_buffer, desc->total_size)")
            )
        blk.add \
            ( C.Statement
               ( "result->descriptor = (%s *) result->bin_buffer"
               % root_table.type_name
               )
            )
        blk2.add (C.Statement ("free (result)"))
        blk2.add (C.Statement ("return 0"))
        for c in meta_struct.uses_global_buffers :
            blk.add \
                ( C.Statement
                    ( "result->%s = (%s *) "
                      "(& (result->bin_buffer [desc->%s]))"
                    % (c.buffer_field_name, c.type_name, c.offset_field_name)
                    )
                )
        c_file.add (func)
        h_file.add (func)
    # end def _aquire_bin_buffer

    def _release_bin_buffer \
        (self, meta_struct, root_table, ptr_table, h_file, c_file, C) :
        h_file.add \
            ( C.Fct_Decl
                ( "void"
                , "release_bin_buffer"
                , "struct _%s * table" % ptr_table.type_name
                , scope = h_file.scope
                )
            )
        func  = C.Function \
            ( "void"
            , "release_bin_buffer"
            , "struct _%s * table" % ptr_table.type_name
            , scope = c_file.scope
            )
        func.add (C.Statement ("free (table->bin_buffer)"))
        func.add (C.Statement ("free (table)"))
        c_file.add (func)
    # end def _release_bin_buffer

# end class Bin_Block_Creator


if __name__ != "__main__" :
    TFL.CDG._Export ("*")

### __END__ TFL.CDG.File
