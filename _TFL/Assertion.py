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
#    Assertion
#
# Purpose
#    Provide Assert function nicer than Python's assert statement
#
# Revision Dates
#     8-Jul-2002 (CT) Creation (factored from U_Test.py)
#    ««revision-date»»···
#--

from caller_globals import caller_globals, caller_locals

def _test_assertion (expr, locals, msg = "", expression = None) :
    if not expr :
        tail  = []
        items = locals.items ()
        items.sort ()
        for k, v in items :
            if k == "self" or k [0] == "_" : continue
            tail.append ("%-20s = %r" % (k, v))
        msg = "%s\n    %s" % ( ", ".join     (filter (None, (expression, msg)))
                             , "\n    ".join (tail)
                             )
        raise AssertionError, msg
# end def _test_assertion

def Assertion (expression, msg = "") :
    """Perform the equivalent of `assert' on `eval (expression)'.

       There are two differences to standard `assert':

       - all elements of `locals' and of the caller's local name space
         are shown in the message passed to `AssertionError'

       - A false value of `__debug__' doesn't prevent the check of
         `expression'
    """
    locals = caller_locals ()
    try :
        result = eval (expression, caller_globals (), locals)
    except Exception, exc :
        _test_assertion (0,      locals, str (exc), expression)
    _test_assertion     (result, locals, msg,       expression)
# end def Assertion

from _TFL import TFL
TFL._Export ("*")

### __END__ Assertion
