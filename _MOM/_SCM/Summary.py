# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package MOM.SCM.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    MOM.SCM.Summary
#
# Purpose
#    Convert a list of changes into a change summary per object
#
# Revision Dates
#     2-Sep-2010 (CT) Creation
#     3-Sep-2010 (CT) Creation continued
#     8-Sep-2010 (CT) Creation continued..
#    14-Sep-2010 (CT) `Summary` rewritten to store `changes`,
#                     `Pid.changed_attrs` added
#    14-Sep-2010 (CT) `entities` added
#    15-Sep-2010 (CT) Use `SCM.Change.modified_attrs` instead of home-grown code
#    16-Sep-2010 (CT) `Summary`: s/clear/_clear/
#    22-Sep-2010 (CT) `Summary.change_conflicts` and `_check_*_conflicts` added
#    24-Sep-2010 (CT) `Attr_Summary.check_conflict` and `.check_ini_vs_cur`
#                     factored
#    24-Sep-2010 (CT) `Pid.epk`, `.by_epk`, and `.type_name` added,
#                     `.check_attr_conflicts` and `.check_ini_vs_cur` factored
#    24-Sep-2010 (CT) `Pid.apply` added
#    28-Sep-2010 (CT) `_Entity_Summary_` factored from `Pid`
#    28-Sep-2010 (CT) `Attr_C_Summary.check_conflict` and `.check_ini_vs_cur`
#                     added
#    ««revision-date»»···
#--

from   _MOM               import MOM
from   _TFL               import TFL

import _MOM._SCM.Change

import _TFL._Meta.Object
import _TFL._Meta.Once_Property
import _TFL.Accessor
import _TFL.defaultdict
import _TFL.Undef

import itertools

class _Entity_Summary_ (TFL.Meta.Object) :

    def check_attr_conflicts (self, entity, initial_values) :
        result = False
        for name, acs in self.attribute_changes.iteritems () :
            attr    = getattr (entity.__class__, name)
            ini     = initial_values.get (name)
            result += acs.check_conflict (attr, entity, ini)
        return result
    # end def check_attr_conflicts

    def check_ini_vs_cur (self, entity, initial_values, r_name) :
        result    = False
        check_all = not self.is_dead
        for name, ini in initial_values.iteritems () :
            attr  = getattr (entity.__class__, name)
            if check_all or not attr.electric :
                result += acs.check_ini_vs_cur (attr, entity, ini, r_name)
        return result
    # end def check_ini_vs_cur

# end class _Entity_Summary_

class Attr_Summary (TFL.Meta.Object) :
    """Change summary for a single attribute of a single `pid`."""

    conflicts = False
    merges    = False

    cur = ini = None
    new = old = undef = TFL.Undef ("attr")

    def add (self, old, new) :
        if self.old is self.undef :
            self.old = old
        self.new = new
    # end def add

    def check_conflict (self, attr, entity, ini) :
        self.conflicts = False
        self.cur = cur = attr.get_raw (entity)
        self.ini = ini
        if not attr.electric :
            self.conflicts = (self.new != cur and ini != cur)
        return self.conflicts
    # end def check_conflict

    def check_ini_vs_cur (self, attr, entity, ini, r_name) :
        self.ini = ini
        self.cur = cur = attr.get_raw (entity)
        result   = (ini != cur)
        setattr (self, r_name, result)
        return result
    # end def check_ini_vs_cur

    def __nonzero__ (self) :
        return self.old is not self.undef
    # end def __nonzero__

    def __repr__ (self) :
        return "(old = %r, new = %r)" % (self.old, self.new)
    # end def __repr__

# end class Attr_Summary

