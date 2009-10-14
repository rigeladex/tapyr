# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Mag. Christian Tanzer. All rights reserved
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
#    MOM.EMS.Hash
#
# Purpose
#    «text»···
#
# Revision Dates
#    14-Oct-2009 (CT) Creation
#    ««revision-date»»···
#--

from   _MOM                  import MOM
from   _TFL                  import TFL

import _MOM._EMS
import _MOM.Object

import _TFL._Meta.Object
import _TFL.Decorator
import _TFL.defaultdict

@TFL.Add_To_Class ("EMS_Hash", MOM.Object)
class Object (TFL.Meta.Object) :
    """Entity manager using a hash table to hold objects."""

    def __init__ (self) :
        self._count = TFL.defaultdict (int)
        self._table = {}
    # end def __init__

    def add (self, obj) :
        epk   = obj.epk
        count = self._count
        table = self._table
        if epk in table :
            raise MOM.Error.Name_Clash (obj, table [epk])
        if obj.max_count and obj.max_count <= count [obj.type_name] :
            raise MOM.Error.Too_Many_Objects (obj, obj.max_count)
        table [epk] = obj
        count [obj.type_name] += 1
    # end def add

    def count (self, what) :
        return self._count [what.type_name]
    # end def count

    def exists (self, * epk) :
        return epk in self._table
    # end def exists

    def extension (self, of_class = None, strict = False, sort_key = None) :
        result = self._table.itervalues ()
        if of_class :
            if strict :
                pred = lambda x : x.__class__.Essence == of_class.Essence
            else :
                pred = lambda x : isinstance (x, of_class.Essence)
            result = itertools.ifilter (pred, result)
        if sort_key is None :
            sort_key = (of_class or MOM.Id_Entity).sorted_by
        return sorted (result, key = sort_key)
    # end def extension

    def instance (self, * epk) :
        return self._table.get (epk)
    # end def instance

    def remove (self, obj) :
        epk   = obj.epk
        count = self._count
        table = self._table
        del table [epk]
        count [obj.type_name] -= 1
    # end def remove

    def __iter__ (self) :
        return self._table.itervalues ()
    # end def __iter__

# end class Object

if __name__ != "__main__" :
    MOM.EMS._Export_Module ()
### __END__ MOM.EMS.Hash
