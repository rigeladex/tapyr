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
#    26-Jul-2004 (CT) Creation continued
#    ««revision-date»»···
#--

from   _TFL               import TFL
import _TFL._Meta.Object
import _TFL._SDG

from   Regexp             import *

class _Formatter_ (TFL.Meta.Object) :
    """Root class of SDG formatters"""

    def __init__ (self, indent_level, format_line) :
        self.indent_level = indent_level
        self.format_line  = format_line
    # end def __init__

    def __repr__ (self) :
        return "%s %s> '%1.20s'" % \
               (self.kind, self.indent_level, self.format_line)
    # end def __repr__

# end class _Formatter_

class Single_Line_Formatter (_Formatter_) :
    """Formatter generating a single line of output"""

    kind = "SLF"

    def __call__ (self, node, context) :
        return (self.format_line % context, )
    # end def __call__

# end class Single_Line_Formatter

class Multi_Line_Formatter (_Formatter_) :
    """Formatter generating a multiple lines of output"""

    kind    = "MLF"

    pattern = Regexp \
        ( r"""%"""
          r"""\( : (?P<sep> [^:]*) : (?P<key> [^:]+) : \)"""
          r"""(?P<form> """
              r"""(?P<flags>  [-+ #0]*)"""
              r"""(?P<mfw>    [0-9]*)"""
              r"""(?P<prec> \.[0-9]+)?"""
              r"""(?P<type>   [diouxXeEfFgGcrs])"""
          r""")"""
        , re.VERBOSE
        )

    def __init__ (self, indent_level, format_line) :
        self.__super.__init__ (indent_level, format_line)
        self._setup_formatters (format_line)
    # end def __init__

    def __call__ (self, node, context) :
        last = ""
        for f in self.formatters :
            g     = iter (f (node, context))
            first = self._first (g)
            last  = "%s%s" % (last, first)
            for l in g :
                yield last % context
                last = l
        if last :
            yield last % context
    # end def __call__

    def _first (self, generator) :
        try :
            return generator.next ()
        except StopIteration :
            ### return an empty string so that preceding part of line
            ### (`last`) doesn't get lost in `__call__`
            return ""
    # end def _first

    def _setup_formatters (self, format_line) :
        self.formatters = formatters = []
        pos = 0
        for match in self.pattern.search_iter (format_line) :
            s = match.start (0)
            if pos < s :
                formatters.append \
                    ( lambda node, context, result = (format_line [pos:s], )
                      : result
                    )
            formatters.append (self._recursive_formatter (match))
            pos = match.end (0)
        if pos < len (format_line) :
            formatters.append \
                ( lambda node, context, result = (format_line [pos:], )
                  : result
                )
    # end def _setup_formatters

    def _recursive_formatter (self, match) :
        sep        = match.group ("sep")
        keys       = match.group ("key").split (",")
        form       = match.group ("form")
        formatters = []
        for key in keys :
            key = key.strip ()
            if key [0] == "*" :
                rf = _Recursive_Formatter_Attr_
            elif key [0] == "@" :
                rf = _Recursive_Formatter_Method_
            else :
                raise ValueError, match.group (0)
            formatters.append (rf (key [1:], "%%%s" % (form, )))
        return _Recursive_Formatters_ (sep, * formatters)
    # end def _recursive_formatter

# end class Multi_Line_Formatter

class _Recursive_Formatter_ (TFL.Meta.Object) :

    def __init__ (self, key, format) :
        self.key    = key
        self.format = format
    # end def __init__

    def __call__ (self, node, context, sep) :
        self.node    = node
        self.context = context
        self.sep     = sep
        return self
    # end def __call__

# end class _Recursive_Formatter_

class _Recursive_Formatters_ (TFL.Meta.Object) :

    def __init__ (self, sep, * formatters) :
        self.sep        = sep
        self.formatters = formatters
    # end def __init__

    def __call__ (self, node, context) :
        self.node    = node
        self.context = context
        return self
    # end def __call__

    def __iter__ (self) :
        node     = self.node
        context  = self.context
        sep      = ""
        i        = 0
        for f in self.formatters :
            for r in f (node, context, sep = self.sep) :
                yield "%s%s" % (sep, r)
                sep = ""
                i  += 1
            if i :
                sep = self.sep
    # end def __iter__

# end class _Recursive_Formatters_

class _Recursive_Formatter_Attr_ (_Recursive_Formatter_) :

    def __iter__ (self) :
        context  = self.context
        format   = self.format
        recurser = context.recurser
        rkw      = context.recurse_args
        sep      = ""
        for x in getattr (self.node, self.key) :
            for y in getattr (x, recurser) (** rkw) :
                yield sep + (format % y)
                sep = ""
            sep = self.sep
    # end def __iter__

# end class _Recursive_Formatter_Attr_

class _Recursive_Formatter_Method_ (_Recursive_Formatter_) :

    def __iter__ (self) :
        context  = self.context
        format   = self.format
        rkw      = context.recurse_args
        sep      = ""
        for x in getattr (self.node, self.key) (** rkw) :
            yield sep + (format % x)
            sep = self.sep
    # end def __iter__

# end class _Recursive_Formatter_Method_

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
