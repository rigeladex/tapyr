# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
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
#    MOM.EMS.__Test
#
# Purpose
#    Test for MOM.EMS
#
# Revision Dates
#    21-Oct-2009 (CT) Creation
#     4-Nov-2009 (CT) Creation continued
#    19-Nov-2009 (CT) Creation continued..
#    ««revision-date»»···
#--

from _MOM.__doc__           import *
from _MOM._EMS.Hash         import Manager as EMS
from _MOM._DBW._HPS.Manager import Manager as DBW

apt = MOM.App_Type ("BMT", BMT).Derived (EMS, DBW)
scope = MOM.Scope.new (apt, "/tmp/bmt_test")
RiT   = scope.BMT.Rodent_in_Trap
PoT   = scope.BMT.Person_owns_Trap
PTL   = scope.BMT.Person_sets_Trap_at_Location
ET_Mouse = apt ["BMT.Mouse"]
if 1 :
    m     = scope.BMT.Mouse      ("Mighty_Mouse")
    p     = scope.BMT.Person     ("Luke", "Lucky")
    q     = scope.BMT.Person     ("Dog",  "Snoopy")
    l1    = scope.BMT.Location   (-16.268799, 48.189956)
    l2    = scope.BMT.Location   (-16.740770, 48.463313)
    b     = scope.BMT.Beaver     ("Toothy_Beaver")
    r     = scope.BMT.Rat        ("Rutty_Rat")
    axel  = scope.BMT.Rat        ("Axel")
    t1    = scope.BMT.Trap       ("X", 1)
    t2    = scope.BMT.Trap       ("X", 2)
    t3    = scope.BMT.Trap       ("Y", 1)
    mit   = RiT                  (m,    t1)
    rit   = RiT                  (r,    t3)
    xit   = RiT                  (axel, t2)
    PoT (p, t1)
    PoT (p, t2)
    PoT (q, t3)
    PTL (p, t1, l1)
    PTL (p, t2, l2)
    PTL (p, t3, l2)
if 0 :
    print scope.BMT.Mouse.t_extension          ()
    print scope.BMT.Rat.t_extension            ()
    print scope.BMT.Trap.t_extension           ()
    print scope.BMT.Rodent.t_extension         ()
    print scope.MOM.Named_Object.t_extension   ()
    print scope.MOM.Object.t_extension         ()
    print
    print scope.BMT.Rodent_in_Trap.t_extension ()
    print scope.BMT.Rodent_in_Trap.t_extension \
        (TFL.Sorted_By (RiT.right.sort_key, RiT.left.sort_key))
    print
    print scope.BMT.Rodent_in_Trap.s_extension ()
    print scope.BMT.Rodent_in_Trap.s_left      (t1)
    print scope.BMT.Rodent_in_Trap.s_left      (t2)
    print scope.BMT.Rodent_in_Trap.s_left      (t3)
    print scope.BMT.Rodent_in_Trap.t_left      (t1)
    print scope.BMT.Rodent_in_Trap.t_left      (t2)
    print scope.BMT.Rodent_in_Trap.t_left      (t3)
    print scope.BMT.Rodent_in_Trap.s_right     (m)
    print scope.BMT.Rodent_in_Trap.s_right     (r)
    print scope.BMT.Rodent_in_Trap.t_right     (m)
    print scope.BMT.Rodent_in_Trap.t_right     (r)
    print
    print PoT.trap (p)
    print PoT.trap (("Dog",  "Snoopy"))
    print
    print PTL.s_middle_right (p)
    print PTL.s_left_middle  ((-16.74077, 48.463313))
    print PTL.s_left_right   (("Y", "1"))

if 0 :
    import pdb; pdb.set_trace ()
    m.color = "white"

### __END__ MOM.EMS.__Test
