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
#    ««revision-date»»···
#--

from   _MOM               import MOM
from   _TFL               import TFL

import _MOM._SCM.Change

import _TFL._Meta.Object
import _TFL._Meta.Once_Property
import _TFL.Accessor
import _TFL.defaultdict

class Attr_Summary (TFL.Meta.Object) :
    """Change summary for a single attribute of a single `pid`."""

    undef = object ()

    def __init__ (self) :
        self.old = self.undef
        self.new = None
    # end def __init__

    def add (self, old, new) :
        if self.old is not self.undef :
            self.old = old
        self.new = new
    # end def add

# end class Attr_Summary

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
            ### XXX SCM.Change.Attr_Composite
            for a in set (c.old_attr, c.new_attr) :
                result [a].add (c.old_attr.get (a), c.new_attr.get (a))
        return result
    # end def attribute_changes

    @TFL.Meta.Once_Property
    def changes (self) :
        return sorted (self._changes, key = TFL.Getter.cid)
    # end def changes

    @TFL.Meta.Once_Property
    def is_born (self) :
        changes = self.changes
        return changes and isinstance (changes [0], SCM.Change.Create)
    # end def is_born

    @TFL.Meta.Once_Property
    def is_dead (self) :
        changes = self.changes
        return changes and isinstance (changes [-1], SCM.Change.Destroy)
    # end def is_dead

# end class Pid

class Summary (TFL.Meta.Object) :
    """Summary of changes per `pid`"""

    def __init__ (self, changes) :
        self._map = TFL.defaultdict_kd (Pid)
        self.add (changes)
    # end def __init__

    def add (self, changes) :
        map = self._map
        for c in changes :
            if c.pid :
                map [c.pid].add (c)
            if c.children :
                self.add (c.children)
    # end def add

# end class Summary

if __name__ != "__main__" :
    MOM.SCM._Export ("Summary")
### __END__ MOM.SCM.Summary
