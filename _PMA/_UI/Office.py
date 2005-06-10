# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 TTTech Computertechnik AG. All rights reserved
# Schönbrunnerstraße 7, A--1040 Wien, Austria. office@undefined.dontknow
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
#    PMA.UI.Office
#
# Purpose
#    Abstract user interface for office
#
# Revision Dates
#     8-Jun-2005 (MG) Creation
#    ««revision-date»»···
#--

from   _TGL                    import TGL
from   _PMA                    import PMA

import _PMA._UI
import _PMA._UI.Mixin
import _PMA._UI.Mailbox_BV
import _PMA._UI.Mailbox_MV

class Office (PMA.UI.Mixin) :
    """Abstract user interface for PMA office."""
    
    def __init__ ( self
                 , model
                 , inboxes   = ()
                 , mailboxes = ()
                 , AC        = None
                 ) :
        self.__super.__init__ (AC = AC)
        UI                  = self.ANS.UI
        TNS                 = self.TNS
        self.inboxes        = inboxes
        self.mailboxes      = mailboxes
        self.inbox_views    = []
        self.mailbox_views  = []
        self.current_folder = None, ()
        try :
            for boxes, l in ( (inboxes,   self.inbox_views)
                            , (mailboxes, self.mailbox_views)
                            ) :
                for box in boxes :
                    bv = UI.Mailbox_BV \
                        (AC = self.AC, show_header = False)
                    bv.update_model (box)
                    l.append        (bv)
            self.tkt = TNS.Office \
                (self.inbox_views, self.mailbox_views, AC = AC)
            self.mb_msg_view = mmv = UI.Mailbox_MV \
                (sort = True, AC = self.AC)
            mmv.tkt.scroll_policies (TNS.AUTOMATIC)
        except AttributeError :
            import traceback
            traceback.print_exc ()
            pass
        else :
            tkt = model.tkt
            tkt.pack (tkt.wc_mb_msg_view, mmv.tkt)
            tkt.pack (tkt.wc_po_box_view, self.tkt)
            interfacers = dict \
                ( cm = TNS.CI_Menu         (name = "context_menu", AC = AC)
                , ev = TNS.CI_Event_Binder
                      ( AC
                      , * [b.tkt for b in ( self.inbox_views
                                           + self.mailbox_views
                                           )
                          ]
                      )
                )
            self.bv_cmd = UI.Command_Mgr \
                ( change_counter = model.changes
                , interfacers    = interfacers
                , if_names       = ("cm:click_3", )
                , AC             = AC
                )
            self.bv_cmd.add_command \
                ( UI.Command ("Select", self.select_folder)
                , if_names = ("cm", "ev:Cursor_Changed")
                )
    # end def __init__

    def select_folder (self, event = None) :
        tree = event.widget
        old_tree, selection = self.current_folder
        if old_tree and old_tree is not tree :
            old_tree.clear_selection ()
        folder = tree.selection ()
        self.current_folder = tree, folder
        self.mb_msg_view.update_model (folder [0])
    # end def 
    
# end class Office

if __name__ != "__main__" :
    PMA.UI._Export ("*")
### __END__ PMA.UI.Office


