# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010 Mag. Christian Tanzer. All rights reserved
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
#    GTW.Form.MOM.__init__
#
# Purpose
#    Support for web forms for MOM
#
# Revision Dates
#    15-Jan-2010 (MG) Creation
#    ««revision-date»»···
#--

from   _TFL.Package_Namespace import Package_Namespace
from   _GTW._Form             import Form

MOM = Package_Namespace ()
Form._Export ("MOM")

del Package_Namespace

### __END__ GTW.Form.MOM.__init__
