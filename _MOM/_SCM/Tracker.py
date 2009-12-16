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
#    MOM.SCM.Tracker
#
# Purpose
#    Provide a tracker for changes of a MOM Scope
#
# Revision Dates
#     7-Oct-2009 (CT) Creation (factored from TOM.SCM.Tracker)
#    16-Dec-2009 (CT) `nested_recorder` changed to yield change object, if any
#    ««revision-date»»···
#--

from   _MOM          import MOM
from   _TFL          import TFL

import _MOM._SCM.Change
import _MOM._SCM.History_Mixin
import _MOM._SCM.Recorder

import _TFL.Context

import weakref

class Tracker (MOM.SCM.History_Mixin) :
    """Track changes of a MOM Scope"""

    Preferred_Recorder = MOM.SCM.Appender

    since_snapshot     = property (lambda s : s.change_count - s.snapsh_count)

    def __init__ (self, scope) :
        self.__super.__init__ ()
        self.total_changes = 0
        self.yrotsih       = []
        self.scope         = weakref.proxy   (scope)
        self._recorder     = MOM.SCM.Ignorer (self)
        self._rec_stack    = []
        self.dependents    = {}
        self.make_snapshot ()
    # end def __init__

    def add_dependency (self, scope) :
        self.dependents [scope.id] = weakref.proxy (scope)
    # end def add_dependency

    def count_change (self) :
        self.total_changes += 1
    # end def count_change

    def has_changed (self) :
        return self.change_count != self.snapsh_count
    # end def has_changed

    def make_snapshot (self) :
        self.snapsh_count = self.change_count
    # end def make_snapshot

    @TFL.Contextmanager
    def nested_recorder (self, Change, * args, ** kw) :
        """Context manager for recording a set of changes nested inside
           `Change`.
        """
        change = self.record (Change, * args, ** kw)
        if change is not None :
            if change.Preferred_Recorder.weight < self._recorder.weight :
                preferred_recorder = change.Preferred_Recorder
            else :
                preferred_recorder = self._recorder.__class__
            self.push_recorder (preferred_recorder (change))
            try :
                yield change
            finally :
                self.pop_recorder ()
        else :
            yield None
    # end def nested_recorder

    def push_recorder (self, recorder) :
        if not isinstance (recorder, MOM.SCM.Recorder) :
            recorder = recorder (self)
        self._rec_stack.append (self._recorder)
        self._recorder = recorder
    # end def push_recorder

    def pop_recorder (self) :
        self._recorder = self._rec_stack.pop ()
    # end def pop_recorder

    def record (self, Change, * args, ** kw) :
        """Record change of type `Change`."""
        result = self._recorder (Change, * args, ** kw)
        self.total_changes += 1
        if self.dependents :
            self._recorder.update (self.dependents.itervalues ())
        return result
    # end def record

    def remove_dependency (self, scope) :
        del self.dependents [scope.id]
    # end def remove_dependency

    def undo (self) :
        last = self.history.pop ()
        history, self.history = self.history, self.yrotsih
        try :
            ### changes done during `undo` will by appended to `self.yrotsih`
            ### (which is history running in reverse)
            last.undo (self.scope)
            self.total_changes += 1
        finally :
            ### restore forward running history
            self.history = history
    # end def undo

    def undoable (self) :
        return bool (self.history and self.history [-1].undoable)
    # end def undoable

# end class Tracker

if __name__ != "__main__" :
    MOM.SCM._Export ("*")
### __END__ MOM.SCM.Tracker
