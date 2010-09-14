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

class Attr_Summary (TFL.Meta.Object) :
    """Change summary for a single attribute of a single `pid`."""

    undef = TFL.Undef ("attr")

    def __init__ (self) :
        self.old = self.undef
        self.new = None
    # end def __init__

    def add (self, old, new) :
        if self.old is self.undef :
            self.old = old
        self.new = new
    # end def add

    def __repr__ (self) :
        return "(old = %r, new = %r)" % (self.old, self.new)
    # end def __repr__

# end class Attr_Summary

class Attr_C_Summary (TFL.Meta.Object) :
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
    def old (self) :
        return tuple \
            (   (k, v.old)
            for (k, v) in sorted (self.attribute_changes.iteritems ())
            )
    # end def old

    @property
    def new (self) :
        return tuple \
            (   (k, v.new)
            for (k, v) in sorted (self.attribute_changes.iteritems ())
            )
    # end def new

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

class Pid (TFL.Meta.Object) :
    """Change summary for a single `pid`."""

    def __init__ (self, pid) :
        self.pid      = pid
        self._changes = set ()
    # end def __init__

    def add (self, c) :
        self._changes.add (c)
    # end def add

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
            if isinstance (c, MOM.SCM.Change.Attr_Composite) :
                result.update ((c.attr_name, "last_cid"))
            else :
                result.update (c.old_attr)
        return result
    # end def changed_attrs

    @TFL.Meta.Once_Property
    def changes (self) :
        return sorted (self._changes, key = TFL.Getter.cid)
    # end def changes

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
        self.clear ()
    # end def __init__

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

    @property
    def by_pid (self) :
        result = self._by_pid
        if result is None :
            result = self._by_pid = TFL.defaultdict_kd (Pid)
            self._add_to_by_pid (self._changes)
        return result
    # end def by_pid

    def add (self, c) :
        self._changes.append (c)
        self._by_pid = None
    # end def add

    def clear (self) :
        self._changes = []
        self._by_pid = None
    # end def clear

    def _add_to_by_pid (self, changes) :
        by_pid = self._by_pid
        for c in changes :
            if c.pid :
                by_pid [c.pid].add (c)
            if c.children :
                self._add_to_by_pid (c.children)
    # end def _add_to_by_pid

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
