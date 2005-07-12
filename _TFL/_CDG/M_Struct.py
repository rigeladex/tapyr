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
#    ««revision-date»»···
#--

from   _TFL             import TFL
import _TFL._Meta.M_Class

### each `project` (e.g.: table driven FT-Com layer, table driven Com-Layer,
### ...) has to define it's own meta class which can be created using the
### `New` function of `M_Struct`

class M_Struct (TFL.Meta.M_Class) :
    """Meta class for CDG Struct classes"""

    def __init__ (cls, name, bases, dict) :
        super (M_Struct, cls).__init__ (name, bases, dict)
        cls._add_class      (name)
        cls.reset_extension ()
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
    # end def _add_class

    def reset_extension (cls) :
        cls.extension = []
        cls.count     = 0
    # end def reset_extension

    def reset_all () :
        for c in M_Struct.classes.values () :
            c.reset_extension ()
    reset_all = staticmethod (reset_all)

# end class M_Struct

def New (name_postfix) :
    cls = M_Struct
    d   = dict \
        ( uses_global_buffers = []
        , needs_struct        = []
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
