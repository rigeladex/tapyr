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
#    ��revision-date�����
#--

from   _MOM import MOM
from   _TFL import TFL

import _MOM.App_Type
import _MOM.Entity
import _MOM.Error
import _MOM.Link
import _MOM.Object
import _MOM.Scope
import _MOM.Sequence_Number

from   _MOM._Attr.Type import *
from   _MOM._Attr      import Attr
from   _MOM._Pred      import Pred

### __END__ MOM.import_MOM
