# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2012 Martin Glueck All rights reserved
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
#    27-Apr-2010 (CT) `MOM.Scaffold` factored
#    12-May-2010 (MG) `create_test_dict` added
#    19-May-2010 (CT) `create_test_dict` improved (use dict interpolation,
#                     parameters `bpt` (backends per test), `combiner`)
#    26-May-2010 (CT) Use anonymous account and database `test` for MySQL
#     1-Jul-2010 (MG) Support for loading a scope added
#     4-Aug-2010 (MG) Changed to new Scaffold structure
#    11-Aug-2010 (MG) `create_test_dict`: parameter `ignore` added
#    11-Aug-2010 (MG) `GTW_FULL_OBJECT_MODEL` added
#    12-Aug-2010 (MG) Fixture support handling added
#    16-Aug-2010 (MG) `scope` added to change the default of `verbose`
#    14-Jun-2011 (MG) `MYST` added to `Backend_Parameters`
#     9-Sep-2011 (CT) `from import_MOM import *` added
#    27-Jan-2012 (CT) Derive from `GTW.Werkzeug.Scaffold`
#    17-Apr-2012 (CT) Add `formatted`, `formatted_1`
#    26-Jul-2012 (CT) Adapt to use of `GTW.RST.TOP` instead of `GTW.NAV`
#    18-Sep-2012 (CT) Factor _GTW/__test__/Test_Command.py
#    ««revision-date»»···
#--

from   _GTW.__test__.Test_Command import *

import _GTW._OMP._Auth.import_Auth

if sos.environ.get ("GTW_FULL_OBJECT_MODEL", "True") != "False" :
    import _GTW._OMP._EVT.import_EVT
    import _GTW._OMP._EVT.Nav
    PNS_Dict = dict (EVT = GTW.OMP.EVT)
else :
    PNS_Dict = dict ()

import _GTW._OMP._PAP.import_PAP
import _GTW._OMP._SRM.import_SRM
import _GTW._OMP._SWP.import_SWP

import _GTW._OMP._PAP.Nav
import _GTW._OMP._SRM.Nav
import _GTW._OMP._SWP.Nav

class _GTW_Test_Command_ (GTW_Test_Command) :

    _rn_prefix            = "_GTW_Test"

    PNS_Aliases           = dict \
        ( Auth            = GTW.OMP.Auth
        , PAP             = GTW.OMP.PAP
        , SRM             = GTW.OMP.SRM
        , SWP             = GTW.OMP.SWP
        , ** PNS_Dict
        )

    SALT                  = bytes \
        ( "ohQueiro7theG4vai9shi4oi9iedeethaeshooqu7oThi9Eecephaj")

    def fixtures (self, scope) :
        if sos.environ.get ("GTW_FIXTURES") :
            from _GTW.__test__.form_app import fixtures
            fixtures (scope)
    # end def fixtures

    def _nav_admin_groups (self) :
        RST = GTW.RST
        return \
            [ self.nav_admin_group
                ( "Personenverwaltung"
                , "Verwaltung von Personen und ihren Eigenschaften"
                , "GTW.OMP.PAP"
                )
            , self.nav_admin_group
                ( "Benutzerverwaltung"
                , "Verwaltung von Benutzer-Konten und Gruppen"
                , "GTW.OMP.Auth"
                , permission = RST.Is_Superuser ()
                )
            , self.nav_admin_group
                ( "Regattaverwaltung"
                , "Verwaltung von Regatten, Booten, "
                  "Teilnehmern und Ergebnissen"
                , "GTW.OMP.SRM"
                , show_aliases = True
                )
            , self.nav_admin_group
                ( "Webseitenverwaltung"
                , "Verwaltung der Webseiten"
                , "GTW.OMP.SWP", "GTW.OMP.EVT"
                , show_aliases = True
                )
            ]
    # end def _nav_admin_groups

_Command_  = _GTW_Test_Command_ # end class

Scaffold   = _Command_ ()

### __END__ GTW.__test__.model
