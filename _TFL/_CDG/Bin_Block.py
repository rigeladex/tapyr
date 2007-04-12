# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006-2007 TTTech Computertechnik AG. All rights reserved
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
#     3-Mar-2006 (MZO) added `C_Code_Creator`, debug_output for bin_blocks
#                      added `_read_bin_buffer`
#     8-Mar-2006 (MZO) unique name for function `read_bin_buffer`
#     9-Mar-2006 (MZO) changed parameter in `read_bin_buffer`
#    10-Mar-2006 (MZO) generate scope independ
#    13-Mar-2006 (MZO) optional tail for function `aquire, release bin_buffer`
#    14-Mar-2006 (MZO) added mode in `map_offset_to_struct`, fixed root_table
#    22-Mar-2006 (MZO) close debug file
#    30-Mar-2006 (MZO) unique name of the debug file
#    12-May-2006 (CED) optional `alignment` added to `add_blob`
#    12-Jun-2006 (CED) `additional_defines` takes c_file also
#    12-Jun-2006 (CED) `ptypes` included at begin of h-file
#    12-Jun-2006 (CED) Include of `ptypes` done in subclasses
#     5-Jul-2006 (MZO) fixed debug directory
#    12-Oct-2006 (MZO) get object from `Filler`
#    16-Oct-2006 (MZO) revert `typedef` change
#    23-Oct-2006 (MZO) note added
#    25-Oct-2006 (MZO) [22162] note removed
#     7-Nov-2006 (MZO) [21988] `reset_extension` called
#     9-Nov-2006 (MZO) [21988] write each block into file immediately
#    20-Nov-2006 (MZO) [21696] `TFL.CDG.Array` used
#    14-Mar-2007 (PGO) `__call__` of `*_Creator` take only CDG Structs now
#    12-Apr-2007 (MZO) `_debug_as_c_code` fortified
#    ««revision-date»»···
#--
#

from     _TFL                  import TFL
import   _TFL._CDG
import   _TFL._CDG.Array
import   _TFL._SDG._C
import   _TFL._Meta.Object
from     _TFL.predicate        import *
import  sos
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

    def add_blob (self, blob, offset_name, alignment = 1) :
        buffer   = "".join (self._binbuffer)
        current  = len (self._binheader) + len (buffer)
        offset   = TFL.rounded_up (current, alignment)
        gap      = offset - current
        if gap :
            fill = struct.pack ("%dx" % gap)
            self._binbuffer.append (fill)
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

# end class Bin_Block

