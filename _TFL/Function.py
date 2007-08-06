# -*- coding: iso-8859-1 -*-
# Copyright (C) 2000-2006 Mag. Christian Tanzer. All rights reserved
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
#    TFL.Function
#
# Purpose
#    Encapsulate function into callable object
#
# Revision Dates
#    16-May-2000 (CT) Creation
#    22-Sep-2000 (CT) Set `__name__'
#    19-Jun-2001 (CT) Assign to `self.__call__' in `__init__' instead of
#                     defining `__call__' as method
#     3-Oct-2001 (CT) `__deepcopy__` added
#     3-Oct-2001 (CT) `_Function_` factored
#    23-Sep-2004 (CT) `_Function_.__getattr__` added to make wrapped
#                     callables more similar to the real thing (e.g., avoid
#                     an AttributeError from `wrapped.func_code`)
#    14-Feb-2006 (CT) Moved into package `TFL`
#    14-Feb-2006 (CT) `_Function_` unfactored (`Function` was empty)
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ««revision-date»»···
#--



from   _TFL             import TFL

class Function :

    def __init__ (self, function, _doc = None) :
        self.function = function
        self.__name__ = function.__name__
        self.__doc__  = _doc or function.__doc__
    # end def __init__

    def __deepcopy__ (self, memo_dict) :
        return self.__class__ (self.function, self.__doc__)
    # end def __getstate__

    def __getattr__ (self, name) :
        return getattr (self.function, name)
    # end def __getattr__

    def __repr__ (self) :
        return "<%s %s at %x>" % \
            (self.__class__.__name__, self.__name__, id (self.function))
    # end def __repr__

    def __str__ (self) :
        return self.__name__
    # end def __str__

# end class Function

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.Function
