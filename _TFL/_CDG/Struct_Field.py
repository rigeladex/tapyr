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
#    TFL.CDG.Struct_Field
#
# Purpose
#    Model a single field of a C struct.
#
# Revision Dates
#    11-Jul-2005 (MG) Creation (Factored from TTA.FTC.TDFT_Data)
#    12-Jul-2005 (MG) Classmethod `add_type_mapping` added
#    12-Jul-2005 (MG) `as_c_code`: `desc` formatted
#    14-Jul-2005 (MG) `add_type_mapping` removed
#    14-Jul-2005 (MG) `format_code` simplified
#    14-Jul-2005 (MG) `Reference_Struct_Field` added
#    09-Nov-2005 (MG) `[us]byte[14]` types added to `type_map`
#    09-Nov-2005 (MG) `Reference_Struct_Field` calculation of `user_code`
#                     fixed
#    11-Nov-2005 (MG)  `Reference_Struct_Field` now supports index and
#                      address based references
#    02-Dec-2005 (KZU) added `typedef_prefix` in Reference_Struct_Field
#    02-Dec-2005 (MG)  use `type_name` of Struct classes/instances
#    20-Jan-2006 (CED) Added `bo_map`,  made `packed` byte-order aware
#    20-Feb-2006 (MZO) Corrected super call of `Reference_Struct_Field`
#    13-Jul-2006 (MZO) [20886] `check_value` added
#    17-Jul-2006 (MZO) [20886] `check_value` fixed
#    17-Jul-2006 (MZO) [22038] `val_range` corrected
#    13-Mar-2007 (MZO) [23693] check char fields
#    14-Mar-2007 (PGO) `check_value` changed to raise Value_Out_Of_Range
#     7-May-2007 (MZO) `check_value` fixed, hex was not checked correctly
#    ««revision-date»»···
#--

from   _TFL                           import TFL
import _TFL._Meta.Object
import _TFL._SDG._C
import operator
import struct
import traceback
import math

class Value_Out_Of_Range (ValueError) : pass

