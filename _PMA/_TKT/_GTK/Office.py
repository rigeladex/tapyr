# -*- coding: utf-8 -*-
# Copyright (C) 2005 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. office@spannberg.com
# ****************************************************************************
#
# This lifbrary is free software; you can redistribute it and/or
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
# License along with this liibrary; if not, write to the Free
# Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
#++
# Name
#    PMA.TKT.GTK.Office
#
# Purpose
#    Display of the mailboxes.
#
# Revision Dates
#     8-Jun-2005 (MG) Creation
#     1-Jan-2006 (MG) Changed to support only one inbox folder tree
#    ««revision-date»»···
#--
#
from   _PMA       import PMA
import _PMA._TKT
import _PMA._TKT._GTK
import _PMA._TKT._GTK.V_Box
import _PMA._TKT._GTK.Paned
import _PMA._TKT._GTK.Constants

class Office (PMA.TKT.GTK.V_Paned) :
    """Display of the mailboxes."""

    def __init__ (self, inbox_view, mailbox_views, AC = None) :
        self.__super.__init__           (name = "IB_MB_Pane", AC = AC)
        self._setup_inbox               (inbox_view)
        self._setup_mailboxes           (mailbox_views)
        self.show                       ()
    # end def __init__

    def _setup_inbox (self, inbox) :
        self.pack_top (inbox)
    # end def _setup_inbox

    def _setup_mailboxes (self, mailboxes) :
        pack = self.pack_bottom
        c    = 0
        for mb in mailboxes :
            pane = self.TNS.V_Paned (name = "MB_ane_%d" % (c, ), AC = self.AC)
            pack                    (pane)
            pack = pane.pack_bottom
            pane.pack_top           (mb.tkt)
            mb.tkt.show             ()
            mb.tkt.scroll_policies  (self.TNS.AUTOMATIC)
            pane.show               ()
            c += 1
    # end def _setup_mailboxes

# end class Office

if __name__ != "__main__" :
    PMA.TKT.GTK._Export ("*")
### __END__ PMA.TKT.GTK.Office


