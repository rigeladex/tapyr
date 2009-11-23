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
#    20-Oct-2009 (NN) Creation
#    ««revision-date»»···
#--

from   _MOM.__doc__ import *
import _MOM._DBW._SA.Session
import _MOM._EMS.SA

EMS     = MOM.EMS.SA.Manager
DBW     = MOM.DBW.SA.Session
apt     = MOM.App_Type    ("BMT", BMT)
apt_c   = apt.Derived     (EMS, DBW)
scope   = MOM.Scope       (apt_c)
DBW.metadata.create_all   (DBW.engine)

session           = scope.dbw.session
session.bind.echo = False
dBMT              = scope.BMT
session.bind.echo = True * 0
#import pdb;pdb.set_trace ()
dBMT.Mouse  ("Mighty_Mouse")
dBMT.Beaver ("Beaver")
dBMT.Mouse  ("Magic_Mouse")
dBMT.Beaver ("Beaver_2")
dBMT.Otter  ("Otter")
dBMT.Trap   ("Mouse_Trap", 1)
dBMT.Trap   ("Mouse_Trap", 2)

session.commit ()
for et in dBMT.Mouse, dBMT.Beaver, dBMT.Otter :
    print et.s_count, et.s_extension ().all ()
    print et.t_count, et.t_extension ().all ()
print dBMT.Mouse.instance ("Mighty_Mouse")
print dBMT.Mouse.instance ("<baz>"), " ===None"
try :
    dBMT.Mouse  ("Mighty_Mouse")
    raise ValueError ("No Name_Clash")
except MOM.Error.Name_Clash, exc :
    print "OK", exc
try :
    ### we test if multi-attr epk's work
    dBMT.Trap ("Mouse_Trap", 1)
    raise ValueError ("No Name_Clash")
except MOM.Error.Name_Clash, exc :
    print "OK", exc
### __END__ __Test
