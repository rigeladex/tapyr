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
#    27-Jul-2004 (CT) Creation continued...
#    28-Jul-2004 (CT) Creation continued....
#    30-Jul-2004 (CT) Use `TFL.Look_Ahead_Gen` instead of home-grown code
#     9-Aug-2004 (CT) `_Recursive_Formatter_Node_.__init__` changed to
#                     discard `None` values
#    11-Aug-2004 (MG) `sep_eol` added
#    12-Aug-2004 (CT) s/recurse_args/recurse_kw/g
#    12-Aug-2004 (CT) `rec_form` added
#    12-Aug-2004 (CT) `indent_anchor` added
#    12-Aug-2004 (CT) `Multi_Line_Formatter.__call__` changed to use
#                     `Look_Ahead_Gen`
#    12-Aug-2004 (MG)  Various `__str__` added (to improve debugging
#                      capabilities)
#    12-Aug-2004 (CT) Complex format specification added (`comp_prec` and
#                     `prec`)
#    ««revision-date»»···
#--

from   _TFL               import TFL
import _TFL._Meta.Object
import _TFL._SDG
import _TFL.Generators

from   Record             import Record
from   Regexp             import *

class _Formatter_ (TFL.Meta.Object) :
    """Root class of SDG formatters"""

    def __init__ (self, indent_level, format_line) :
        self.indent_level = indent_level
        self.format_line  = format_line
    # end def __init__

    def __repr__ (self) :
        return "%s %s> '%s'" % \
               (self.kind, self.indent_level, self.format_line)
    # end def __repr__

# end class _Formatter_

class _Recursive_Formatter_ (TFL.Meta.Object) :

    def __init__ (self, key, format, head_form, tail_form) :
        key, rec_form  = (key.split (".", 1) + [None]) [:2]
        self.key       = key
        self.rec_form  = rec_form
        self._format   = format
        self.head_form = head_form
        self.tail_form = tail_form
    # end def __init__

    def __call__ (self, node, context, sep_form) :
        self.node       = node
        self.context    = context
        self.recurse_kw = recurse_kw = context.recurse_kw.copy ()
        self.sep        = sep_form % context
        _format         = self._format
        if isinstance (_format, Record) :
            prec        = _format.prec % context
            _format     = "%%%s%s%s" % (_format.flags, prec, _format.type)
            recurse_kw  ["format_prec"] = float (prec)
        self.format     = \
            ( self.head_form % context
            + _format
            + self.tail_form % context
            )
        if self.rec_form :
            self.recurse_kw ["format_name"] = self.rec_form
        return self
    # end def __call__

# end class _Recursive_Formatter_

class _Recursive_Formatters_ (TFL.Meta.Object) :

    def __init__ (self, x_forms, * formatters) :
        self.x_forms    = x_forms
        self.formatters = formatters
    # end def __init__

    def __str__ (self) :
        return "RFS (%s)" % (", ".join ([str (f) for f in self.formatters]), )
    # end def __str__

    def __call__ (self, node, context) :
        self.node    = node
        self.context = context
        self.empty   = self.x_forms.empty   % context
        self.front   = self.x_forms.front   % context
        self.rear    = self.x_forms.rear    % context
        self.sep     = self.x_forms.sep     % context
        self.sep_eol = self.x_forms.sep_eol % context
        return self
    # end def __call__

    def __iter__ (self) :
        node       = self.node
        context    = self.context
        sep        = self.front
        eol        = self.sep_eol
        i          = 0
        formatters = TFL.Look_Ahead_Gen (self.formatters)
        for f in formatters :
            lines  = TFL.Look_Ahead_Gen \
                (f (node, context, sep_form = self.x_forms.sep))
            for r in lines :
                if formatters.is_finished and lines.is_finished :
                    yield "%s%s%s" % (sep, r, self.rear)
                else :
                    yield "%s%s%s"   % (sep, r, eol)
                sep = ""
                i  += 1
            if i :
                sep = self.sep
        if i == 0 and self.empty :
            yield self.empty
    # end def __iter__

# end class _Recursive_Formatters_

