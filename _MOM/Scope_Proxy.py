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
#    MOM.Scope_Proxy
#
# Purpose
#    Scope-specific proxy for essential object- and link-types
#
# Revision Dates
#    16-Oct-2009 (CT) Creation
#    ««revision-date»»···
#--

from   _MOM import MOM
from   _TFL import TFL

import _TFL._Meta.Object

class Scope_Proxy (TFL.Meta.Object) :
    """Scope-specific proxy for essential object- and link-types."""

    def __init__ (self, etype, scope) :
        self._etype     = etype
        self.home_scope = scope
    # end def __init__

    def __call__ (self, * args, ** kw) :
        return self._etype (* args, scope = self.home_scope, ** kw)
    # end def __call__

    def exists (self, * epk) :
        return self.home_scope.ems.exists      (self._etype, epk)
    # end def exists

    def instance (self, * epk) :
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

# end class Scope_Proxy

class Scope_Proxy_O (Scope_Proxy) :
    """Scope-specific proxy for essential object-types."""

# end class Scope_Proxy_O

class Scope_Proxy_L (Scope_Proxy) :
    """Scope-specific proxy for essential link-types."""

# end class Scope_Proxy_L

if __name__ != "__main__" :
    MOM._Export ("*")
### __END__ MOM.Scope_Proxy
