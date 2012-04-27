# -*- coding: iso-8859-15 -*-
# Copyright (C) 2009-2012 Mag. Christian Tanzer. All rights reserved
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
#    10-Dec-2009 (CT) `as_active` changed to use `Scope.LET` instead of
#                     home-grown code
#    10-Dec-2009 (CT) `compute_defaults_internal` and `check_inv` corrected
#    10-Dec-2009 (CT) Scope initialization revamped
#    10-Dec-2009 (CT) `id` added
#    10-Dec-2009 (CT) Allow instance-specific `init_callbacks`
#    14-Dec-2009 (CT) `copy` added
#    14-Dec-2009 (CT) `unlocked` made method
#    16-Dec-2009 (CT) `commit` added
#    16-Dec-2009 (CT) Calls to `ems.register_change` added to `record_change`
#                     and `nested_change_recorder`
#    17-Dec-2009 (CT) `_init_context` changed to call `start_change_recorder`
#    17-Dec-2009 (CT) Don't record `add` and `remove` of electric objects
#    17-Dec-2009 (CT) Don't `register_change` for empty composite changes
#    17-Dec-2009 (CT) `async_changes` and `query_changes` added
#    17-Dec-2009 (CT) `user_diff` and `user_equal` added
#    21-Dec-2009 (CT) `relevant_roots` added, `_register_root` factored
#    21-Dec-2009 (CT) `destroy` changed to call `ems.close`
#    30-Dec-2009 (MG) `Scope.copy` use `epk_raw` instead of `epk`
#    14-Jan-2010 (CT) `_setup_pkg_ns` changed to handle `_Outer` and
#                     `PNS_Aliases`
#    16-Jan-2010 (CT) `_outer_pgk_ns` factored
#    19-Jan-2010 (CT) `rollback` added
#    27-Jan-2010 (CT) `rollback` changed to call `count_change`
#     8-Feb-2010 (CT) `remove` changed to call `entity._destroy` before
#                     `ems.remove`
#     8-Feb-2010 (CT) `snapshot` removed
#    15-Feb-2010 (CT) `attr_changes` added
#    16-Mar-2010 (CT) `record_change` changed to call `result.callbacks`, if any
#    17-May-2010 (CT) `add_from_pickle_cargo` added and used for `copy`
#    17-May-2010 (CT) `migrate` added
#    17-May-2010 (CT) `nested_change_recorder` and `record_change` changed to
#                     set `result.user`
#    18-May-2010 (CT) `migrate` changed to not filter `query_changes` to
#                     `parent = None`
#    19-May-2010 (MG) `rollback` clear `attr_changes` added
#    26-May-2010 (CT) `self.db_errors = []` added to `_init_context`
#    24-Jun-2010 (CT) Adpated to change of `db_url`
#    29-Jun-2010 (CT) s/from_pickle_cargo/from_attr_pickle_cargo/
#    29-Jun-2010 (CT) Adapted to change of `entity.as_pickle_cargo`
#    30-Jun-2010 (CT) `_locked` and friends removed
#    30-Jun-2010 (CT) `ilk` added
#     1-Jul-2010 (CT) Adapted to `Id_Entity.as_pickle_cargo` change (`pid` last)
#     1-Jul-2010 (CT) `migrate` renamed to `copy`
#    11-Aug-2010 (CT) Optional argument `ignore` added to `user_diff`
#    17-Aug-2010 (CT) Properties `db_meta_data` and `readonly` added
#    14-Sep-2010 (CT) `r_incorrect` added (and optional argument `eiter`
#                     added to `_check_inv`)
#    14-Sep-2010 (CT) Call to `r_incorrect` added to `commit`
#    15-Sep-2010 (CT) `attr_changes` removed
#    28-Sep-2010 (CT) `temp_change_recorder` added
#    30-Nov-2010 (CT) `Fatal_Exceptions` added
#     8-Mar-2011 (CT) `pid_query` added
#    21-Mar-2011 (MG) `copy` assert fixed
#     9-Sep-2011 (CT) Use `.E_Type` instead of `._etype`
#    19-Jan-2012 (CT) Change `add` to consider `entity._home_scope`
#    11-Apr-2012 (CT) Change `add` and `add_from_pickle_cargo` to call
#                     `._finish__init__` after `self.ems.add`
#    15-Apr-2012 (CT) Adapted to changes of `MOM.Error`
#    27-Apr-2012 (CT) Add call to `.rollback` to `commit` in case of errors
#    27-Apr-2012 (CT) Add exception handler around `rollback` to `commit`
#    ««revision-date»»···
#--

from   _MOM                  import MOM
from   _TFL                  import TFL

import _MOM.Error
import _MOM._Pred.Err_and_Warn_List
import _MOM._SCM.Summary
import _MOM._SCM.Tracker

