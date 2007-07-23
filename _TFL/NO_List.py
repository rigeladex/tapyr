# -*- coding: iso-8859-1 -*-
# Copyright (C) 1999-2006 Mag. Christian Tanzer. All rights reserved
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
#     5-Oct-1999 (CT)  Creation
#     3-Feb-2000 (MG)  `__getslice__' added
#    28-Mar-2000 (CT)  `__add__' changed to allow addition of normal lists and
#                      tuples to NO_Lists
#    28-Jun-2000 (CT)  `insert' changed to allow `index == None'
#    30-Jun-2000 (CT)  `keys' added
#     8-Aug-2000 (CT)  `get' added
#    16-Mar-2001 (CT)  `Ordered_Set' factored
#    16-Mar-2001 (CT)  `update' added
#    21-Mar-2001 (MG)  Redefine `_check_value' because TTPbuild currently uses
#                      objects with the same name !
#    11-Jun-2003 (CT)  s/== None/is None/
#    11-Jun-2003 (CT)  s/!= None/is not None/
#    20-Nov-2003 (CT)  Calls to `self.__len__` removed
#    28-Sep-2004 (CT)  Use `isinstance` instead of type comparison
#     8-Nov-2006 (PGO) Inheritance changed
#    23-Jul-2007 (CED) Activated absolute_import
#    ««revision-date»»···
#--
from __future__ import absolute_import


from   _TFL                 import TFL

import _TFL._Meta.M_Class
import _TFL.Accessor
import _TFL.Decorator
import _TFL.Ordered_Set


class M_Name_Dict (TFL.Meta.M_Class) :

    def __init__ (cls, name, bases, dct) :
        super (M_Name_Dict, cls).__init__ (name, bases, dct)
        for method_name in dct.get ("_convert_methods", ()) :
            setattr \
                ( cls, method_name
                , cls.name_of_key (getattr (cls, method_name))
                )
    # end def __init__

    @staticmethod
    @TFL.Decorator
    def name_of_key (method) :
        def _ (self, key, * args, ** kw) :
            if not isinstance (key, basestring) :
                key = key.name
            return method (self, key, * args, ** kw)
        return _
    # end def name_of_key

# end class M_Name_Dict


class Name_Dict (dict) :

    __metaclass__    = M_Name_Dict
    _convert_methods = \
        ("get", "has_key", "pop", "__getitem__", "__delitem__", "__setitem__")

# end class Name_Dict


class NO_List (TFL.Ordered_Set):
    """List of named objects. Access to the list elements is provided by
       numerical index and by name.

       Each element of the list must provide an attribute `name' of a
       non-numeric type.
    """
    _reverse_mapping_cls = Name_Dict
    _cannot_hold         = basestring

    def has_key (self, name) :
        return self.index_dict.has_key (name)
    # end def has_key

    def sort (self, cmp = None, key = None, reverse = False) :
        if key is None :
            key = TFL.Attribute.name
        self.__super.sort (cmp = cmp, key = key, reverse = reverse)
    # end def sort

    def __getitem__ (self, name_or_index) :
        if isinstance (name_or_index, int) :
            index = name_or_index
        else :
            index = self.index_dict [name_or_index]
        return self.__super.__getitem__ (index)
    # end def __getitem__

# end class NO_List

if __name__ != "__main__" :
    TFL._Export ("*")

### __END__ TFL.NO_List
