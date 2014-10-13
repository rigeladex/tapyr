# -*- coding: utf-8 -*-
# Copyright (C) 2005 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
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
#     2-Jan-2006 (CT) `sync_box` added
#     5-Jan-2006 (CT) `train_ham` and `train_spam` added
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
    , sync_box        = Key_Binder      ("<Shift>y")
    , train_ham       = Key_Binder      ("<Meta>h")
    , train_spam      = Key_Binder      ("<Meta>s")
    , unmark_message  = Key_Binder      ("u")
    )

if __name__ != "__main__" :
    PMA.TKT.GTK._Export ("Eventname")
### __END__ PMA.TKT.GTK.Eventname
