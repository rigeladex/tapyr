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
#    ««revision-date»»···
#--

from   _MOM import MOM
from   _TFL import TFL

import _TFL._Meta.Object

from   _TFL.predicate import paired

class Id_Entity (TFL.Meta.Object) :
    """Scope-specific manager for essential object- and link-types."""

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
        return self.home_scope.ems.s_count     (self._etype)
    # end def s_count

    def s_extension (self, sort_key = None) :
        return self.home_scope.ems.s_extension (self._etype, sort_key)
    # end def s_extension

    @property
    def t_count (self) :
        return self.home_scope.ems.t_count     (self._etype)
    # end def t_count

    def t_extension (self, sort_key = None) :
        return self.home_scope.ems.t_extension (self._etype, sort_key)
    # end def t_extension

    def __getattr__ (self, name) :
        return getattr (self._etype, name)
    # end def __getattr__

# end class Id_Entity

class Object (Id_Entity) :
    """Scope-specific manager for essential object-types."""

    def exists (self, * epk, ** kw) :
        if kw.pop ("raw", False) :
            epk = tuple (self._cooked_epk_iter (epk))
        return self.__super.exists   (* epk, ** kw)
    # end def exists

    def instance (self, * epk, ** kw) :
        if kw.pop ("raw", False) :
            epk = tuple (self._cooked_epk_iter (epk))
        return self.__super.instance (* epk, ** kw)
    # end def instance

    def _cooked_epk_iter (self, epk) :
        for (pka, v) in zip (self._etype.primary, epk) :
            yield pka.from_string (v, None)
    # end def _cooked_epk

# end class Object

class Link (Id_Entity) :
    """Scope-specific manager for essential link-types."""

    def __call__ (self, * args, ** kw) :
        if kw.get ("raw", False) :
            args = tuple (self._role_to_raw_iter    (args))
        else :
            args = tuple (self._role_to_cooked_iter (args))
        return self.__super.__call__ (* args, ** kw)
    # end def __call__

    def applicable_objects (self, objects) :
        """Returns all `objects` not refusing to be linked by `self._etype`."""
        type_name = self._etype.Essence.type_name
        return [o for o in objects if type_name not in o.refuse_links]
    # end def applicable_objects

    def exists (self, * epk, ** kw) :
        if kw.pop ("raw", False) :
            epk = tuple (self._cooked_epk_iter (epk))
        else :
            epk = tuple (self._role_to_cooked_iter (epk))
        return self.__super.exists   (* epk, ** kw)
    # end def exists

    def instance (self, * epk, ** kw) :
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

    def _cooked_epk_iter (self, epk) :
        for (pka, v) in zip (self._etype.primary, epk) :
            if getattr (pka, "role_type", None) :
                ### Allow role attributes to be passed as objects even if
                ### `raw` is specified
                v = self._cooked_role (pka, v)
            else :
                v = pka.from_string   (v, None)
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
                result.update (query (r, obj))
        return result
    # end def _links_of_obj

    def _role_to_cooked_iter (self, epk) :
        for (r, v) in paired (self._etype.Roles, epk) :
            if r is not None :
                ### Allow role attributes to be passed as raw values even if
                ### `raw` is not specified
                v = self._cooked_role (r, v)
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

    def _role_query (self, role, obj, q_name) :
        query = getattr (self.home_scope.ems, q_name)
        return query (role, obj)
    # end def _role_query

# end class Link2

if __name__ != "__main__" :
    MOM._Export_Module ()
### __END__ MOM.E_Type_Manager
