# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 TTTech Computertechnik AG. All rights reserved
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
#    09-Nov-2005 (MG) Creation
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
        ( "Byte_Copy_Spec_Ref"
        , "byte_cs"
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
        ( "Bit_Copy_Spec_Ref"
        , "bit_cs"
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
        self.mask     = "0x%02X" % mask
        self.shift    = shift
    # end def __init__

# end class Bit_Copy_Spec

class Message_Pack_Copy (Struct) :
    """Structure defining which message has to be copied into the double
       buffer during the `pack` operation.
    """
    SF                 = TFL.CDG.Struct_Field
    uses_global_buffer = True
    struct_fields      = \
        ( Byte_Copy_Spec.reference_field
        , Bit_Copy_Spec. reference_field
        )

    def __init__ (self, msg_name, length) :
        bytes = length // 8
        bits  = length % 8
        off   = 0
        self.byte_cs = Byte_Copy_Spec.count
        self.bit_cs  = Bit_Copy_Spec. count
        for i in range (bytes) :
            Byte_Copy_Spec ("(& %s) + %d" % (msg_name, off), off)
            off += 1
        if bits :
            mask = (1 << bits) - 1
            Bit_Copy_Spec  ("(& %s) + %d" % (msg_name, off), off, mask)
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
            type_name  = c.__name__
            array_name = "".join ([type_name.lower (), "_data"])
            for o in c.extension :
                values.append (o.dict ())
            c_block.add \
                ( C.Array \
                    (type_name, array_name, len (values), init = values)
                )
        return c_block
    # end def pack_as_c_code

# end class TDCOM_Descriptor

if __name__ == "__main__" :
    m1 = Message_Pack_Copy ("m1", 28)
    m2 = Message_Pack_Copy ("m2",  5)
    m  = TFL.SDG.C.Module (name = "test")
    C  = TFL.SDG.C
    add = m.add
    for c in Meta_Struct.needs_struct :
        add (c.as_forward_typedef (const = c.const, scope = C.H))
        add (C.New_Line (scope = C.H))
    add (C.New_Line (scope = C.H))
    for c in Meta_Struct.needs_struct :  # write struct
        add ( c.as_c_code (scope = C.H, standalone = 1))
        add ( C.New_Line  (scope = C.H))
    add (C.New_Line (scope = C.H))
    if 1 :
        x = TDCOM_Descriptor (C)
        print "\n".join (x.c_block.as_c_code ())
    else :
        print "\n".join (m.as_h_code ())
        print "-" * 70
        print "\n".join (m.as_c_code ())
### __END__ TFL.CDG._test
