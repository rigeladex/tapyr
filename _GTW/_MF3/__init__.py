# -*- coding: utf-8 -*-
# Copyright (C) 2014 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This package is part of the package GTW.
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
# along with this package. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    GTW.MF3.__init__
#
# Purpose
#    Package providing support for MOM forms, 3rd edition
#
# Revision Dates
#    24-Apr-2014 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL.Package_Namespace import Package_Namespace
from   _GTW                   import GTW

MF3 = Package_Namespace ()
GTW._Export ("MF3")

del Package_Namespace

### __END__ GTW.MF3.__init__
