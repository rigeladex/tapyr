# -*- coding: utf-8 -*-
# Copyright (C) 2009-2010 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This package is part of the package _MOM.
#
# This package is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This package is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this package.  If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    MOM.EMS.__init__
#
# Purpose
#    Package for entity manager strategies for MOM
#
# Revision Dates
#    14-Oct-2009 (CT) Creation
#    ««revision-date»»···
#--

from   _MOM                   import MOM
from   _TFL.Package_Namespace import Package_Namespace

EMS = Package_Namespace ()
MOM._Export ("EMS")

del Package_Namespace

### __END__ MOM.EMS.__init__
