#! /usr/bin/python
# Copyright (C) 2001 Mag. Christian Tanzer. All rights reserved
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
#    Caller
#
# Purpose
#    Return information about the context of the caller's caller (e.g.,
#    globals, locals, ...)
#
#    Started with a posting by Fredrik Lundh <effbot@telia.com> to
#    comp.lang.python (see http://www.deja.com/=dnc/getdoc.xp?AN=586687655)
#
#    For a description of frame objects, see the Python Reference Manual,
#    section `The standard type hierarchy', entry `Frame objects' (for 1.5.2,
#    on page 16)
#
# Revision Dates
#     6-Mar-2000 (CT) Creation
#     5-Apr-2000 (CT) `caller_code' added
#    10-Aug-2000 (CT) `caller_info' added
#     2-Sep-2000 (CT) Simplified `caller_info' (try/except isn't necessary)
#    18-May-2001 (CT) Renamed from caller_globals to TFL/Caller.py
#    18-May-2001 (CT) `depth' added
#    16-Sep-2001 (CT) Protect `import U_Test`
#    18-Sep-2001 (CT) `globs` and `locls` arguments added to `Scope.__init__`
#     3-Nov-2001 (MG) import `TFL.Caller` instead of `Caller`
#    25-Feb-2002 (CT) `Caller.__getitem__` changed to allow nested format
#                     expressions (stolen from Skip Montanaro <skip@pobox.com>)
#    12-Mar-2002 (CT) `_Export_Module` added
#     1-Jun-2002 (CT) Try `sys._getframe` in `frame` instead of raising
#                     `AssertionError`
#    ««revision-date»»···
#--

import sys
import traceback

def frame (depth = 0) :
    """Return the execution frame of the caller's caller (for depth == 1, the
       frame of the caller's caller's caller is returned, and so on).
    """
    try:
        result = sys._getframe (2 + depth)
    except AttributeError :
        result = sys.exc_traceback.tb_frame.f_back.f_back
        try :
            for i in range (depth) :
                result = result.f_back
        except AttributeError :
            raise ValueError, "call stack is not deep enough: %d" % (depth, )
    return result
# end def frame

def globals (depth = 0) :
    """Return the `globals ()' of the caller's caller (larger values of
       `depth' return caller's farther up the call stack).

       This is useful for evaluating an expression in the context of a
       function's caller or for changing the context of a functions caller
       (e.g., for implementing a Common Lisp like `trace' function)
    """
    return frame (depth).f_back.f_globals
# end def globals

def locals (depth = 0) :
    """Return the `locals ()' of the caller's caller (larger values of
       `depth' return caller's farther up the call stack).

       This is useful for evaluating an expression in the context of a
       function's caller.
    """
    return frame (depth).f_back.f_locals
# end def locals

def code (depth = 0) :
    """Returns the code object of the caller's caller (larger values of
       `depth' return caller's farther up the call stack).
    """
    return frame (depth).f_back.f_code
# end def code

def info (level = -3) :
    """Returns `file-name', `line-number', `function-name' of caller at
       position `level' in the call stack (-3 being the caller of
       `info's caller).
    """
    return traceback.extract_stack () [level] [:3]
# end def info

class Scope :
    """Global and local variables visible in caller's scope.

       The variables are available as attributes and via the index operator.
       The index operator also supports expressions as indices and will
       return the result of such expressions as evaluated in the caller's
       scope.

       The supplied index operator allows Scope objects to be used as mapping
       arguments for the string formatting operator `%s':

       >>> "42*3 == %(42*3)d" % Scope ()
       '42*3 == 126'
       >>> a,b,c = 2,3,4
       >>> "a = %(a)s, b = %(b)d, c = %(c)f, d = %(b*c)s" % Scope ()
       'a = 2, b = 3, c = 4.000000, d = 12'
       >>> list = [x*x for x in range (10)]
       >>> "%(list)s, %(list [2:4])s, %(list [-1])s" % Scope ()
       '[0, 1, 4, 9, 16, 25, 36, 49, 64, 81], [4, 9], 81'
       >>> square = lambda n : n * n
       >>> "%(square (%(3*4)s))s" % Scope ()
       '144'

    """

    def __init__ (self, depth = 0, globs = None, locls = None) :
        self.globals = globs or globals (depth)
        self.locals  = locls or locals  (depth)
    # end def __init__

    def __getitem__ (self, index) :
        ### following Skip Montanaro, we interpolate `self` first to allow
        ### nested `%(expression)s`, ### e.g., "%(2*(%(3*4)s))s" % Scope ()
        index = index % self
        return eval (index, self.globals, self.locals)
    # end def __getitem__

    def __getattr__ (self, name) :
        try :
            return self.locals [name]
        except KeyError :
            try :
                return self.globals [name]
            except KeyError :
                raise AttributeError, name
    # end def __getattr__

# end class Scope

### unit-test code ############################################################

if __debug__ :
    try :
        import U_Test
    except ImportError :
        pass
    else :
        def _doc_test () :
            import _TFL.Caller
            return U_Test.run_module_doc_tests (Caller)
        # end def _doc_test

        if __name__ == "__main__" :
            _doc_test ()
# end if __debug__

### end unit-test code ########################################################

from _TFL import TFL
if __name__ != "__main__" :
    TFL._Export_Module ()

### __END__ Caller
