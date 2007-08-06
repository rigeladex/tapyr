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
#    Assertion
#
# Purpose
#    Provide Assert function nicer than Python's assert statement
#
# Revision Dates
#     8-Jul-2002 (CT) Creation (factored from U_Test.py)
#    24-Mar-2005 (CT) Use `TFL.Caller.globals` instead of `caller_globals`
#                     (and ditto for `locals`)
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ««revision-date»»···
#--



from   _TFL import TFL
import _TFL.Caller

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
    locals = TFL.Caller.locals ()
    try :
        result = eval (expression, TFL.Caller.globals (), locals)
    except Exception, exc :
        _test_assertion (0,      locals, str (exc), expression)
    _test_assertion     (result, locals, msg,       expression)
# end def Assertion

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.Assertion
