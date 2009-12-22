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
#    MOM.E_Type_Manager
#
# Purpose
#    Scope-specific manager for essential object- and link-types
#
# Revision Dates
#    16-Oct-2009 (CT) Creation
#    27-Oct-2009 (CT) s/Scope_Proxy/E_Type_Manager/
#     3-Nov-2009 (CT) Type conversions for `epk` added
#     4-Nov-2009 (CT) Rename classes to `Id_Entity`, `Object`, and `Link` and
#                     call `MOM._Export_Module` instead of `MOM._Export`
#     4-Nov-2009 (CT) Type conversions for `epk` fixed
#     4-Nov-2009 (CT) `Link.s_links_of_obj`, `Link.t_links_of_obj` added
#     4-Nov-2009 (CT) `Link2` added
#    20-Nov-2009 (CT) `Link3` and `Link2_Ordered` added
#    22-Nov-2009 (CT) Documentation added
#    23-Nov-2009 (CT) `Link.__init__` added to define queries for `role_names`
#    23-Nov-2009 (CT) `_check_multiplicity` added
#    23-Nov-2009 (CT) `_role_query` changed to sue `_cooked_role`
#    23-Nov-2009 (CT) `__repr__` added
#    24-Nov-2009 (CT) Support for `No_Such_Object` added to
#                     `_cooked_epk_iter` and `_role_to_cooked_iter`
#    25-Nov-2009 (CT) `_role_query` guarded agains `No_Such_Object`
#     1-Dec-2009 (CT) `role_names` queries changed from `s_` to `t_`
#     2-Dec-2009 (CT) Queries `count` and `query` added
#     2-Dec-2009 (CT) Use `ems.role_query` instead of `s_role` and `t_role`
#     3-Dec-2009 (CT) `count` changed to be a property,
#                     `t_count` renamed to `count_transitive`
#     3-Dec-2009 (MG) `r_query` type check of role objects added
#    14-Dec-2009 (CT) `__call__` changed to call `scope.add`
#    ««revision-date»»···
#--

from   _MOM import MOM
from   _TFL import TFL

import _TFL._Meta.Object

from   _TFL.predicate import paired

class Id_Entity (TFL.Meta.Object) :
    """Scope-specific manager for a specific essential object- or link-type."""

    def __init__ (self, etype, scope) :
        self._etype     = etype
        self.home_scope = scope
    # end def __init__

    def __call__ (self, * args, ** kw) :
        scope  = self.home_scope
        result = self._etype (* args, scope = scope, ** kw)
        scope.add (result)
        return result
    # end def __call__

    @property
    def count (self) :
        """Return the strict count of objects or links."""
        return self.home_scope.ems.count (self._etype, strict = True)
    # end def count

    @property
    def count_transitive (self) :
        """Return the transitive count of objects or links."""
        return self.home_scope.ems.count (self._etype, strict = False)
    # end def count_transitive

    def exists (self, * epk, ** kw) :
        if kw :
            raise TypeError (kw)
        return self.home_scope.ems.exists (self._etype, epk)
    # end def exists

    def instance (self, * epk, ** kw) :
        if kw :
            raise TypeError (kw)
        return self.home_scope.ems.instance (self._etype, epk)
    # end def instance

    def query (self, * filters, ** kw) :
        """Return all entities matching the conditions in `filters` and `kw`.

           When no `filters` or `kw` are specified, `query` returns the
           transitive extension of the type in question, i.e., all instances
           of the type and all its subclasses.

           When `strict = True` is specified as the only argument, `query`
           returns the strict extension, i.e., all instances of the type in
           question, but none of its subclasses.

           All other filters reduce the number of instances returned to those
           that satisfy the filter conditions.
        """
        sort_key = kw.pop ("sort_key", None)
        Type     = self._etype
        result   = self.home_scope.ems.query (Type, * filters, ** kw)
        if sort_key is not None :
            result = result.order_by (sort_key)
        return result
    # end def query

    def query_s (self, * filters, ** kw) :
        """Return `self.query (* filters, ** kw)`
           sorted by `Type.sort_key (kw.get ("sort_key"))`.
        """
        sort_key = kw.pop ("sort_key", None)
        result   = self.query (* filters, ** kw)
        result   = TFL.Q_Result_Composite \
            ([result], self._etype.sort_key (sort_key))
        return result
    # end def query_s

    def __getattr__ (self, name) :
        return getattr (self._etype, name)
    # end def __getattr__

    def __repr__ (self) :
        return "<E_Type_Manager for %s of scope %s>" % \
            (self._etype.type_name, self.home_scope.name)
    # end def __repr__

