# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004-2010 Mag. Christian Tanzer. All rights reserved
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
#    MOM.SCM.Tracker
#
# Purpose
#    Provide a tracker for changes of a MOM Scope
#
# Revision Dates
#     7-Oct-2009 (CT) Creation (factored from TOM.SCM.Tracker)
#    16-Dec-2009 (CT) `nested_recorder` changed to yield change object, if any
#     8-Feb-2010 (CT) `snapshot` removed
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

    def __init__ (self, scope) :
        self.__super.__init__ ()
        self.total_changes = 0
        self.yrotsih       = []
        self.scope         = weakref.proxy   (scope)
        self._recorder     = MOM.SCM.Ignorer (self)
        self._rec_stack    = []
        self.dependents    = {}
    # end def __init__

    def add_dependency (self, scope) :
        self.dependents [scope.id] = weakref.proxy (scope)
    # end def add_dependency

    def count_change (self) :
        self.total_changes += 1
    # end def count_change

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
