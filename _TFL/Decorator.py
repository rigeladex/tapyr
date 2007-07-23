# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006 Mag. Christian Tanzer. All rights reserved
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
#    TFL.Decorator
#
# Purpose
#    Provide a decorator for defining well-behaved decorators
#
# Revision Dates
#    14-Apr-2006 (CT)  Creation
#    19-Apr-2006 (CT)  Set `__module__`, too
#    26-Sep-2006 (PGO) `wrapper` fixed to work with builtin functions, too
#    23-Jul-2007 (CED) Activated absolute_import
#    ««revision-date»»···
#--
from __future__ import absolute_import


from _TFL import TFL

def Decorator (decorator) :
    """Decorate `decorator` so that `__name__`, `__doc__`, and `__dict__` of
       decorated functions/methods are preserved.

       >>> def deco (f) :
       ...     def wrapper () :
       ...         "Wrapper around decorated function"
       ...         return f ()
       ...     return wrapper
       ...
       >>> @deco
       ... def foo () :
       ...     "Function to test decoration"
       ...     pass
       ...
       >>> foo.__name__, foo.__doc__
       ('wrapper', 'Wrapper around decorated function')

       >>> @Decorator
       ... def deco (f) :
       ...     def wrapper () :
       ...         "Wrapper around decorated function"
       ...         return f ()
       ...     return wrapper
       ...
       >>> @deco
       ... def foo () :
       ...     "Function to test decoration"
       ...     pass
       ...
       >>> foo.__name__, foo.__doc__
       ('foo', 'Function to test decoration')
    """
    def wrapper (f) :
        decorated            = decorator (f)
        decorated.__name__   = f.__name__
        decorated.__module__ = getattr (f, "__module__", "<builtin>")
        decorated.__doc__    = f.__doc__
        decorated.__dict__.update (getattr (f, "__dict__", {}))
        return decorated
    wrapper.__name__   = decorator.__name__
    wrapper.__module__ = decorator.__module__
    wrapper.__doc__    = decorator.__doc__
    wrapper.__dict__.update (decorator.__dict__)
    return wrapper
# end def Decorator

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.Decorator
