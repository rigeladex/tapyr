# -*- coding: iso-8859-1 -*-
# Copyright (C) 1999-2005 Mag. Christian Tanzer. All rights reserved
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
#    TFL.PL_List
#
# Purpose
#    Provide a list similar to those in Perl. Referencing undefined
#    indices doesn't trigger an exception but returns an undefined value.
#
# Revision Dates
#     6-Apr-1999 (CT) Creation
#     8-Apr-1999 (CT) Constructor semantics changed (`* args' instead of
#                     argument `data = None')
#    22-Feb-2001 (CT) Use `raise' instead of `raise exc' for re-raise
#    19-Apr-2003 (CT) `__iter__` added
#    24-Mar-2005 (CT) Moved into package `TFL`
#    11-May-2007 (MG) `__getslice__` added becasue the implementation of the
#                     `UserList.__getslice__`does not work
#    23-Jul-2007 (CED) Activated absolute_import
#    ««revision-date»»···
#--
from __future__ import absolute_import


from   UserList  import UserList
from   copy      import deepcopy

from   _TFL      import TFL

class PL_List (UserList) :
    """Perl like list: references to undefined indices return an undefined
       value instead of raising an exception.
    """

    def __init__ (self, undefined = None, * args) :
        """Construct a new `PL_List' with elements specified as optional
           arguments `args' and undefined value `undefined'.
        """
        UserList.__init__ (self)
        self.data      = list (args [:])
        self.body      = self.data ### alias name for `self.data'
        self.undefined = undefined
    # end def __init__

    def shift (self, i = 0) :
        if self.data :
            result = self.data [i]
            del      self.data [i]
        else :
            result = deepcopy (self.undefined)
        return result
    # end def shift

    def __delitem__ (self, item) :
        try :
            del self.data [item]
        except IndexError :
            pass
    # end def __delitem__

    def __delslice__ (self, i, j) :
        try :
            del self.data [i:j]
        except IndexError :
            pass
    # end def __delslice__

    def __getslice__ (self, i, j) :
        return self.__class__ (self.undefined, * self.data [i:j])
    # end def __getslice__

    def __getitem__ (self, item) :
        try :
            return self.data [item]
        except IndexError :
            return deepcopy (self.undefined)
    # end def __getitem__

    def __iter__ (self) :
        return iter (self.data)
    # end def __iter__

    def __setitem__ (self, item, value) :
        try :
            self.data [item] = value
        except IndexError, exc :
            l = len (self.data)
            if item >= l :
                for i in range (l, item) :
                    self.data.append (deepcopy (self.undefined))
                self.data.append (value)
            else :
                raise
    # end def __setitem__

# end class PL_List

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.PL_List