class C_Code_Creator (TFL.Meta.Object) :

    def __init__ (self, gauge = None) :
        self.gauge      = gauge
        self.out_block  = None
    # def __init__

    def __call__ \
        ( self, C, meta_struct, root
        , reset_extension = True
        , filename        = None
        ) :
        return self._pack_as_c_code (C, meta_struct, reset_extension, filename)
    # end def __call__

    def _define_fmt (self, C, struct_cls) :
        ### Array does not work with init dict if not a struct definition
        ### before...
        hs = C.Struct (struct_cls.type_name)
        for f in struct_cls.struct_fields :
            hs.add ("long %s" % f.name)
    # end def _define_fmt

    def _pack_as_c_code \
        (self, C, Meta_Struct, reset_extension = True, filename = None) :
        c_block = C.Stmt_Group ()
        content = ""
        for c in Meta_Struct.uses_global_buffers :
            values = []
            for o in c.extension :
                values.append (o.dict ())
            values = self.hook_pack_values (values, c)
            self._define_fmt (C, c)
            if not filename :
                c_block.add \
                    ( C.Array
                        ( c.type_name
                        , c.buffer_name ()
                        , bounds = len (values)
                        , init   = values
                        )
                    )
            else :
                c_block = TFL.CDG.Array \
                    ( c.type_name
                    , c.buffer_name ()
                    , bounds    = len (values)
                    , init      = values
                    )
                if c_block :
                    content = \
                        "%s%s" % (content, "\n".join (c_block.as_c_code ()))
                    c_block.destroy ()
                c_block = None
            if reset_extension :
                c.reset_extension ()
        if filename and content :
            self._write_block_start (filename)
            try :
                self._write_str (content)
            finally :
                self._write_block_end ()
        return c_block
    # end def _pack_as_c_code

    def hook_pack_values (self, values, struct_cls) :
        return values
    # end def hook_pack_values

    def write_module (self, filename, c_block) :
        self._write_block_start (filename)
        try :
            self._write_block (c_block)
        finally :
            self._write_block_end ()
    # end def write_module

    def _write_block (self, c_block) :
        assert self.out_block
        try :
            self.out_block.write ("%s\n" % "\n".join (c_block.as_c_code ()))
            self.out_block.flush ()
        except (OSError, TFL.sos.error), exc :
            print exc
    # end def _write_block

    def _write_block_start (self, filename) :
        try :
            self.out_block = open (filename, "a")
        except (IOError, TFL.sos.error), exc :
            print "Cannot open file `%s`. %s" % (self.name, exc)
    # end def _write_block_start

    def _write_block_end (self) :
        if self.out_block :
            self.out_block.close ()
    # end def _write_block_end

    def _write_str (self, block) :
        assert self.out_block
        try :
            self.out_block.write ("%s\n" % block)
            self.out_block.flush ()
        except (OSError, TFL.sos.error), exc :
            print exc
    # end def _write_str

# end class C_Code_Creator

