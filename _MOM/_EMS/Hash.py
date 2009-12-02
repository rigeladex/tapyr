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
#    28-Oct-2009 (CT) I18N
#     4-Nov-2009 (CT) `sort_key` argument added to `s_role` and `t_role`
#     4-Nov-2009 (CT) `epk_to_hpk` and `hpk` for `MOM.Link` fixed
#    19-Nov-2009 (CT) Use `Type.sort_key (sort_key)` instead of
#                     `sort_key or Type.sorted_by` (3-compatibility)
#    20-Nov-2009 (CT) `sort_key = None` means no sorting,
#                     `sort_key = False` means use default sort-key for sorting
#    23-Nov-2009 (CT) `t_extension` changed to filter siblings of `Type` that
#                     are derived from the same `relevant_root`
#    23-Nov-2009 (CT) `exists`, `instance` and `s_extension` changed to
#                     filter siblings of `Type` that are derived from the
#                     same `relevant_root`
#    25-Nov-2009 (CT) `rename` (and `add`) changed to preserve `id`
#    27-Nov-2009 (CT) `add` and `remove` changed to call `register_dependency`
#                     and `unregister_dependency`, respectively
#    27-Nov-2009 (CT) `all_links` added
#     2-Dec-2009 (CT) `_Manager_` factored
#     2-Dec-2009 (CT) Query interface changed
#                     - added `count`, `query`, `_query_multi_root`, and
#                       `_query_single_root`
#                     - removed `s_count`, `s_extension`, and `t_extension`
#                     - s/t_count/_t_count/
#    ««revision-date»»···
#--

from   _MOM                  import MOM
from   _TFL                  import TFL

import _MOM._EMS._Manager_
import _MOM.Error
import _MOM.Link
import _MOM.Object

import _TFL._Meta.Object

import _TFL.Decorator
import _TFL.defaultdict

from   _TFL.I18N             import _, _T, _Tn

import itertools

