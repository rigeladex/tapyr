# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package MOM.
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
#    MOM.__test__
#
# Purpose
#    Some helper functions for MOM related testing
#
# Revision Dates
#    18-Feb-2010 (MG) Creation
#    ««revision-date»»···
#--

from   _MOM.import_MOM           import *
from   _MOM.Product_Version      import Product_Version, IV_Number

Version = Product_Version \
    ( productid           = u"GTW Test"
    , productnick         = u"GTW"
    , productdesc         = u"Example web application "
    , date                = "20-Jan-2010"
    , major               = 0
    , minor               = 5
    , patchlevel          = 42
    , author              = u"Christian Tanzer, Martin Glück"
    , copyright_start     = 2010
    , db_version          = IV_Number
        ( "db_version"
        , ("Hello World", )
        , ("Hello World", )
        , program_version = 1
        , comp_min        = 0
        , db_extension    = ".how"
        )
    )

def define_app_type (name, PKG, EMS, DBW, ** pns_aliases) :
    if name not in MOM.App_Type.Table :
        PKG.Version = Version
        MOM.App_Type (name, PKG, PNS_Aliases = pns_aliases)
    app = MOM.App_Type.Table [name]
    return app.Derived (EMS, DBW)
# end def define_app_type

### __END__ __test__
