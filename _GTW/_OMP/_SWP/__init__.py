# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This package is part of the package GTW.OMP.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    GTW.OMP.SWP.__init__
#
# Purpose
#    Package defining a partial object model for static web pages
#
# Revision Dates
#    31-Jan-2010 (CT) Creation
#     9-Oct-2012 (CT) Add `_desc_`
#    15-Jun-2013 (CT) Use `MOM.Derived_PNS`
#    ««revision-date»»···
#--

from   _GTW._OMP              import OMP
from   _MOM                   import MOM
import _MOM.Derived_PNS

_desc_ = """
Partial object model for static web pages.
"""

SWP = MOM.Derived_PNS (parent = MOM, pns_alias = "SWP")
OMP._Export ("SWP")

### __END__ GTW.OMP.SWP.__init__