class Manager (MOM.EMS._Manager_) :
    """Entity manager using hash tables to hold entities."""

    type_name = "Hash"

    def __init__ (self, scope) :
        self.__super.__init__ (scope)
        self._counts = TFL.defaultdict (int)
        self._tables = TFL.defaultdict (dict)
        self._r_map  = TFL.defaultdict (lambda : TFL.defaultdict (set))
        self.__id    = 0
    # end def __init__

    def add (self, entity, id = None) :
        count = self._counts
        hpk   = entity.hpk
        root  = entity.relevant_root
        table = self._tables [root.type_name]
        if hpk in table :
            raise MOM.Error.Name_Clash (entity, table [hpk])
        if entity.max_count and entity.max_count <= count [entity.type_name] :
            raise MOM.Error.Too_Many_Objects (entity, entity.max_count)
        if id is None :
            id = self.__id
            self.__id += 1
        entity.id                 = id
        count [entity.type_name] += 1
        table [hpk]               = entity
        if entity.Roles :
            r_map = self._r_map
            for r in entity.Roles :
                obj = r.get_role (entity)
                obj.register_dependency (entity.__class__)
                r_map [r] [obj.id].add (entity)
    # end def add

    def all_links (self, obj_id) :
        r_map  = self._r_map
        result = sorted \
            ( itertools.chain (* (rm [obj_id] for rm in r_map.itervalues ()))
            , key = self.scope.MOM.Id_Entity.sort_key ()
            )
        return result
    # end def all_links

    def count (self, Type, * filters, ** kw) :
        strict = kw.pop ("strict", False)
        if filters or kw :
            if strict :
                kw ["strict"] = strict
            result = self.__super.count (* filters, ** kw)
        else :
            if strict :
                result = self._counts  [Type.type_name]
            else :
                result = self._t_count (Type)
        return result
    # end def count

    def exists (self, Type, epk) :
        scope  = self.scope
        tables = self._tables
        root   = Type.relevant_root
        if root :
            roots = {root.type_name : root}
        else :
            roots = Type.relevant_roots
        return \
            [ getattr (scope, e.type_name)
            for e in (   tables [n].get (R.epk_to_hpk (* epk))
                     for (n, R) in roots.iteritems ()
                     )
            if  isinstance (e, Type.Essence)
            ]
    # end def exists

    def instance (self, Type, epk) :
        root   = Type.relevant_root
        hpk    = Type.epk_to_hpk (* epk)
        if root :
            result = self._tables [root.type_name].get (hpk)
            if not isinstance (result, Type.Essence) :
                result = None
            return result
        raise TypeError \
            ( "\n".join
                ( ( _T ("Cannot query `instance` of non-root type `%s`.")
                  , _T ("Use one of the types %s instead.")
                  )
                )
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
                obj = r.get_role (entity)
                obj.unregister_dependency (entity.__class__)
                r_map [r] [obj.id].remove (entity)
    # end def remove

    def rename (self, entity, new_epk, renamer) :
        new_hpk = entity.epk_to_hpk (* new_epk)
        root    = entity.relevant_root
        table   = self._tables [root.type_name]
        if new_hpk in table :
            raise MOM.Error.Name_Clash (entity, table [new_hpk])
        self.remove (entity)
        renamer     ()
        self.add    (entity, entity.id)
    # end def rename

    def s_role (self, role, obj, sort_key = False) :
        result = self._r_map [role] [obj.id]
        if sort_key is not None :
            result = sorted (result, key = role.assoc.sort_key (sort_key))
        return result
    # end def s_role

    def t_role (self, role, obj, sort_key = False) :
        r_map  = self._r_map
        i      = role.role_index
        result = itertools.chain \
            ( r_map [role] [obj.id]
            , * ( r_map [c.Roles [i]] [obj.id]
                for c in role.assoc.children.itervalues ()
                )
            )
        if sort_key is not None :
            result = sorted (result, key = role.assoc.sort_key (sort_key))
        return result
    # end def t_role

    def _query_multi_root (self, Type) :
        tables = self._tables
        return list \
            (   self.Q_Result (tables [t].itervalues ())
            for t in Type.relevant_roots
            )
    # end def _query_multi_root

    def _query_single_root (self, Type, root) :
        tables = self._tables
        result = tables [root.type_name].itervalues ()
        if root is not Type :
            ### filter siblings derived from same `relevant_root`
            result = itertools.ifilter \
                (lambda x : isinstance (x, Type), result)
        return result
    # end def _query_single_root

    def _t_count (self, Type, seen = None) :
        if seen is None :
            seen = set ()
        result = self._counts [Type.type_name]
        for n, c in Type.children.iteritems () :
            if n not in seen :
                seen.add (n)
                result += self._t_count (c, seen)
        return result
    # end def _t_count

    def __iter__ (self) :
        return itertools.chain \
            (* (t.itervalues () for t in self._tables.itervalues ()))
    # end def __iter__

# end class Manager

@TFL.Add_Method (MOM.Link)
@TFL.Meta.Class_Method
def epk_to_hpk (cls, * epk) :
    def gen (epk) :
        for r, pka in TFL.paired (cls.Roles, epk) :
            if pka is not None :
                pka = pka.id
            yield pka
    return tuple (gen (epk))
# end def epk_to_hpk

@TFL.Add_Method (MOM.Link, decorator = property)
def hpk (self) :
    return self.epk_to_hpk (* self.epk)
# end def hpk

@TFL.Add_Method (MOM.Id_Entity)
@TFL.Meta.Class_Method
def epk_to_hpk (cls, * epk) :
    return epk
# end def epk_to_hpk

MOM.Id_Entity.hpk = TFL.Meta.Alias_Property ("epk")

if __name__ != "__main__" :
    MOM.EMS._Export_Module ()
### __END__ MOM.EMS.Hash
