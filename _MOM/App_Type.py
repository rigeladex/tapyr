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
#    ««revision-date»»···
#--

from   _MOM                  import MOM
from   _TFL                  import TFL

import _TFL.Ordered_Set
import _TFL._Meta.Object

class App_Type (TFL.Meta.Object) :
    """Encapsulate information about a specific application type."""

    Table            = {}

    def __init__ (self, name, ANS, Root_Type_Name = None) :
        assert bool (name)
        assert name not in self.Table
        self.Table [name]      = self
        self.name              = name
        self.ANS               = ANS
        self.Root_Type_Name    = Root_Type_Name
        self.EMS               = None
        self.DBW               = None
        self.etypes            = {}
        self._T_Extension      = []
        self.derived           = {}
        self.parent            = None
        self.init_callback     = TFL.Ordered_Set ()
        self.kill_callback     = TFL.Ordered_Set ()
        self.PNS_Map           = {}
    # end def __init__

    def Derived (self, EMS, DBW) :
        assert self.parent is None
        assert not (EMS, DBW) in self.derived
        result                  = self.__class__.__new__ (self.__class__)
        self.derived [EMS, DBW] = result
        result.name             = "__".join \
            ((self.name, EMS.type_name, DBW.type_name))
        result.ANS              = self.ANS
        result.Root_Type_Name   = self.Root_Type_Name
        result.EMS              = EMS
        result.DBW              = DBW
        result.etypes           = {}
        result._T_Extension     = []
        result.derived          = None
        result.parent           = self
        result.init_callback    = TFL.Ordered_Set ()
        result.kill_callback    = TFL.Ordered_Set ()
        result.PNS_Map          = self.PNS_Map
        return result
    # end def Derived

    @property
    def Root_Type (self) :
        if self.Root_Type_Name :
            return self.etypes [self.Root_Type_Name]
    # end def Root_Type

    def add_init_callback (self, * callbacks) :
        """Add all `callbacks` to `init_callback`. These
           callbacks are executed whenever a :class:`~_TOM.Scope.Scope` is
           created (the new scope is passed as the single argument to each
           callback).
        """
        self.init_callback.extend (callbacks)
    # end def add_init_callback

    def add_kill_callback (self, * callbacks) :
        """Add all `callbacks` to `kill_callback`. These
           callbacks` are executed whenever a :class:`~_TOM.Scope.Scope` is
           destroyed (the scope to be destroyed is passed as the single
           argument to each callback).
        """
        self.kill_callback.extend (callbacks)
    # end def add_kill_callback

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

    @staticmethod
    def instance (name) :
        return App_Type.Table [name]
    # end def instance

    def run_init_callbacks (self, scope) :
        if self.parent :
            for c in self.parent.init_callback :
                c (scope)
        for c in self.init_callback :
            c (scope)
    # end def run_init_callbacks

    def run_kill_callbacks (self, scope) :
        for c in self.kill_callback :
            c (scope)
        if self.parent :
            for c in self.parent.kill_callback :
                c (scope)
    # end def run_kill_callbacks

    def setup_etypes (self) :
        """Setup EMS- and DBW -specific essential types for all classes in
           `self.parent._T_Extension`.
        """
        assert self.parent
        assert self.parent._T_Extension
        self.parent._T_Extension [0].m_setup_etypes (self)
    # end def setup_etypes

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

# end class App_Type


if __name__ != "__main__" :
    MOM._Export ("*")
### __END__ MOM.App_Type
