# -*- coding: utf-8 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.OMP.SRM.
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
#    GTW.OMP.SRM.__babel__
#
# Purpose
#    This file is the entry point for the Babel translation extraction
#    process.
#
# Revision Dates
#    10-May-2010 (CT) Creation
#    ««revision-date»»···
#--

from   _MOM.import_MOM import *
import _MOM.Babel
import _GTW._OMP._SRM.import_SRM

def main (encoding, config, method) :
    from   _MOM._EMS.Hash         import Manager as EMS
    from   _MOM._DBW._HPS.Manager import Manager as DBW
    from   _GTW                   import GTW

    return MOM.Babel.Add_Translations \
        ( encoding, config, method
        , MOM.App_Type ("SRM", GTW).Derived (EMS, DBW)
        )
# end def main

### __END__ GTW.OMP.SRM.__babel__
