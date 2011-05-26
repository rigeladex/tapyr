# -*- coding: iso-8859-15 -*-
# Copyright (C) 2009 Mag. Christian Tanzer All rights reserved
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
#    MOM.Product_Version
#
# Purpose
#    Model product version of form `major.minor.patchlevel'
#
# Revision Dates
#    18-Dec-2009 (CT) Creation
#    ««revision-date»»···
#--

from _MOM import MOM

from _TFL.Product_Version import *

if __name__ == "__main__" :
    MOM._Export ("Product_Version")
### __END__ MOM.Product_Version
