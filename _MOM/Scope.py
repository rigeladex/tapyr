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
#    MOM.Scope
#
# Purpose
#    Provide scopes for objects and links of MOM meta object model
#
# Revision Dates
#    16-Oct-2009 (CT) Creation (factored from `TOM.Scope`)
#    27-Oct-2009 (CT) s/Scope_Proxy/E_Type_Manager/
#    27-Oct-2009 (CT) `_etm` and `_get_etm` added and used in `__getattr__`
#                     and `__getitem__`
#    26-Nov-2009 (CT) Use `except ... as ...` (3-compatibility)
#     4-Dec-2009 (MG) `Scope.new` added, `name` changed to `root_epk`
#     4-Dec-2009 (CT) Handling of `root_epk` corrected (needs to be a tuple)
#    ««revision-date»»···
#--

from   _MOM                  import MOM
from   _TFL                  import TFL

import _MOM.App_Type
import _MOM.Error
import _MOM._Pred.Err_and_Warn_List
import _MOM._SCM.Tracker

from   _TFL.Gauge_Logger      import Gauge_Logger
from   _TFL.predicate         import split_hst

import _TFL.Accessor
import _TFL.Context
import _TFL.Decorator
import _TFL.Ordered_Set
import _TFL._Meta.Lazy_Method
import _TFL._Meta.Object

import uuid

@TFL.Contextmanager
def unlocked (scope) :
    old_locked    = scope._locked
    scope._locked = False
    try :
        yield scope
    finally :
        scope._locked = old_locked
# end def unlocked

@TFL.Decorator
def _with_lock_check (f) :
    def _ (self, * args, ** kw) :
        if self._locked :
            raise RuntimeError ("Trying to modify locked scope %s." % self)
        f (self, * args, ** kw)
    return _
# end def _with_lock_check

