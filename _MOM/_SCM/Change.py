# -*- coding: iso-8859-15 -*-
# Copyright (C) 2004-2013 Mag. Christian Tanzer. All rights reserved
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
#    MOM.SCM.Change
#
# Purpose
#    Model a toplevel change of a MOM scope
#
# Revision Dates
#     7-Oct-2009 (CT) Creation (factored from TOM.SCM.Change)
#    27-Nov-2009 (CT) Creation continued
#    14-Dec-2009 (CT) Major surgery
#    16-Dec-2009 (CT) Use `pid_query` to get `entity`
#    16-Dec-2009 (CT) Alias_Property `children` added and used
#    16-Dec-2009 (CT) `new_attr` added to `Create` and `Attr`
#    16-Dec-2009 (CT) `Copy` added
#    17-Dec-2009 (CT) `add_change`, `parent`, and `redo` added;
#                     `_create`, `_destroy`, and `_modify` factored;
#                     store raw values of `epk`;
#                     `_Entity_._repr` changed to sort;
#                     `as_pickle` and `from_pickle` added
#    17-Dec-2009 (CT) `Destroy.children` redefined to sort `history`
#    17-Dec-2009 (CT) `__iter__` added
#    18-Dec-2009 (CT) `as_pickle_cargo` and `from_pickle_cargo` factored
#    20-Jan-2010 (CT) Use `pid_query` of `E_Type_Manager` instead that of `EMS`
#     5-Feb-2010 (CT) `_Attr_` factored and `Attr_Composite` added
#    14-Feb-2010 (MG) Change inheritance of `Copy` back to `_Entity_`
#                     (otherwise the source entity would be created as well)
#     1-Mar-2010 (CT) `_Entity_._to_change` and `._to_save` factored
#    12-Mar-2010 (CT) `Attr_Composite.__new__` added to guard for
#                     `composite.owner`
#    16-Mar-2010 (CT) `add_callback`, `do_callbacks` and `remove_callback` added
#    17-May-2010 (CT) Changed `change_count` from class variable into
#                     instance variable
#    18-May-2010 (CT) `restore` added
#    18-May-2010 (CT) `Create` changed to store and use `pickle_cargo`
#    29-Jun-2010 (CT) Adapted to change of `entity.as_pickle_cargo`
#    30-Jun-2010 (CT) `tool_version` added
#     1-Jul-2010 (CT) `_Entity._restore` added
#                     (default implementation does nothing -- `Copy` needs it)
#    11-Aug-2010 (CT) `register` and handling for `last_cid` added
#    11-Aug-2010 (MG) `last_cid` special handling added
#    12-Aug-2010 (MG) `_Change_.register` parameter `scope` added
#    13-Aug-2010 (CT) `last_cid` handling corrected
#    16-Aug-2010 (MG) `_Entity_.register` add `last_cid` to the
#                     `attr_changes` dict of the scope
#     7-Sep-2010 (CT) `attr_changes` added
#     8-Sep-2010 (CT) `_register_last_cid` added
#     8-Sep-2010 (CT) Put `str` of `last_cid` into `new_attr` and `old_attr`
#     9-Sep-2010 (CT) `_new_attr` vs `new_attr` (don't store `last_cid`)
#    15-Sep-2010 (CT) `modified_attrs` added (to `Attr` and `Attr_Composite`)
#    16-Sep-2010 (CT) `modified_attrs` added `Create`
#    21-Oct-2010 (CT) `_modify_last_cid` factored and redefined for
#                     `Attr_Composite`
#    20-Jul-2011 (CT) Use `datetime.utcnow` instead of `datetime.now`
#    26-Jun-2012 (CT) Use `entity.type_name`, not `entity.Essence.type_name`
#    27-Jun-2012 (CT) Change `do_callbacks` to use `Essence.type_name`
#     4-Aug-2012 (CT) Change `Destroy.undo` to use `ems.restored`
#     4-Aug-2012 (CT) Change `_create` to use `entity.restore` if applicable
#     5-Aug-2012 (CT) Use `epk_raw_pid`, `get_raw_pid`
#     9-Sep-2012 (CT) Add `Create.c_time`, `.c_user`
#    11-Sep-2012 (CT) Add `_Attr_.do_callbacks` to call `ems.update`
#    12-Sep-2012 (CT) Streamline `_Entity_.do_callbacks`
#    14-Sep-2012 (MG) Change `do_callbacks` to support early update of
#                     entites
#     6-Dec-2012 (CT) Store `user.pid`, if any, else `user`
#    ««revision-date»»···
#--

from   _MOM               import MOM
from   _TFL               import TFL

