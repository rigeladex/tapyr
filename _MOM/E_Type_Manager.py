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
        return self._etype (* args, scope = self.home_scope, ** kw)
    # end def __call__

    def exists (self, * epk, ** kw) :
        if kw :
            raise TypeError (kw)
        return self.home_scope.ems.exists      (self._etype, epk)
    # end def exists

    def instance (self, * epk, ** kw) :
        if kw :
            raise TypeError (kw)
        return self.home_scope.ems.instance    (self._etype, epk)
    # end def instance

    @property
    def s_count (self) :
        """Return the strict count of objects or links."""
        return self.home_scope.ems.s_count     (self._etype)
    # end def s_count

    def s_extension (self, sort_key = False) :
        """Return the strict extension of objects or links."""
        return self.home_scope.ems.s_extension (self._etype, sort_key)
    # end def s_extension

    @property
    def t_count (self) :
        """Return the transitive count of objects or links."""
        return self.home_scope.ems.t_count     (self._etype)
    # end def t_count

    def t_extension (self, sort_key = False) :
        """Return the transitive extension of objects or links."""
        return self.home_scope.ems.t_extension (self._etype, sort_key)
    # end def t_extension

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
            try :
                yield pka.from_string (v, None)
            except MOM.Error.No_Such_Object :
                yield None
    # end def _cooked_epk

# end class Object

