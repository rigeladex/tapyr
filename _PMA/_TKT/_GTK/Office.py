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


