# -*- coding: utf-8 -*-
# Copyright (C) 2005 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. office@spannberg.com
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
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
