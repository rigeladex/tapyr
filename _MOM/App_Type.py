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
#    MOM.App_Type
#
# Purpose
#    Encapsulate information about a specific application type
#
# Revision Dates
#    16-Oct-2009 (CT) Creation
#    18-Oct-2009 (CT) Creation continued
#    18-Nov-2009 (CT) `_App_Type_` and `_App_Type_D_` factored
#    ««revision-date»»···
#--

from   _MOM                  import MOM
from   _TFL                  import TFL

import _TFL.Ordered_Set
import _TFL._Meta.Object

class _App_Type_ (TFL.Meta.Object) :
    """Encapsulate information about a specific application type."""

    @property
    def Root_Type (self) :
        if self.Root_Type_Name :
            return self.etypes [self.Root_Type_Name]
    # end def Root_Type

    def add_init_callback (self, * callbacks) :
        """Add all `callbacks` to `init_callback`. These
           callbacks are executed whenever a :class:`~_MOM.Scope.Scope` is
           created (the new scope is passed as the single argument to each
           callback).
        """
        self.init_callback.extend (callbacks)
    # end def add_init_callback

    def add_kill_callback (self, * callbacks) :
        """Add all `callbacks` to `kill_callback`. These
           callbacks` are executed whenever a :class:`~_MOM.Scope.Scope` is
           destroyed (the scope to be destroyed is passed as the single
           argument to each callback).
        """
        self.kill_callback.extend (callbacks)
    # end def add_kill_callback

    @staticmethod
    def instance (name) :
        return App_Type.Table [name]
    # end def instance

    def run_init_callbacks (self, scope) :
        for c in self.init_callback :
            c (scope)
    # end def run_init_callbacks

    def run_kill_callbacks (self, scope) :
        for c in self.kill_callback :
            c (scope)
    # end def run_kill_callbacks

    def __getitem__ (self, name) :
        return self.etypes [name]
    # end def __getitem__

    def __repr__ (self) :
        return "%s (%r, %s)" % \
            ( self.__class__.__name__
            , self.name, self.ANS._Package_Namespace__qname
            )
    # end def __repr__

    def __str__ (self) :
        return self.name
    # end def __str__

# end class _App_Type_

class _App_Type_D_ (_App_Type_) :
    """App_Type derived for a specific combination of `EMS` and `DBW`"""

    def __init__ (self, parent, EMS, DBW) :
        assert parent
        self.name             = "__".join \
            ((parent.name, EMS.type_name, DBW.type_name))
        self.ANS              = parent.ANS
        self.Root_Type_Name   = parent.Root_Type_Name
        self.EMS              = EMS
        self.DBW              = DBW
        self.etypes           = {}
        self._T_Extension     = []
        self.derived          = None
        self.parent           = parent
        self.init_callback    = TFL.Ordered_Set ()
        self.kill_callback    = TFL.Ordered_Set ()
        self.PNS_Map          = parent.PNS_Map
        import _MOM.Entity
        MOM.Entity.m_setup_etypes (self)
    # end def __init__

    def add_type (self, etype) :
        pns = etype.Package_NS
        qn  = pns._Package_Namespace__qname
        self.PNS_Map [qn]                      = pns
        self.etypes  [etype.Essence.type_name] = etype
        self._T_Extension.append (etype)
    # end def add_type

    def entity_type (self, entity) :
        """Returns app-type specific type of `entity`."""
        if isinstance (entity, basestring) :
            name = entity
        else :
            name = entity.Essence.type_name
        result   = self.etypes.get (name)
        return result
    # end def entity_type

    def run_init_callbacks (self, scope) :
        for c in self.parent.init_callback :
            c (scope)
        self.__super.run_init_callbacks (scope)
    # end def run_init_callbacks

    def run_kill_callbacks (self, scope) :
        self.__super.run_kill_callbacks (scope)
        for c in self.parent.kill_callback :
            c (scope)
    # end def run_kill_callbacks

# end class _App_Type_D_

class App_Type (_App_Type_) :
    """Encapsulate information about a specific application type."""

    Table            = {}

    DBW              = None
    EMS              = None
    etypes           = None
    _T_Extension     = None
    parent           = None

    def __init__ (self, name, ANS, Root_Type_Name = None) :
        assert bool (name)
        assert name not in self.Table
        self.Table [name]      = self
        self.name              = name
        self.ANS               = ANS
        self.Root_Type_Name    = Root_Type_Name
        self.derived           = {}
        self.init_callback     = TFL.Ordered_Set ()
        self.kill_callback     = TFL.Ordered_Set ()
        self.PNS_Map           = {}
    # end def __init__

    def Derived (self, EMS, DBW) :
        if (EMS, DBW) in self.derived :
            result = self.derived [EMS, DBW]
        else :
            result = self.derived [EMS, DBW] = _App_Type_D_ (self, EMS, DBW)
        return result
    # end def Derived

# end class App_Type

if __name__ != "__main__" :
    MOM._Export ("*")
### __END__ MOM.App_Type
