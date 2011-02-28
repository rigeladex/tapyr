# -*- coding: iso-8859-1 -*-
# Copyright (C) 2011 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package TFL.
#
# This module is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public License
# along with this module; if not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    TFL.Formatter
#
# Purpose
#    Provide callable to convert python data structures to a nicely formatted
#    string (similar to pprint, but using much less indentation and leading
#    instead of trailing separators)
#
# Revision Dates
#    24-Feb-2011 (CT) Creation
#    25-Feb-2011 (CT) `Look_Ahead_Gen` used to compact output for
#                     single-element structures
#    28-Feb-2011 (CT) More output compaction (`nl_r`)
#    28-Feb-2011 (CT) `_repr` added and used to remove leading `u` from strings
#    ««revision-date»»···
#--

from   _TFL import TFL

import _TFL._Meta.Object
import _TFL.Decorator
import _TFL.Generators

from   itertools import chain as ichain

class Formatter (TFL.Meta.Object) :
    """Provide callable to convert python data structures to a nicely formatted
       string.

    >>> thing = ["abc", "dfg", {1: "abc", 2: "xyz", 0: (42, 137)}]
    >>> print formatted (thing)
    [ 'abc'
    , 'dfg'
    , { 0 :
          ( 42
          , 137
          )
      , 1 : 'abc'
      , 2 : 'xyz'
      }
    ]
    >>> thing.append (thing)
    >>> print formatted (thing)
    [ 'abc'
    , 'dfg'
    , { 0 :
          ( 42
          , 137
          )
      , 1 : 'abc'
      , 2 : 'xyz'
      }
    , <Recursion on list...>
    ]
    """

    def __init__ (self, indent = 2, width = 80) :
        self.indent = indent
        self.width  = width
    # end def __init__

    def __call__ (self, thing, level = 0, seen = None, leader = "") :
        return "\n".join (self.format_iter (thing, level, seen, leader))
    # end def __call__

    def format_iter (self, thing, level = 0, seen = None, leader = "", nl_r = False) :
        if seen is None :
            seen = set ()
        tid  = id (thing)
        wd   = self.width
        ws   = " " * self.indent * level
        f, a = self.formatter (thing)
        recurses = getattr (f, "recurses", False)
        if recurses and tid in seen :
            yield "%s<Recursion on %s...>" % (leader, thing.__class__.__name__)
        else :
            seen.add (tid)
            if recurses and nl_r and leader :
                yield leader.rstrip ()
                leader = ""
            for l in f (thing, level, seen, ws, leader, * a) :
                yield l [:wd]
    # end def format_iter

    def formatter (self, thing) :
        a = ()
        if isinstance (thing, dict) :
            f = self._format_dict
        elif isinstance (thing, list) :
            f = self._format_list
            a = "[", "]"
        elif isinstance (thing, tuple) :
            f = self._format_list
            a = "(", ")"
        else :
            f = self._format_obj
        return f, a
    # end def formatter

    @TFL.Attributed (recurses = True)
    def _format_dict (self, thing, level, seen, ws, leader) :
        sep = "{"
        if thing :
            head = leader or ws
            tail = "}" if len (thing) == 1 else ""
            for k, v in sorted (thing.iteritems ()) :
                rk = self._repr (k)
                vl = "%s%s %s : " % (head, sep, rk)
                v2 = "%s%s %s : " % (ws,   sep, rk)
                it = TFL.Look_Ahead_Gen \
                    (self.format_iter (v, level + 2, seen, vl, True))
                for l in it :
                    if tail and it.is_finished :
                        yield "%s%s %s" % (ws, l.lstrip (), tail)
                        return
                    yield l
                    tail = ""
                    vl   = v2
                head = ws
                sep  = ","
            yield "%s}" % (ws, )
        else :
            yield "%s{}" % (leader or ws, )
    # end def _format_dict

    @TFL.Attributed (recurses = True)
    def _format_list (self, thing, level, seen, ws, leader, open, clos) :
        sep = open
        if thing :
            head = leader
            tail = clos if len (thing) == 1 else ""
            for v in thing :
                vl = "%s%s " % (ws, sep)
                it = TFL.Look_Ahead_Gen \
                    (self.format_iter (v, level + 1, seen, vl))
                for l in it :
                    if tail and it.is_finished :
                        yield "%s%s %s" % (head, l.lstrip (), tail)
                        return
                    elif head :
                        yield head.rstrip ()
                        head = ""
                    tail = ""
                    yield l
                sep = ","
            yield "%s%s" % (ws, clos)
        else :
            yield "%s%s%s" % (leader or ws, open, clos)
    # end def _format_list

    def _format_obj (self, thing, level, seen, ws, leader) :
        yield "%s%s" % (leader, self._repr (thing))
    # end def _format_obj

    def _repr (self, thing) :
        result = "%r" % (thing, )
        if result.startswith (("u'", 'u"')) :
            result = result [1:]
        return result
    # end def _repr


# end class Formatter

formatted = Formatter ()

if __name__ != "__main__" :
    TFL._Export ("Formatter", "formatted")
### __END__ TFL.Formatter
