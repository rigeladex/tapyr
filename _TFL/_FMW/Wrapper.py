# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 Mag. Christian Tanzer. All rights reserved
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
#    TFL.FMW.Wrapper
#
# Purpose
#    Model wrapper for functions and methods
#
# Revision Dates
#    22-Sep-2004 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL                   import TFL
import _TFL._FMW
import _TFL._Meta.Object

import new

class Wrapped_FM (TFL.Meta.Object) :
    """Model a wrapped function/method."""

    def __init__ (self, __name__, name, fct, * args, ** kw) :
        self.__name__ = __name__
        self.__doc__  = getattr (fct, "__doc__", None)
        self.name     = name
        self.fct      = fct
        self.args     = args
        self.kw       = kw
    # end def __init__

    def __call__ (self, * args, ** kw) :
        raise NotImplementedError, \
            "%s.__call__ must be redefined" % self.__class__.__name__
        return self.fct (* args, ** kw)
    # end def __call__

    def __repr__ (self) :
        return "<%s for %r>" % (self.__class__.__name__, self.fct)
    # end def __repr__

    def __str__ (self) :
        return self.name
    # end def __str__

# end class Wrapped_FM

class Wrapper (TFL.Meta.Object) :
    """Provide wrappers for functions and methods"""

    def __init__ (self, * wrapped_args, ** wrapped_kw) :
        if wrapped_kw.get ("Wrapped_FM") is not None :
            self.Wrapped_FM = wrapped_kw ["Wrapped_FM"]
            del wrapped_kw ["Wrapped_FM"]
        self.wrapped_args = wrapped_args
        self.wrapped_kw   = wrapped_kw
    # end def __init__

    def add_function (self, module, name) :
        """Wrap function with `name` of module or package-namespace
           `module`.
        """
        setattr (module, name, self._wrapped (module, name))
    # end def add_function

    def add_method (self, cls, name) :
        """Wrap method with `name` of class `cls`"""
        wrapped = self._wrapped (cls, name)
        setattr (cls, name, new.instancemethod (wrapped, None, cls))
    # end def add_method

    def _wrapped (self, cm, name) :
        qname  = "%s.%s" % (cm.__name__, name)
        fct    = getattr (cm, name)
        return self.Wrapped_FM \
            (name, qname, fct, * self.wrapped_args, ** self.wrapped_kw)
    # end def _wrapped

# end class Wrapper

if __name__ != "__main__" :
    TFL.FMW._Export ("*")
### __END__ TFL.FMW.Wrapper
