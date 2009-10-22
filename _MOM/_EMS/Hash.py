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
#
# Revision Dates
#    14-Oct-2009 (CT) Creation
#    15-Oct-2009 (CT) Creation continued
#    16-Oct-2009 (CT) Creation continued..
#    ««revision-date»»···
#--

from   _MOM                  import MOM
from   _TFL                  import TFL

import _MOM._EMS
import _MOM.Error
import _MOM.Link
import _MOM.Object

import _TFL._Meta.Object

import _TFL.Decorator
import _TFL.defaultdict

import itertools

class Manager (TFL.Meta.Object) :
    """Entity manager using hash tables to hold entities."""

    type_name = "Hash"

    def __init__ (self, scope) :
        self.scope   = scope
        self._counts = TFL.defaultdict (int)
        self._tables = TFL.defaultdict (dict)
        self._r_map  = TFL.defaultdict (lambda : TFL.defaultdict (set))
        self.__id    = 0
    # end def __init__

    def add (self, entity) :
        count = self._counts
        hpk   = entity.hpk
        root  = entity.relevant_root
        table = self._tables [root.type_name]
        if hpk in table :
            raise MOM.Error.Name_Clash (entity, table [hpk])
        if entity.max_count and entity.max_count <= count [entity.type_name] :
            raise MOM.Error.Too_Many_Objects (entity, entity.max_count)
        entity.id                 = self.__id
        self.__id                += 1
        count [entity.type_name] += 1
        table [hpk]               = entity
        if entity.Roles :
            r_map = self._r_map
            for r in entity.Roles :
                r_map [r] [r.get_role (entity).id].add (entity)
    # end def add

    def exists (self, Type, epk) :
        tables = self._tables
        root   = Type.relevant_root
        if root :
            roots = {root.type_name : root}
        else :
            roots = Type.relevant_roots
        return \
            [  T for (n, T) in roots.iteritems ()
            if T.epk_to_hpk (* epk) in tables [n]
            ]
    # end def exists

    def instance (self, Type, epk) :
        root   = Type.relevant_root
        hpk    = Type.epk_to_hpk (* epk)
        if root :
            return self._tables [root.type_name].get (hpk)
        raise TypeError \
            ( "Cannot query `instance` of non-root type `%s`."
              "\n"
              "Use one of the types %s instead."
            % (Type.type_name, ", ".join (sorted (Type.relevant_roots)))
            )
    # end def instance

    def remove (self, entity) :
        count = self._counts
        hpk   = entity.hpk
        root  = entity.relevant_root
        table = self._tables [root.type_name]
        del table [hpk]
        count [entity.type_name] -= 1
        if entity.Roles :
            r_map = self._r_map
            for r in entity.Roles :
                r_map [r] [r.get_role (entity).id].remove (entity)
    # end def remove

    def rename (self, entity, new_epk, renamer) :
        new_hpk = Type.epk_to_hpk (* new_epk)
        root    = entity.relevant_root
        table   = self._tables [root.type_name]
        if new_hpk in table :
            raise MOM.Error.Name_Clash (entity, table [new_hpk])
        self.remove (entity)
        renamer     ()
        self.add    (entity)
    # end def rename

    def s_count (self, Type) :
        return self._counts [Type.type_name]
    # end def s_count

    def s_extension (self, Type, sort_key = None) :
        root   = Type.relevant_root
        tables = self._tables
        result = []
        if root :
            result = tables [root.type_name].itervalues ()
            if Type.children :
                pred   = lambda x : x.Essence is Type.Essence
                result = itertools.ifilter (pred, result)
        return sorted (result, key = sort_key or Type.sorted_by)
    # end def s_extension

    def s_role (self, role, obj) :
        return self._r_map [role] [obj.id]
    # end def s_role

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

    def t_extension (self, Type , sort_key = None) :
        root   = Type.relevant_root
        tables = self._tables
        if root :
            result = tables [root.type_name].itervalues ()
        else :
            result = itertools.chain \
                (* (tables [t].itervalues () for t in Type.relevant_roots))
        return sorted (result, key = sort_key or Type.sorted_by)
    # end def t_extension

    def t_role (self, role, obj) :
        r_map = self._r_map
        i     = role.role_index
        return itertools.chain \
            ( r_map [role] [obj.id]
            , * ( r_map [c.Roles [i]] [obj.id]
                for c in role.assoc.children.itervalues ()
                )
            )
    # end def t_role

    def __iter__ (self) :
        return itertools.chain \
            (* (t.itervalues () for t in self._tables.itervalues ()))
    # end def __iter__

# end class Manager

@TFL.Add_Method (MOM.Link)
@TFL.Meta.Class_Method
def epk_to_hpk (cls, * epk) :
    return epk
# end def epk_to_hpk

@TFL.Add_Method (MOM.Link)
@TFL.Meta.Once_Property
def hpk (self) :
    return tuple (a.get_value (self) for a in self.roles) ### XXX ???
# end def epk

@TFL.Add_Method (MOM.Object)
@TFL.Meta.Class_Method
def epk_to_hpk (cls, * epk) :
    return epk
# end def epk_to_hpk

MOM.Object.hpk = TFL.Meta.Alias_Property ("epk")

if __name__ != "__main__" :
    MOM.EMS._Export_Module ()
### __END__ MOM.EMS.Hash
