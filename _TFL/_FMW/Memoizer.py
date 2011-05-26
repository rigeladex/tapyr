# -*- coding: iso-8859-15 -*-
# Copyright (C) 2005 Mag. Christian Tanzer. All rights reserved
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
#    Memoizer
#
# Purpose
#    Add memoization to functions and methods without changing the
#    source code of the memoized components
#
# Revision Dates
#     5-Jun-2005 (CT) Creation
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ««revision-date»»···
#--



"""
Add memoization to functions and methods of modules/classing without
changing the source code of the memoized components.

Caveats:
- the functions/methods memoized must be idempotent
- all arguments passed to the function/methods must be hashable
- keyword arguments cannot be used

>>> class Test :
...     def method (self, i) :
...         print "Test.method called with", i,
...         return i * i
...
>>> Memoizer.add_method (Test, "method")
>>> t = Test ()
>>> for j in range (5) :
...     print "First  call", j, t.method (j)
...     print "Second call", j, t.method (j)
...
First  call 0 Test.method called with 0 0
Second call 0 0
First  call 1 Test.method called with 1 1
Second call 1 1
First  call 2 Test.method called with 2 4
Second call 2 4
First  call 3 Test.method called with 3 9
Second call 3 9
First  call 4 Test.method called with 4 16
Second call 4 16

"""

from   _TFL                   import TFL
import _TFL._FMW.Wrapper

class _Memoized_ (TFL.FMW.Wrapped_FM) :
    """Wrapper adding memoization to a single function or method"""

    __undef = object ()

    def __init__ (self, * args, ** kw) :
        self._cache = {}
        self.__super.__init__ (* args, ** kw)
    # end def __init__

    def __call__ (self, * args) :
        _cache = self._cache
        _undef = self.__undef
        result = _cache.get (args, _undef)
        if result is _undef :
            result = _cache [args] = self.fct (* args)
        return result
    # end def __call__

# end class _Memoized_

class _Memoizer_ (TFL.FMW.Wrapper) :
    """Add memoization to functions and methods without changing the
       source code of the memoized components.
    """

    Wrapped_FM = _Memoized_

# end class _Memoizer_

Memoizer = _Memoizer_ ()

if __name__ != "__main__" :
    TFL.FMW._Export ("Memoizer")
### __END__ Memoizer