class Bin_Block_Creator (TFL.Meta.Object) :

    use_internal_data_formats = False

    def __init__ (self, scope = None, gauge = None) :
        self.scope  = scope ### XXX remove me
        self.gauge  = gauge
    # def __init__

    def __call__ \
        (self, byte_order, meta_struct, root) :
        bblock = self.create_bin_block \
            ( meta_struct
            , root
            , byte_order
            )
        if self.use_internal_data_formats :
            self._debug_as_c_code (meta_struct)
        return bblock
    # end def __call__

    def additional_blobs (self, bin_block) :
        pass
    # end def additional_blobs

    def additional_defines (self, C, h_file, c_file) :
        if c_file :
            c_file.add (C.App_Include (h_file.inc_name))
    # end def additional_defines

    def create_api \
        ( self, filename, meta_struct, config_struct, table_struct
        , main_name, C, c_file = None, h_file = None
        ) :
        self.additional_defines (C, h_file, c_file)
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
                assert len (c.extension) == 1, c.extension
                continue
            bblock.add (c.extension)
        self.additional_blobs (bblock)
        return bblock
    # def create_bin_block

    def create_c_code \
        ( self, meta_struct, root, ptr_table, C, c_file, h_file
        , main = "root", function_name_tail = ""
        ) :
        for c in meta_struct.needs_struct :
            h_file.add \
                (c.as_forward_typedef (const = c.const, scope = h_file.scope))
        meta_struct.define_access_macros (C, h_file, main)
        for sf in meta_struct.needs_typedef :
            h_file.add (sf.as_typedef (scope = h_file.scope))
        for c in meta_struct.needs_struct :
            h_file.add (c.as_c_code (scope = h_file.scope, standalone = 1))
        if root is not None and ptr_table is not None :
            self._aquire_bin_buffer  \
                ( meta_struct, root, ptr_table, h_file, c_file, C
                , function_name_tail
                )
            self._release_bin_buffer \
                ( meta_struct, root, ptr_table, h_file, c_file, C
                , function_name_tail
                )
    # def create_c_code

    def _add_c_node (self, h_file, c_file, node) :
        for f in [h_file, c_file] :
            if f is not None :
                f.add (node)
    # end def _add_c_node

    def _aquire_bin_buffer \
        ( self, meta_struct, root_table, ptr_table, h_file, c_file, C
        , function_name_tail = ""
        ) :
        table  = ptr_table.type_name
        root   = root_table.type_name
        func   = C.Function \
            ( "%s *" % table
            , "aquire_bin_buffer%s" %  function_name_tail
            , "const ubyte1 * bin_buffer"
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
        self._map_offset_to_struct \
            (meta_struct, blk, C, root_table, read_buf_mode = False)
        self._add_c_node (h_file, c_file, func)
    # end def _aquire_bin_buffer

    def _debug_as_c_code (self, meta_struct) :
        C = TFL.SDG.C
        if self.scope :
            filename = \
                ( "debug_%s_%s.c"
                % (getattr (self.scope.root, "name"), self.__class__.__name__)
                )
            filename = sos.path.join \
                ( self.scope.db_name.directory
                , filename
                )
        else :
            cnt     = getattr (self, "debug_file_counter", -1)
            cnt    += 1
            setattr (self, "debug_file_counter", cnt)
            filename = \
                ( "debug_%s_%s_%05x.c"
                % (self.__class__.__name__, str (meta_struct.__name__), cnt)
                )
            filename = sos.path.join (sos.getcwd (), filename)
        filename = sos.path.normpath (filename)
        module   = C.Module ()
        cc       = C_Code_Creator (self.gauge)
        module.add (cc (C, meta_struct, None, reset_extension = False))
        f        = None
        try :
            try :
                print "Write file `%s`" % filename
                f = open (filename, "w")
                module.write_to_c_stream (cstream = f)
            except IOError :
                pass
        finally :
            if f is not None :
                f.close ()
    # end def _debug_as_c_code

    def _map_offset_to_struct \
        (self, meta_struct, blk, C, root_table, read_buf_mode = False) :
        if read_buf_mode :
            bin_buffer = "bin_buffer"
        else :
            bin_buffer = "result->bin_buffer"
        for c in meta_struct.uses_global_buffers :
            if c is root_table :
                blk.add \
                    ( C.Statement
                        ( "result->%s = (%s *) %s"
                        % ( c.buffer_field_name, c.type_name, bin_buffer)
                        , scope = C.C
                        )
                    )
            else :
                blk.add \
                    ( C.Statement
                        ( "result->%s = (%s *) (& (%s [desc->%s]))"
                        % ( c.buffer_field_name, c.type_name
                          , bin_buffer, c.offset_field_name
                          )
                        , scope = C.C
                        )
                    )
    # end def _map_offset_to_struct

    def _read_bin_buffer \
        ( self, meta_struct, root_table, ptr_table, h_file, c_file, C
        , function_name_tail = ""
        ) :
        if ptr_table is None or root_table is None :
            return
        table  = ptr_table.type_name
        root   = root_table.type_name
        func   = C.Function \
            ( "void"
            , "read_bin_buffer%s" % function_name_tail
            , "const ubyte1 * bin_buffer, struct _%s * result" % (table, )
            )
        func.add \
            ( C.Var
                ( "%s *" % root
                , "desc"
                , "(%s *) bin_buffer" % root
                )
            )
        blk  = C.Stmt_Group (scope = c_file.scope)
        self._map_offset_to_struct \
            (meta_struct, blk, C, root_table, read_buf_mode = True)
        func.add (blk)
        self._add_c_node (h_file, c_file, func)
    # end def _read_bin_buffer

    def _release_bin_buffer \
        ( self, meta_struct, root_table, ptr_table, h_file, c_file, C
        , function_name_tail = ""
        ) :
        func  = C.Function \
            ( "void"
            , "release_bin_buffer%s" %  function_name_tail
            , "struct _%s * table" % ptr_table.type_name
            )
        func.add (C.Statement ("free (table->bin_buffer)"))
        func.add (C.Statement ("free (table)"))
        self._add_c_node (h_file, c_file, func)
    # end def _release_bin_buffer

# end class Bin_Block_Creator


if __name__ != "__main__" :
    TFL.CDG._Export ("*")

### __END__ TFL.CDG.File
