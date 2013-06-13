# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2013 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.OMP.PAP.
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
#    GTW.OMP.PAP.__test__
#
# Purpose
#    Simple test
#
# Revision Dates
#     6-Feb-2010 (MG) Creation
#    24-Feb-2010 (CT) s/Lifetime/Date_Interval/
#    13-Jun-2013 (CT) Remove `PNS_Aliases`
#    ««revision-date»»···
#--

from   _MOM.import_MOM        import *
from   _GTW                   import GTW
from   _MOM.import_MOM        import Q
import _GTW._OMP._Auth.import_Auth
import _GTW._OMP._PAP .import_PAP

if 0 :
    from   _MOM._EMS.Hash         import Manager as EMS
    from   _MOM._DBW._HPS.Manager import Manager as DBW
else :
    from   _MOM._EMS.SAS          import Manager as EMS
    from   _MOM._DBW._SAS.Manager import Manager as DBW

from   _MOM                      import MOM
from   _MOM.Product_Version      import Product_Version, IV_Number

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

apt = MOM.App_Type (u"HWO", GTW).Derived (EMS, DBW)

if 1:
    scope        = MOM.Scope.new (apt, None)
    p            = scope.PAP.Person ("Glueck", "Martin")
    #a            = scope.PAP.Address ("Langstrasse 4", "2244", "Spannberg", "Austria")
    date         = scope.MOM.Date_Interval (start ="1976-03-16", raw = True)
    p.date       = date
    scope.commit ()
    scope.ems.session.expunge ()
    scope.PAP.Person.query ().all ()
    #q_fn         = Q.first_name.STARTSWITH ("Ma")
    #q_sb         = Q.first_name
    #print q_fn (p.__class__._SAQ)

else :
    #scope = MOM.Scope.load (apt, "sqlite:///test.sqlite")
    scope = MOM.Scope.load (apt, None)
    address.position = pos
    scope.commit ()
### __END__ GTW.OMP.PAP.__test__
