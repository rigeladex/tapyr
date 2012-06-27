# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.__test__.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.__test__.RST
#
# Purpose
#    Test RESTful api
#
# Revision Dates
#    27-Jun-2012 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _JNJ                     import JNJ
from   _MOM                     import MOM
from   _TFL                     import TFL

from   _MOM.import_MOM          import *
from   _MOM.Product_Version     import Product_Version, IV_Number

from   _TFL                     import sos
from   _TFL._Meta.Once_Property import Once_Property
from   _TFL._Meta.Property      import Class_Property
from   _TFL.I18N                import _, _T, _Tn

from   _TFL.Formatter           import Formatter, formatted_1

formatted = Formatter (width = 240)

import _GTW._Werkzeug.Command_X

import _GTW._OMP._PAP.import_PAP
import _GTW._OMP._SRM.import_SRM

import datetime

GTW.Version = Product_Version \
    ( productid           = u"MOM/GTW Test Cases"
    , productnick         = u"MOM-Test"
    , productdesc         = u"Test application for the regressiontest"
    , date                = "27-Jun-2012 "
    , major               = 0
    , minor               = 2
    , patchlevel          = 0
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

_Ancestor = GTW.Werkzeug.Command_X

class _GTW_Test_Command_ (_Ancestor) :

    _rn_prefix            = "_GTW_Test"

    ANS                   = GTW
    nick                  = u"MOMT"
    default_db_name       = "test"
    PNS_Aliases           = dict \
        ( PAP             = GTW.OMP.PAP
        , SRM             = GTW.OMP.SRM
        )

    SALT                  = bytes \
        ( "ohQueiro7theG4vai9shi4oi9iedeethaeshooqu7oThi9Eecephaj")

    _defaults               = dict \
        ( config            = "~/.gtw-test.config"
        , fixtures          = "yes"
        , port              = 9090
        , UTP               = "RST"
        )

    Backend_Parameters    = dict \
        ( HPS             = "'hps://'"
        , SQL             = "'sqlite://'"
        , POS             = "'postgresql://regtest:regtest@localhost/regtest'"
        , MYS             = "'mysql://:@localhost/test'"
        , MYST            = "'mysql://:@localhost/test?unix_socket=/var/run/mysqld/mysqld-ram.sock'"
        )

    Backend_Default_Path  = dict \
        ( (k, None) for k in Backend_Parameters)

    def combiner (self, backends, bpt) :
        if bpt > 1 :
            backends = backends + [backends [0]]
        return TFL.window_wise (backends, bpt)
    # end def combiner

    def create_rst (self, cmd, app_type, db_url, ** kw) :
        from _GTW._RST import MOM as R_MOM
        return GTW.RST.Root \
            ( App_Type          = app_type
            , DB_Url            = db_url
            , encoding          = cmd.output_encoding
            , HTTP              = cmd.HTTP
            , input_encoding    = cmd.input_encoding
            , language          = "de"
            , entries           = [R_MOM.Scope (name = "v1")]
            , ** kw
            )
    # end def create_rst

    def create_test_dict ( self, test_spec
                         , backends = None
                         , bpt      = 1
                         , combiner = None
                         , ignore   = set ()
                         ) :
        result = {}
        if backends is None :
            backends = sos.environ.get ("GTW_test_backends", ("HPS:SQL"))
            if backends == "*" :
                backends = sorted (self.Backend_Parameters)
            else :
                backends = list (p.strip () for p in backends.split (":"))
        if combiner is None :
            combiner = self.combiner
        if isinstance (ignore, basestring) :
            ignore   = set ((ignore, ))
        elif not isinstance (ignore, set) :
            ignore   = set (ignore)
        if not isinstance (test_spec, dict) :
            test_spec = {"" : test_spec}
        for w in combiner ((b for b in backends if b not in ignore), bpt) :
            for name, code in test_spec.iteritems () :
                key = "_".join (p for p in (name, ) + w if p)
                result [key] = code % dict (self._backend_spec (w))
        return result
    # end def create_test_dict

    def fixtures (self, scope) :
        PAP   = scope.PAP
        SRM   = scope.SRM
        BiR   = SRM.Boat_in_Regatta
        ct    = PAP.Person ("Tanzer", "Christian")
        lt    = PAP.Person ("Tanzer", "Laurens", "William")
        cat   = PAP.Person ("Tanzer", "Clarissa", "Anna")
        ct_s  = SRM.Sailor (ct,  nation = "AUT", mna_number = "29676")
        lt_s  = SRM.Sailor (lt,  nation = "AUT", raw = True)
        cat_s = SRM.Sailor (cat, nation = "AUT", raw = True)
        opti  = SRM.Boat_Class ("Optimist", max_crew = 1)
        b     = SRM.Boat ("Optimist", "AUT", 1107)
        ys    = SRM.Handicap ("Yardstick")
        rev   = SRM.Regatta_Event \
            (u"Himmelfahrt", dict (start = u"20080501"), raw = True)
        reg   = SRM.Regatta_C (rev, opti)
        reh   = SRM.Regatta_H (rev, ys)
        bir   = SRM.Boat_in_Regatta (b, reg, skipper = lt_s)
    # end def fixtures

    @Once_Property
    def jnj_src (self) :
        return "/tmp/test"
    # end def jnj_src

    def scope (self, * args, ** kw) :
        verbose = kw.pop ("verbose", True)
        return self.__super.scope (* args, verbose = verbose, ** kw)
    # end def scope

    @Once_Property
    def web_src_root (self) :
        return "/tmp/test"
    # end def web_src_root

    def _backend_spec (self, backends) :
        i = 0
        for b in backends :
            i += 1
            path = self.Backend_Default_Path [b]
            for k, v in zip \
                    ( ("p",                        "n",  "BN")
                    , (self.Backend_Parameters [b], path, repr (b))
                    ) :
                yield ("%s%d" % (k, i), v)
    # end def _backend_spec

    def _wsgi_app (self, cmd) :
        self._handle_create (cmd)
        result = self.__super._wsgi_app (cmd)
        return result
    # end def _wsgi_app

_Command_  = _GTW_Test_Command_ # end class

Scaffold   = _Command_ ()
Scope      = Scaffold.scope

import logging
import multiprocessing
import requests
import sys
import time

logger = multiprocessing.log_to_stderr ()

def _run_server (* args) :
    result = Scaffold (server_args)
    return result
# end def run_server

def run_server (* args) :
    p = multiprocessing.Process (target = _run_server, args = args)
    p.start    ()
    time.sleep (2)
    return p
# end def run_server

def _normal (k, v) :
    if k in ("date", "last-modified") :
        v = "<datetime instance>"
    elif k in ("etag",) :
        v = "ETag value"
    return k, v
# end def _normal

def show (r) :
    output = formatted \
        ( dict
            ( headers = dict
                (_normal (k, v) for k, v in r.headers.iteritems ())
            , json    = r.json if r.content else None
            , status  = r.status_code
            )
        )
    print (output)
    return r
# end def show

server_args = \
    [ "run_server"
    , "-UTP=RST"
    , "-auto_reload=no"
    , "-db_url=hps://"
    , "-db_name=test"
    , "-debug=yes"
    , "-load_I18N=no"
    , "-port=9999"
    ]

_test_code = """
    >>> server = run_server ()

    >>> r = show (requests.get ("http://localhost:9999"))
    { 'headers' :
        { 'content-length' : '49'
        , 'content-type' : 'application/json'
        , 'date' : '<datetime instance>'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        }
    , 'json' :
        { 'entries' : [ 'v1' ]
        , 'url_template' : '%s/{entry}'
        }
    , 'status' : 200
    }

    >>> r = show (requests.get ("http://localhost:9999/v1"))
    { 'headers' :
        { 'content-length' : '1099'
        , 'content-type' : 'application/json'
        , 'date' : '<datetime instance>'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        }
    , 'json' :
        { 'entries' :
            [ 'MOM.Id_Entity'
            , 'MOM.Link'
            , 'MOM.Link1'
            , 'MOM._MOM_Link_n_'
            , 'MOM.Link2'
            , 'MOM.Link2_Ordered'
            , 'MOM.Link3'
            , 'MOM.Object'
            , 'MOM.Named_Object'
            , 'PAP.Address'
            , 'PAP.Subject'
            , 'PAP.Company'
            , 'PAP.Email'
            , 'PAP.Phone'
            , 'PAP.Person'
            , 'PAP.Subject_has_Property'
            , 'PAP.Subject_has_Address'
            , 'PAP.Company_has_Address'
            , 'PAP.Subject_has_Email'
            , 'PAP.Company_has_Email'
            , 'PAP.Subject_has_Phone'
            , 'PAP.Company_has_Phone'
            , 'PAP.Entity_created_by_Person'
            , 'PAP.Person_has_Address'
            , 'PAP.Person_has_Email'
            , 'PAP.Person_has_Phone'
            , 'SRM.Link1'
            , 'SRM.Link2'
            , 'SRM.Object'
            , 'SRM._Boat_Class_'
            , 'SRM.Boat_Class'
            , 'SRM.Handicap'
            , 'SRM.Boat'
            , 'SRM.Club'
            , 'SRM.Regatta_Event'
            , 'GTW.OMP.SWP.Link1'
            , 'GTW.OMP.SWP.Link2'
            , 'GTW.OMP.SWP.Object'
            , 'GTW.OMP.SWP.Object_PN'
            , 'GTW.OMP.SWP.Page'
            , 'GTW.OMP.SWP.Page_Y'
            , 'GTW.OMP.SWP.Clip_O'
            , 'GTW.OMP.SWP.Clip_X'
            , 'GTW.OMP.SWP.Gallery'
            , 'GTW.OMP.SWP.Picture'
            , 'SRM.Page'
            , 'SRM.Regatta'
            , 'SRM.Regatta_C'
            , 'SRM.Regatta_H'
            , 'SRM.Sailor'
            , 'SRM.Boat_in_Regatta'
            , 'SRM.Race_Result'
            , 'SRM.Team'
            , 'SRM.Crew_Member'
            , 'SRM.Team_has_Boat_in_Regatta'
            ]
        , 'url_template' : '%s/{entry}'
        }
    , 'status' : 200
    }

    >>> r = show (requests.get ("http://localhost:9999/v1/PAP.Person"))
    { 'headers' :
        { 'content-length' : '52'
        , 'content-type' : 'application/json'
        , 'date' : '<datetime instance>'
        , 'etag' : 'ETag value'
        , 'last-modified' : '<datetime instance>'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        }
    , 'json' :
        { 'entries' :
            [ 1
            , 2
            , 3
            ]
        , 'url_template' : '%s/{entry}'
        }
    , 'status' : 200
    }

    >>> for pid in r.json ["entries"] :
    ...     _ = show (requests.get ("http://localhost:9999/v1/PAP.Person/%s" % pid))
    { 'headers' :
        { 'content-length' : '145'
        , 'content-type' : 'application/json'
        , 'date' : '<datetime instance>'
        , 'etag' : 'ETag value'
        , 'last-modified' : '<datetime instance>'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        }
    , 'json' :
        { 'attributes' :
            { 'first_name' : 'Christian'
            , 'last_name' : 'Tanzer'
            , 'middle_name' : ''
            , 'title' : ''
            }
        , 'cid' : 1
        , 'pid' : 1
        , 'type_name' : 'PAP.Person'
        }
    , 'status' : 200
    }
    { 'headers' :
        { 'content-length' : '150'
        , 'content-type' : 'application/json'
        , 'date' : '<datetime instance>'
        , 'etag' : 'ETag value'
        , 'last-modified' : '<datetime instance>'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        }
    , 'json' :
        { 'attributes' :
            { 'first_name' : 'Laurens'
            , 'last_name' : 'Tanzer'
            , 'middle_name' : 'William'
            , 'title' : ''
            }
        , 'cid' : 2
        , 'pid' : 2
        , 'type_name' : 'PAP.Person'
        }
    , 'status' : 200
    }
    { 'headers' :
        { 'content-length' : '148'
        , 'content-type' : 'application/json'
        , 'date' : '<datetime instance>'
        , 'etag' : 'ETag value'
        , 'last-modified' : '<datetime instance>'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        }
    , 'json' :
        { 'attributes' :
            { 'first_name' : 'Clarissa'
            , 'last_name' : 'Tanzer'
            , 'middle_name' : 'Anna'
            , 'title' : ''
            }
        , 'cid' : 3
        , 'pid' : 3
        , 'type_name' : 'PAP.Person'
        }
    , 'status' : 200
    }

    >>> r = show (requests.get ("http://localhost:9999/v1/PAP.Person/1"))
    { 'headers' :
        { 'content-length' : '145'
        , 'content-type' : 'application/json'
        , 'date' : '<datetime instance>'
        , 'etag' : 'ETag value'
        , 'last-modified' : '<datetime instance>'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        }
    , 'json' :
        { 'attributes' :
            { 'first_name' : 'Christian'
            , 'last_name' : 'Tanzer'
            , 'middle_name' : ''
            , 'title' : ''
            }
        , 'cid' : 1
        , 'pid' : 1
        , 'type_name' : 'PAP.Person'
        }
    , 'status' : 200
    }

    >>> last_modified = r.headers ["last-modified"]
    >>> last_etag     = r.headers ["etag"]
    >>> r = show (requests.get ("http://localhost:9999/v1/PAP.Person/1", headers = { "If-Modified-Since" : last_modified }))
    { 'headers' :
        { 'connection' : 'close'
        , 'date' : '<datetime instance>'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        }
    , 'json' : None
    , 'status' : 304
    }

    >>> r = show (requests.get ("http://localhost:9999/v1/PAP.Person/1", headers = { "If-None-Match" : last_etag }))
    { 'headers' :
        { 'connection' : 'close'
        , 'date' : '<datetime instance>'
        , 'etag' : 'ETag value'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        }
    , 'json' : None
    , 'status' : 304
    }

    >>> r = show (requests.get ("http://localhost:9999/v1/SRM.Regatta"))
    { 'headers' :
        { 'content-length' : '51'
        , 'content-type' : 'application/json'
        , 'date' : '<datetime instance>'
        , 'etag' : 'ETag value'
        , 'last-modified' : '<datetime instance>'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        }
    , 'json' :
        { 'entries' :
            [ 11
            , 12
            ]
        , 'url_template' : '%s/{entry}'
        }
    , 'status' : 200
    }

    >>> r = show (requests.get ("http://localhost:9999/v1/SRM.Regatta_C"))
    { 'headers' :
        { 'content-length' : '47'
        , 'content-type' : 'application/json'
        , 'date' : '<datetime instance>'
        , 'etag' : 'ETag value'
        , 'last-modified' : '<datetime instance>'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        }
    , 'json' :
        { 'entries' : [ 11 ]
        , 'url_template' : '%s/{entry}'
        }
    , 'status' : 200
    }

    >>> r = show (requests.get ("http://localhost:9999/v1/SRM.Regatta_H"))
    { 'headers' :
        { 'content-length' : '47'
        , 'content-type' : 'application/json'
        , 'date' : '<datetime instance>'
        , 'etag' : 'ETag value'
        , 'last-modified' : '<datetime instance>'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        }
    , 'json' :
        { 'entries' : [ 12 ]
        , 'url_template' : '%s/{entry}'
        }
    , 'status' : 200
    }

    >>> server.terminate ()

"""

__test__ = dict \
    ( RST_test = _test_code
    )

if __name__ == "__main__" :
    Scaffold (server_args)
### __END__ GTW.__test__.RST
