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
#    14-Nov-2005 (MG) ´as_dot` added
#    01-Dec-2005 (MG)  `typedef_prefix` added
#    02-Dec-2005 (MG)  Use `typedef_prefix` to define the `type_name`
#    04-Dec-2005 (KZU) `typedef_prefix` added to method buffer_fields
#    23-Jan-2006 (CED) Additional classmethods for structfield creation
#                      added
#    28-Feb-2006 (CED) Minor modifications to `define_access_macros`
#    12-May-2006 (CED) `reset_state` added
#    19-Mar-2007 (DAL) changed offset_field default from -1 to 0xFFFFFFFF
#                      (RUP 23577)
#    24-Apr-2007 (DAL) `as_tex` addded
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ««revision-date»»···
#--



from   _TFL             import TFL
import _TFL._Meta.M_Class

### each `project` (e.g.: table driven FT-Com layer, table driven Com-Layer,
### ...) has to define it's own meta class which can be created using the
### `New` function of this module.

class M_Struct (TFL.Meta.M_Class) :
    """Meta class for CDG Struct classes"""

    ref_field_name = "%s_Ref"

    def __init__ (cls, name, bases, dict) :
        super (M_Struct, cls).__init__ (name, bases, dict)
        cls._add_class      (name)
        cls.reset_extension ()
        if cls.typedef_prefix :
            cls.type_name = "%s_%s" % (cls.typedef_prefix, cls.__name__)
        else :
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

    def reset_state (cls) :
        pass ### subclasses implement this
    # def reset_state

    @classmethod
    def reset_all (cls) :
        for c in cls.classes.values () :
            c.reset_extension ()
            c.reset_state     ()
    # end def reset_all

    @classmethod
    def bin_buffer_fields (cls, field_cls) :
        return \
           ( field_cls
               ( "ubyte1 *", "bin_buffer"
               , "Pointer to the bin_buffer"
               , 0
               )
           ,
           )
    # end def bin_buffer_fields

    @classmethod
    def buffer_fields (cls, field_cls) :
        pref = ""
        if cls.typedef_prefix :
            pref = cls.typedef_prefix + "_"
        return tuple \
            ([ field_cls
                 ( "%s%s *" % (pref, c.__name__, )
                 , c.buffer_field_name
                 , "Base address of all %s entries" % (c.__name__, )
                 , -1
                 )
               for c in cls.uses_global_buffers
             ]
            )
    # end def buffer_fields

    @classmethod
    def descriptor_fields (cls, field_cls, target_cls) :
        return \
           ( field_cls
               ( "%s *" % target_cls.type_name, "descriptor"
               , "Pointer to the main config table"
               , 0
               )
           ,
           )
    # end def descriptor_fields

    @classmethod
    def offset_fields (cls, field_cls) :
        return tuple \
            ([ field_cls
                 ( "ubyte4"
                 , c.offset_field_name
                 , "in `bin_buffer`"
                 , 0xFFFFFFFF
                 )
               for c in cls.uses_global_buffers
             ]
            )
    # end def offset_fields

    @classmethod
    def size_fields (cls, field_cls) :
        return \
           ( field_cls
               ( "ubyte4", "total_size"
               , "Total size of bin_buffer"
               , 0
               )
           ,
           )
    # end def size_fields

    @classmethod
    def define_access_macros (cls, C, node, main) :
        for c in cls.uses_global_buffers :
            b_name = c.buffer_field_name
            name   = c.__name__.upper ()
            if cls.typedef_prefix :
                name = "%s%s" % (cls.prefix, name)
            if c.reference_field :
                index  = c.reference_field.index
            else :
                index  = True
                print ">>>", c.type_name
            if c.is_solitaire:
                node.add \
                    (C.Define ( name, main
                              , "(& (%s)->%s)" % (main, b_name, )
                              , scope = C.H
                              )
                    )
            else :
                paramater = "ref"
                if index :
                    code = "(& (%s)->%s [%s])" % (main, b_name, paramater)
                else :
                    code = "(%s)" % (paramater, )
                node.add \
                    ( C.Define
                        ( name, "%s, %s" % (main, paramater)
                        , code
                        , scope = C.H
                        )
                    )
    # end def define_access_macros

    @classmethod
    def as_dot (cls, filename) :
        """ create dot file from Meta_Struct"""
        const_node = "node"
        dot        = \
            [ 'digraph g {'
            , 'graph [rankdir = "LR"];'
            , 'node [fontsize = "16" shape = "ellipse"];'
            , 'edge [];'
            ]
        add        = dot.append
        for index, c in enumerate (cls.needs_struct) :
            fields   = \
                [ "%s %s |<f%s> " % (f.type, f.name, n)
                    for (n, f) in enumerate (c.struct_fields)
                ]
            fields   = \
                [ "<f%s> %s" % (f.name, f.name)
                    for (n, f) in enumerate (c.struct_fields)
                ]
            add ( '%s%s ' % (const_node, c.type_name))
            add ( '  [ label = "<f%s> %s | %s"'
                % (c.type_name, c.type_name, " | ".join (fields))
                )
            add ( '    shape = "record"')
            add ( '  ]')
        add ("")
        id = 0
        for index, c in enumerate (cls.needs_struct) :
            for f in c.struct_fields :
                if isinstance (f, TFL.CDG.Reference_Struct_Field) :
                    add ( '"%s%s":f%s -> "%s%s":f%s'
                        % ( const_node, c.type_name, f.name
                          , const_node, f.struct.type_name, f.struct.type_name
                          )
                        )
                    add (' [ id = %d]' % (id, ))
                    id += 1
        add     ("}")
        if isinstance (filename, str) :
            f = open     (filename, "w")
            f.write      ("\n".join (dot))
            f.close      ()
        else :
            filename.write      ("\n".join (dot))
    # end def as_dot

    @classmethod
    def as_tex (cls, filename):
        """create TeX file from Meta_Struct"""
        tex       = \
            [ r"% \def\BeginTable#1#2"
            , r"% {"
            , r"%   \verb|#1|: \verb|#2|"
            , r"%"
            , r"%     \begin{longtable}{|l|l|c|p{2cm}|}"
            , r"%     \hline"
            , r"%     Attribute & Type & Valid Value Range & Requirements\\"
            , r"%     \hline"
            , r"% }"
            , r"% \def\EndTable{"
            , r"%   \end{longtable}"
            , r"% }"
            , r"% \def\Entry#1#2#3#4"
            , r"% {"
            , r"%   \verb|#1| & \verb|#2| & #3 & \verb|#4|\\"
            , r"%   \hline"
            , r"% }"
            ]
        begin_fmt = "\\BeginTable{%s}{}"
        entry_fmt = "  \\Entry{%s}{%s}{}{}"
        end_fmt   = "\\EndTable"
        for c in cls.needs_struct:
            tex.append (begin_fmt % c.type_name)
            for f in c.struct_fields:
                if isinstance (f, TFL.CDG.Reference_Struct_Field):
                    t = "%s*" % f.struct.type_name
                else:
                    t = f.type_name
                tex.append (entry_fmt % (f.name, t))
            tex.append (end_fmt)
        if isinstance (filename, str) :
            f = open  (filename, "w")
            f.write   ("\n".join (tex))
            f.close   ()
        else :
            filename.write ("\n".join (tex))
    # end def as_tex

# end class M_Struct

def New ( name_postfix
        , typedef_prefix = ""
        ) :
    cls = M_Struct
    d   = dict \
        ( uses_global_buffers = []
        , needs_struct        = []
        , needs_typedef       = []
        , classes             = {}
        , prefix              = "%s_" % (name_postfix, )
        , typedef_prefix      = typedef_prefix
        )
    name = "%s_%s" % (cls.__name__, name_postfix)
    return type (cls) (name, (cls, ), d)
# end def New

if __name__ != "__main__" :
    import _TFL._CDG
    TFL.CDG._Export_Module ()
### __END__ TFL.CDG.M_Struct
