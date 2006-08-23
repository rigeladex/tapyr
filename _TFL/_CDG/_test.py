# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 - 2006 TTTech Computertechnik AG. All rights reserved
# Schönbrunnerstraße 7, A--1040 Wien, Austria. office@tttech.com
#
#++
# Name
#    TFL.CDG._test
#
# Purpose
#    Test the basic functions of TFL.CDG.Struct
#
# Revision Dates
#    09-Nov-2005 (MG)  Creation
#    11-Nov-2005 (MG)  Test extended
#    10-Mar-2006 (MZO) added `S_With_Array`
#    23-Aug-2006 (PGO) Using alternate form of %x
#    ««revision-date»»···
#--
#
from   _TFL                 import TFL
import _TFL._Meta.Object
import _TFL._CDG.M_Struct
import _TFL._CDG.Struct_Field
import _TFL._CDG.Struct
import _TFL._SDG._C
import _TFL._SDG._C.import_C

Meta_Struct = TFL.CDG.M_Struct.New ("TDCOM")

class Struct (TFL.CDG.Struct) :
    """Base class for all structs"""

    __metaclass__ = Meta_Struct

# end class Struct

class Byte_Copy_Spec (Struct) :
    """Structure defining how to copy a byte. The source is specified as
       absolute address and the desition is only an offset.
    """

    SF                 = TFL.CDG.Struct_Field
    uses_global_buffer = True
    reference_field    = TFL.CDG.Reference_Struct_Field \
        ( "byte_cs"
        , "Index into `byte_copy_spec_buffer` defining how to copy "
          "byte-parts of a message into the double buffer"
        , typedef      = "ubyte4"
        )

    struct_fields      = \
        ( SF ( "ubyte1 *"
             , "source"
             , "Address of the source byte"
             )
        , SF ( "ubyte2"
             , "destination"
             , "Offset relative to the base address of a a double buffer"
             )
        )

    def __init__ (self, source, destination) :
        self.source      = source
        self.destination = destination
    # end def __init__

# end class Byte_Copy_Spec

class Bit_Copy_Spec (Byte_Copy_Spec) :
    """Structure defining how to copy a bit. The source is specified as
       absolute address and the desition is only an offset.
    """

    SF                 = TFL.CDG.Struct_Field
    reference_field    = TFL.CDG.Reference_Struct_Field \
        ( "bit_cs"
        , "Index into `bit_copy_spec_buffer` defining how to copy "
          "bit-parts of a message into the double buffer"
        , typedef      = "ubyte4"
        )

    struct_fields      = Byte_Copy_Spec.struct_fields + \
        ( SF ( "ubyte1"
             , "mask"
             , "Mask applied to the source during the copy operation"
             , 0
             )
        , SF ( "sbyte1"
             , "shift"
             , "XXX"
             , 0
             )
        )

    def __init__ (self, source, desition, mask, shift = 0) :
        self.__super.__init__ (source, desition)
        self.mask     = "%#02X" % mask
        self.shift    = shift
    # end def __init__

# end class Bit_Copy_Spec

class S_With_Array (Struct) :
    """.
    """
    uses_global_buffer = True

    SF                 = TFL.CDG.Struct_Field
    reference_field    = TFL.CDG.Reference_Struct_Field \
        ( "sa_entry"
        , "."
        , typedef      = "ubyte4"
        )

    struct_fields      = \
        ( SF ( "ubyte1"
             , "mask"
             , "Mask applied to the source during the copy operation"
             )
        , SF ( "ubyte4"
             , "cni_offset"
             , "."
             , bounds = 2
             )
        )

    def __init__ (self) :
        self.__super.__init__ ()
        self.mask     = "1233"
        self.cni_offset   = []
        length = 2
        for i in xrange (length) :
            self.cni_offset.append \
                (i)
    # end def __init__

# end class S_With_Array

