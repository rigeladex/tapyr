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
#    PMA.TKT.GTK.Eventname
#
# Purpose
#    Define PMA specific eventnames for GTK
#    ««text»»···
#
# Revision Dates
#    28-Jul-2005 (CT) Creation
#    30-Jul-2005 (MG) New commands added
#    31-Jul-2005 (MG) New commands added
#    ««revision-date»»···
#--

from   _PMA                        import PMA
from   _TGL                        import TGL
import _TGL._TKT._GTK
import _TGL._TKT._GTK.Eventname

Eventname       = TGL.TKT.GTK.Eventname
Key_Binder      = TGL.TKT.GTK.Key_Binder
Combined_Binder = TGL.TKT.GTK.Combined_Binder

Eventname.add \
    ( commit_box      = Key_Binder      ("<Control>Return")
    , commit_message  = Key_Binder      ("<Alt>Return")
    , copy_message    = Key_Binder      ("c")
#    , delete_message  = Combined_Binder (Key_Binder ("d"), Key_Binder ("Delete"))
    , delete_message  = Key_Binder      ("d")
    , forward_message = Key_Binder      ("<Shift>f")
    , move_message    = Key_Binder      ("m")
    , next_message    = Key_Binder      ("n")
    , next_unseen     = Key_Binder      ("<Shift>n")
    , prev_message    = Key_Binder      ("p")
    , prev_unseen     = Key_Binder      ("<Shift>p")
    , reply           = Key_Binder      ("r")
    , reply_all       = Key_Binder      ("<Shift>r")
    , resend_message  = Key_Binder      ("f")
    , select_all      = Key_Binder      ("<Control>a")
    , unmark_message  = Key_Binder      ("u")
    )

if __name__ != "__main__" :
    PMA.TKT.GTK._Export ("Eventname")
### __END__ PMA.TKT.GTK.Eventname