from   _TFL.Gauge_Logger      import Gauge_Logger
from   _TFL.predicate         import split_hst, rsplit_hst

import _TFL.Accessor
import _TFL.Context
import _TFL.Decorator
import _TFL.Ordered_Set
import _TFL._Meta.Lazy_Method
import _TFL._Meta.Object
import _TFL._Meta.Once_Property

import itertools
import traceback
import uuid

class Scope (TFL.Meta.Object) :

    active                 = None
    ilk                    = "S"
    Table                  = {}

    init_callback          = TFL.Ordered_Set ()
    kill_callback          = TFL.Ordered_Set ()
    is_universe            = False
    _deprecated_type_names = {}
    _pkg_ns                = None
    __id                   = 0

    root                   = None
    _roots                 = None

    changes                = property (TFL.Getter.historian.total_changes)
    changes_to_save        = property \
        (lambda s : len (s.ems.uncommitted_changes))
    db_meta_data           = property (TFL.Getter.ems.db_meta_data)
    etypes                 = property (TFL.Getter.app_type.etypes)
    Fatal_Exceptions       = property (TFL.Getter.ems.pm.dbs.Fatal_Exceptions)
    name                   = property (lambda s : s.qname or s.bname)
    readonly               = property (TFL.Getter.ems.db_meta_data.readonly)
    uncommitted_changes    = property (TFL.Getter.ems.uncommitted_changes)

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

    ### Scope creation methods

    @classmethod
    def load (cls, app_type, db_url, user = None) :
        db_url = app_type.Url (db_url)
        with cls._init_context (app_type, db_url, user) as self :
            app_type  = self.app_type
            self.ems  = ems = app_type.EMS.connect (self, db_url)
            with self._init_root_context () :
                self._register_root (ems.load_root ())
        return self
    # end def load

    @classmethod
    def new (cls, app_type, db_url, root_epk = (), user = None) :
        db_url = app_type.Url (db_url)
        with cls._init_context (app_type, db_url, user, root_epk) as self :
            app_type  = self.app_type
            self.guid = self._new_guid ()
            self.ems  = ems = app_type.EMS.new (self, db_url)
            with self._init_root_context (root_epk) :
                self._setup_root   (app_type, root_epk)
                ems.register_scope ()
        return self
    # end def new

    @classmethod
    @TFL.Contextmanager
    def _init_context (cls, app_type, db_url, user, root_epk = ()) :
        self                = cls.__new__ (cls)
        self.app_type       = app_type
        self.db_url         = db_url
        self.user           = user
        self.root_epk       = root_epk
        self.bname          = "__".join (str (e) for e in root_epk)
        self.qname          = self.bname or app_type.name
        self.id             = self._new_id ()
        self.init_callback  = self.init_callback [:] ### copy from cls to self
        self.kill_callback  = self.kill_callback [:] ###
        self.root           = None
        self.db_cid         = 0
        self.historian      = MOM.SCM.Tracker (self)
        self.db_errors      = []
        self._attr_errors   = []
        self._etm           = {}
        self._pkg_ns        = {}
        self._roots         = {}
        self._setup_pkg_ns  (app_type)
        old_active = Scope.active
        try :
            Scope.active = self
            yield self
            self._run_init_callbacks   ()
            self.start_change_recorder ()
        except :
            Scope.active = old_active
            raise
    # end def _init_context

    @TFL.Contextmanager
    def _init_root_context (self, root_epk = ()) :
        yield
    # end def _init_root_context

    def __init__ (self) :
        raise TypeError \
            ( "Use {name}.new or {name}.load to create new scopes".format
                (name = self.__class__.__name__)
            )
    # end def __init__

    ### Scope methods

    def add (self, entity) :
        """Adds `entity` to scope `self`."""
        if entity._home_scope is None :
            entity.home_scope = self
        self.ems.add (entity)
        if not entity.init_finished :
            entity._finish__init__ ()
        if not entity.electric :
            self.record_change (MOM.SCM.Change.Create, entity)
    # end def add

    def add_from_pickle_cargo (self, type_name, cargo, pid) :
        """Add an entity defined by (`type_name`, `pid`, `cargo`)."""
        Type = self.entity_type (type_name)
        if Type :
            try :
                result = Type.from_attr_pickle_cargo (self, cargo)
            except Exception, exc :
                self.db_errors.append ((type_name, pid, cargo))
                if __debug__ :
                    traceback.print_exc ()
                print repr (exc)
                print "   Couldn't restore %s %s %s (app-type %s)" % \
                    (type_name, pid, cargo, self.app_type)
            else :
                self.ems.add (result, id = pid)
                if not result.init_finished :
                    result._finish__init__ ()
                return result
    # end def add_from_pickle_cargo

    @TFL.Meta.Class_and_Instance_Method
    def add_init_callback (soc, * callbacks) :
        """Add all `callbacks` to `init_callback`. These
           callbacks are executed whenever a scope is
           created (the new scope is passed as the single argument to each
           callback).
        """
        soc.init_callback.extend (callbacks)
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
        with Scope.LET (active = self) :
            yield
    # end def as_active

    def async_changes (self, * filter, ** kw) :
        return self.ems.async_changes (* filter, ** kw)
    # end def async_changes

    def commit (self) :
        ems = self.ems
        ucc = ems.uncommitted_changes
        if ucc :
            errs = self.r_incorrect (eiter = ucc.entities (ems))
            if errs :
                exc = MOM.Error.Invariants (errs.errors)
                try :
                    self.ems.rollback ()
                except Exception as rexc :
                    print rexc
                raise exc
        self.ems.commit ()
    # end def commit

    @TFL.Meta.Lazy_Method_RLV
    def compute_defaults_internal (self, gauge = Gauge_Logger ()) :
        """Lazily call `compute_defaults_internal` for all entities."""
        with self.as_active () :
            sk = TFL.Sorted_By ("rank", "id")
            gauge.reset ("Compute default internal attributes")
            for et in sorted (self.etypes.itervalues (), key = TFL.Getter.rank) :
                et.compute_type_defaults_internal ()
            for e in self.entity_iter_gauge \
                    (gauge, label = "Reset syncable attributes") :
                e.reset_syncable ()
            for e in self.entity_iter_gauge \
                    (gauge, sort_key = sk, label = "Sync attributes") :
                e.sync_attributes ()
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

    def copy (self, app_type, db_url) :
        """Copy all entities and change-history  of `self` into a new
           scope for `app_type` and `db_url`.
        """
        assert self.app_type.parent is app_type.parent
        db_url = app_type.Url (db_url)
        assert (      db_url is None
               or not db_url.path
               or self.db_url.path != db_url.path
               )
        with self.as_active () :
            result = self.__class__.new \
                (app_type, db_url, self.root_epk, user = self.user)
            for e in sorted (self, key = TFL.Getter.pid) :
                result.add_from_pickle_cargo (* e.as_pickle_cargo ())
            for c in self.query_changes ().order_by (TFL.Sorted_By ("cid")) :
                result.ems.register_change (c)
            result.ems.compact ()
        return result
    # end def copy

    def count_change (self) :
        self.historian.count_change ()
    # end def count_change

    def destroy (self) :
        self.ems.close ()
        if self.qname in Scope.Table :
            del Scope.Table [self.qname]
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
            , g_range = self.ems.count (self.MOM.Id_Entity, strict = False)
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
        except MOM.Error.Invariant :
            pass
        with self.as_active () :
            return self._check_inv (gauge, "system")
    # end def g_incorrect

    def has_changed (self) :
        """Indicates whether something saveworthy has changed"""
        return bool (self.ems.uncommitted_changes)
    # end def has_changed

    @TFL.Meta.Lazy_Method_RLV
    def i_incorrect (self, gauge = Gauge_Logger ()) :
        """Returns all objects which are object-wise incorrect (i.e., violating
           the object's `object` predicates).
        """
        with self.as_active () :
            return self._check_inv (gauge, "object")
    # end def i_incorrect

    @TFL.Contextmanager
    def nested_change_recorder (self, Change, * args, ** kw) :
        with self.historian.nested_recorder (Change, * args, ** kw) as c :
            yield c
            if c :
                c.user = self.user
                self.ems.register_change (c)
    # end def nested_change_recorder

    def pid_query (self, pid) :
        return self.ems.pid_query (pid)
    # end def pid_query

    def query_changes (self, * filter, ** kw) :
        return self.ems.changes (* filter, ** kw)
    # end def query_changes

    @TFL.Meta.Lazy_Method_RLV
    def r_incorrect (self, gauge = Gauge_Logger (), eiter = None) :
        """Returns all objects which are region-wise incorrect (i.e., violating
           the object's `region` predicates).
        """
        with self.as_active () :
            return self._check_inv (gauge, "region", eiter)
    # end def i_incorrect

    def record_change (self, Change, * args, ** kw) :
        result = self.historian.record (Change, * args, ** kw)
        if result is not None :
            result.user = self.user
            self.ems.register_change (result)
            if result.callbacks :
                result.do_callbacks (self)
        return result
    # end def record_change

    @TFL.Meta.Once_Property
    def relevant_roots (self) :
        Top = self.MOM.Id_Entity.E_Type
        return sorted \
            (Top.relevant_roots.itervalues (), key = Top.m_sorted_by)
    # end def relevant_roots

    def remove (self, entity) :
        """Remove `entity` from scope `self`"""
        assert (entity != self.root)
        def remove () :
            entity._destroy ()
            self.ems.remove (entity)
        if entity.electric :
            remove ()
        else :
            Change = MOM.SCM.Change.Destroy
            with self.nested_change_recorder (Change, entity) :
                remove ()
    # end def remove

    def rename (self, entity, new_epk, renamer) :
        self.ems.rename (entity, new_epk, renamer)
    # end def rename

    def rollback (self) :
        self.ems.rollback ()
        self.count_change ()
    # end def rollback

    def start_change_recorder (self) :
        if not self.historian._rec_stack :
            self.historian.push_recorder (MOM.SCM.Tracker.Preferred_Recorder)
    # end def start_change_recorder

    def stop_change_recorder (self) :
        if self.historian._rec_stack :
            self.historian.pop_recorder ()
    # end def stop_change_recorder

    @TFL.Contextmanager
    def temp_change_recorder (self, Recorder) :
        with self.historian.temp_recorder (Recorder) :
            yield
    # end def temp_change_recorder

    def user_diff (self, other, ignore = ()) :
        """Return differences of entities `self` and `other` concerning user attributes."""
        result = {}
        seen   = set ()
        def diff (lhs, rhs) :
            for e in lhs :
                k = e.epk_raw
                t = e.type_name
                if k not in seen :
                    seen.add (k)
                    o = rhs [t].instance (* k, raw = True)
                    if o is None :
                        diff = "Present in %s, missing in %s" % (lhs, rhs)
                    else :
                        diff = e.user_diff (o, ignore)
                    if diff :
                        result [(t, k)] = diff
        diff (self,  other)
        diff (other, self)
        return result
    # end def user_diff

    def user_equal (self, other) :
        """Compare entities of `self` and `other` regarding user attributes."""
        s_count = self.ems.count  (self.MOM.Id_Entity.E_Type,  strict = False)
        o_count = other.ems.count (other.MOM.Id_Entity.E_Type, strict = False)
        if s_count == o_count :
            for e in self :
                o = other [e.type_name].instance (* e.epk_raw, raw = True)
                if not (o and e.user_equal (o)) :
                    break
            else :
                return True
        return False
    # end def user_equal

    def _add_to_scopes (self) :
        for n in (self.qname, ) :
            if n :
                Scope.Table [n] = self
    # end def _add_to_scopes

    def _canonical_name (self, name) :
        return self._deprecated_type_names.get (name, name)
    # end def _canonical_name

    def _check_inv (self, gauge, kind, eiter = None) :
        err_result = []
        wrn_result = []
        sk         = self.MOM.Id_Entity.sort_key
        if eiter is None :
            eiter  = self.entity_iter_gauge \
                (gauge, label = "Checking %s invariants" % kind)
        for e in eiter :
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
        return MOM.Pred.Err_and_Warn_List \
            (sorted (err_result, key = sk), sorted (wrn_result, key = sk))
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

    def _new_guid (self) :
        return str (uuid.uuid4 ())
    # end def _new_guid

    def _new_id (self) :
        result = Scope.__id
        Scope.__id += 1
        return result
    # end def _new_id

    def _outer_pgk_ns (self, outer, pns, _pkg_ns) :
        while True :
            outer, _, name = rsplit_hst (outer, ".")
            if (not outer) or outer in _pkg_ns :
                break
            pns = pns._Outer
            yield outer, pns
    # end def _outer_pgk_ns

    def _register_root (self, root) :
        if root is not None :
            self.root = root
            self._roots [root.Essence.type_base_name] = root
            if not self.root_epk :
                self.root_epk = root.epk
    # end def _register_root

    def _run_init_callbacks (self) :
        for c in self.init_callback :
            c (self)
        self.app_type.run_init_callbacks (self)
    # end def _run_init_callbacks

    def _setup_pkg_ns (self, app_type) :
        _pkg_ns = self._pkg_ns
        Pkg_NS  = self.Pkg_NS
        for name, pns in sorted \
                (app_type.PNS_Map.iteritems (), key = TFL.Getter [0]) :
            if name not in _pkg_ns :
                _pkg_ns [name]  = Pkg_NS (self, pns, name)
                for outer, pns in self._outer_pgk_ns (name, pns, _pkg_ns):
                    _pkg_ns [outer] = Pkg_NS (self, pns, outer)
        for alias, pns in app_type.PNS_Aliases.iteritems () :
            assert not alias in _pkg_ns
            _pkg_ns [alias] = _pkg_ns [pns._Package_Namespace__qname]
    # end def _setup_pkg_ns

    def _setup_root (self, app_type, root_epk) :
        if root_epk and app_type.Root_Type :
            Root_Type = self [app_type.Root_Type.type_name]
            self._register_root (Root_Type (* root_epk))
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
        return "%s %s<%s>" % \
            (self.__class__.__name__, self.bname, self.db_url)
    # end def __str__

# end class Scope

if __name__ != "__main__" :
    MOM._Export ("*")
### __END__ MOM.Scope