import _MOM._SCM.History_Mixin
import _MOM._SCM.Recorder

import _TFL._Meta.Property
import _TFL._Meta.Once_Property

import datetime
import itertools
import pickle
import weakref

class _Change_ (MOM.SCM.History_Mixin) :
    """Model a change of a MOM Scope"""

    kind               = "Composite change"

    attr_changes       = ()
    callbacks          = None
    children           = TFL.Meta.Alias_Property ("history")
    cid                = None
    epk                = None
    modified_attrs     = ()
    parent             = None
    pid                = None
    time               = None
    tool_version       = None
    user               = None

    def __init__ (self) :
        self.__super.__init__ ()
        self.time = datetime.datetime.utcnow ()
    # end def __init__

    def add_change (self, child) :
        assert child.parent is None
        child.parent = self
        self.__super.add_change (child)
    # end def add_change

    def as_pickle (self, transitive = False) :
        cargo = self.as_pickle_cargo (transitive)
        return pickle.dumps (cargo, pickle.HIGHEST_PROTOCOL)
    # end def as_pickle

    def as_pickle_cargo (self, transitive = False) :
        children = self.children if transitive else ()
        result   = \
            ( self.__class__
            , self._pickle_attrs ()
            , [c.as_pickle_cargo (transitive) for c in children]
            )
        return result
    # end def as_pickle

    def do_callbacks (self) :
        pass
    # end def do_callbacks

    @classmethod
    def from_pickle (cls, string, parent = None) :
        return cls.from_pickle_cargo (pickle.loads (string), parent)
    # end def from_pickle

    @classmethod
    def from_pickle_cargo (cls, cargo, parent = None) :
        Class, attrs, children = cargo
        result                 = MOM.SCM.History_Mixin ()
        result.__class__       = Class
        result.parent          = parent
        result.children        = \
            [cls.from_pickle_cargo (c, result) for c in children]
        result.__dict__.update (attrs)
        return result
    # end def from_pickle

    def redo (self, scope) :
        for c in self.children :
            c.redo (scope)
    # end def redo

    def register (self, scope) :
        pass
    # end def register

    def restore (self, scope) :
        for c in self.children :
            c.restore (scope)
    # end def restore

    def _pickle_attrs (self) :
        return dict \
            ( cid          = self.cid
            , time         = self.time
            , user         = getattr (self.user, "pid", self.user)
            )
    # end def _pickle_attrs

    def _repr (self) :
        return self.kind
    # end def _repr

    def _repr_lines (self, level = 0) :
        result = ["%s<%s>" % ("  " * level, self._repr ())]
        for c in self.children :
            result.extend (c._repr_lines (level + 1))
        return result
    # end def _repr_lines

    def __iter__ (self) :
        yield self
        for c in self.children :
            yield c
    # end def __iter__

    def __repr__ (self) :
        return "\n  ".join (self._repr_lines ())
    # end def __repr__

# end class _Change_

class Undoable (_Change_) :
    """Model an undoable change of a MOM Scope"""

    Preferred_Recorder = MOM.SCM.Appender
    undoable           = True

    def undo (self, scope) :
        for c in reversed (self.children) :
            c.undo (scope)
    # end def undo

# end class Undoable

class Non_Undoable (_Change_) :
    """Model a change that cannot be undone"""

    Preferred_Recorder = MOM.SCM.Counter
    undoable           = False

# end class Non_Undoable

