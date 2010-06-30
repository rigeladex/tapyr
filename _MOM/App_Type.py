# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009-2010 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package _MOM.
#
# This module is free software; you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this library. If not, see <http://www.gnu.org/licenses/>.
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
#    23-Nov-2009 (CT) `finalized` added and used to guard `add_type`
#    23-Nov-2009 (CT) Documentation added
#    30-Dec-2009 (CT) s/Package_NS/PNS/
#    14-Jan-2010 (CT) `PNS_Aliases` added
#     4-Mar-2010 (CT) `delete_database` added
#    24-Jun-2010 (CT) `Url` added
#    24-Jun-2010 (CT) `db_sig` and `db_version_hash` added
#    30-Jun-2010 (CT) `Once_Property` for `Version` added
#    ««revision-date»»···
#--

from   _MOM                  import MOM
from   _TFL                  import TFL

import _MOM._EMS.Backends

import _TFL.Ordered_Set
import _TFL._Meta.Object
import _TFL._Meta.Once_Property

import base64
import hashlib

class _App_Type_ (TFL.Meta.Object) :
    """Encapsulate information about a specific application type."""

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

    def Url (self, db_url) :
        if isinstance (db_url, basestring) :
            _, _, DBS = MOM.EMS.Backends.get (db_url)
            return DBS.Url (db_url, self.ANS)
        return db_url
    # end def Url

    @TFL.Meta.Once_Property
    def Version (self) :
        return self.ANS.Version
    # end def Version

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

    @TFL.Meta.Once_Property
    def db_version_hash (self) :
        hash = hashlib.sha224 (str (self.db_sig)).digest ()
        return base64.b64encode (hash, "_-").replace ("=", "")
    # end def db_version_hash

    @TFL.Meta.Once_Property
    def db_sig (self) :
        return tuple (T.db_sig for T in self._T_Extension if T.relevant_root)
    # end def db_sig

    @property
    def Root_Type (self) :
        if self.Root_Type_Name :
            return self.etypes [self.Root_Type_Name]
    # end def Root_Type

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
        self.PNS_Aliases      = parent.PNS_Aliases
        self.finalized        = False
        import _MOM.Entity
        MOM.Entity.m_setup_etypes (self)
        self.finalized        = True
    # end def __init__

    def add_type (self, etype) :
        assert not self.finalized
        pns = etype.PNS
        qn  = pns._Package_Namespace__qname
        self.PNS_Map [qn]                      = pns
        self.etypes  [etype.Essence.type_name] = etype
        self._T_Extension.append (etype)
    # end def add_type

    def delete_database (self, db_url) :
        if db_url :
            url = self.Url (db_url)
            self.DBW.delete_database (url)
    # end def delete_database

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

    def __init__ (self, name, ANS, Root_Type_Name = None, PNS_Aliases = None) :
        assert bool (name)
        assert name not in self.Table
        self.Table [name]   = self
        self.name           = name
        self.ANS            = ANS
        self.Root_Type_Name = Root_Type_Name
        self.derived        = {}
        self.init_callback  = TFL.Ordered_Set ()
        self.kill_callback  = TFL.Ordered_Set ()
        self.PNS_Map        = {}
        self.PNS_Aliases    = PNS_Aliases if PNS_Aliases is not None else {}
    # end def __init__

    def Derived (self, EMS, DBW) :
        """Return an :class:`_App_Type_D_` derived for a specific
           combination of `EMS` and `DBW`.
        """
        if (EMS, DBW) in self.derived :
            result = self.derived [EMS, DBW]
        else :
            result = self.derived [EMS, DBW] = _App_Type_D_ (self, EMS, DBW)
        return result
    # end def Derived

# end class App_Type

__doc__ = """
Class `MOM.App_Type`
====================

.. class:: App_Type

    `MOM.App_Type` defines the characteristics of a specific
    application. It encapsulates information about the essential
    object model of the application.

    Each `App_Type` is instantiated with the attributes:

    .. attribute:: name

      Name of the app-type.

    .. attribute:: ANS

      Specifies the package namespace of the application (Application
      Name Space).

    .. attribute:: Root_Type_Name

      Specifies the name of the `root type` of the application, if
      any. If there is a root type, each sscope created has its own
      specific root object which is an instance of the root type.

    `App_Type` provides the methods:

    .. automethod:: add_init_callback
    .. automethod:: add_kill_callback
    .. automethod:: Derived

.. class:: _App_Type_D_

    A derived `App_Type` adds a specific `entity manager strategy`
    `EMS` and a specific data base wrapper `DBW` to a parent
    `App_Type`.

    For each essential objecta nd link tyoe of an application, a
    derived `App_Type` holds an app-type specifc entity type (short
    `etype`) derived from the essential type. For some `DBWs`, the
    etype might contain additional properties injected by the `DBW`.

    As the etypes are automatically created, when a derived `App_Type`
    is instantiated, all essential classes must be defined by then.
    The current implementation does not allow defining essential
    object or link classes after the creation of the app-type.

    Derived `App_Types` provide the additonal properties:

    .. attribute:: Root_Type

      The entity type of the root object, if any.

    .. attribute:: etypes

      Maps names of essential associations and objects to the
      appropriate app-type specific classes.

          For each essential class defined for a `App_Type`, the meta
          machinery automatically creates an app-type specific class that
          combines essential properties and app-type specific properties
          of the class in question.

    .. automethod:: entity_type


"""

if __name__ != "__main__" :
    MOM._Export ("*")
### __END__ MOM.App_Type
