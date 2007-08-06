# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.cluster
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
#    TFL.SDG.M_Node
#
# Purpose
#    Meta class for SDG.Node classes
#
# Revision Dates
#    23-Jul-2004 (CT) Creation
#    26-Jul-2004 (CT) Creation continued
#    15-Dec-2005 (CT) `normalize_formats` changed to normalize for each class
#                     anew (to avoid nasty surprises with `sep` aliasing when
#                     format is shared between sibling classes with different
#                     values for `sep`)
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ««revision-date»»···
#--



from   _TFL                            import TFL

import _TFL._Meta.M_Auto_Combine_Dicts
import _TFL._Meta.M_Class
import _TFL._SDG
import _TFL._SDG.Formatter

from   Regexp                          import *

_indent_pat = Regexp (r">*")

class M_Node (TFL.Meta.M_Auto_Combine_Dicts, TFL.Meta.M_Class) :
    """Meta class for SDG.Node classes"""

    __id              = 0
    _dicts_to_combine = ("init_arg_defaults", "_autoconvert")

    def __init__ (cls, name, bases, dict) :
        super (M_Node, cls).__init__ (name, bases, dict)
        cls._normalize_formats ()
    # end def __init__

    def __call__ (cls, * args, ** kw) :
        result     = cls.__new__  (cls, * args, ** kw)
        cls.__id  += 1
        result.id  = cls.__id
        result.__init__ (* args, ** kw)
        return result
    # end def __call__

    def _normalize_format (cls, fn, f) :
        format_lines = []
        for line in f.strip ().split ("\n") :
            line  = line.strip ().replace ("\\n", "\n")
            level = _indent_pat.match (line).end ()
            cf    = line [level:]
            format_lines.append (TFL.SDG.Formatter (level, cf))
        setattr (cls, fn, format_lines)
        setattr (cls, "__%s" % fn, f)
    # end def _normalize_format

    def _normalize_formats (cls) :
        for fn in cls._list_of_formats :
            f = getattr (cls, fn, None)
            if f is not None :
                if not isinstance (f, (str, unicode)) :
                    f = getattr (cls, "__%s" % fn)
                cls._normalize_format (fn, f)
    # end def _normalize_formats

# end class M_Node

if __name__ != "__main__" :
    TFL.SDG._Export ("*")
### __END__ TFL.SDG.M_Node
