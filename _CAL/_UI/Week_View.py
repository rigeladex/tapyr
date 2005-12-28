# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. office@spannberg.com
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
#    CAL.UI.Week_View
#
# Purpose
#    Abstract user interface for week view of a calendar.
#
# Revision Dates
#    17-Jun-2005 (MG) Creation
#    ««revision-date»»···
#--

from   _TGL                    import TGL
from   _CAL                    import CAL

import _CAL._UI
import _CAL._UI.Mixin
import _CAL._UI.Tree
import _CAL._UI.Tree_Adapter
import _CAL.Date

class _CAL_Column_ (CAL.UI.Column) :
    """A day column."""

    _real_name    = "Column"
    Column_Widget = "Day_Column"

    default_attributes = dict \
        ( visible       = True
        , clickable     = False
        , resizable     = False
        , reorderable   = False
        , alignment     = 0.5
        , header_widget = None
        , sort_function = None
        )

Column = _CAL_Column_ # end class Column

class Day_Cell (CAL.UI.Cell) :
    """Models a day cell."""

    current_day         = CAL.Date ()

    renderer_class      = "Day_Cell_Renderer"
    renderer_attributes = ("day", )

    def __init__ (self, day, * args, ** kw) :
        self.__super.__init__ ((day, object, self._get_day), * args, ** kw)
    # end def __init__

    def _get_day (self, week, attr_name) :
        return getattr (week, attr_name)
    # end def _get_day

# end class Day_Cell

class Week_View (CAL.UI.Tree) :
    """XXX"""

    class Adapter (CAL.UI.Tree_Adapter) :
        """XXX"""

        Model_Type = "List_Model"

        rules_hint = False
        schema     = \
            ( Column ("Mo", Day_Cell ("mon"))
            , Column ("Tu", Day_Cell ("tue"))
            , Column ("We", Day_Cell ("wed"))
            , Column ("Th", Day_Cell ("thu"))
            , Column ("Fr", Day_Cell ("fri"))
            , Column ("Sa", Day_Cell ("sat"))
            , Column ("So", Day_Cell ("sun"))
            )

        def has_children (cls, week) :
            return False
        # end def has_children

        def root_children (cls, year) :
            return year.weeks
        # end def children

    # end class Adapter

    def __init__ (self, model, AC = None) :
        self.__super.__init__ \
            (model.calendar.year [AC.memory.current_day.year], AC = AC)
        self.model = model
        self._setup_cmd_mgr   ()
    # end def __init__

    def _setup_cmd_mgr (self) :
        TNS         = self.TNS
        AC          = self.AC
        UI          = self.ANS.UI
        interfacers = dict \
            ( cm = TNS.CI_Menu         (name = "context_menu", AC = AC)
            , ev = TNS.CI_Event_Binder (AC, self.tkt)
            )
        self.cmd_mgr         = UI.Command_Mgr \
            ( change_counter = self.model.changes
            , interfacers    = interfacers
            , if_names       = ("cm:click_3", )
            , AC             = AC
            )
        self.cmd_mgr.add_command \
            ( UI.Command ("Select", self.select_day)
            , if_names = ("cm", "ev:Cursor_Changed")
            )
        self.cmd_mgr.bind_interfacers (self.tkt)
    # end def _setup_cmd_mgr

    def select_day (self, event) :
        tree                = event.widget
        #memory              = self.AC.memory
        #old                 = memory.current_day
        #if event.move_type == self.TNS.gtk.MOVEMENT_VISUAL_POSITIONS :
        #    memory.current_day += event.move_count
        #print memory.current_day
        print "XXX"
    # end def select_day

# end class Week_View

if __name__ != "__main__" :
    CAL.UI._Export ("Week_View")
### __END__ CAL.UI.Week_View
