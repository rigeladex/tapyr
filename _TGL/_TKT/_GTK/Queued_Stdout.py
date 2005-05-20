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
#    TGL.TKT.GTK.Queued_Stdout
#
# Purpose
#    Provide thread-safe redirection of stdout for GTK toolkit wrapper
#
# Revision Dates
#    20-May-2005 (MG) Creation
#    ««revision-date»»···
#--
#
from   _TGL           import TGL
import _TGL._TKT
import _TGL._TKT.Queued_Stdout

class Queued_Stdout (TGL.TKT.Queued_Stdout) :
    """Thread-safe redirection of stdout for GTK"""

    def _cancel_pending (self) :
        if self.out_widget and self._pending is not None :
            self.out_widget.idle_remove (self._pending)
    # end def _cancel_pending

    def _schedule_pending (self) :
        return self.out_widget.idle_add (self.update)
    # end def _schedule_pending

# end class Queued_Stdout


if __name__ != "__main__" :
    from   _TGL._TKT._GTK import GTK
    GTK._Export ("Queued_Stdout")
### __END__ TGL.TKT.GTK.Queued_Stdout
