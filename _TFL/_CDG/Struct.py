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
#    TFL.CDG.Struct
#
# Purpose
#    Root class for class modelling C structs.
#
# Revision Dates
#    11-Jul-2005 (MG) Creation (Factored from TTA.FTC.TDFT_Data)
#    ««revision-date»»···
#--

from   _TFL                           import TFL
import _TFL._Meta.Object
import _TFL._Meta.Property
import _TFL._SDG._C

class Struct (TFL.Meta.Object) :
    """Root class for classes modelling C structs of the table-driven FT-Com
       Layer.

       Each descendent class must define a list `struct_fields' containing
       `Struct_Field' instances.
    """

    ### Set the __metaclass__ attribute a new Meta_Struct class, e.g.:
    ### __metaclass__      = TFL.CDG.Meta_Struct.New ("TDFT")

    __autowrap         = TFL.d_dict \
      ( as_forward_typedef = TFL.Meta.Class_Method
      , as_typedef         = TFL.Meta.Class_Method
      , as_c_code          = TFL.Meta.Class_Method
      , _struct_fields     = staticmethod
      )

    struct_fields      = ()

    uses_global_buffer = 0
    is_solitaire       = 0
    const              = 1

    def __new__ (cls, * args, ** kw) :
        result = object.__new__ (cls, * args, ** kw)
        for sf in result.struct_fields :
            setattr (result, sf.name, sf.init)
        return result
    # end def __new__

    def as_forward_typedef (cls, C = TFL.SDG.C, c_node = None, ** kw) :
        """Returns a typedef for a struct-object (using `C` as name-space for
           the C classes. `C` should be a subclass of `TFL.SDG.C`).

           If a `c_node` is passed in, the `result` will be added to it.
        """
        result = C.Typedef \
            ("struct _%s" % cls.__name__, cls.__name__, ** kw)
        if c_node :
            c_node.add (result)
        return result
    # end def as_forward_typedef

    def as_typedef (cls, C = TFL.SDG.C, c_node = None, ** kw) :
        """Returns a typedef for a struct-object (using `C` as name-space for
           the C classes. `C` should be a subclass of `TFL.SDG.C`).

           If a `c_node` is passed in, the `result` will be added to it.
        """
        result = C.Typedef (cls.as_c_code (C), ** kw)
        if c_node :
            c_node.add (result)
        return result
    # end def as_typedef

    def as_c_code (cls, C = TFL.SDG.C, ** kw) :
        """Returns c-code for the definition of C.Struct for `self`"""
        return C.Struct \
            ( cls.__name__
            , [f.as_c_code (C) for f in cls.struct_fields]
            , description = cls.__doc__
            , ** kw
            )
    # end def as_c_code

    def packed (self) :
        """Returns a string containing a binary representation of the actual
           value of the struct's attributes.
        """
        format, values = self.format_and_values ()
        try :
            result = struct.pack (format, * values)
        except :
            traceback.print_exc ()
            print self.__class__.__name__, format, values
            raise
        return result
    # end def packed

    def format_and_values (self) :
        values  = []
        formats = []
        for f in self.struct_fields :
            value  = getattr (self, f.name)
            format = f.format_code ()
            if format :
                ### `value` is a primitive data type
                formats.append (format)
                if isinstance (value, (list, tuple)) :
                    values.extend (value)
                else :
                    values.append (value)
            else :
                ### `value` is a `Struct` or sequence of `Struct`
                if isinstance (value, Struct) :
                    value = (value, )
                for v in value :
                    format, value = v.format_and_values ()
                    formats.append  (format)
                    values.extend   (value)
        format  = "".join (formats)
        ### add trailing pad bytes for correct alignment
        ###   XXX for cross architecture/compiler use, a cross-struct is needed
        parts   = [(struct.calcsize ("c0%s" % f), f) for f in format]
        parts.sort ()
        format  = "%s0%s" % (format, parts [-1] [-1])
        return format, values
    # end def format_and_values

# end class Struct

if __name__ != "__main__" :
    import _TFL._CDG
    TFL.CDG._Export ("*")
### __END__ TFL.CDG.Struct