class Link (Id_Entity) :
    """Scope-specific manager for essential link-types."""

    def __init__ (self, etype, scope) :
        self.__super.__init__ (etype, scope)
        for r in etype.Roles :
            setattr \
                (self, r.role_name, getattr (self, "s_" + r.generic_role_name))
    # end def __init__

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

    def s_links_of_obj (self, obj) :
        """Return all strict links to `obj`
           (considers `obj` for each of the roles).
        """
        return self._links_of_obj (obj, "s_role")
    # end def s_links_of_obj

    def t_links_of_obj (self, obj) :
        """Return all transitive links to `obj`
           (considers `obj` for each of the roles).
        """
        return self._links_of_obj (obj, "t_role")
    # end def t_links_of_obj

    def _check_multiplicity (self, * epk, ** kw) :
        if kw.get ("raw", False) :
            epk = tuple (self._cooked_epk_iter (epk))
        else :
            epk = tuple (self._role_to_cooked_iter (epk))
        etype = self._etype
        if self.__super.exists (* epk) :
            raise MOM.Error.Duplicate_Link \
                (etype, self.__super.instance (* epk))
        errors = []
        for r, pk in zip (etype.Roles, epk) :
            if r.max_links :
                links = list (self._role_query (r, pk, "s_role", None))
                nol   = len  (links)
                if nol >= r.max_links :
                    errors.append \
                        ( MOM.Error.Multiplicity_Error \
                            (pk, r.max_links, epk, links)
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
                else :
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

    def _links_of_obj (self, obj, q_name) :
        query  = getattr (self.home_scope.ems, q_name)
        result = set ()
        for r in self._etype.Roles :
            if isinstance (obj, r.role_type) :
                result.update (query (r, obj, None))
        return result
    # end def _links_of_obj

    def _query_intersection (self, q1, * qs) :
        result = set (q1)
        for q in qs :
            result.intersection_update (q)
        return sorted (result, key = self._etype.sort_key ())
    # end def _query_intersection

    def _role_query (self, role, obj, q_name, sort_key = False) :
        query = getattr (self.home_scope.ems, q_name)
        return query (role, self._cooked_role (role, obj), sort_key)
    # end def _role_query

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

    def s_left (self, r) :
        """Return all strict links related to right `r`."""
        return self._role_query (self._etype.right, r, "s_role")
    # end def s_left

    def s_links_of (self, l = None, r = None, ** kw) :
        """Returns the set of strict links for `l` and `r`.
           If any of `l` or `r` is None all links for the corresponding role
           are returned.
        """
        return self._links_of \
            (l, r, self.s_left, self.s_right, self.s_extension, kw)
    # end def s_links_of

    def s_right (self, l) :
        """Return all strict links related to left `l`."""
        return self._role_query (self._etype.left, l, "s_role")
    # end def s_right

    def t_left (self, r) :
        """Return all transitive links related to right `r`."""
        return self._role_query (self._etype.right, r, "t_role")
    # end def t_left

    def t_links_of (self, l = None, r = None, ** kw) :
        """Returns the set of transitive links for `l` and `r`.
           If any of `l` or `r` is None all links for the corresponding role
           are returned.
        """
        return self._links_of \
            (l, r, self.t_left, self.t_right, self.t_extension, kw)
    # end def t_links_of

    def t_right (self, l) :
        """Return all transitive links related to left `l`."""
        return self._role_query (self._etype.left, l, "t_role")
    # end def t_right

    def _links_of (self, l, r, l_query, r_query, e_query, kw) :
        if l :
            if r :
                result = self.instance (l, r, ** kw)
                if result :
                    return [result]
                else :
                    return []
            else :
                return r_query (l)
        elif r :
            return l_query (r)
        else :
            return e_query ()
    # end def _links_of

# end class Link2

class Link3 (Link) :
    """Scope-specific manager for essential ternary link-types."""

    def s_left (self, m, r) :
        """Return all strict links related to both middle `m` and right `r`."""
        return self._query_intersection \
            (self.s_left_middle (r, None), self.s_left_right (m, None))
    # end def s_left

    def s_left_middle (self, r, sort_key = False) :
        """Return all strict links related to right `r`."""
        return self._role_query (self._etype.right, r, "s_role", sort_key)
    # end def s_left_middle

    def s_left_right (self, m, sort_key = False) :
        """Return all strict links related to right `m`."""
        return self._role_query (self._etype.middle, m, "s_role", sort_key)
    # end def s_left_right

    def s_links_of (self, l = None, m = None, r = None, ** kw) :
        """Returns the set of strict links for `l`, `m`, and `r`.
           If any of `l`, `m`, or `r` is None all links for the corresponding
           role are returned.
        """
        return self._links_of \
            ( l, m, r
            , self.s_left, self.s_middle, self.s_right
            , self.s_left_middle, self.s_left_right, self.s_middle_right
            , self.s_extension
            , kw
            )
    # end def s_links_of

    def s_middle (self, l, r) :
        """Return all strict links related to both left `l` and right `r`."""
        return self._query_intersection \
            (self.s_middle_right (l, None), self.s_left_middle (r, None))
    # end def s_middle

    def s_middle_right (self, l, sort_key = False) :
        """Return all strict links related to left `l`."""
        return self._role_query (self._etype.left, l, "s_role", sort_key)
    # end def s_middle_right

    def s_right (self, l, m) :
        """Return all strict links related to both left `l` and middle `m`."""
        return self._query_intersection \
            (self.s_middle_right (l, None), self.s_left_right (m, None))
    # end def s_right

    def t_left (self, m, r) :
        """Return all transitive links related to both middle `m` and right `r`."""
        return self._query_intersection \
            (self.t_left_middle (r, None), self.t_left_right (m, None))
    # end def t_left

    def t_left_middle (self, r, sort_key = False) :
        """Return all transitive links related to right `r`."""
        return self._role_query (self._etype.right, r, "t_role", sort_key)
    # end def t_left_middle

    def t_left_right (self, m, sort_key = False) :
        """Return all transitive links related to right `m`."""
        return self._role_query (self._etype.middle, m, "t_role", sort_key)
    # end def t_left_right

    def t_links_of (self, l = None, m = None, r = None, ** kw) :
        """Returns the set of transitive links for `l`, `m`, and `r`.
           If any of `l`, `m`, or `r` is None all links for the corresponding
           role are returned.
        """
        return self._links_of \
            ( l, m, r
            , self.t_left, self.t_middle, self.t_right
            , self.t_left_middle, self.t_left_right, self.t_middle_right
            , self.t_extension
            , kw
            )
    # end def s_links_of

    def t_middle (self, l, r) :
        """Return all transitive links related to both left `l` and right `r`."""
        return self._query_intersection \
            (self.t_middle_right (l, None), self.t_left_middle (r, None))
    # end def t_middle

    def t_middle_right (self, l, sort_key = False) :
        """Return all transitive links related to left `l`."""
        return self._role_query (self._etype.left, l, "t_role", sort_key)
    # end def t_middle_right

    def t_right (self, l, m) :
        """Return all transitive links related to both left `l` and middle `m`."""
        return self._query_intersection \
            (self.t_middle_right (l, None), self.t_left_right (m, None))
    # end def t_right

    def _links_of (self, l, m, r, l_query, m_query, r_query, lm_query, lr_query, mr_query, e_query, kw) :
        if l :
            if m :
                if r :
                    result = self.instance (l, m, r, ** kw)
                    if result :
                        return [result]
                    else :
                        return []
                else :
                    return r_query (l, m)
            elif r :
                return m_query  (l, r)
            else :
                return mr_query (l)
        elif m :
            if r :
                return l_query  (m, r)
            else :
                return lr_query (m)
        elif r :
            return lm_query (r)
        else :
            return e_query ()
    # end def _links_of

# end class Link3

class Link2_Ordered (Link2) :
    """Scope-specific manager for essential ordered binary link-types."""

    ### XXX check_duplicate

    def s_links_of (self, l = None, r = None, seq_no = None, ** kw) :
        """Returns the set of strict links for `l`, `r`, and `seq_no`.
           If any of `l` or `r` is None all links for the corresponding role
           are returned.
        """
        return self._links_of \
            (l, r, seq_no, self.s_left, self.s_right, self.s_extension, kw)
    # end def s_links_of

    def t_links_of (self, l = None, r = None, seq_no = None, ** kw) :
        """Returns the set of transitive links for `l`, `r`, and `seq_no`.
           If any of `l` or `r` is None all links for the corresponding role
           are returned.
        """
        return self._links_of \
            (l, r, seq_no, self.t_left, self.t_right, self.t_extension, kw)
    # end def t_links_of

    def _links_of (self, l, r, seq_no, l_query, r_query, e_query, kw) :
        if l :
            if r :
                if seq_no is not None :
                    result = self.instance (l, r, seq_no, ** kw)
                    if result :
                        return [result]
                    else :
                        return []
                else :
                    return self._query_intersection \
                        (l_query (r, None), r_query (l, None))
            else :
                result = r_query (l)
        elif r :
            result = l_query (r)
        else :
            return e_query ()
        if seq_no is not None :
            result = [lnk for lnk in result if lnk.seq_no == seq_no]
        return result
    # end def _links_of

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

      s.BMT.Mouse.t_extension ()



.. autoclass:: Object()
    :members:
    :inherited-members:
.. autoclass:: Link2()
    :members:
    :inherited-members:
.. autoclass:: Link3()
    :members:
    :inherited-members:
.. autoclass:: Link2_Ordered()
    :members:
    :inherited-members:



"""

if __name__ != "__main__" :
    MOM._Export_Module ()
### __END__ MOM.E_Type_Manager
