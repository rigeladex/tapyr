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
#    Formatter
#
# Purpose
#    Formatter objects for SDG
#
# Revision Dates
#    23-Jul-2004 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL               import TFL
import _TFL._Meta.Object
import _TFL._SDG

from   Regexp             import *

class _Formatter_ (TFL.Meta.Object) :
    """Root class of SDG formatters"""

# end class _Formatter_

class Single_Line_Formatter (_Formatter_) :
    """Formatter generating a single line of output"""

    def __init__ (self, indent_level, format_line) :
        self.indent_level = indent_level
        self.format_line  = format_line
    # end def __init__

    def __call__ (self, node, context, head = "") :
        return (self.format_line % context, )
    # end def __call__

# end class Single_Line_Formatter

class Multi_Line_Formatter (_Formatter_) :
    """Formatter generating a multiple lines of output"""

    pattern = Regexp \
        ( r"""%"""
          r"""\(\* (?P<key> .+) \*\)"""
          r"""(?P<form> """
              r"""(?P<flags>  [-+ #0]*)"""
              r"""(?P<mfw>    [0-9]*)"""
              r"""(?P<prec> \.[0-9]+)?"""
              r"""(?P<type>   [diouxXeEfFgGcrs])"""
          r""")"""
        , re.VERBOSE
        )

    def __init__ (self, indent_level, format_line) :
        self.indent_level = indent_level
        self._setup_formatters (format_line)
    # end def __init__

    def __call__ (self, node, context, head = "") :
        last = None
        for f in self.formatters :
            g    = iter (f (node, context, head))
            last = g.next ()
            for l in g :
                yield last % context
                last = l
                head = ""
            head += last
        if last :
            yield last % context
    # end def __call__

    def _setup_formatters (self, format_line) :
        self.formatters = formatters = []
        pos = 0
        for match in self.pattern.search_iter (format_line) :
            s = match.start (0)
            if pos < s :
                print "«%s»" % format_line [pos:s]
                formatters.append \
                    ( lambda node, context, head = "",
                             result = (format_line [pos:s], )
                      : result
                    )
            formatters.append (self._recursive_formatter (match))
            pos = match.end (0)
    # end def _setup_formatters

    def _recursive_formatter (self, match) :
        key  = match.group ("key")
        form = match.group ("form")
        return _Recursive_Formatter_ (key, "%%%s" % (form, ))
    # end def _recursive_formatter

# end class Multi_Line_Formatter

class _Recursive_Formatter_ (TFL.Meta.Object) :

    def __init__ (self, key, format) :
        self.key    = key
        self.format = format
    # end def __init__

    def __call__ (self, node, context, head = "") :
        self.node    = node
        self.context = context
        self.head    = head
        return self
    # end def __call__

    def __iter__ (self) :
        context  = self.context
        format   = self.format
        recurser = context.recurser
        rkw      = context.recurse_args
        for x in getattr (self.node, self.key) :
            for y in getattr (x, recurser) (** rkw) :
                yield format % y
    # end def __iter__

# end class _Recursive_Formatter_

def Formatter (level, format_line) :
    if Multi_Line_Formatter.pattern.search (format_line) :
        formatter = Multi_Line_Formatter
    else :
        formatter = Single_Line_Formatter
    return formatter (level, format_line)
# end def Formatter

if __name__ != "__main__" :
    TFL.SDG._Export ("Formatter")
### __END__ Formatter
