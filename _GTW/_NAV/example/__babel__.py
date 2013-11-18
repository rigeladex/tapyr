# -*- coding: utf-8 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.OMP.Auth.
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
#    GTW.NAV.example.__babel__
#
# Purpose
#    This file is the entry point for the Babel translation extraction
#    process.
#
# Revision Dates
#    21-Jan-2010 (MG) Creation
#    ««revision-date»»···
#--

from   _MOM.import_MOM import *
import _MOM.Babel
import _GTW._NAV.example.app_import
import _JNJ

def main (encoding, config, method) :
    from   _MOM._EMS.Hash         import Manager as EMS
    from   _MOM._DBW._HPS.Manager import Manager as DBW
    from   _GTW                   import GTW

    return MOM.Babel.Add_Translations \
        ( encoding, config, method
        , MOM.App_Type ("Auth", GTW).Derived (EMS, DBW))
# end def main

### __END__ GTW.NAV.example.__babel__
