# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 TTTech Computertechnik AG. All rights reserved
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
#    ««revision-date»»···
#--

from   _TFL                           import TFL
import _TFL._Meta.Object
import operator
import struct
import traceback

class Struct_Field (TFL.Meta.Object):
    """Model a single field of a C struct."""

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
        }

    def __init__ (self, type, name, desc, init = None, user_code = None, bounds = None) :
        self.type      = self.type_map.get (type, type)
        self.name      = name
        self.desc      = desc
        self.init      = init
        self.user_code = user_code
        self.bounds    = bounds
    # end def __init__

    @classmethod
    def add_type_mapping (cls, ** kw) :
        for new_type, maps_to_type in kw.iteritems () :
            if new_type in cls.type_map :
                if maps_to_type != cls.type_map [new_type] :
                    msg = "\n".join \
                        ( ( "A mapping f0r type `%s` already exists:"
                            % (new_type, )
                          , "old mapping: `%s`" % (cls.type_map [new_type], )
                          , "new mapping: `%s`" % (maps_to_type, )
                          )
                        )
                    raise ValueError, msg
            cls.type_map [new_type] = maps_to_type
    # end def add_type_mapping

    def as_c_code (self, C) :
        """Returns an object which can be passed as `field' to
           `C.Struct'.
        """
        if not self.bounds :
            if self.init is not None :
                init = "= %s " % self.init
            else :
                init = ""
            return "%s %s %s// %s" % (self.type, self.name, init, self.desc)
        else :
            return C.Array ( self.type, self.name, self.bounds
                           , eol_desc = self.desc
                           )
    # end def as_c_code

    def __str__ (self) :
        return "(%s, %s, %s, %s, %s)" % \
               (self.type, self.name, self.desc, self.init, self.user_code)
    # end def __str__

    def __repr__ (self) :
        return "%s %s" % (self.__class__.__name__, str (self))
    # end def __repr__

    def packed (self, value) :
        format = self.format_code ()
        if not format :
            raise ValueError, \
                  "%s [%s] cannot be packed -- no format code" % (self, value)
        try :
            result = struct.pack (format, value)
        except :
            traceback.print_exc ()
            print repr (self), format, value
            raise
        return result
    # end def packed

    def format_code (self) :
        if not self.user_code :
            if self.fmt_code.has_key (self.type) :
                result = self.fmt_code [self.type]
            else :
                result = None
        else :
            result = self.user_code
        if self.bounds and result :
            if isinstance (self.bounds, (list, tuple)) :
                result = "%d%s" % (reduce (operator.mul, self.bounds), result)
            else :
                result = "%d%s" % (self.bounds, result)
        return result
    # end def format_code

# end class Struct_Field

if __name__ != "__main__" :
    import _TFL._CDG
    TFL.CDG._Export ("*")
### __END__ TFL.CDG.Struct_Field
