# -*- coding: utf-8 -*-
# Copyright (C) 2011-2013 Mag. Christian Tanzer All rights reserved
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
#    25-Oct-2011 (CT) `_repr` changed to chop off trailing the `L` from longs
#    18-Nov-2011 (CT) Add optional argument `sep`
#    18-Nov-2011 (CT) Add formatting of `TFL.Record`
#    12-Jun-2012 (CT) Don't show `Recursion` on empty `things`
#    ««revision-date»»···
#--

from   __future__       import print_function

from   _TFL             import TFL
from   _TFL.pyk         import pyk

import _TFL._Meta.Object
import _TFL.Decorator
import _TFL.Generators
import _TFL.Record

from   itertools        import chain as ichain

try :
    long
except NameError :
    class long (int) :
        """Just for backwards compatibility with Python 2"""

class Formatter (TFL.Meta.Object) :
    """Provide callable to convert python data structures to a nicely formatted
       string.

    >>> thing = ["abc", "dfg", {1: "abc", 2: "xyz", 0: (42, 137)}]
    >>> thinl = ["abc", "dfg", {1: "abc", 2: "xyz", 0: (42, long (137))}]
    >>> print (formatted (thing))
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
    >>> print (formatted_1 (thing))
    ['abc', 'dfg', {0 : (42, 137), 1 : 'abc', 2 : 'xyz'}]

    >>> print (formatted (thinl))
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
    >>> print (formatted_1 (thinl))
    ['abc', 'dfg', {0 : (42, 137), 1 : 'abc', 2 : 'xyz'}]

    >>> thing.append (thing)
    >>> print (formatted (thing))
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
    >>> print (formatted_1 (thing))
    ['abc', 'dfg', {0 : (42, 137), 1 : 'abc', 2 : 'xyz'}, <Recursion on list...>]

    >>> thinr = TFL.Record (foo = 42, bar = u"wrzl", baz = "MadamImadam")
    >>> print (formatted (thinr))
    Record
    ( bar = 'wrzl'
    , baz = 'MadamImadam'
    , foo = 42
    )
    >>> print (formatted_1 (thinr))
    Record (bar = 'wrzl', baz = 'MadamImadam', foo = 42)

    >>> thinq = ["abc", "dfg", { 1 : "yxz" }, thinr]
    >>> print (formatted (thinq))
    [ 'abc'
    , 'dfg'
    , { 1 : 'yxz' }
    , Record
      ( bar = 'wrzl'
      , baz = 'MadamImadam'
      , foo = 42
      )
    ]
    >>> print (formatted_1 (thinq))
    ['abc', 'dfg', {1 : 'yxz'}, Record (bar = 'wrzl', baz = 'MadamImadam', foo = 42)]

    """

    def __init__ (self, indent = 2, width = 80, sep = "\n") :
        self.indent = indent
        self.width  = width
        self.sep    = sep
    # end def __init__

    def __call__ (self, thing, level = 0, seen = None, leader = "") :
        return self.sep.join (self.format_iter (thing, level, seen, leader))
    # end def __call__

    def format_iter (self, thing, level = 0, seen = None, leader = "", nl_r = False) :
        if seen is None :
            seen = set ()
        tid      = id (thing)
        wd       = self.width
        ws       = " " * self.indent * level
        f, a     = self.formatter (thing)
        recurses = getattr (f, "recurses", False)
        if recurses and thing and tid in seen :
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
        elif isinstance (thing, TFL.Record) :
            f = self._format_record
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
            for k, v in sorted (pyk.iteritems (thing)) :
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
            if len (thing) == 1 :
                tail = clos if clos != ")" else ",)"
            else :
                tail = ""
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
                    yield l
                    tail = ""
                sep = ","
            yield "%s%s" % (ws, clos)
        else :
            yield "%s%s%s" % (leader or ws, open, clos)
    # end def _format_list

    def _format_obj (self, thing, level, seen, ws, leader) :
        yield "%s%s" % (leader, self._repr (thing))
    # end def _format_obj

    def _format_record (self, thing, level, seen, ws, leader) :
        kw = thing._kw
        if len (kw) == 1 :
           for k, v in sorted (pyk.iteritems (kw)) :
                yield "%sRecord (%s = %s)" % \
                    (leader or ws, k, formatted_1 (v))
                break
        elif kw :
            head = "%sRecord%s%s" % (leader, self.sep, ws)
            sep  = "("
            for k, v in sorted (pyk.iteritems (kw)) :
                rk = str (k)
                vl = "%s%s %s = " % (head, sep, rk)
                for l in self.format_iter (v, level + 2, seen, vl, True) :
                    yield l
                head = ws
                sep  = ","
            yield "%s)" % (ws, )
        else :
            yield "%sRecord ()" % (leader or ws, )
    # end def _format_record

    def _repr (self, thing) :
        result = "%r" % (thing, )
        if result.startswith (("u'", 'u"')) :
            result = result [1:]
        if isinstance (thing, long) and result.endswith ("L") :
            result = result [:-1]
        return result
    # end def _repr

# end class Formatter

formatted = Formatter ()

_formatted_1 = Formatter (indent = 0, width = 2 << 10, sep = " ")

def formatted_1 (* args, ** kw) :
    result = \
        ( _formatted_1 (* args, ** kw)
            .replace (" ,", ",")
            .replace ("( ", "(")
            .replace ("[ ", "[")
            .replace ("{ ", "{")
            .replace (" )", ")")
            .replace (" ]", "]")
            .replace (" }", "}")
        )
    return result
# end def formatted_1

if __name__ != "__main__" :
    TFL._Export ("Formatter", "formatted", "formatted_1")
### __END__ TFL.Formatter
