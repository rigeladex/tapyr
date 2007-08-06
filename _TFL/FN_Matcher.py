# -*- coding: iso-8859-1 -*-
# Copyright (C) 2002-2005 Mag. Christian Tanzer. All rights reserved
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
#    FN_Matcher
#
# Purpose
#    Provides classes to find matching filenames
#
# Revision Dates
#    30-Oct-2002 (CT) Creation
#     6-Mar-2003 (CT) Inherit from `TFL.Meta.Object`
#     6-Mar-2003 (CT) `FN_Matcher_Grep` added
#    10-Apr-2003 (CT) `FN_Matcher_Grep` changed to pass `re.M` to
#                     `re.compile`
#    12-Aug-2003 (CT) Import for `StringIO` added
#    12-Aug-2003 (CT) `Alias_Property` replaced by explicit function
#                     delegation to avoid doctest hiccups
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ««revision-date»»···
#--



from   _TFL import TFL
import _TFL._Meta.Object

import fnmatch
import re

from   StringIO import StringIO

class FN_Matcher (TFL.Meta.Object) :
    """Filename matcher for regular expressions.

       >>> names = ["%s.%s" % (a,b) for a in ("a","b","c","d","e") \
                                    for b in ("x","y","z")]
       >>> FN_Matcher (re.compile ("[a-c]\.[^x]")) (names)
       ['a.y', 'a.z', 'b.y', 'b.z', 'c.y', 'c.z']
    """

    def __init__ (self, pattern) :
        self.pattern = pattern
    # end def __init__

    def __call__ (self, file_names) :
        return filter (self.matches, file_names)
    # end def __call__

    def matches (self, file_name) :
        return self.pattern.search (file_name)
    # end def matches

    ### Alias_Property trips doctest
    ### TypeError: Tester.run__test__: values in dict must be strings, functions or classes; <_TFL._Meta.Property.Alias_Property object at 0x819f28c>
    #    search = TFL.Meta.Alias_Property ("matches")
    def search (self, * args, ** kw) :
        return self.matches (* args, ** kw)
    # end def search

    def _Matcher (self, pattern) :
        if isinstance (pattern, FN_Matcher) :
            return pattern
        elif isinstance (pattern, (str, unicode)) :
            return FN_Matcher_Glob (pattern)
        else :
            return FN_Matcher (pattern)
    # end def _Matcher

# end class FN_Matcher

class FN_Matcher_Glob (FN_Matcher) :
    """Filename matcher for glob-style matches.

       >>> names = ["%s.%s" % (a,b) for a in ("a","b","c","d","e") \
                                    for b in ("x","y","z")]
       >>> qnames = ["/u/v/w/%s.%s" % (a,b) for a in ("a","b","c","d","e") \
                                            for b in ("x","y","z")]
       >>> FN_Matcher_Glob ("*.a") (names)
       []
       >>> FN_Matcher_Glob ("*.x") (names)
       ['a.x', 'b.x', 'c.x', 'd.x', 'e.x']
       >>> FN_Matcher_Glob ("a.*") (names)
       ['a.x', 'a.y', 'a.z']
       >>> FN_Matcher_Glob ("*") (names) == names
       1
       >>> FN_Matcher_Glob ("") (names) == names
       1
       >>> FN_Matcher_Glob ("*/v/*") (qnames) == qnames
       1
       >>> FN_Matcher_Glob ("*/v/*.x") (qnames)
       ['/u/v/w/a.x', '/u/v/w/b.x', '/u/v/w/c.x', '/u/v/w/d.x', '/u/v/w/e.x']
    """

    def __init__ (self, pattern) :
        self.__super.__init__ (re.compile (fnmatch.translate (pattern)))
    # end def __init__

# end class FN_Matcher_Glob

class FN_Matchers (FN_Matcher) :
    """Filename matcher for multiple patterns.

       >>> names = ["%s.%s" % (a,b) for a in ("a","b","c","d","e") \
                                    for b in ("x","y","z")]
       >>> qnames = ["/u/v/w/%s.%s" % (a,b) for a in ("a","b","c","d","e") \
                                            for b in ("x","y","z")]
       >>> FN_Matchers ("*.x", "a.*") (names)
       ['a.x', 'a.y', 'a.z', 'b.x', 'c.x', 'd.x', 'e.x']
       >>> FN_Matchers  ("*.a") (names)
       []
       >>> FN_Matchers ("*.x") (names)
       ['a.x', 'b.x', 'c.x', 'd.x', 'e.x']
       >>> FN_Matchers ("a.*") (names)
       ['a.x', 'a.y', 'a.z']
       >>> FN_Matchers (re.compile ("[a-c]\.[^x]"))  (names)
       ['a.y', 'a.z', 'b.y', 'b.z', 'c.y', 'c.z']
       >>> FN_Matchers (re.compile ("[a-c]\.[^x]"), "b.x")  (names)
       ['a.y', 'a.z', 'b.x', 'b.y', 'b.z', 'c.y', 'c.z']
    """

    def __init__ (self, * patterns) :
        self.patterns = []
        add = self.patterns.append
        for p in patterns :
            add (self._Matcher (p))
    # end def __init__

    def matches (self, file_name) :
        for p in self.patterns :
            m = p.search (file_name)
            if m :
                return m
    # end def matches

# end class FN_Matchers

class FN_Matcher_Grep (FN_Matcher) :
    """Filename matcher returning all files containing a match to a grep
       pattern.

       >>> names = ["abcd.x", "abcd.y", "cdef.x", "cdef.y", "rstu.x", "rstu.y"]
       >>> FN_Matcher_Grep ("cd", "*.x", _open = StringIO) (names)
       ['abcd.x', 'cdef.x']
       >>> FN_Matcher_Grep ("cd", "*.y", _open = StringIO) (names)
       ['abcd.y', 'cdef.y']
       >>> FN_Matcher_Grep ("cd", "*", _open = StringIO) (names)
       ['abcd.x', 'abcd.y', 'cdef.x', 'cdef.y']
       >>> FN_Matcher_Grep ("u", "*", _open = StringIO) (names)
       ['rstu.x', 'rstu.y']
       >>> FN_Matcher_Grep ("cd", "*.x", predicate = lambda x : not x, _open = StringIO) (names)
       ['rstu.x']
    """

    def __init__ (self, grep_pattern, name_pattern, predicate = lambda x : x, _open = open) :
        if isinstance (grep_pattern, (str, unicode)) :
            grep_pattern  = re.compile (grep_pattern, re.M)
        self.grep_pattern = grep_pattern
        self.pattern      = self._Matcher (name_pattern)
        self.predicate    = predicate
        self._open        = _open ### just for unit testing
    # end def __init__

    def matches (self, file_name) :
        if self.pattern.matches (file_name) :
            try :
                file = self._open (file_name)
            except IOError, exc :
                pass
            else :
                try :
                    result = self.grep_pattern.search (file.read ())
                    return self.predicate (result)
                finally :
                    try :
                        file.close
                    except AttributeError :
                        pass
                    else :
                        file.close ()
    # end def matches

# end class FN_Matcher_Grep

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.FN_Matcher
