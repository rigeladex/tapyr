# -*- coding: iso-8859-1 -*-
# Copyright (C) 1999-2004 Mag. Christian Tanzer. All rights reserved
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
#    TFL.NO_List
#
# Purpose
#    List of named objects
#
# Revision Dates
#     5-Oct-1999 (CT) Creation
#     3-Feb-2000 (MG) `__getslice__' added
#    28-Mar-2000 (CT) `__add__' changed to allow addition of normal lists and
#                     tuples to NO_Lists
#    28-Jun-2000 (CT) `insert' changed to allow `index == None'
#    30-Jun-2000 (CT) `keys' added
#     8-Aug-2000 (CT) `get' added
#    16-Mar-2001 (CT) `Ordered_Set' factored
#    16-Mar-2001 (CT) `update' added
#    21-Mar-2001 (MG) Redefine `_check_value' because TTPbuild currently uses
#                     objects with the same name !
#    11-Jun-2003 (CT) s/== None/is None/
#    11-Jun-2003 (CT) s/!= None/is not None/
#    20-Nov-2003 (CT) Calls to `self.__len__` removed
#    28-Sep-2004 (CT) Use `isinstance` instead of type comparison
#    ««revision-date»»···
#--

"""List of named objects. Access to the list elements is provided by
   numerical index and by name.

   Each element of the list must provide an attribute `name' of a non-numeric
   type.
"""

from   _TFL                 import TFL
import _TFL.Ordered_Set
from   _TFL.predicate       import paired

class NO_List (TFL.Ordered_Set):
    """List of named objects. Access to the list elements is provided by
       numerical index and by name.

       Each element of the list must provide an attribute `name' of a
       non-numeric type.
    """

    def _check_value (self, value) :
        """Does currently not work in TTPbuild ! XXX"""
        pass ### XXX
    # end def _check_value

    def append (self, value) :
        try :
            self._check_value (value.name)
        except :
            print value
            raise
        self.index_dict  [value.name] = len (self.data)
        self.data.append (value)
    # end def append

    def insert (self, index, value, delta = 0) :
        self._check_value (value.name)
        if index is None :
            index = len (self.data)
        if not isinstance (index, int) :
            if not isinstance (index, str) :
                index = index.name
            i = self.index_dict [index] + delta
        else :
            i = index                   + delta
        self.data [i:i] = [value]
        self._fix (i)
    # end def insert

    def update (self, other) :
        for o in other :
            i = self.index_dict.get (o.name)
            if i is not None :
                self [i] = o
            else :
                self.append (o)
    # end def update

    def _fix (self, from_index) :
        if from_index < 0 :
            from_index += len (self.data)
        map ( lambda (e, i), d = self.index_dict : d.update ({e.name : i})
            , paired ( self.data [from_index:]
                     , range     (from_index, len (self.data))
                     )
            )
    # end def _fix

    def _indices (self, index) :
        if not isinstance (index, int) :
            if not isinstance (index, str) :
                index = index.name
            i = self.index_dict [index]
            n = index
        else :
            l = len (self.data)
            if index < l :
                i = index
                n = self.data [i].name
            else :
                i = l
                n = ""
        return i, n
    # end def _indices

    def __setitem__ (self, index, value) :
        i, n = self._indices (index)
        del self.index_dict  [n]
        self.index_dict      [value.name] = i
        self.data            [i]          = value
    # end def __setitem__

# end class NO_List

if __name__ != "__main__" :
    TFL._Export ("*")
else :
    class T :
        def __init__ (self, v) :
            self.v = v

        def __getattr__ (self, name) :
            if name == "name" :
                return "%s" % self.v
            raise AttributeError, name

        def __cmp__ (self, other) :
            return cmp (self.v, other.v)

        def __str__ (self) :
            return self.name

        def __repr__ (self) :
            return "%s" % self.v

    def show (l) :
        print l, sorted (l.index_dict.items(), lambda l, r : cmp (l[1], r[1]))

    l = NO_List (T (1), T(2), T("abc"), T(3))
    show (l)
    t = T ("xyz")
    l.append (t)
    show (l)
    l.insert (2, T ("kieselack"))
    show (l)
    print l ["kieselack"], l [l.n_index ("kieselack")]
    print "has_key (kieselack) :", l.has_key ("kieselack")
    print "has_key (kieseluck) :", l.has_key ("kieseluck")
    l.insert ("abc", T ("foo"))
    show (l)
    l.insert ("abc", T ("bar"), 1)
    show (l)
    l.reverse ()
    show (l)
    l.sort ()
    show (l)
    l [1] = T (137)
    show (l)
    l.pop ()
    show (l)
    del l ["abc"]
    show (l)
    del l [1:3]
    show (l)
### __END__ TFL.NO_List
