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
            args = tuple (self._role_to_raw_iter (args))
        return self.__super.__call__ (* args, ** kw)
    # end def __call__

    def exists (self, * epk, ** kw) :
        if kw.pop ("raw", False) :
            epk = tuple (self._cooked_epk_iter (epk))
        else :
            epk = tuple (self._role_to_cooked_iter (args))
        return self.__super.exists   (* epk, ** kw)
    # end def exists

    def instance (self, * epk, ** kw) :
        if kw.pop ("raw", False) :
            epk = tuple (self._cooked_epk_iter (epk))
        else :
            epk = tuple (self._role_to_cooked_iter (args))
        return self.__super.instance (* epk, ** kw)
    # end def instance

    def _cooked_epk_iter (self, epk) :
        for (pka, v) in zip (self._etype.primary, epk) :
            if getattr (pka, "role_type", None) :
                ### Allow role attributes to be passed as objects even if
                ### `raw` is specified
                v = self._cooked_role (pka, v)
            else :
                v = pka.from_string   (v, None)
            yield v
    # end def _cooked_epk

    def _cooked_role (self, r, v) :
        result = v
        if not isinstance (result, MOM.Entity) :
            if not isinstance (v, (tuple, list)) :
                v = (v, )
            result = r.from_string (v, None)
        return result
    # end def _cooked_role

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
                if not isinstance (v, basestring) :
                    v = r.as_code (v)
            yield v
    # end def _role_to_raw_iter

# end class Link

if __name__ != "__main__" :
    MOM._Export_Module ()
### __END__ MOM.E_Type_Manager