class Struct_Field (TFL.Meta.Object):
    """Model a single field of a C struct."""

    typedef  = None

    fmt_code = \
        { "char"                  : "c", "unsigned char"         : "B"
        , "char []"               : "s"
        , "double"                : "d", "float"                 : "f"
        , "int"                   : "i", "unsigned int"          : "I"
        , "long"                  : "l", "unsigned long"         : "L"
        , "llong"                 : "q", "ullong"                : "Q"
        , "short"                 : "h", "unsigned short"        : "H"
        , "signed char"           : "b"
        , "void *"                : "P"
        }

    type_map = \
        { "char[]"                     : "char []"
        , "long long"                  : "llong"
        , "schar"                      : "signed char"
        , "uchar"                      : "unsigned char"
        , "uint"                       : "unsigned int"
        , "ulong"                      : "unsigned long"
        , "unsigned long long"         : "ullong"
        , "ushort"                     : "unsigned short"
        , "void*"                      : "void *"
        , "sbyte1"                     : "char"
        , "sbyte2"                     : "short"
        , "sbyte4"                     : "long"
        , "ubyte1"                     : "unsigned char"
        , "ubyte2"                     : "unsigned short"
        , "ubyte4"                     : "unsigned long"
        , "ubyte1 *"                   : "void *"
        }

    bo_map                 = dict \
      ( little_endian      = "<"
      , big_32_endian      = ">"
      , native             = "@"
      )

    def __init__ ( self, type, name, desc
                 , init        = None
                 , user_code   = None
                 , bounds      = None
                 , ** kw ### ignore additional parameters
                 ) :
        self.type_name   = type
        self.type        = self.type_map.get (type, type)
        self.name        = name
        self.desc        = desc
        self.init        = init
        self.user_code   = user_code
        self.bounds      = bounds
    # end def __init__

    def as_c_code (self, C) :
        """Returns an object which can be passed as `field' to
           `C.Struct'.
        """
        desc = "\n".join \
            ( [ p.strip ()
                  for p in " ".join
                      ( [s.strip () or "\n" for s in self.desc.splitlines ()]
                      ).splitlines ()
              ]
            )
        if not self.bounds :
            if self.init is not None :
                init = "= %s " % self.init
            else :
                init = ""
            return "%s %s %s// %s" % (self.type_name, self.name, init, desc)
        else :
            return C.Array \
                (self.type_name, self.name, self.bounds, description = desc)
    # end def as_c_code

    def as_typedef (self, C = TFL.SDG.C, c_node = None, ** kw) :
        """Returns a typedef for a struct-object (using `C` as name-space for
           the C classes. `C` should be a subclass of `TFL.SDG.C`).

           If a `c_node` is passed in, the `result` will be added to it.
        """
        result = C.Typedef (self.typedef, self.type, ** kw)
        if c_node :
            c_node.add (result)
        return result
    # end def as_typedef

    def __str__ (self) :
        return "(%r, %r, %r, %r, %r)" % \
               (self.typedef, self.name, self.desc, self.init, self.user_code)
    # end def __str__

    def __repr__ (self) :
        return "%s %s" % (self.__class__.__name__, str (self))
    # end def __repr__

    def packed (self, value, byte_order = "native") :
        format = self.format_code ()
        if not format :
            raise ValueError \
                ("%s [%s] cannot be packed -- no format code" % (self, value))
        try :
            result = struct.pack \
                ( "%s%s"
                % (self.bo_map [byte_order], format)
                , value
                )
        except :
            traceback.print_exc ()
            print repr (self), format, value
            raise
        return result
    # end def packed

    def check_value (self, original_value) :
        result  = True
        size    = 0
        value   = str (original_value)
        if   value.lower () == "true" :
            value = "1"
        elif value.lower () == "false" :
            value = "0"
        format = self.user_code or self.fmt_code.get (self.type, None)
        if format and not format in ("s", "P") : # char
            size = struct.calcsize (format)
        if format == "f" :
            try :
                value = float (value)
            except (ValueError, TypeError) :
                value = None
        else :
            try :
                value = long (value, 0)
            except (ValueError, TypeError) :
                value = None
        if size > 0 and value is not None :
            val_range = math.pow (2, (size * 8)) - 1
            if format in  ("I", "L", "Q", "H", "B", "c") :        # unsigned
                if value > val_range :
                    result     = False
                    error_text = \
                        ( ( "Unexpected value in %s `%s` "
                            "(typesize `%s` bytes): Value `%s` is not"
                            " within range (%s)."
                          )
                        % ( self.__class__.__name__, self.name
                          , size, original_value , "0 .. %s" % val_range
                          )
                        )
                    raise Value_Out_Of_Range (error_text)
            else :
                val_range = val_range // 2 + 1                   # signed
                if abs (value) > (val_range) :
                    result     = False
                    error_text = \
                        ( ( "Unexpected value in %s `%s` "
                            "(typesize `%s` bytes): Value `%s` is not"
                            " within range (%s)."
                          )
                        % ( self.__class__.__name__, self.name
                          , size, original_value
                          , "-%s .. +%s" % (val_range, val_range)
                          )
                        )
                    raise Value_Out_Of_Range (error_text)
        return result
    # end def check_value

    def format_code (self) :
        result = self.user_code or self.fmt_code.get (self.type, None)
        if self.bounds and result :
            if isinstance (self.bounds, (list, tuple)) :
                result = "%d%s" % (reduce (operator.mul, self.bounds), result)
            else :
                result = "%d%s" % (self.bounds, result)
        return result
    # end def format_code

# end class Struct_Field

class Reference_Struct_Field (Struct_Field) :
    """A struct field which references a other `Struct_Field`."""

    index = True

    def __init__ ( self, name, desc
                 , init        = None
                 , user_code   = None
                 , bounds      = None
                 , typedef     = None
                 , index       = None
                 ) :
        self.__super.__init__ \
            ("<none>", name, desc
            , init      = init
            , user_code = user_code
            , bounds    = bounds
            )
        self.typedef    = typedef
        if index is not None :
            ### only override class default if explicitly specfied
            self.index = index
        if self.typedef and not self.user_code :
            type           = self.type_map.get (self.typedef, self.typedef)
            self.user_code = self.fmt_code.get (type, None)
    # end def __init__

    def set_type (self, type) :
        self.type_name = type
        self.type      = self.type_map.get (type, type)
    # end def set_type

    def as_typedef (self, * args, ** kw) :
        if not self.index :
            self.type_name = "%s *" % (self.struct.type_name, )
        return self.__super.as_typedef (* args, ** kw)
    # end def as_typedef

    def as_c_code (self, * args, ** kw) :
        if not self.index :
            self.type_name = "%s *" % (self.struct.type_name, )
        return self.__super.as_c_code (* args, ** kw)
    # end def as_c_code

    def check_value (self, original_value) :
        return True
    # end def check_value

# end class Reference_Struct_Field

if __name__ != "__main__" :
    import _TFL._CDG
    TFL.CDG._Export ("*")
### __END__ TFL.CDG.Struct_Field