class Scope (TFL.Meta.Object) :

    active                 = None
    Table                  = {}

    init_callback          = TFL.Ordered_Set ()
    kill_callback          = TFL.Ordered_Set ()
    is_universe            = False
    _deprecated_type_names = {}
    _locked                = False
    _pkg_ns                = None

    root                   = None
    _roots                 = None

    changes                = property (TFL.Getter.historian.total_changes)
    changes_to_save        = property (TFL.Getter.historian.since_snapshot)
    etypes                 = property (TFL.Getter.app_type.etypes)
    name                   = property (lambda s : s.qname or s.bname)

    PNS_Proxy              = None

    class Pkg_NS :
        """Just a container for the scope-specific etype-proxies for the
           essential classes of a package-namespace (delegates everything
           else to the original package namespace).
        """

        def __init__ (self, scope, pns, qn) :
            self._scope = scope
            self._pns   = pns
            self._qname = qn
        # end def __init__

        def __getattr__ (self, name) :
            scope  = self._scope
            etypes = scope.etypes
            pkg_ns = scope._pkg_ns
            qname  = ".".join ((self._qname, name))
            result = None
            if qname in pkg_ns :
                result = pkg_ns [qname]
            elif qname in etypes :
                etype  = etypes [qname]
                result = scope._etm [qname] = etype.Manager (etype, scope)
                setattr (self, name, result)
            else :
                result = getattr (self._pns, name)
            return result
        # end def __getattr__

    # end class Pkg_NS

    def __init__ ( self, app_type, db_uri
                 , guid      = None
                 , root_epk  = ()
                 , user      = None
                 , create_db = False
                 ) :
        with self._self_active () :
            if isinstance (app_type, (str, unicode)) :
                app_type             = MOM.App_Type.instance (app_type)
            self.app_type            = app_type
            self.bname               = "__".join (str (e) for e in root_epk)
            self.guid                = self._new_guid (guid)
            self._etm                = {}
            self._pkg_ns             = {}
            self._roots              = {}
            self.root                = None
            self.snapshot_count      = 0
            self.historian           = MOM.SCM.Tracker (self)
            self.user                = user
            self.ems                 = app_type.EMS    (self, db_uri, create_db)
            self._attr_errors        = []
            self._setup_pkg_ns         (app_type)
            if root_epk :
                self._setup_root       (app_type, root_epk)
            self._run_init_callbacks   ()
        ### copy `kill_callback` from class into instance to allow appending
        ### of instance specific callbacks by clients
        self.kill_callback = self.kill_callback [:]
    # end def __init__

    @_with_lock_check
    def add (self, entity) :
        """Adds `entity` to scope `self`."""
        self.ems.add       (entity)
        self.record_change (MOM.SCM.Entity_Change_Create, entity)
    # end def add

    @classmethod
    def add_init_callback (cls, * callbacks) :
        """Add all `callbacks` to `init_callback`. These
           callbacks are executed whenever a scope is
           created (the new scope is passed as the single argument to each
           callback).
        """
        cls.init_callback.extend (callbacks)
    # end def add_init_callback

    @TFL.Meta.Class_and_Instance_Method
    def add_kill_callback (soc, * callbacks) :
        """Add all `callbacks` to `kill_callback` of the scope class
           or instance. These callbacks` are executed whenever the
           scope is destroyed (the scope to be destroyed is passed as
           the single argument to each callback).
        """
        soc.kill_callback.extend (callbacks)
    # end def add_kill_callback

    @TFL.Contextmanager
    def as_active (self) :
        """Provide context with `self` as active scope."""
        old_active = Scope.active
        try :
            Scope.active = self
            yield
        finally :
            Scope.active = old_active
    # end def as_active

    @TFL.Meta.Lazy_Method_RLV
    def compute_defaults_internal (self, gauge = Gauge_Logger ()) :
        """Lazily call `compute_defaults_internal` for all entities."""
        with self.as_active () :
            sk = TFL.Sorted_By ("rank", "id")
            gauge.reset ("Compute default internal attributes")
            for et in sorted (self.etypes, key = TFL.Getter.rank) :
                et.compute_type_defaults_internal ()
            for e in self.entity_iter_gauge (gauge) :
                e.reset_syncable (label = "Reset syncable attributes")
            for e in self.entity_iter_gauge (gauge, sort_key = sk) :
                e.sync_attributes (label = "Sync attributes")
            for e in self.entity_iter_gauge \
                    ( gauge
                    , sort_key = sk
                    , label = "Computing default internal attributes"
                    ) :
                try :
                    e.compute_defaults_internal ()
                except StandardError as exc :
                    print \
                        ( "Exception in compute_defaults_internal for %s:\n    %s"
                        % (e, exc)
                        )
                    if __debug__ :
                        traceback.print_exc ()
    # end def compute_defaults_internal

    def count_change (self) :
        self.historian.count_change ()
    # end def count_change

    def destroy (self) :
        if self.qname in Scope.Table :
            del Scope.Table [self.qname]
        self._locked = False
        self.stop_change_recorder ()
        self.app_type.run_kill_callbacks (self)
        for c in self.kill_callback :
            c (self)
        del self.kill_callback
        self.root = None
        for d in (self._roots, self._pkg_ns) :
            d.clear ()
        ### XXX break circular links (references to this scope from
        ###     importers... )
        if Scope.active == self :
            Scope.active = None
        self.__dict__.clear ()
    # end def destroy

    def entity_iter (self) :
        """Yields all objects and links alive in `self` in unspecified
           order.
        """
        return iter (self.ems)
    # end def entity_iter

    def entity_iter_gauge (self, gauge = Gauge_Logger (), sort_key = None, label = None) :
        """Yields all entities alive in `self` in the
           order specified by `sort_key`.
        """
        gauge.reset \
            ( g_delta = 100
            , g_range = self.ems.t_count (MOM.Id_Entity)
            , label   = label
            )
        entities = iter (self.ems)
        if sort_key :
            entities = sorted (entities, key = sort_key)
        i = 1
        for e in entities :
            yield e
            if i == 100 :
                gauge.inc (100)
                i = 0
            i += 1
    # end def entity_iter_gauge

    def entity_type (self, entity) :
        if isinstance (entity, basestring) :
            name = entity
        else :
            name = entity.Essence.type_name
        return self.app_type.entity_type (self._canonical_name (name))
    # end def entity_type

    @TFL.Meta.Lazy_Method_RLV
    def g_incorrect (self, gauge = Gauge_Logger ()) :
        """Returns all objects which are globally incorrect (i.e., violating
           the object's `system` predicates).
        """
        try :
            self.compute_defaults_internal (gauge)
        except MOM.Error.Invariant_Error :
            pass
        with self.as_active () :
            return self._check_inv (gauge, "system")
    # end def g_incorrect

    def has_changed (self) :
        """Indicates whether something saveworthy has changed"""
        if self.historian.has_changed () :
            i = 0
            for entity in self.ems :
                if entity.has_changed () :
                    return True
                i += 1
            return self.snapshot_count != i
        return False
    # end def has_changed

    @classmethod
    def new (cls, app_type, db_uri, root_epk = (), user = None) :
        return cls \
            ( app_type, db_uri
            , root_epk  = root_epk
            , user      = user
            , create_db = True
            )
    # end def new

    @TFL.Meta.Lazy_Method_RLV
    def i_incorrect (self, gauge = Gauge_Logger ()) :
        """Returns all objects which are object-wise incorrect (i.e., violating
           the object's `object` predicates).
        """
        with self.as_active () :
            return self._check_inv (gauge, "object")
    # end def i_incorrect

    def make_snapshot (self) :
        self.historian.make_snapshot ()
        i = 0
        for o in self.entity_iter () :
            o.make_snapshot ()
            i += 1
        self.snapshot_count = i
    # end def make_snapshot

    @TFL.Contextmanager
    def nested_change_recorder (self, Change, * args, ** kw) :
        with self.historian.nested_recorder (Change, * args, ** kw) :
            yield
    # end def nested_change_recorder

    def record_change (self, Change, * args, ** kw) :
        return self.historian.record (Change, * args, ** kw)
    # end def record_change

    @_with_lock_check
    def remove (self, entity) :
        """Remove `entity` from scope `self`"""
        assert (entity != self.root)
        Change = MOM.SCM.Entity_Change_Destroy
        with self.historian.nested_recorder (Change, entity) :
            self.ems.remove (entity)
            entity._destroy ()
    # end def remove

    @_with_lock_check
    def rename (self, entity, new_epk, renamer) :
        old_epk = entity.epk
        self.ems.rename    (entity, new_epk, renamer)
        self.record_change (MOM.SCM.Entity_Change_Rename, entity, old_epk)
    # end def rename

    def start_change_recorder (self) :
        if not self.historian._rec_stack :
            self.historian.push_recorder (MOM.SCM.Tracker.Preferred_Recorder)
            self.make_snapshot ()
    # end def start_change_recorder

    def stop_change_recorder (self) :
        if self.historian._rec_stack :
            self.historian.pop_recorder ()
    # end def stop_change_recorder

    def _add_to_scopes (self) :
        for n in (self.qname, ) :
            if n :
                Scope.Table [n] = self
    # end def _add_to_scopes

    def _canonical_name (self, name) :
        return self._deprecated_type_names.get (name, name)
    # end def _canonical_name

    def _check_inv (self, gauge, kind) :
        err_result = []
        wrn_result = []
        for e in self.entity_iter_gauge \
            (gauge, sort_key = sk, label = "Checking %s invariants" % kind) :
            try :
                ews = e._pred_man.check_kind (kind, e)
                if ews.errors :
                    err_result.append (e)
                if ews.warnings :
                    wrn_result.append (e)
            except StandardError :
                print "Error during evaluation of invariant for ", e
                traceback.print_exc ()
                err_result.append (e)
        return MOM.Pred.Err_and_Warn_List (err_result, wrn_result)
    # end def _check_inv

    def _get_etm (self, name) :
        try :
            result = self._etm [name]
        except KeyError :
            pn, _, rest = split_hst (name, ".")
            try :
                result = self._pkg_ns [pn]
            except KeyError :
                raise AttributeError (name)
            for k in rest.split (".") :
                result = getattr (result, k)
            self._etm [name] = result
        return result
    # end def _get_etm

    def _new_guid (self, guid) :
        if not guid :
            guid = uuid.uuid4 ().bytes
        return guid
    # end def _new_guid

    def _run_init_callbacks (self) :
        for c in self.init_callback :
            c (self)
        self.app_type.run_init_callbacks (self)
    # end def _run_init_callbacks

    @TFL.Contextmanager
    def _self_active (self) :
        old_active = Scope.active
        try :
            Scope.active = self
            yield
        except :
            Scope.active = old_active
            raise
    # end def _self_active

    def _setup_pkg_ns (self, app_type) :
        _pkg_ns = self._pkg_ns
        for name, pns in sorted (app_type.PNS_Map.iteritems (), key = len) :
            if name not in _pkg_ns :
                _pkg_ns [name] = self.Pkg_NS (self, pns, name)
    # end def _setup_pkg_ns

    def _setup_root (self, app_type, root_epk) :
        if app_type.Root_Type :
            ### use `__new__` here to allow setting of `self.root` and
            ### `self._roots` before `__init__` of the root object is
            ### executed and might refer to `self.root`
            Root_Type = self.entity_type (app_type.Root_Type)
            self.root = root = Root_Type.__new__ (* root_epk, scope = self)
            self._roots [root.Essence.type_base_name] = root
            root.__init__           (* root_epk)
            root_cls.after_creation (root)
    # end def _setup_root

    def __getattr__ (self, name) :
        if "." in name :
            if name in self._etm :
                return self._etm [name]
            else :
                return self._get_etm (name)
        else :
            for dict in self._roots, self._pkg_ns :
                try :
                    result = dict [name]
                except KeyError :
                    pass
                else :
                    setattr (self, name, result)
                    return result
            return getattr (self.app_type, name)
    # end def __getattr__

    def __getitem__ (self, name) :
        try :
            return self._get_etm (name)
        except AttributeError :
            raise KeyError (name)
    # end def __getitem__

    def __iter__ (self) :
        return iter (self.ems)
    # end def __iter__

    def __str__ (self) :
        return "%s `%s`" % (self.__class__.__name__, self.bname)
    # end def __str__

# end class Scope

if __name__ != "__main__" :
    MOM._Export ("*")
### __END__ MOM.Scope
