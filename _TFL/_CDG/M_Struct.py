# -*- coding: iso-8859-1 -*-
# Copyright (C) 2002-2003 TTTech Computertechnik AG. All rights reserved
# Schönbrunnerstraße 7, A--1040 Wien, Austria. office@tttech.com
#
#++
# Name
#    TFL.CDG.M_Struct
#
# Purpose
#    Provide meta-class for FTC struct definitions
#
# Revision Dates
#     2-Dec-2003 (CT)  Creation (factored from `Error_Code.py`)
#    11-Jul-2005 (MG)  Move from the TTA.FTC package to the TFL.CDG package
#    11-Jul-2005 (MG)  `New` added
#    14-Jul-2005 (MG)  `reset_all` changed to a `classmethod`
#    14-Jul-2005 (MG)  `reference_field` handling added
#    10-Nov-2005 (MG)  `offset_fields` and `buffer_fields` added
#    11-Nov-2005 (MG)  `define_access_macros` added
#    11-Nov-2005 (MG)  `reference_field` handling changed (no need to specify
#                      a name for the field)
#    ««revision-date»»···
#--

from   _TFL             import TFL
import _TFL._Meta.M_Class

### each `project` (e.g.: table driven FT-Com layer, table driven Com-Layer,
### ...) has to define it's own meta class which can be created using the
### `New` function of tghis module.

class M_Struct (TFL.Meta.M_Class) :
    """Meta class for CDG Struct classes"""

    ref_field_name = "%s_Ref"

    def __init__ (cls, name, bases, dict) :
        super (M_Struct, cls).__init__ (name, bases, dict)
        cls._add_class      (name)
        cls.reset_extension ()
        cls.type_name = cls.__name__
    # end def __init__

    def __call__ (cls, * args, ** kw) :
        cls.count += 1
        result     = super (M_Struct, cls).__call__ (* args, ** kw)
        result.id  = cls.count
        cls.extension.append (result)
        return result
    # end def __call__

    def _add_class (cls, name) :
        cls.classes [name] = cls
        if not name.startswith ("_") :
            struct_fields = getattr (cls, "struct_fields", ())
            if struct_fields :
                cls.needs_struct.append (cls)
            if getattr (cls, "uses_global_buffer", 0) :
                cls.uses_global_buffers.append (cls)
                if not cls.__dict__.has_key ("field_name") :
                    if name.startswith (cls.prefix) :
                        name = name [len (cls.prefix):]
                    setattr (cls, "field_name", name.lower ())
                if cls.is_solitaire :
                    tail = ""
                else :
                    tail = "_buffer"
                for attr_name, value in \
                    ( ("buffer_field_name", "%s%s"  % (cls.field_name, tail))
                    , ("offset_field_name", "%s_offset" % (cls.field_name))
                    ) :
                    setattr (cls, attr_name, value)
            ref_field = getattr (cls, "reference_field", None)
            if ref_field :
                ref_field.set_type (cls.ref_field_name % cls.__name__)
                ref_field.struct    = cls
                if ref_field.typedef :
                    cls.needs_typedef.append (ref_field)
    # end def _add_class

    def reset_extension (cls) :
        cls.extension = []
        cls.count     = 0
    # end def reset_extension

    @classmethod
    def reset_all (cls) :
        for c in cls.classes.values () :
            c.reset_extension ()
    # end def reset_all

    @classmethod
    def offset_fields (cls, field_cls) :
        return tuple \
            ([ field_cls
                 ( "ubyte4"
                 , c.offset_field_name
                 , "in `bin_buffer`"
                 , -1
                 )
               for c in cls.uses_global_buffers
             ]
            )
    # end def offset_fields

    @classmethod
    def buffer_fields (cls, field_cls) :
        return tuple \
            ([ field_cls
                 ( "%s *" % (c.__name__, )
                 , c.buffer_field_name
                 , "Base address of all %s entries" % (c.__name__, )
                 , -1
                 )
               for c in cls.uses_global_buffers
             ]
            )
    # end def buffer_fields

    @classmethod
    def define_access_macros (cls, C, node, main) :
        for c in cls.uses_global_buffers :
            b_name = c.buffer_field_name
            index  = c.reference_field.index
            if c.is_solitaire:
                node.add \
                    (C.Define ( c.__name__.upper (), main
                              , "(& %s->%s)" % (main, b_name, )
                              , scope = C.H
                              )
                    )
            else :
                paramater = "ref"
                if index :
                    code = "(& %s->%s [%s])" % (main, b_name, paramater)
                else :
                    code = "(%s)" % (paramater, )
                node.add \
                    ( C.Define
                        ( c.__name__.upper (), "%s, %s" % (main, paramater)
                        , code
                        , scope = C.H
                        )
                    )
    # end def define_access_macros

# end class M_Struct

def New (name_postfix) :
    cls = M_Struct
    d   = dict \
        ( uses_global_buffers = []
        , needs_struct        = []
        , needs_typedef       = []
        , classes             = {}
        , prefix              = "%s_" % (name_postfix, )
        )
    name = "%s_%s" % (cls.__name__, name_postfix)
    return type (cls) (name, (cls, ), d)
# end def New

if __name__ != "__main__" :
    import _TFL._CDG
    TFL.CDG._Export_Module ()
### __END__ TFL.CDG.M_Struct
