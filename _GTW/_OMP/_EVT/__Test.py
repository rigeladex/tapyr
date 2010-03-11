# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.OMP.EVT.
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
#    GTW.OMP.EVT.__test__
#
# Purpose
#    Simple test
#
# Revision Dates
#     6-Feb-2010 (MG) Creation
#    ««revision-date»»···
#--

from   _MOM.import_MOM        import *
from   _GTW                   import GTW
import _GTW._OMP._SWP.import_SWP
import _GTW._OMP._PAP .import_PAP
import _GTW._OMP._EVT.Event

if 1 :
    from   _MOM._EMS.Hash         import Manager as EMS
    from   _MOM._DBW._HPS.Manager import Manager as DBW
else :
    from   _MOM._EMS.SAS          import Manager as EMS
    from   _MOM._DBW._SAS.Manager import Manager as DBW

from   _MOM                       import MOM
from   _MOM.Product_Version       import Product_Version, IV_Number

GTW.Version = Product_Version \
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

apt = MOM.App_Type \
    (u"HWO", GTW, PNS_Aliases = dict
       (EVT = GTW.OMP.EVT, SWP = GTW.OMP.SWP, PAP = GTW.OMP.PAP)
    ).Derived (EMS, DBW)

scope        = MOM.Scope.new (apt, None)
per          = scope.PAP.Person ("Test", "Author", raw = True)
page         = scope.SWP.Page   ("Title", text = "Text")
### __END__ GTW.OMP.EVT.__test__