class _Entity_ (Undoable) :
    """Model a change of an MOM entity"""

    change_count = 1

    def __init__ (self, entity) :
        self.__super.__init__ ()
        self.epk          = entity.epk_raw
        self.epk_pid      = entity.epk_raw_pid
        self.pid          = getattr (entity, "pid", None)
        self.tool_version = entity.home_scope.Version.id
        self.type_name    = entity.type_name
        self.user         = entity.home_scope.user
        self.old_attr     = {}
        self._new_attr    = {}
        self._entity      = weakref.ref (entity)
    # end def __init__

    @classmethod
    def add_callback (cls, etype, callback) :
        if cls.callbacks is None :
            cls.callbacks = {}
        cls.callbacks [etype.type_name] = callback
    # end def add_callback

    @property
    def attr_changes (self) :
        return set \
            (itertools.chain (self._new_attr, self.old_attr, ["last_cid"]))
    # end def attr_changes

    def do_callbacks (self, scope) :
        callbacks = self.callbacks
        if callbacks :
            etype     = scope.entity_type (self.type_name)
            type_name = etype.Essence.type_name
            if type_name in callbacks :
                callbacks [type_name] (scope, self)
    # end def do_callbacks

    def entity (self, scope) :
        etm = scope [self.type_name]
        try :
            return etm.pid_query (self.pid)
        except LookupError :
            pass
    # end def entity

    @property
    def new_attr (self) :
        result = self._new_attr
        if self.cid :
            result = dict (result, last_cid = str (self.cid))
        return result
    # end def new_attr

    def register (self, scope) :
        try :
            _entity = self._entity
            del self._entity
        except AttributeError :
            try :
                entity = self.entity (scope)
            except LookupError :
                entity = None
        else :
            entity = _entity ()
        if entity :
            entity.last_cid = self.cid
    # end def register

    @classmethod
    def remove_callback (cls, etype) :
        if cls.callbacks is not None :
            for type_name in etype.type_name, etype.Essence.type_name :
                try :
                    del cls.callbacks [type_name]
                except KeyError :
                    pass
    # end def remove_callback

    def restore (self, scope) :
        self._restore        (scope)
        self.__super.restore (scope)
    # end def restore

    @TFL.Meta.Once_Property
    def type_repr (self) :
        return self.type_name
    # end def type_repr

    def _create (self, scope, attr, entity = None) :
        kw = dict (attr, raw = True)
        if entity is None :
            etm          = scope [self.type_name]
            kw ["__pid"] = self.pid
            result       = etm            (* self.epk_pid, ** kw)
        else :
            result       = entity.restore (* self.epk_pid, ** kw)
        return result
    # end def _create

    def _destroy (self, scope) :
        entity = self.entity (scope)
        if entity :
            entity.destroy ()
    # end def _destroy

    def _modify (self, scope, attr) :
        if attr :
            entity = self.entity (scope)
            if entity :
                self._modify_last_cid (scope, entity, attr)
                entity.set_raw (** attr)
    # end def _modify

    def _modify_last_cid (self, scope, entity, attr) :
        attr.setdefault ("last_cid", str (self.cid))
    # end def _modify_last_cid

    def _pickle_attrs (self) :
        return dict \
            ( self.__super._pickle_attrs ()
            , epk           = self.epk
            , epk_pid       = self.epk_pid
            , _new_attr     = self._new_attr
            , old_attr      = self.old_attr
            , pid           = self.pid
            , tool_version  = self.tool_version
            , type_name     = self.type_name
            )
    # end def _pickle_attrs

    def _repr (self) :
        result = ["%s %s %s" % (self.kind, self.type_repr, self.epk)]
        def format (d) :
            return ", ".join \
                (sorted ("%r : %r" % (k, v) for (k, v) in d.iteritems ()))
        if self.old_attr :
            result.append ("old-values = {%s}" % format (self.old_attr))
        if self.new_attr :
            result.append ("new-values = {%s}" % format (self.new_attr))
        return ", ".join (result)
    # end def _repr

    def _restore (self, scope) :
        pass
    # end def _restore

    def _to_change (self, entity, old_attr) :
        return dict \
            ( (a.name, a.get_raw_pid (entity))
            for a in entity.recordable_attrs if a.name in old_attr
            )
    # end def _to_change

    def _to_save (self, entity) :
        return dict \
            ( (a.name, a.get_raw_pid (entity))
            for a in entity.recordable_attrs
              if (not a.is_primary) and a.to_save (entity)
            )
    # end def _to_save

# end class _Entity_

class Copy (_Entity_) :
    """Model a change that copies an existing entity."""

    ### This is a container for a `Create` and a `Attr` change-object.

    kind = "Copy"

# end class Copy

class Create (_Entity_) :
    """Model a change that creates a new entity (object or link)"""

    kind = "Create"

    def __init__ (self, entity) :
        self.__super.__init__ (entity)
        self.c_time       = self.time
        self.c_user       = self.user
        self._new_attr    = self._to_save (entity)
        self.pickle_cargo = entity.as_pickle_cargo ()
    # end def __init__

    def do_callbacks (self, scope) :
        entity = self.entity      (scope)
        scope.ems.update          (entity, ("last_cid", ))
        self.__super.do_callbacks (scope)
    # end def do_callbacks

    @TFL.Meta.Once_Property
    def modified_attrs (self) :
        return set (("last_cid", ))
    # end def modified_attrs

    def redo (self, scope) :
        self._create      (scope, self.new_attr)
        self.__super.redo (scope)
    # end def redo

    def undo (self, scope) :
        self.__super.undo (scope)
        self._destroy     (scope)
    # end def undo

    def _pickle_attrs (self) :
        return dict \
            ( self.__super._pickle_attrs ()
            , c_time       = self.c_time
            , c_user       = getattr (self.c_user, "pid", self.c_user)
            , pickle_cargo = self.pickle_cargo
            )
    # end def _pickle_attrs

    def _restore (self, scope) :
        ### XXX Add legacy lifting
        return scope.add_from_pickle_cargo (* self.pickle_cargo)
    # end def _restore

