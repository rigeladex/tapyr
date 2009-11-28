# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
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
#    MOM.DBW.SA.__Test
#
# Purpose
#    «text»···
#
# Revision Dates
#    20-Oct-2009 (MG) Creation
#    26-Nov-2009 (CT) Use `except ... as ...` (3-compatibility)
#    ««revision-date»»···
#--

from   _MOM.__doc__ import *
import _MOM._DBW._SA.Session
import _MOM._EMS.SA

EMS     = MOM.EMS.SA.Manager
DBW     = MOM.DBW.SA.Session
apt     = MOM.App_Type    ("BMT", BMT).Derived     (EMS, DBW)

scope   = MOM.Scope       (apt)
DBW.metadata.create_all   (DBW.engine)


session           = scope.dbw.session
session.bind.echo = False
dBMT              = scope.BMT
session.bind.echo = True * 0

p     = scope.BMT.Person     ("Luke", "Lucky")
q     = scope.BMT.Person     ("Dog",  "Snoopy")
l1    = scope.BMT.Location   (-16.268799, 48.189956)
l2    = scope.BMT.Location   (-16.740770, 48.463313)
m     = scope.BMT.Mouse      ("Mighty_Mouse")
b     = scope.BMT.Beaver     ("Toothy_Beaver")
r     = scope.BMT.Rat        ("Rutty_Rat")
axel  = scope.BMT.Rat        ("Axel")
t1    = scope.BMT.Trap       ("X", 1)
t2    = scope.BMT.Trap       ("X", 2)
t3    = scope.BMT.Trap       ("Y", 1)
t4    = scope.BMT.Trap       ("Y", 2)

RiT   = scope.BMT.Rodent_in_Trap
PoT   = scope.BMT.Person_owns_Trap
PTL   = scope.BMT.Person_sets_Trap_at_Location

#RiT (m, t1)
#RiT (r, t3)
#RiT (p, t1)
#print scope.MOM.Named_Object.exists ("Mighty_Mouse")
#print scope.BMT.Rodent.exists ("Mighty_Mouse")
#print scope.BMT.Rodent.s_extension ()
#print list (scope)
axel.set (name = "betty")
### __END__ __Test
