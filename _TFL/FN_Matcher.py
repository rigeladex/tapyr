#! /swing/bin/python
# Copyright (C) 2002 Mag. Christian Tanzer. All rights reserved
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
#    ««revision-date»»···
#--

import fnmatch
import re

class FN_Matcher :
    """Filename matcher for regular expressions.

       >>> names = ["%s.%s" % (a,b) for a in ("a","b","c","d","e") \
                                    for b in ("x","y","z")]
       >>> FN_Matcher (re.compile ("[a-c]\.[^x]"))  (names)
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

    search = matches
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
        FN_Matcher.__init__ (self, re.compile (fnmatch.translate (pattern)))
    # end def __init__

# end class FN_Matcher_Glob

class FN_Matchers (FN_Matcher) :
    """Filename matcher for multiple patterns.

       >>> names = ["%s.%s" % (a,b) for a in ("a","b","c","d","e") \
                                    for b in ("x","y","z")]
       >>> qnames = ["/u/v/w/%s.%s" % (a,b) for a in ("a","b","c","d","e") \
                                            for b in ("x","y","z")]
       >>> FN_Matchers ("*.x", "a.*")  (names)
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
        add           = self.patterns.append
        for p in patterns :
            if isinstance (p, FN_Matcher) :
                add (p)
            elif isinstance (p, str) :
                add (FN_Matcher_Glob (p))
            else :
                add (FN_Matcher (p))
    # end def __init__

    def matches (self, file_name) :
        for p in self.patterns :
            m = p.search (file_name)
            if m :
                return m
    # end def matches

    search = matches
# end class FN_Matchers

### unit-test code ############################################################

if __debug__ :
    import U_Test

    def _doc_test () :
        import FN_Matcher
        return U_Test.run_module_doc_tests (FN_Matcher)
    # end def _doc_test

    def _test () :
        _doc_test  ()
    # end def _test

    if __name__ == "__main__" :
        _test ()
# end if __debug__

### end unit-test code ########################################################

if __name__ != "__main__" :
    from _TFL import TFL
    TFL._Export ("*")
### __END__ FN_Matcher