# end class Id_Entity

class Object (Id_Entity) :
    """Scope-specific manager for essential object-types."""

    def exists (self, * epk, ** kw) :
        """Return true if an object with primary key `epk` exists."""
        if kw.pop ("raw", False) :
            epk = tuple (self._cooked_epk_iter (epk))
        return self.__super.exists   (* epk, ** kw)
    # end def exists

    def instance (self, * epk, ** kw) :
        """Return the object with primary key `epk` or None."""
        if kw.pop ("raw", False) :
            epk = tuple (self._cooked_epk_iter (epk))
        return self.__super.instance (* epk, ** kw)
    # end def instance

    def _cooked_epk_iter (self, epk) :
        for (pka, v) in zip (self._etype.primary, epk) :
            if v :
                try :
                    yield pka.from_string (v, None)
                except MOM.Error.No_Such_Object :
                    yield None
            else :
                yield None
    # end def _cooked_epk

# end class Object

class Link (Id_Entity) :
    """Scope-specific manager for essential link-types."""

    def __call__ (self, * args, ** kw) :
        self._check_multiplicity (* args, ** kw)
        if kw.get ("raw", False) :
            args = tuple (self._role_to_raw_iter    (args))
        else :
            args = tuple (self._role_to_cooked_iter (args, auto_create = True))
        return self.__super.__call__ (* args, ** kw)
    # end def __call__

    def applicable_objects (self, objects) :
        """Returns all `objects` not refusing to be linked by `self._etype`."""
        type_name = self._etype.Essence.type_name
        return [o for o in objects if type_name not in o.refuse_links]
    # end def applicable_objects

    def exists (self, * epk, ** kw) :
        """Return true if a link with primary key `epk` exists."""
        if kw.pop ("raw", False) :
            epk = tuple (self._cooked_epk_iter (epk))
        else :
            epk = tuple (self._role_to_cooked_iter (epk))
        return self.__super.exists   (* epk, ** kw)
    # end def exists

    def instance (self, * epk, ** kw) :
        """Return the link with primary key `epk` or None."""
        if kw.pop ("raw", False) :
            epk = tuple (self._cooked_epk_iter (epk))
        else :
            epk = tuple (self._role_to_cooked_iter (epk))
        return self.__super.instance (* epk, ** kw)
    # end def instance

    def r_query (self, * filters, ** kw) :
        """Return all links matching the conditions in `filters` and `kw`.

           `r_query` behaves similar to `query` but provides the additional
           features:

           - if `kw` contains role names,

             * the values passed can be `epk` in cooked or raw form (for
               `query`, objects must be passed)

             * the returned links are restricted to those linking the
               specified objects

           - some backends optimize link queries triggered via `r_query`.
        """
        sort_key = kw.pop ("sort_key", None)
        Type     = self._etype
        map      = getattr (Type, "role_map", None)
        rkw      = {}
        if map :
            for k in list (kw) :
                if k in map :
                    role = Type.Roles [map [k]]
                    try :
                        obj = self._cooked_role (role, kw.pop (k))
                        if not isinstance (obj, role.Class) :
                            return []
                        rkw [role.name] = obj
                    except MOM.Error.No_Such_Object :
                        return []
        ems = self.home_scope.ems
        if rkw :
            result = ems.r_query (self._etype, rkw, * filters, ** kw)
        else :
            result = ems.query   (self._etype, * filters, ** kw)
        if sort_key is not None :
            result = result.order_by (sort_key)
        return result
    # end def r_query

    def r_query_s (self, * filters, ** kw) :
        """Return `self.r_query (* filters, ** kw)`
           sorted by `Type.sort_key (kw.get ("sort_key"))`.
        """
        sort_key = kw.pop ("sort_key", None)
        result   = self.r_query (* filters, ** kw)
        result   = TFL.Q_Result_Composite \
            ([result], self._etype.sort_key (sort_key))
        return result
    # end def r_query_s

    def links_of (self, obj, * filters, ** kw) :
        """Return all links to `obj`
           (considers `obj` for each of the roles).
        """
        queries  = []
        r_query  = self.home_scope.ems.r_query
        sort_key = kw.pop ("sort_key", False)
        strict   = kw.pop ("strict", False)
        Type     = self._etype
        for r in Type.Roles :
            if isinstance (obj, r.role_type) :
                pk = self._cooked_role (r, obj)
                queries.append \
                    (r_query (r.assoc, {r.name : pk}, strict = strict))
        result = self.home_scope.ems.Q_Result_Composite (queries)
        if sort_key is not None :
            result = result.order_by (Type.sort_key (sort_key))
        return result
    # end def links_of

    def _check_multiplicity (self, * epk, ** kw) :
        if kw.get ("raw", False) :
            epk = tuple (self._cooked_epk_iter (epk))
        else :
            epk = tuple (self._role_to_cooked_iter (epk))
        etype = self._etype
        if self.__super.exists (* epk) :
            raise MOM.Error.Duplicate_Link \
                (etype, self.__super.instance (* epk))
        errors  = []
        r_query = self.home_scope.ems.r_query
        for r, pk in zip (etype.Roles, epk) :
            if r.max_links :
                links = r_query (r.assoc, {r.name : pk}, strict = True)
                nol   = links.count ()
                if nol >= r.max_links :
                    errors.append \
                        ( MOM.Error.Multiplicity_Error \
                            (pk, r.max_links, epk, list (links))
                        )
        if errors :
            raise MOM.Error.Multiplicity_Errors (etype.type_name, errors)
    # end def _check_multiplicity

    def _cooked_epk_iter (self, epk) :
        for (pka, v) in zip (self._etype.primary, epk) :
            try :
                if getattr (pka, "role_type", None) :
                    ### Allow role attributes to be passed as objects even if
                    ### `raw` is specified
                    v = self._cooked_role (pka, v)
                elif v :
                    v = pka.from_string   (v, None)
            except MOM.Error.No_Such_Object :
                v = None
            yield v
    # end def _cooked_epk_iter

    def _cooked_role (self, r, v) :
        result = v
        if not isinstance (result, MOM.Entity) :
            if not isinstance (v, (tuple, list)) :
                if not (v.startswith ("(") and v.endswith (")")) :
                    v = (v, )
            result = r.from_string (v, None)
        return result
    # end def _cooked_role

    def _role_to_cooked_iter (self, epk, auto_create = False) :
        for (r, v) in paired (self._etype.Roles, epk) :
            if r is not None :
                ### Allow role attributes to be passed as raw values even if
                ### `raw` is not specified
                try :
                    v = self._cooked_role (r, v)
                except MOM.Error.No_Such_Object :
                    if auto_create :
                        scope = self.home_scope
                        et    = getattr (scope, r.role_type.type_name)
                        v     = et (* v, implicit = True, raw = True)
                    else :
                        v = None
            yield v
    # end def _role_to_cooked_iter

    def _role_to_raw_iter (self, epk) :
        for (r, v) in paired (self._etype.Roles, epk) :
            if r is not None :
                ### Allow role attributes to be passed as objects even if
                ### `raw` is specified
                if isinstance (v, MOM.Entity) :
                    v = r.as_code (v)
            yield v
    # end def _role_to_raw_iter

