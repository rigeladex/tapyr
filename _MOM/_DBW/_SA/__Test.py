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

from   _MOM.__Test import *
import _MOM._DBW._SA.Session
import _MOM._EMS.SA

class Beaver (Mouse) :
    """Model a beaver of the Better Mouse Trap application."""

    class _Attributes (MOM.Object._Attributes) :

        class region (A_String) :
            """In wich are lives the beaver"""

            kind     = Attr.Optional

        # end class region

    # end class _Attributes

# end class Beaver

EMS   = MOM.EMS.SA.Manager
DBW   = MOM.DBW.SA.Session
apt   = MOM.App_Type                   ("BMT", MOM)
apt_c = apt.Derived                    (EMS, DBW)
MOM.Entity.m_setup_etypes              (apt)
apt_c.setup_etypes                     ()
scope = MOM.Scope                      (apt_c)
MOM.DBW.SA.Session.Mapper              (scope.MOM.Mouse._etype)
MOM.DBW.SA.Session.Mapper              (scope.MOM.Beaver._etype)
MOM.DBW.SA.Session.Mapper              (scope.MOM.Rat._etype)
MOM.DBW.SA.Session.Mapper              (scope.MOM.Trap._etype)

session    = scope.dbw.session
session.bind.echo = True
MOM.DBW.SA.Session.metadata.create_all (MOM.DBW.SA.Session.engine)
session.bind.echo = False
dMOM       = scope.MOM
#session.bind.echo = True
m          = dMOM.Mouse ("Mighty Mouse")
print dMOM.Mouse.s_count
print dMOM.Mouse.exists      (m.name)
print dMOM.Mouse.instance    (m.name)
print dMOM.Mouse.instance    ("<Baz>")
print list (dMOM.Mouse.s_extension ())
print dMOM.Rodent.t_count

### __END__ __Test
