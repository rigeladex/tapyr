# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.CSS.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    GTW.CSS.Rule
#
# Purpose
#    Model CSS rules
#
# Revision Dates
#    29-Dec-2010 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division
from   __future__  import print_function, unicode_literals

from   _GTW                       import GTW
from   _TFL                       import TFL

import _GTW.CSS

import _TFL._Meta.Object

from   _TFL._Meta.Once_Property   import Once_Property
from   _TFL.predicate             import cartesian

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
Ra = Rule_Attr
Rc = Rule_Class
Rd = Rule_Child
Rp = Rule_Pseudo
Rs = Rule_Sibling

__all__ = tuple \
    (k for (k, v) in globals ().iteritems () if isinstance (v, Rule))

if __name__ != "__main__" :
    GTW.CSS._Export (* __all__)
### __END__ GTW.CSS.Rule
