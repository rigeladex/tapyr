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
#    MOM.Link
#
# Purpose
#    Root class for link-types of MOM meta object model
#
# Revision Dates
#    22-Oct-2009 (CT) Creation (factored from TOM.Link)
#    ««revision-date»»···
#--

from   _TFL      import TFL
from   _MOM      import MOM

from   _MOM._Attr.Type import *
from   _MOM._Attr      import Attr
from   _MOM._Pred      import Pred

import  _MOM._Meta.M_Link

import _MOM.Entity

class _MOM_Link_ (MOM.Id_Entity) :
    """Root class for link-types of MOM meta object model."""

    __metaclass__         = MOM.Meta.M_Link
    _real_name            = "Link"
    entity_kind           = "link"

Link = _MOM_Link_ # end class

if __name__ != "__main__" :
    MOM._Export ("*")
### __END__ MOM.Link