class Attr_C_Summary (_Entity_Summary_) :
    """Change summary for a composite attribute of a single `pid`."""

    def __init__ (self, attr_summary = None) :
        self.attribute_changes = TFL.defaultdict (Attr_Summary)
        if attr_summary :
            old = dict (attr_summary.old)
            new = dict (attr_summary.new)
            for a in set (itertools.chain (old, new)) :
                self [a].add (old.get (a), new.get (a))
    # end def __init__

    @property
    def cur (self) :
        return tuple \
            (   (k, v.cur)
            for (k, v) in sorted (self.attribute_changes.iteritems ())
            )
    # end def cur

    @property
    def new (self) :
        return tuple \
            (   (k, v.new)
            for (k, v) in sorted (self.attribute_changes.iteritems ())
            )
    # end def new

    @property
    def old (self) :
        return tuple \
            (   (k, v.old)
            for (k, v) in sorted (self.attribute_changes.iteritems ())
            )
    # end def old

    def check_conflict (self, attr, entity, ini) :
        if ini is None :
            ini        = {}
        an_entity      = attr.get_value (entity)
        self.conflicts = result = self.check_attr_conflicts (an_entity, ini)
        self.entity    = an_entity
        self.ini       = ini
        return result
    # end def check_conflict

    def check_ini_vs_cur (self, attr, entity, ini, r_name) :
        if ini is None :
            ini        = {}
        an_entity      = attr.get_value (entity)
        self.entity    = an_entity
        self.ini       = ini
        self.merges    = result = self.__super.check_ini_vs_cur \
            (an_entity, ini, r_name)
        return result
    # end def check_ini_vs_cur

    def items (self) :
        return self.attribute_changes.items ()
    # end def items

    def iteritems (self) :
        return self.attribute_changes.iteritems ()
    # end def iteritems

    def iterkeys (self) :
        return self.attribute_changes.iterkeys ()
    # end def iterkeys

    def itervalues (self) :
        return self.attribute_changes.itervalues ()
    # end def itervalues

    def keys (self) :
        return self.attribute_changes.keys ()
    # end def keys

    def values (self) :
        return self.attribute_changes.values ()
    # end def values

    def __getitem__ (self, key) :
        return self.attribute_changes [key]
    # end def __getitem__

    def __iter__ (self) :
        return iter (self.attribute_changes)
    # end def __iter__

    def __len__ (self) :
        return len (self.attribute_changes)
    # end def __len__

    def __nonzero__ (self) :
        return bool (self.attribute_changes)
    # end def __nonzero__

    def __getitem__ (self, key) :
        return self.attribute_changes [key]
    # end def __getitem__

    def __repr__ (self) :
        return "(old = %r, new = %r)" % (self.old, self.new)
    # end def __repr__

# end class Attr_C_Summary

class Pid (_Entity_Summary_) :
    """Change summary for a single `pid`."""

    entity = None

    def __init__ (self, pid) :
        self.pid      = pid
        self._changes = set ()
    # end def __init__

    @TFL.Meta.Once_Property
    def attribute_changes (self) :
        result = TFL.defaultdict (Attr_Summary)
        for c in self.changes :
            r = result
            if isinstance (c, MOM.SCM.Change.Attr_Composite) :
                r = result [c.attr_name] = Attr_C_Summary \
                    (result.get (c.attr_name))
            for a in set (itertools.chain (c.old_attr, c.new_attr)) :
                (result if a == "last_cid" else r) \
                    [a].add (c.old_attr.get (a), c.new_attr.get (a))
        return result
    # end def attribute_changes

    @TFL.Meta.Once_Property
    def changed_attrs (self) :
        result = set ()
        for c in self.changes :
            result.update (c.modified_attrs)
        return result
    # end def changed_attrs

    @TFL.Meta.Once_Property
    def changes (self) :
        return sorted (self._changes, key = TFL.Getter.cid)
    # end def changes

    @TFL.Meta.Once_Property
    def epk (self) :
        changes = self.changes
        return changes and changes [-1].epk
    # end def epk

    @TFL.Meta.Once_Property
    def is_born (self) :
        changes = self.changes
        return changes and isinstance (changes [0], MOM.SCM.Change.Create)
    # end def is_born

    @TFL.Meta.Once_Property
    def is_dead (self) :
        changes = self.changes
        return changes and isinstance (changes [-1], MOM.SCM.Change.Destroy)
    # end def is_dead

    @TFL.Meta.Once_Property
    def type_name (self) :
        changes = self.changes
        return changes and changes [0].type_name
    # end def type_name

    def add (self, c) :
        self._changes.add (c)
    # end def add

    def apply (self, scope) :
        kw = dict \
            ( (name, acs.new)
            for name, acs in self.attribute_changes.iteritems ()
            if  acs.merges
            )
        if self.is_born and not self.entity :
            etm = scope [self.type_name]
            self.entity = etm (self.epk, raw = True)
        if self.entity :
            self.entity.set_raw (kw)
    # end def apply

    def _repr (self) :
        parts = []
        n     = len (self) - self.is_born - self.is_dead
        if self.is_born :
            parts.append ("newborn")
        if n > 0 :
            parts.append ("%s change%s" % (n, "s" if n > 1 else ""))
        if self.is_dead :
            parts.append ("just died")
        return "Change Summary for pid %s: %s" % (self.pid, ", ".join (parts))
    # end def _repr

    def _repr_lines (self, level = 0) :
        result = ["%s<%s>" % ("  " * level, self._repr ())]
        for c in self.changes :
            result.extend (c._repr_lines (level + 1))
        return result
    # end def _repr_lines

    def __len__ (self) :
        return len (self._changes)
    # end def __len__

    def __nonzero__ (self) :
        return bool (self._changes)
    # end def __nonzero__

    def __repr__ (self) :
        return "\n  ".join (self._repr_lines ())
    # end def __repr__

