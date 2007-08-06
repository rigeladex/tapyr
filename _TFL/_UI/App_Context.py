# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 Mag. Christian Tanzer. All rights reserved
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
#    TFL.UI.App_Context
#
# Purpose
#    Encapsulate context of application
#
# Revision Dates
#    18-Jan-2005 (CT) Creation
#    21-Jan-2006 (MG) Imports fixed
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ««revision-date»»···
#--



from   _TFL                 import TFL
import _TFL._Meta.Object
import _TFL._UI
import _TFL.Record

class App_Context (TFL.Meta.Object) :
    """Application context"""

    def __init__ (self, ANS, memory = None, ui_state = None) :
        self.ANS      = ANS
        self.memory   = memory
        if ui_state is None :
            ui_state  = TFL.Record ()
        self.ui_state = ui_state
    # end def __init__

# end class App_Context

if __name__ != "__main__" :
    TFL.UI._Export ("*")
### __END__ TFL.UI.App_Context
