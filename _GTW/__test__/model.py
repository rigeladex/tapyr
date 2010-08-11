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
#    27-Apr-2010 (CT) `MOM.Scaffold` factored
#    12-May-2010 (MG) `create_test_dict` added
#    19-May-2010 (CT) `create_test_dict` improved (use dict interpolation,
#                     parameters `bpt` (backends per test), `combiner`)
#    26-May-2010 (CT) Use anonymous account and database `test` for MySQL
#     1-Jul-2010 (MG) Support for loading a scope added
#     4-Aug-2010 (MG) Changed to new Scaffold structure
#    ««revision-date»»···
#--

from   _GTW                   import GTW
from   _MOM                   import MOM
from   _TFL                   import TFL

from   _MOM.Product_Version   import Product_Version, IV_Number
from   _TFL                   import sos

import _GTW._OMP._Auth.import_Auth
import _GTW._OMP._EVT.import_EVT
import _GTW._OMP._PAP.import_PAP
import _GTW._OMP._SRM.import_SRM
import _GTW._OMP._SWP.import_SWP
import _GTW._OMP.Scaffold
import _TFL.Filename
import _TFL.Generators

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

class Scaffold (GTW.OMP.Scaffold) :

    ANS                   = GTW
    nick                  = u"MOMT"
    default_db_name       = "test"
    PNS_Aliases           = dict \
        ( Auth            = GTW.OMP.Auth
        , EVT             = GTW.OMP.EVT
        , PAP             = GTW.OMP.PAP
        , SRM             = GTW.OMP.SRM
        , SWP             = GTW.OMP.SWP
        )

    cmd__base__opts_x     = \
        ( "-config:C=~/.gtw-test.config?File specifying defaults for options"
        ,
        )
    cmd__wsgi__opts       = \
        ( "create:B=Run the fixtures function"
        ,
        )
    Backend_Parameters    = dict \
        ( HPS             = "'hps://'"
        , SQL             = "'sqlite://'"
        , POS             = "'postgresql://regtest:regtest@localhost/regtest'"
        , MYS             = "'mysql://:@localhost/test'"
        )
    Backend_Default_Path  = dict \
        ( (k, None) for k in Backend_Parameters)

    @classmethod
    def combiner (cls, backends, bpt) :
        if bpt > 1 :
            backends = backends + [backends [0]]
        return TFL.window_wise (backends, bpt)
    # end def combiner

    @classmethod
    def create_test_dict ( cls, test_spec
                         , backends = None
                         , bpt      = 1
                         , combiner = None
                         , ignore   = set ()
                         ) :
        result = {}
        if backends is None :
            backends = sos.environ.get ("GTW_test_backends", ("HPS:SQL"))
            if backends == "*" :
                backends = sorted (cls.Backend_Parameters)
            else :
                backends = list (p.strip () for p in backends.split (":"))
        if combiner is None :
            combiner = cls.combiner
        if isinstance (ignore, basestring) :
            ignore   = set ((ignore, ))
        elif not isinstance (ignore, set) :
            ignore   = set (ignore)
        if not isinstance (test_spec, dict) :
            test_spec = {"" : test_spec}
        for w in combiner ((b for b in backends if b not in ignore), bpt) :
            for name, code in test_spec.iteritems () :
                key = "_".join (p for p in (name, ) + w if p)
                result [key] = code % dict (cls._backend_spec (w))
        return result
    # end def create_test_dict

    @classmethod
    def _backend_spec (cls, backends) :
        i = 0
        for b in backends :
            i += 1
            path = cls.Backend_Default_Path [b]
            for k, v in zip \
                    ( ("p",                        "n",  "BN")
                    , (cls.Backend_Parameters [b], path, repr (b))
                    ) :
                yield ("%s%d" % (k, i), v)
    # end def _backend_spec

    @classmethod
    def do_run_server (cls, cmd) :
        from form_app import run
        apt, url  = cls.app_type_and_url (cmd.db_url, cmd.db_name)
        return run (cmd, apt, url)
    # end def do_run_server

    @classmethod
    def do_wsgi (cls, cmd) :
        from form_app import wsgi
        apt, url  = cls.app_type_and_url (cmd.db_url, cmd.db_name)
        return wsgi (cmd, apt, url)
    # end def do_wsgi

# end class Scaffold

Scope = Scaffold.scope

_Command = Scaffold.cmd

if __name__ == "__main__" :
    _Command ()
### __END__ GTW.__test__.model
