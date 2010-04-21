# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.__test__.
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
#    GTW.__test__.model
#
# Purpose
#    Helper function to create the App-Type for other tests
#
# Revision Dates
#    21-Apr-2010 (MG) Creation
#    ««revision-date»»···
#--

from   _TFL                   import TFL
import _TFL.Filename

from   _GTW                   import GTW
from   _MOM                   import MOM
from   _MOM.Product_Version   import Product_Version, IV_Number
from   _TFL                   import sos

import _GTW._OMP._Auth.import_Auth
import _GTW._OMP._PAP.import_PAP
import _GTW._OMP._EVT.import_EVT

GTW.Version = Product_Version \
    ( productid           = u"MOM/GTW Test Cases"
    , productnick         = u"MOM-Test"
    , productdesc         = u"Test application for the regressiontest"
    , date                = "21-Apr-2010 "
    , major               = 0
    , minor               = 1
    , patchlevel          = 2
    , author              = u"Martin Glueck/Christian Tanzer"
    , copyright_start     = 2010
    , db_version          = IV_Number
        ( "db_version"
        , ("MOMT", )
        , ("MOMT", )
        , program_version = 1
        , comp_min        = 0
        , db_extension    = ".momt"
        )
    )

def app_type (* ems_dbw) :
    result = MOM.App_Type.Table.get ("MOMT")
    if result is None :
        result = MOM.App_Type \
            ( u"MOMT", GTW
            , PNS_Aliases = dict
                ( Auth = GTW.OMP.Auth
                , PAP  = GTW.OMP.PAP
                , SWP  = GTW.OMP.SWP
                )
            )
    if ems_dbw :
        result = result.Derived (* ems_dbw)
    return result
# end def app_type

def app_type_hps () :
    from _MOM._EMS.Hash         import Manager as EMS
    from _MOM._DBW._HPS.Manager import Manager as DBW
    return app_type (EMS, DBW)
# end def app_type_hps

def app_type_sas () :
    from _MOM._EMS.SAS          import Manager as EMS
    from _MOM._DBW._SAS.Manager import Manager as DBW
    return app_type (EMS, DBW)
# end def app_type_sas

def Scope (db_prefix = None, db_name = None, create = True) :
    uri = None
    if db_prefix :
        apt = app_type_sas  ()
        if db_prefix.startswith ("sqlite:////") :
            ### SQLite database with absolute path
            uri = "".join ((db_prefix, db_name))
        elif db_name :
            uri = sos.path.join \
                (db_prefix, TFL.Filename (db_name).base_ext)
    else :
        apt = app_type_hps  ()
        if db_name :
            uri = "%s.ams" %    (db_name, )
        if not uri or not sos.path.exists (uri) :
            create = True
    if create :
        print "Creating new scope", apt, uri or "in memory"
        if uri :
            apt.delete_database (uri)
        scope = MOM.Scope.new   (apt, uri)
    else :
        print "Loading scope", apt, uri
        scope = MOM.Scope.load (apt, uri)
    return scope
# end def Scope

### __END__ GTW.__test__.model
