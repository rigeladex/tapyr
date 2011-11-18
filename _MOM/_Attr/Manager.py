# -*- coding: iso-8859-15 -*-
# Copyright (C) 2009-2011 Mag. Christian Tanzer. All rights reserved
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
#    MOM.Attr.Manager
#
# Purpose
#    Attribute manager for a specific instance of a MOM.Entity
#
# Revision Dates
#    29-Sep-2009 (CT) Creation (factored from TOM.Attr.Manager)
#    16-Dec-2009 (CT) `snapshot` changed to use `save_to_db` instead of
#                     `record_changes` to filter attributes
#    16-Dec-2009 (CT) `raw_values_record` removed
#     2-Feb-2010 (CT) `updates_pending` added
#     8-Feb-2010 (CT) `snapshot` removed
#    18-Nov-2011 (CT) Import `unicode_literals` from `__future__`
#    ««revision-date»»···
#--

from   __future__            import unicode_literals

from   _MOM                  import MOM
from   _TFL                  import TFL

import _MOM._Attr

import _TFL._Meta.Object
import _TFL.Accessor
import _TFL.predicate

class Manager (TFL.Meta.Object) :
    """Attribute manager for instances of MOM entities (objects and links)."""

    def __init__ (self, attr_spec) :
        self.attr_dict           = attr_spec._attr_dict
        self.attr_spec           = attr_spec
        self.locked_attr         = set ()
        self.needs_sync          = {}
        self._syncable           = set (attr_spec._syncable)
        self.total_changes       = 0
        self.update_at_changes   = {}
        self.reset_pending         ()
        self.reset_syncable        ()
        self.reset_updates_pending ()
    # end def __init__

    def do_updates_pending (self, obj) :
        if self.updates_pending :
            for a in TFL.uniq (self.updates_pending) :
                a.update (obj)
            self.reset_updates_pending ()
    # end def do_updates_pending

    def inc_changes (self, inc = 1) :
        self.total_changes += inc
    # end def inc_changes

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

    def reset_updates_pending (self) :
        self.updates_pending = []
    # end def reset_updates_pending

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

"""

if __name__ != "__main__" :
    MOM.Attr._Export ("*")
### __END__ MOM.Attr.Manager
