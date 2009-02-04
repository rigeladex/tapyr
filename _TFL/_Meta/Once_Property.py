# -*- coding: iso-8859-1 -*-
# Copyright (C) 2007-2009 Mag. Christian Tanzer. All rights reserved
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
#    TFL.Meta.Once_Property
#
# Purpose
#    Define a property which value is computed once per instance
#
# Revision Dates
#     9-Nov-2007 (CT) Creation
#     4-Feb-2009 (CT) Documentation improved
#    ««revision-date»»···
#--

from   _TFL             import TFL
import _TFL._Meta

### XXX `wraps` should go somewhere else (and be used for `TFL.Decorator`, too)
try :
    from functools import wraps
except ImportError :
    def wraps (wrapped) :
        def _ (wrapper) :
            wrapper.__name__   = wrapped.__name__
            wrapper.__doc__    = wrapped.__doc__
            wrapper.__module__ = getattr (wrapped, "__module__", "<builtin>")
            wrapper.__dict__.update (getattr (wrapped, "__dict__", {}))
            return wrapper
        return _

def Once_Property (f) :
    """Define a property that is computed once (per instance) by
       calling `f` and stored in the instance attribute `__<name>`.
    """
    key = "__%s" % (f.__name__, )
    @wraps (f)
    def _ (self) :
        dict = self.__dict__
        try :
            result = dict [key]
        except KeyError :
            result = dict [key] = f (self)
        return result
    return property (_, doc = f.__doc__)
# end def Once_Property

if __name__ != "__main__" :
    TFL.Meta._Export ("Once_Property")
### __END__ Once_Property