# end class Pid

class Summary (TFL.Meta.Object) :
    """Summary of changes per `pid`"""

    def __init__ (self) :
        self._clear ()
    # end def __init__

    @property
    def by_pid (self) :
        result = self._by_pid
        if result is None :
            result = self._by_pid = TFL.defaultdict_kd (Pid)
            self._add_to_by_pid (self._changes)
        return result
    # end def by_pid

    @property
    def changed_attrs (self) :
        result = dict ()
        for pid, csp in self.by_pid.iteritems () :
            if csp.changed_attrs and not csp.is_dead :
                result [pid] = csp.changed_attrs
        return result
    # end def changed_attrs

    @property
    def changes (self) :
        return self._changes
    # end def changes

    def add (self, c) :
        self._changes.append (c)
        self._by_pid = None
    # end def add

    def change_conflicts (self, initial_values, scope) :
        """Determine conflicts between `self.changes` and the entities of
           `scope`, compared to attribute values in `initial_values`.
        """
        result = self.conflicts, self.merges = set (), set ()
        by_epk = self.by_epk
        for csp in self.by_pid.itervalues () :
            args = (initial_values.get (csp.pid, {}), scope, csp) + result
            by_epk [(csp.type_name, csp.epk)] = csp
            if csp.is_dead :
                self._check_dead_conflicts (* args)
            elif csp.is_born :
                self._check_born_conflicts (* args)
            else :
                self._check_attr_conflicts (* args)
        return result
    # end def change_conflicts

    def entities (self, ems) :
        for pid, csp in self.by_pid.iteritems () :
            if not csp.is_dead :
                yield ems.pid_query (pid)
    # end def entities

    def _add_to_by_pid (self, changes) :
        by_pid = self._by_pid
        for c in changes :
            if c.pid :
                by_pid [c.pid].add (c)
            if c.children :
                self._add_to_by_pid (c.children)
    # end def _add_to_by_pid

    def _check_attr_conflicts (self, initial_values, scope, csp, conflicts, merges) :
        try :
            entity = csp.entity = scope.ems.pid_query (csp.pid)
        except LookupError :
            conflicts.add (csp.pid)
        else :
            if csp.check_attr_conflicts (entity, initial_values) :
                conflicts.add (csp.pid)
            if csp.check_ini_vs_cur (entity, initial_values, "merges") :
                merges.add (csp.pid)
    # end def _check_attr_conflicts

    def _check_born_conflicts (self, initial_values, scope, csp, conflicts, merges) :
        etm    = scope [csp.type_name]
        entity = csp.entity = etm.instance (* csp.epk, raw = True)
        if entity :
            if csp.check_attr_conflicts (entity, initial_values) :
                conflicts.add (csp.pid)
    # end def _check_born_conflicts

    def _check_dead_conflicts (self, initial_values, scope, csp, conflicts, merges) :
        try :
            entity = csp.entity = scope.ems.pid_query (csp.pid)
        except LookupError :
            pass
        else :
            if csp.check_ini_vs_cur (entity, initial_values, "conflicts") :
                conflicts.add (csp.pid)
    # end def _check_dead_conflicts

    def _clear (self) :
        self._changes = []
        self._by_pid  = None
        self.by_epk   = {}
    # end def _clear

    def __getitem__ (self, index) :
        return self._changes [index]
    # end def __getitem__

    def __iter__ (self) :
        return iter (self._changes)
    # end def __iter__

    def __len__ (self) :
        return len (self._changes)
    # end def __len__

    def __nonzero__ (self) :
        return bool (self._changes)
    # end def __nonzero__

# end class Summary

if __name__ != "__main__" :
    MOM.SCM._Export ("Summary")
### __END__ MOM.SCM.Summary