# end class Link

class Link2 (Link) :
    """Scope-specific manager for essential binary link-types."""

    ### XXX dfc_synthesizer

# end class Link2

class Link3 (Link) :
    """Scope-specific manager for essential ternary link-types."""

# end class Link3

class Link2_Ordered (Link2) :
    """Scope-specific manager for essential ordered binary link-types."""

    ### XXX check_duplicate

# end class Link2_Ordered

__doc__ = """
Module `MOM.E_Type_Manager`
===========================

  `MOM.E_Type_Manager` provides classes implementing scope-specific managers
  for essential object and link types.

  For each essential object and link type, a scope provides a
  `E_Type_Manager` that is accessible under the `type_name` of the essential
  type in question.

  For instance, the `E_Type_Manager` for an essential
  object type `BMT.Mouse` of a scope `s` can be accessed as::

      s.BMT.Mouse

  and provides methods to create and query instances of `BMT.Mouse`. A new
  mouse named `mickey` is created by::

      s.BMT.Mouse ("mickey")

  The transitive extension of mice, i.e., the extension of `BMT.Mouse` and
  all classes derived from it, is computed by the query::

      s.BMT.Mouse.query ()



.. autoclass:: Object()
    :members:
    :inherited-members:
.. autoclass:: Link()
    :members:
    :inherited-members:

"""

if __name__ != "__main__" :
    MOM._Export_Module ()
### __END__ MOM.E_Type_Manager