class _Recursive_Formatter_Attr_ (_Recursive_Formatter_) :

    def __str__ (self) :
        return "RF_Attr %s" % (self.key)
    # end def __str__

    def __iter__ (self) :
        attr = getattr (self.node, self.key, None)
        if attr is not None :
            format = self.format
            sep    = ""
            if isinstance (attr, str) :
                attr = (attr, )
            for x in attr :
                yield sep + (format % x)
                sep = self.sep
    # end def __iter__

# end class _Recursive_Formatter_Attr_

class _Recursive_Formatter_Method_ (_Recursive_Formatter_) :

    def __str__ (self) :
        return "RF_Meth %s" % (self.key)
    # end def __str__

    def __iter__ (self) :
        result = getattr (self.node, self.key) \
            (indent_offset = self.context.indent_anchor, ** self.recurse_kw)
        if result is not None :
            format = self.format
            sep    = ""
            for x in result :
                yield sep + (format % x)
                sep = self.sep
    # end def __iter__

# end class _Recursive_Formatter_Method_

class _Recursive_Formatter_Node_ (_Recursive_Formatter_) :

    def __str__ (self) :
        return "RF_Node %s" % (self.key)
    # end def __str__

    def __iter__ (self) :
        context  = self.context
        format   = self.format
        recurser = context.recurser
        ioffset  = context.indent_anchor
        rkw      = self.recurse_kw
        sep      = ""
        nodes    = getattr (self.node, self.key)
        if nodes is not None :
            if isinstance (nodes, TFL.SDG.Node) :
                nodes = (nodes, )
            for x in nodes :
                if x is not None :
                    meth = getattr (x, recurser)
                    for y in meth (indent_offset = ioffset, ** rkw) :
                        yield sep + (format % y)
                        sep = ""
                    sep = self.sep
    # end def __iter__

# end class _Recursive_Formatter_Node_

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
          r"""\( : (?P<x_forms> [^:]*) : (?P<key> [^:]+) : \)"""
          r"""(?P<form> """
              r"""(?P<flags>  [-+ #0]*)"""
              r"""(?:"""
                  r"""(?:"""
                      r"""(?P<mfw>    [0-9]*)"""
                      r"""(?P<prec> \.[0-9]+)?"""
                  r""")"""
                  r"""|"""
                  r"""(?:"""
                      r"""\{ (?P<comp_prec> [^\}]+) \}"""
                  r""")"""
              r""")?"""
              r"""(?P<type>   [diouxXeEfFgGcrs])"""
          r""")"""
        , re.VERBOSE
        )
    Formatters = \
        { "." : _Recursive_Formatter_Attr_
        , "@" : _Recursive_Formatter_Method_
        , "*" : _Recursive_Formatter_Node_
        }

    def __init__ (self, indent_level, format_line) :
        self.__super.__init__ (indent_level, format_line)
        self._setup_formatters (format_line)
    # end def __init__

    def __call__ (self, node, context) :
        last       = ""
        for f in self.formatters :
            lines = TFL.Look_Ahead_Gen (f (node, context))
            for l in lines :
                context.locals ["indent_anchor"] = \
                    len (last) + context.locals ["indent_anchor"]
                if not lines.is_finished :
                    yield "%s%s"  % (last, l % context)
                    last = ""
                else :
                    last = "%s%s" % (last, l % context)
        if last :
            yield last
    # end def __call__

    def _x_forms (self, x_forms) :
        result = Record \
            ( empty   = ""
            , front   = ""
            , head    = ""
            , rear    = ""
            , sep     = ""
            , sep_eol = ""
            , tail    = ""
            )
        if x_forms :
            for spec in x_forms.split ("¡") :
                key, form = spec.split ("=", 1)
                setattr (result, key, form)
        return result
    # end def _x_forms

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
        x_forms    = self._x_forms (match.group ("x_forms"))
        keys       = match.group ("key").split (",")
        comp_prec  = match.group ("comp_prec")
        if comp_prec :
            form   = Record \
                ( flags = match.group ("flags")
                , prec  = "%%(%s)s" % (comp_prec, )
                , type  = match.group ("type")
                )
        else :
            form   = "%%%s" % (match.group ("form"), )
        formatters = []
        for key in keys :
            key    = key.strip ()
            rf     = self.Formatters [key [0]]
            formatters.append \
                (rf (key [1:], form, x_forms.head, x_forms.tail))
        return _Recursive_Formatters_ (x_forms, * formatters)
    # end def _recursive_formatter

# end class Multi_Line_Formatter

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
