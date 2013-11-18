# -*- coding: utf-8 -*-
# Copyright (C) 2009-2012 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
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
#    DJO.CSS
#
# Purpose
#    Model CSS rules and style files
#
# Revision Dates
#    31-Aug-2009 (CT) Creation
#     7-Sep-2009 (CT) `Rule_Attr` and `Rule_Class` added
#     7-Sep-2009 (CT) `Rule.level` changed to subtract
#                     `(not parent.declarations)`
#     7-Sep-2009 (CT) `Rule.__iter__` changed to not yield `self` if there
#                     aren't `self.declarations`
#    11-Sep-2009 (CT) `Parameters`, `Parameter_Scope` and `Style_Sheet.Read`
#                     added
#    29-Mar-2012 (CT) Rename `CSS_Parameters` to `Media_Parameters`
#    ««revision-date»»···
#--

from   __future__                 import with_statement

from   _TFL                       import TFL
from   _DJO                       import DJO

import _TFL._Meta.Object
import _TFL.Caller

from   _TFL._Meta.Once_Property   import Once_Property
from   _TFL.predicate             import cartesian

def Parameters (* bases, ** kw) :
    """Model parameters for CSS rules and stylesheets, defined by `kw` and
       inherited from `bases`.
    """
    return type ("Media_Parameters", bases, kw)
# end def Parameters

class Parameter_Scope (TFL.Caller.Object_Scope_Mutable) :
    """Encapsulate a CSS parameters class so that it is usable as context for
       `exec` of a file containing CSS.Style_Sheet declarations.
    """

    def __init__ (self, parameters) :
        self.__super.__init__ (object = parameters, locls = {})
        self.style_sheets = []
    # end def __init__

    def __setitem__ (self, key, value) :
        self.__super.__setitem__ (key, value)
        if isinstance (value, Style_Sheet) :
            self.style_sheets.append (value)
    # end def __setitem__

# end class Parameter_Scope

class Rule (TFL.Meta.Object) :
    """Model a CSS rule.

       >>> import itertools
       >>> tr = Rp ("target", background_color = "yellow", color = "red")
       >>> r1 = R ("tr.row1", "div.row1", color = "grey", clear = "both", children = [tr])
       >>> r2 = R ("tr.row2", "div.row2", color = "blue", clear = "both", children = [tr])
       >>> for x in itertools.chain (r1, r2) :
       ...   print x
       ...
       tr.row1, div.row1
         { clear : both
         ; color : grey
         }
         tr.row1:target, div.row1:target
           { background-color : yellow
           ; color            : red
           }
       tr.row2, div.row2
         { clear : both
         ; color : blue
         }
         tr.row2:target, div.row2:target
           { background-color : yellow
           ; color            : red
           }

    """

    parent_sep = " "

    def __init__ (self, * selectors, ** declarations) :
        self.children      = list (self._pop_children (declarations))
        self.parent = p    = declarations.pop ("parent",     None)
        self.parent_sep    = declarations.pop ("parent_sep", self.parent_sep)
        self._selectors    = selectors
        self.declarations  = declarations
        if p is not None :
            p.children.append (self)
    # end def __init__

    def copy (self) :
        d = dict \
            ( self.declarations
            , children   = self.children
            , parent_sep = self.parent_sep
            )
        return self.__class__ (* self._selectors, ** d)
    # end def copy

    @property
    def level (self) :
        parent = self.parent
        if parent is not None :
            return parent.level - (not parent.declarations) + 1
        return 0
    # end def level

    @Once_Property
    def selectors (self) :
        parent = self.parent
        if parent is not None :
            parent_sep = self.parent_sep
            return \
                [   parent_sep.join (s)
                for s in cartesian (parent.selectors, self._selectors)
                ]
        return self._selectors
    # end def selectors

    def _formatted_decl (self, declarations, sep) :
        pvs    = sorted \
            ((p.replace ("_", "-"), v) for (p, v) in declarations.iteritems ())
        format = "%%s %%-%ds : %%s" % max (len (p) for p in declarations)
        yield format % (("{", ) + pvs [0])
        for p, v in pvs [1:] :
            yield format % (";", p, v)
        yield "}"
    # end def _formatted_decl

    def _pop_children (self, declarations) :
        for c in declarations.pop ("children", []) :
            if c.parent is not None :
                c = c.copy ()
            c.parent = self
            yield c
    # end def _pop_children

    def __iter__ (self) :
        if self.declarations :
            yield self
        for c in self.children :
            for r in c :
                yield r
    # end def __iter__

    def __str__ (self) :
        selectors    = self.selectors
        declarations = self.declarations
        level        = self.level
        indent0      = "  " * level
        indent1      = "  " * (level + 1)
        result       = ""
        if declarations :
            ls     = sum (len (s) for s in selectors) + 2 * (len(selectors) - 1)
            s_sep  = (",\n%s" % indent0) if (ls >= 80)               else ", "
            d_sep  = ("\n%s"  % indent1) if (len (declarations) > 1) else " "
            result = "%s%s%s%s" % \
                ( indent0
                , s_sep.join (selectors)
                , d_sep
                , d_sep.join (self._formatted_decl (declarations, d_sep))
                )
        return result
    # end def __str__

# end class Rule

class Rule_Attr (Rule) :
    """Rule for attribute selection"""

    parent_sep = ""

# end class Rule_Attr

class Rule_Child (Rule) :
    """Rule for a child of another element."""

    parent_sep = " > "

# end class Rule_Child

class Rule_Class (Rule) :
    """Rule for a class."""

    parent_sep = "."

# end class Rule_Class

class Rule_Pseudo (Rule) :
    """Rule for pseudo-classes"""

    parent_sep = ":"

# end class Rule_Pseudo

class Rule_Sibling (Rule) :
    """Rule for adjacent sibling element."""

    parent_sep = " + "

# end class Rule_Sibling

R  = Rule
Rc = Rule_Child
Rp = Rule_Pseudo
Rs = Rule_Sibling

class Style_Sheet (TFL.Meta.Object) :
    """Model a CSS style sheet"""

    _CSS_globs = {}

    def __init__ (self, * rules, ** attrs) :
        self.rules   = list (rules)
        self.imports = list (attrs.pop ("imports", []))
        self.media   = attrs.pop ("media", "all")
        self.name    = attrs.pop ("name",  None)
        self.attrs   = attrs
    # end def __init__

    def add_import (self, * imports) :
        self.imports.extend (imports)
    # end def add_import

    def add_rule (self, * rules) :
        self.rules.extend (rules)
    # end def add_rule

    @classmethod
    def Read (cls, file_name, parameters = None) :
        """Read style sheets definitions from `file_name`."""
        scope = Parameter_Scope (parameters)
        with open (file_name, "rt") as file :
            exec file in cls._get_CSS_globs (), scope
        return scope.style_sheets
    # end def Read

    @classmethod
    def _get_CSS_globs (cls) :
        result = cls._CSS_globs
        ignore = set (("Parameter_Scope", "Parameters"))
        if not result :
            from _TFL.Module import names_of
            from _DJO        import CSS
            for name in names_of (CSS) :
                if name not in ignore :
                    result [name] = getattr (CSS, name)
        return result
    # end def _get_CSS_globs

    def __iter__ (self) :
        for i in self.imports :
            for r in i :
                yield i
        for r in self.rules :
            for x in r :
                yield x
    # end def __iter__

    def __str__ (self) :
        return "\n\n".join (str (r) for r in self)
    # end def __str__

# end class Style_Sheet

S = Style_Sheet

if __name__ != "__main__" :
    DJO._Export_Module ()
### __END__ DJO.CSS
