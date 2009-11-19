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

from   _MOM.__doc__          import *
import _MOM._EMS.Hash
import _MOM._DBW.Session

EMS   = MOM.EMS.Hash.Manager
DBW   = MOM.DBW.Session ### XXX change to a real DBW
apt   = MOM.App_Type                 ("BMT", MOM)
apt_c = apt.Derived                  (EMS, DBW)
scope = MOM.Scope                    (apt_c)
RiT   = scope.MOM.Rodent_in_Trap
if 1 :
    m     = scope.MOM.Mouse          ("Mighty_Mouse")
    r     = scope.MOM.Rat            ("Rutty_Rat")
    axel  = scope.MOM.Rat            ("Axel")
    t1    = scope.MOM.Trap           ("X", 1)
    t2    = scope.MOM.Trap           ("X", 2)
    t3    = scope.MOM.Trap           ("Y", 1)
    if 1 :
        mit   = RiT                  (m,    t1)
        rit   = RiT                  (r,    t3)
        xit   = RiT                  (axel, t2)
if 1 :
    print scope.MOM.Mouse.t_extension          ()
    print scope.MOM.Rat.t_extension            ()
    print scope.MOM.Trap.t_extension           ()
    print scope.MOM.Rodent.t_extension         ()
    print scope.MOM.Named_Object.t_extension   ()
    print scope.MOM.Object.t_extension         ()
    print
    print scope.MOM.Rodent_in_Trap.t_extension ()
    print scope.MOM.Rodent_in_Trap.t_extension \
        (TFL.Sorted_By (RiT.right.sort_key, RiT.left.sort_key))
    print
    print scope.MOM.Rodent_in_Trap.s_extension ()
    print scope.MOM.Rodent_in_Trap.s_left      (t1)
    print scope.MOM.Rodent_in_Trap.s_left      (t2)
    print scope.MOM.Rodent_in_Trap.s_left      (t3)
    print scope.MOM.Rodent_in_Trap.t_left      (t1)
    print scope.MOM.Rodent_in_Trap.t_left      (t2)
    print scope.MOM.Rodent_in_Trap.t_left      (t3)
    print scope.MOM.Rodent_in_Trap.s_right     (m)
    print scope.MOM.Rodent_in_Trap.s_right     (r)
    print scope.MOM.Rodent_in_Trap.t_right     (m)
    print scope.MOM.Rodent_in_Trap.t_right     (r)

if 0 :
    import pdb; pdb.set_trace ()
    m.color = "white"

### __END__ MOM.EMS.__Test
