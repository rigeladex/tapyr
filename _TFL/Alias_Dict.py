# -*- coding: utf-8 -*-
# Copyright (C) 2009-2013 Mag. Christian Tanzer. All rights reserved
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
#    TFL.Alias_Dict
#
# Purpose
#    Dictionary with support for aliases for the keys
#
# Revision Dates
#    30-Sep-2009 (CT) Creation
#    23-May-2013 (CT) Use `TFL.Meta.BaM` for Python-3 compatibility
#     2-Jun-2013 (CT) Add `copy`
#    ««revision-date»»···
#--

from   _TFL                  import TFL
from   _TFL.pyk              import pyk
import _TFL._Meta.M_Class

class Alias_Dict (TFL.Meta.BaM (dict, metaclass = TFL.Meta.M_Class)) :
    """A dictionary with support for aliases for the keys.

       >>> ad = Alias_Dict (a = 1, b = 42, z = 137)
       >>> sorted (pyk.iteritems (ad))
       [('a', 1), ('b', 42), ('z', 137)]
       >>> 5 in ad
       False
       >>> ad.add_alias (5, "z")
       >>> 5 in ad
       True
       >>> sorted (pyk.iteritems (ad))
       [('a', 1), ('b', 42), ('z', 137)]
    """

    def __init__ (self, * args, ** kw) :
        self.__super.__init__ (* args, ** kw)
        self._alias_names = {}
    # end def __init__

    def add_alias (self, alias_name, real_name) :
        self._alias_names [alias_name] = real_name
    # end def add_alias

    def copy (self, ** kw) :
        result = self.__class__ (self, ** kw)
        result._alias_names = dict (self._alias_names)
        return result
    # end def copy

    def get (self, key, default = None) :
        key = self._alias_names.get (key, key)
        return self.__super.get (key, default)
    # end def get

    def __contains__ (self, key) :
        key = self._alias_names.get (key, key)
        return self.__super.__contains__ (key)
    # end def __contains__

    def __getitem__ (self, key) :
        key = self._alias_names.get (key, key)
        return self.__super.__getitem__ (key)
    # end def __getitem__

# end class Alias_Dict

if __name__ != "__main__" :
    TFL._Export ("Alias_Dict")
### __END__ TFL.Alias_Dict
