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
#    Entity manager strategy using hash tables for entities
#    ««text»»···
#
# Revision Dates
#    14-Oct-2009 (CT) Creation
#    15-Oct-2009 (CT) Creation continued
#    ««revision-date»»···
#--

from   _MOM                  import MOM
from   _TFL                  import TFL

import _MOM._EMS
import _MOM.Entity

import _TFL._Meta.Object

import _TFL.Decorator
import _TFL.defaultdict

import itertools

@TFL.Add_To_Class ("EMS_Hash", MOM.Id_Entity)
class Manager (TFL.Meta.Object) :
    """Entity manager using hash tables to hold entities."""

    def __init__ (self) :
        self._counts = TFL.defaultdict (int)
        self._tables = TFL.defaultdict (dict)
    # end def __init__

    def add (self, obj) :
        count = self._counts
        epk   = obj.epk
        root  = obj.relevant_root
        table = self._tables [root.type_name]
        if epk in table :
            raise MOM.Error.Name_Clash (obj, table [epk])
        if obj.max_count and obj.max_count <= count [obj.type_name] :
            raise MOM.Error.Too_Many_Objects (obj, obj.max_count)
        table [epk] = obj
        count [obj.type_name] += 1
        ### XXX ??? How to deal with link role tables
    # end def add

    def s_count (self, Type) :
        return self._counts [Type.type_name]
    # end def s_count

    def t_count (self, Type, seen = None) :
        if seen is None :
            seen = set ()
        result = self._counts [Type.type_name]
        for n, c in Type.children.iteritems () :
            if n not in seen :
                seen.add (n)
                result += self.t_count (c, seen)
        return result
    # end def t_count

    def exists (self, epk, Type = None) :
        if Type is None :
            Type = MOM.Id_Entity
        tables = self._tables
        if Type.relevant_root :
            return epk in tables [Type.relevant_root.type_name]
        else :
            roots = Type.relevant_roots
            return [T for (n, T) in roots.iteritems () if epk in tables [n]]
    # end def exists

    def instance (self, epk, Type) :
        root = Type.relevant_root
        if root :
            return epk in self._tables [root.type_name]
        raise TypeError \
            ( "Cannot query `instance` of non-root type `%s`."
              "\n"
              "Use one of the types %s instead."
            % (Type.type_name, ", ".join (sorted (Type.relevant_roots)))
            )
    # end def instance

    def remove (self, obj) :
        count = self._counts
        epk   = obj.epk
        root  = obj.relevant_root
        table = self._tables [root.type_name]
        del table [epk]
        count [obj.type_name] -= 1
        ### XXX ??? How to deal with link role tables
    # end def remove

    def rename (self, obj, new_epk, renamer) :
        pass ### XXX
    # end def rename

    def s_extension (self, Type = None, sort_key = None) :
        if Type is None :
            Type = MOM.Id_Entity
        root   = Type.relevant_root
        tables = self._tables
        result = []
        if root :
            result = tables [root.type_name].itervalues ()
            if Type.children :
                pred   = lambda x : x.Essence == Type.Essence
                result = itertools.ifilter (pred, result)
        return sorted (result, key = sort_key or Type.sorted_by)
    # end def s_extension

    def t_extension (self, Type = None, sort_key = None) :
        if Type is None :
            Type = MOM.Id_Entity
        root   = Type.relevant_root
        tables = self._tables
        if root :
            result = tables [root.type_name].itervalues ()
        else :
            result = itertools.chain \
                (* (tables [t].itervalues () for t in Type.relevant_roots))
        return sorted (result, key = sort_key or Type.sorted_by)
    # end def t_extension

    def __iter__ (self) :
        return itertools.chain \
            (* (t.itervalues () for t in self._tables.itervalues ()))
    # end def __iter__

# end class Manager

if __name__ != "__main__" :
    MOM.EMS._Export_Module ()
### __END__ MOM.EMS.Hash
