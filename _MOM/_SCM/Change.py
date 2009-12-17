# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004-2009 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.cluster
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
#    ««revision-date»»···
#--

from   _MOM               import MOM
from   _TFL               import TFL

import _MOM._SCM.History_Mixin
import _MOM._SCM.Recorder

import _TFL._Meta.Property

import datetime

class _Change_ (MOM.SCM.History_Mixin) :
    """Model a change of a MOM Scope"""

    kind               = "Composite change"

    children           = TFL.Meta.Alias_Property ("history")
    cid                = None
    epk                = None
    pid                = None
    user               = None

    def __init__ (self) :
        self.__super.__init__ ()
        self.time = datetime.datetime.now ()
    # end def __init__

    def __repr__ (self) :
        return "\n  ".join (self._repr_lines ())
    # end def __repr__

    def _repr (self) :
        return self.kind
    # end def _repr

    def _repr_lines (self, level = 0) :
        result = ["%s<%s>" % ("  " * level, self._repr ())]
        for c in self.children :
            result.extend (c._repr_lines (level + 1))
        return result
    # end def _repr_lines

# end class _Change_

class Undoable (_Change_) :
    """Model an undoable change of a MOM Scope"""

    Preferred_Recorder = MOM.SCM.Appender
    undoable           = True

    def undo (self, scope) :
        for c in reversed (self.children) :
            c.undo (scope)
    # end def undo

# end class Change

class Non_Undoable (_Change_) :
    """Model a change that cannot be undone"""

    Preferred_Recorder = MOM.SCM.Counter
    undoable           = False

# end class Non_Undoable

class _Entity_ (Undoable) :
    """Model a change of an MOM entity"""

    new_attr = old_attr = {}

    def __init__ (self, entity) :
        self.__super.__init__ ()
        self.epk          = entity.epk
        self.pid          = getattr (entity, "pid", None)
        self.type_name    = entity.Essence.type_name
        self.user         = entity.home_scope.user
        self.change_count = 1
    # end def __init__

    def entity (self, scope) :
        etm = scope [self.type_name]
        return scope.ems.pid_query (self.pid, etm._etype)
    # end def entity

    def _repr (self) :
        result = ["%s %s %s" % (self.kind, self.type_name, self.epk)]
        if self.old_attr :
            result.append ("old-values = %s" % (self.old_attr))
        if self.new_attr :
            result.append ("new-values = %s" % (self.new_attr))
        return ", ".join (result)
    # end def _repr

# end class _Entity_

class Copy (_Entity_) :
    """Model a change that copies an existing entity."""
# end class Copy

class Create (_Entity_) :
    """Model a change that creates a new entity (object or link)"""

    kind = "Create"

    def __init__ (self, entity) :
        self.__super.__init__ (entity)
        self.new_attr = dict \
            ( (a.name, a.get_raw (entity))
            for a in entity.user_attr if a.to_save (entity)
            )
    # end def __init__

    def undo (self, scope) :
        self.__super.undo (scope)
        entity = self.entity (scope)
        if entity :
            entity.destroy ()
    # end def undo

# end class

class Destroy (_Entity_) :
    """Model a change that destroys an entity"""

    kind = "Destroy"

    def __init__ (self, entity) :
        self.__super.__init__ (entity)
        self.old_attr = dict \
            ( (a.name, a.get_raw (entity))
            for a in entity.user_attr if a.to_save (entity)
            )
    # end def __init__

    def undo (self, scope) :
        etm = scope [self.type_name]
        etm (* self.epk, raw = True, ** self.old_attr)
        self.__super.undo (scope)
    # end def undo

# end class Destroy

class Attr (_Entity_) :
    """Model a change that modifies attributes of an entity"""

    kind = "Modify"

    def __init__ (self, entity, old_attr) :
        self.__super.__init__ (entity)
        self.new_attr = dict \
            ( (a.name, a.get_raw (entity))
            for a in (entity.user_attr + entity.primary) if a.name in old_attr
            )
        self.old_attr = old_attr
    # end def __init__

    def undo (self, scope) :
        self.__super.undo (scope)
        entity   = self.entity (scope)
        old_attr = self.old_attr
        if entity and old_attr :
            entity.set_raw (** old_attr)
    # end def undo

# end class Attr

if __name__ != "__main__" :
    MOM.SCM._Export_Module ()
### __END__ MOM.SCM.Change
