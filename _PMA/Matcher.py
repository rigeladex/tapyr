# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 Mag. Christian Tanzer. All rights reserved
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
#    PMA.Matcher
#
# Purpose
#    Match PMA.Messages with predicate
#
# Revision Dates
#    28-Dec-2005 (CT) Creation
#    29-Dec-2005 (CT) doctest extended
#    ««revision-date»»···
#--

from   _TFL                    import TFL
from   _PMA                    import PMA

import _TFL._Meta.Object

class Matcher (TFL.Meta.Object) :
    """Match PMA.Messages with predicate

       >>> from _PMA.Matcher import *
       >>> import _TFL.Caller
       >>> import _TFL.Regexp
       >>>
       >>> class Tester (TFL.Meta.Object) :
       ...     def __init__ (self, ** kw) :
       ...         self.kw = dict (kw)
       ...         self.scope = TFL.Caller.Scope (globs = kw)
       ...     def __repr__ (self) :
       ...         items = [str (v) for (k, v) in sorted (self.kw.items ())]
       ...         return "(%s)" % (", ".join (items,))
       ...
       >>> t1 = Tester (sender = "foo", receiver = "bar", spam_score = 0.00)
       >>> t2 = Tester (sender = "foo", receiver = "baz", spam_score = 0.10)
       >>> t3 = Tester (sender = "bar", receiver = "baz", spam_score = 0.25)
       >>> t4 = Tester (sender = "bar", receiver = "foo", spam_score = 0.25)
       >>> t5 = Tester (sender = "baz", receiver = "foo", spam_score = 0.90)
       >>> t6 = Tester (sender = "baz", receiver = "bar", spam_score = 0.99)
       >>> ts = t1, t2, t3, t4, t5, t6
       >>> m1 = Matcher ("sender == 'foo'")
       >>> m2 = Matcher ("spam_score > 0.8")
       >>> m3 = Matcher ("pat.search (receiver)", pat = TFL.Regexp ("^ba"))
       >>> [m1.match (t) for t in ts]
       [True, True, False, False, False, False]
       >>> [m2.match (t) for t in ts]
       [False, False, False, False, True, True]
       >>> [m3.match (t) for t in ts]
       [True, True, True, False, False, True]
       >>> list (m1.filter (* ts))
       [(bar, foo, 0.0), (baz, foo, 0.1)]
       >>> list (m2.filter (* ts))
       [(foo, baz, 0.9), (bar, baz, 0.99)]
       >>> list (m3.filter (* ts))
       [(bar, foo, 0.0), (baz, foo, 0.1), (baz, bar, 0.25), (bar, baz, 0.99)]
       >>> ma = m1 + m2 + m3
       >>> [ma.match (t) for t in ts]
       [False, False, False, False, False, False]
       >>> len (ma.matchers)
       3
       >>> [m.__class__.__name__ for m in ma.matchers]
       ['Matcher', 'Matcher', 'Matcher']
       >>> mo = m1 * m2 * m3
       >>> [mo.match (t) for t in ts]
       [True, True, True, False, True, True]
       >>> [m.__class__.__name__ for m in mo.matchers]
       ['Matcher', 'Matcher', 'Matcher']
       >>> len (mo.matchers)
       3
       >>> mn = ~ m1
       >>> [mn.match (t) for t in ts]
       [False, False, True, True, True, True]
       >>> man = mn + m2 + m3
       >>> [man.match (t) for t in ts]
       [False, False, False, False, False, True]

    """

    def __init__ (self, condition, ** ckw) :
        self.condition = condition
        self.ckw       = ckw
        self._code     = compile (condition.strip (), condition, "eval")
    # end def __init__

    def filter (self, * msg) :
        for m in msg :
            if self.match (m) :
                yield m
    # end def filter

    def match (self, msg) :
        return bool (msg.scope.eval (self._code, self.ckw))
    # end def match

    def split (self, * msg) :
        result = [], []
        for m in msg :
            result [self.match (m)].append (m)
        return result [1], result [0]
    # end def split

    def __add__ (self, rhs) :
        return And_Matcher (self, rhs)
    # end def __add__

    def __invert__ (self) :
        return Not_Matcher (self)
    # end def __invert__

    def __mul__ (self, rhs) :
        return Or_Matcher (self, rhs)
    # end def __mul__

# end class Matcher

class And_Matcher (Matcher) :
    """And-combination of Matcher instances"""

    def __init__ (self, * matchers) :
        if matchers [0].__class__ is self.__class__ :
            matchers = matchers [0].matchers + matchers [1:]
        self.matchers = matchers
    # end def __init__

    def match (self, msg) :
        for m in self.matchers :
            if not m.match (msg) :
                return False
        return True
    # end def match

# end class And_Matcher

class Not_Matcher (Matcher) :
    """Invert condition of Matcher instance"""

    def __init__ (self, matcher) :
        self.matcher = matcher
    # end def __init__

    def match (self, msg) :
        return not self.matcher.match (msg)
    # end def match

# end class Not_Matcher

class Or_Matcher (And_Matcher) :
    """Or-combination of Matcher instances"""

    def match (self, msg) :
        for m in self.matchers :
            if m.match (msg) :
                return True
        return False
    # end def match

# end class Or_Matcher

if __name__ != "__main__" :
    PMA._Export ("*")
### __END__ PMA.Matcher