class Message_Pack_Copy (Struct) :
    """Structure defining which message has to be copied into the double
       buffer during the `pack` operation.
    """
    SF                 = TFL.CDG.Struct_Field
    uses_global_buffer = True

    reference_field    = TFL.CDG.Reference_Struct_Field \
        ( "msg_pack_copy"
        , "Index into `message_apck_copy_buffer` defining which messages"
          "should be copied"
        , typedef      = "ubyte4"
        )
    struct_fields      = \
        ( SF ( "ubyte1"
             , "no_of_bylc"
             , "number of byte_copy_spe"
             , 0
             )
        , Byte_Copy_Spec.reference_field
        , Bit_Copy_Spec. reference_field
        , S_With_Array.  reference_field
        )

    def __init__ (self, msg_name, length) :
        bytes = length // 8
        bits  = length % 8
        off   = 0
        self.no_of_bylc = str(bytes)
        self.byte_cs = Byte_Copy_Spec.current ()
        self.bit_cs  = Bit_Copy_Spec. current ()
        for i in range (bytes) :
            Byte_Copy_Spec ("(& %s) + %d" % (msg_name, off), off)
            off += 1
        if bits :
            mask = (1 << bits) - 1
            Bit_Copy_Spec  ("(& %s) + %d" % (msg_name, off), off, mask)
        self.sa_entry = S_With_Array.current ()
        S_With_Array ()
    # end def __init__

# end class Message_Pack_Copy

class TDCOM_Descriptor (Struct) :
    """Structure containing all information about table-driven FT-Com Layer."""

    SF                    = TFL.CDG.Struct_Field

    struct_fields         = \
        ( ( SF  ( "long"
                , "total_size"
                , "Total size of `bin_buffer` of TDCOM_Table"
                , 0
                )
          )
          ,
        ) + tuple \
        ([ SF   ( "long"
                , c.offset_field_name
                , "in `bin_buffer`"
                , -1
                )
         for c in Meta_Struct.uses_global_buffers
         ]
        )


    def __init__ (self, as_c = True) :
        self.c_block = self.pack_as_c_code (TFL.SDG.C)
    # end def __init__

    def pack_as_c_code (self, C) :
        c_block = C.Stmt_Group ()
        for c in Meta_Struct.uses_global_buffers :
            values     = []
            for o in c.extension :
                values.append (o.dict ())
            c_block.add \
                ( C.Array
                    ( c.type_name, c.buffer_name ()
                    , bounds = len (values)
                    , init   = values
                    )
                )
        return c_block
    # end def pack_as_c_code

# end class TDCOM_Descriptor

if __name__ == "__main__" :
    from Command_Line import Command_Line

    cmd = Command_Line \
        ( option_spec = ( "index:B"
                        , "header:B"
                        )
        ,
        )

    C                                    = TFL.SDG.C
    C.Var.type_name_length               = 30
    TFL.CDG.Reference_Struct_Field.index = not not cmd.index

    m1 = Message_Pack_Copy ("m1", 28)
    m2 = Message_Pack_Copy ("m2",  5)
    m  = TFL.SDG.C.Module (name = "test")
    add = m.add

    for sf in Meta_Struct.needs_typedef :
        add (sf.as_typedef (C = C, scope = C.H))
    add (C.New_Line (scope = C.H))

    for c in Meta_Struct.needs_struct :
        add (c.as_forward_typedef (const = c.const, scope = C.H))
    add (C.New_Line (scope = C.H))

    for c in Meta_Struct.needs_struct :  # write struct
        add ( c.as_c_code (scope = C.H, standalone = 1))
        add ( C.New_Line  (scope = C.H))
    add (C.New_Line (scope = C.H))

    Meta_Struct.define_access_macros (C, m, "tdcom")

    if not cmd.header :
        x = TDCOM_Descriptor (C)
        print "\n".join (x.c_block.as_c_code ())
    else :
        print "\n".join (m.as_h_code ())
        print "-" * 70
        print "\n".join (m.as_c_code ())
### __END__ TFL.CDG._test