# end class Create

class Destroy (_Entity_) :
    """Model a change that destroys an entity"""

    kind = "Destroy"

    @property
    def children (self) :
        return sorted \
            (self.history, key = TFL.Sorted_By ("type_name", "pid", "cid"))
    # end def children

    @children.setter
    def children (self, value) :
        self.history = value
    # end def children

    def __init__ (self, entity) :
        self.__super.__init__ (entity)
        self.old_attr = dict \
            (self._to_save (entity), last_cid = str (entity.last_cid))
    # end def __init__

    @property
    def new_attr (self) :
        return self._new_attr
    # end def new_attr

    def redo (self, scope) :
        self.__super.redo (scope)
        self._restore     (scope)
    # end def redo

    def undo (self, scope) :
        entity = scope.ems.restored (self.pid)
        self._create      (scope, self.old_attr, entity = entity)
        self.__super.undo (scope)
    # end def undo

    def _restore (self, scope) :
        self._destroy (scope)
    # end def _restore

# end class Destroy

class _Attr_ (_Entity_) :
    """Base class for changes that modify attributes of an entity"""

    kind = "Modify"

    def __init__ (self, entity, old_attr) :
        self.__super.__init__ (entity)
        self.old_attr = dict (old_attr, last_cid = str (entity.last_cid))
    # end def __init__

    def do_callbacks (self, scope) :
        self._update_entity       (scope)
        self.__super.do_callbacks (scope)
    # end def do_callbacks

    def redo (self, scope) :
        self._restore     (scope)
        self.__super.redo (scope)
    # end def redo

    def undo (self, scope) :
        self.__super.undo (scope)
        self._modify      (scope, self.old_attr)
    # end def undo

    def _restore (self, scope) :
        cargo = self.new_attr
        try :
            self._modify (scope, cargo)
        except Exception, exc :
            print exc
            print "   ", self.pid, self.epk, sorted (cargo.iteritems())
            raise
    # end def _restore

    def _update_entity (self, scope) :
        entity = self.entity (scope)
        scope.ems.update     (entity, self.new_attr)
    # end def _update_entity

# end class _Attr_

class Attr (_Attr_) :
    """Model a change that modifies attributes of an entity"""

    kind = "Modify"

    def __init__ (self, entity, old_attr) :
        self.__super.__init__ (entity, old_attr)
        self._new_attr = self._to_change (entity, old_attr)
    # end def __init__

    @TFL.Meta.Once_Property
    def modified_attrs (self) :
        return set (self.old_attr)
    # end def modified_attrs

# end class Attr

class Attr_Composite (_Attr_) :
    """Model a change that modifies attributes of a composite attribute of an
       entity
    """

    kind = "Modify/C"

    def __new__ (cls, composite, old_attr) :
        if composite.owner :
            return super (Attr_Composite, cls).__new__ \
                (cls, composite, old_attr)
    # end def __new__

    def __init__ (self, composite, old_attr) :
        entity = composite.owner
        owner  = getattr (entity, "owner", None)
        if owner is not None :
            entity = owner
        self.__super.__init__ (entity, old_attr)
        self.attr_name = composite.attr_name
        self._new_attr = self._to_change (composite, old_attr)
    # end def __init__

    def entity (self, scope) :
        entity = self.__super.entity (scope)
        if entity is not None :
            return getattr (entity, self.attr_name)
    # end def entity

    @TFL.Meta.Once_Property
    def modified_attrs (self) :
        return set ((self.attr_name, "last_cid"))
    # end def modified_attrs

    @TFL.Meta.Once_Property
    def type_repr (self) :
        return ".".join ((self.type_name, self.attr_name or "???"))
    # end def type_repr

    def _modify_last_cid (self, scope, entity, attr) :
        entity = self.__super.entity (scope)
        entity.set_raw (last_cid = attr.pop ("last_cid", self.cid))
    # end def _modify_last_cid

    def _pickle_attrs (self) :
        return dict \
            ( self.__super._pickle_attrs ()
            , attr_name   = self.attr_name
            )
    # end def _pickle_attrs

    def _update_entity (self, scope) :
        entity = self.__super.entity (scope)
        scope.ems.update     (entity, (self.attr_name, ))
    # end def _update_entity

# end class Attr_Composite

if __name__ != "__main__" :
    MOM.SCM._Export_Module ()
### __END__ MOM.SCM.Change
