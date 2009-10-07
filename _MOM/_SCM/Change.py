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
#    ««revision-date»»···
#--

from   _MOM               import MOM
from   _TFL               import TFL

import _MOM._SCM.History_Mixin
import _MOM._SCM.Recorder

class Change (MOM.SCM.History_Mixin) :
    """Model a change of a MOM Scope"""

    Preferred_Recorder = MOM.SCM.Appender
    kind               = "Composite change"
    verbose            = False
    undoable           = True

    def undo (self, scope) :
        if self.verbose :
            print "Undoing <%-70.70s>" % (self._repr (), )
        for c in reversed (self.history) :
            c.undo (scope)
    # end def undo

    def __repr__ (self) :
        return "\n  ".join (self._repr_lines ())
    # end def __repr__

    def _repr (self) :
        return self.kind
    # end def _repr

    def _repr_lines (self, level = 0) :
        result = ["%s<%s>" % ("  " * level, self._repr ())]
        for c in self.history :
            result.extend (c._repr_lines (level + 1))
        return result
    # end def _repr_lines

# end class Change

class Non_Undoable_Change (Change) :
    """Model a change that cannot be undone"""

    Preferred_Recorder = MOM.SCM.Counter
    kind               = "Change that isn't undoable"
    undoable           = False

# end class Non_Undoable_Change

class Entity_Change (Change) :
    """Model an entity change of a MOM Scope"""

    def __init__ (self, entity) :
        self.__super.__init__ ()
        self.etype        = entity.Essence.type_name
        self.name         = entity._names ()
        self.change_count = 1
    # end def __init__

    def entity (self, scope) :
        return scope.entity (self.etype, self.name)
    # end def entity

    def _repr (self) :
        return "%s %s %s" % (self.kind, self.etype, self.name)
    # end def _repr

# end class Entity_Change

class Entity_Change_Create (Entity_Change) :
    """Entity_Change: create a new object"""

    kind = "Create"

    def undo (self, scope) :
        self.__super.undo (scope)
        entity = self.entity (scope)
        if entity :
            entity.destroy ()
    # end def undo

# end class Entity_Change_Create

class Entity_Change_Copy (Entity_Change_Create) :
    """Entity_Change: copy an object"""

    kind = "Copy"

# end class Entity_Change_Copy

class Entity_Change_Destroy (Entity_Change) :
    """Entity_Change: destroy a object"""

    kind = "Destroy"

    def __init__ (self, entity) :
        self.__super.__init__ (entity)
        self.attr = attr = {}
        for a in entity._attr_man.attr_dict.itervalues () :
            if a.save_to_db :
                attr [a.name] = a.get_raw (entity)
    # end def __init__

    def undo (self, scope) :
        etype = scope.entity_type (self.etype)
        ### XXX change to handle obbjects and links identically?
        if issubclass (etype, MOM.Object) :
            entity = etype     (* self.name)
        else :
            entity = etype.add (* self.name)
        if entity :
            entity.set_raw (** self.attr)
        self.__super.undo (scope)
    # end def undo

# end class Entity_Change_Destroy

class Entity_Change_Rename (Entity_Change) :
    """Entity_Change: rename an object"""

    kind = "Rename"

    def __init__ (self, entity, old_name) :
        self.__super.__init__ (entity)
        self.old_name = old_name
    # end def __init__

    def undo (self, scope) :
        assert not self.history
        entity = self.entity (scope)
        if entity :
            entity.rename (self.old_name)
    # end def undo

    def _repr (self) :
        return "%s %s" % (self.__super._repr (), self.old_name)
    # end def _repr

# end class Entity_Change_Rename

class Entity_Change_Attr (Entity_Change) :
    """Entity_Change: change attributes"""

    kind = "Change attributes of"

    def __init__ (self, entity, old_attr) :
        self.__super.__init__ (entity)
        self.old_attr = old_attr
    # end def __init__

    def undo (self, scope) :
        self.__super.undo (scope)
        entity = self.entity (scope)
        if entity :
            entity.set_raw (** self.old_attr)
    # end def undo

    def _repr (self) :
        return "%s, old values = %s" % (self.__super._repr (), self.old_attr)
    # end def _repr

# end class Entity_Change_Attr

if __name__ != "__main__" :
    MOM.SCM._Export ("*")
### __END__ MOM.SCM.Change
