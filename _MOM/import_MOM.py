# -*- coding: iso-8859-15 -*-
# Copyright (C) 2009-2013 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package _MOM.
#
# This module is free software; you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this library. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    MOM.import_MOM
#
# Purpose
#    Provide all imports necessary to define application-specific essential
#    classes based on the MOM meta object model
#
#    Usage:
#        from MOM.import_MOM import *
#
# Revision Dates
#    22-Oct-2009 (CT) Creation
#     7-Dec-2009 (CT) `Q` added
#    22-Dec-2009 (CT) `Sequence_Number` removed
#     4-May-2010 (CT) `Q` moved to `MOM.Attr.Type`
#     5-Jul-2011 (CT) `MOM.Attr.Selector` added
#    19-Jul-2011 (CT) `MOM.Q_Exp_Raw` added
#    15-Jun-2013 (CT) Import `Derived_PNS`
#    ««revision-date»»···
#--

from   _MOM import MOM
from   _TFL import TFL

import _MOM.App_Type
import _MOM.Entity
import _MOM.Error
import _MOM.Link
import _MOM.Object
import _MOM.Q_Exp_Raw
import _MOM.Scope

import _MOM._Attr.Selector

from   _MOM._Attr.Type  import *
from   _MOM._Attr       import Attr
from   _MOM._Pred       import Pred

import _MOM.Derived_PNS

### __END__ MOM.import_MOM
