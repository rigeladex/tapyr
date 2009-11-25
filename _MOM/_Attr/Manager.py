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
#    MOM.Attr.Manager
#
# Purpose
#    Attribute manager for a specific instance of a MOM.Entity
#
# Revision Dates
#    29-Sep-2009 (CT) Creation (factored from TOM.Attr.Manager)
#    ««revision-date»»···
#--

from   _MOM                  import MOM
from   _TFL                  import TFL

import _MOM._Attr

import _TFL._Meta.Object
import _TFL.Accessor

class Manager (TFL.Meta.Object) :
    """Attribute manager for instances of MOM entities (objects and links)."""

    def __init__ (self, attr_spec) :
        self.attr_dict           = attr_spec._attr_dict
        self.attr_spec           = attr_spec
        self.last_snapshot       = None
        self.locked_attr         = set ()
        self.needs_sync          = {}
        self._syncable           = set (attr_spec._syncable)
        self.total_changes       = 0
        self.update_at_changes   = {}
        self.reset_pending  ()
        self.reset_syncable ()
    # end def __init__

    def has_changed (self, obj) :
        return self.last_snapshot != self.snapshot (obj)
    # end def has_changed

    def inc_changes (self, inc = 1) :
        self.total_changes += inc
    # end def inc_changes

    def make_snapshot (self, obj) :
        self.last_snapshot = self.snapshot (obj)
    # end def make_snapshot

    def raw_values_record (self, obj, kw) :
        """Return raw values of attributes of `kw` that satisfy
           `record_changes` and which values differ from those in `kw`.
        """
        result    = {}
        attr_dict = self.attr_dict
        for k, v in kw.iteritems () :
            attr = attr_dict.get (k)
            if attr and attr.record_changes and attr.get_value (obj) != v :
                result [k] = attr.get_raw (obj)
        return result
    # end def raw_values_record

    def reset_attributes (self, obj) :
        self.reset_pending ()
        for a in sorted (self.attr_dict.itervalues (), key = TFL.Getter.rank) :
            a.reset (obj)
        if self.pending_cross_ref :
            self.sync_pending (obj)
    # end def reset_attributes

    def reset_pending (self) :
        self.pending_cross_ref = {}
    # end def reset_pending

    def reset_syncable (self) :
        needs_sync = self.needs_sync
        for attr in self._syncable :
             needs_sync [attr.name] = True
    # end def reset_syncable

    def snapshot (self, obj) :
        result = {}
        attr_dict = self.attr_dict
        for name, attr in attr_dict.iteritems () :
            if attr.record_changes :
                value = attr.get_raw (obj)
                if value not in (attr.default, "") :
                    result [name] = value
        return result
    # end def snapshot

    def sync_attributes (self, obj) :
        self.sync_pending   (obj)
        self.reset_syncable ()
    # end def sync_attributes

    def sync_pending (self, obj) :
        pending = self.pending_cross_ref
        self.reset_pending ()
        for a, updater in pending.iteritems () :
            updater (a)
    # end def sync_pending

# end class Manager

__doc__ = """
Class `MOM.Attr.Manager`
========================

.. moduleauthor:: Christian Tanzer <tanzer@swing.co.at>

.. class:: Manager

  `MOM.Attr.Manager` manages the attributes of specific instances of an
  :class:`objects<_MOM.Object.Object>` and :class:`links<_MOM.Link.Link>` of
  essential object models. Each essential entity has its own attribute
  manager.

  The attribute manager

  - Manages a change count that is incremented each time an attribute
    value is changed.

  - Manages syncing for attributes that are syncable.

  - Manages pending cross references.

  - Manages snapshots as needed by :mod:`MOM.SCM<_MOM._SCM>` (scope
    change manager).

"""

if __name__ != "__main__" :
    MOM.Attr._Export ("*")
### __END__ MOM.Attr.Manager
