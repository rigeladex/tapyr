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
#    ««revision-date»»···
#--

from   _GTW                     import GTW
from   _JNJ                     import JNJ
from   _MOM                     import MOM
from   _TFL                     import TFL

from   _MOM.import_MOM          import *
from   _MOM.Product_Version     import Product_Version, IV_Number

from   _TFL                     import sos
from   _TFL._Meta.Once_Property import Once_Property
from   _TFL._Meta.Property      import Class_Property
from   _TFL.I18N              import _, _T, _Tn

import _GTW._OMP.Scaffold
import _GTW._Werkzeug.Scaffold

import _GTW._OMP._Auth.import_Auth

if sos.environ.get ("GTW_FULL_OBJECT_MODEL", "True") != "False" :
    import _GTW._OMP._EVT.import_EVT
    import _GTW._OMP._EVT.Nav
    PNS_Dict = dict (EVT = GTW.OMP.EVT)
else :
    PNS_Dict = dict ()
    print "Ignore _GTW._OMP._EVT.import_EVT"

import _GTW._OMP._PAP.import_PAP
import _GTW._OMP._SRM.import_SRM
import _GTW._OMP._SWP.import_SWP

import _GTW._OMP._PAP.Nav
import _GTW._OMP._SRM.Nav
import _GTW._OMP._SWP.Nav

import _GTW._NAV.import_NAV
import _GTW._NAV.Calendar
import _GTW._NAV.Console
import _GTW._NAV._E_Type.Gallery
import _GTW._NAV._E_Type.SRM

import _JNJ.Templateer

import _TFL.Filename
import _TFL.Generators

from   posixpath import join  as pjoin

import _GTW._AFS._MOM.Spec

GTW.AFS.MOM.Spec.setup_defaults ()

model_src        = sos.path.dirname (__file__)
form_pickle_path = sos.path.join    (model_src, "afs_form_table.pck")

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

class _GTW__test__Scaffold_ (GTW.Werkzeug.Scaffold) :

    _real_name            = "Scaffold"

    ANS                   = GTW
    nick                  = u"MOMT"
    default_db_name       = "test"
    PNS_Aliases           = dict \
        ( Auth            = GTW.OMP.Auth
        , PAP             = GTW.OMP.PAP
        , SRM             = GTW.OMP.SRM
        , SWP             = GTW.OMP.SWP
        , ** PNS_Dict
        )
    SALT                  = bytes \
        ( "ohQueiro7theG4vai9shi4oi9iedeethaeshooqu7oThi9Eecephaj")

    cmd__base__opts_x     = \
        ( "-config:C=~/.gtw-test.config?File specifying defaults for options"
        ,
        )
    cmd__create__opts     = \
        ( "fixtures:B?Run the fixtures after the scope has been created"
        ,
        )
    cmd__wsgi__opts       = \
        ( "create:B=Create a new scope during WSGI application careation"
        , "fixtures:B?Run the fixtures after the scope has been created"
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

    @classmethod
    def combiner (cls, backends, bpt) :
        if bpt > 1 :
            backends = backends + [backends [0]]
        return TFL.window_wise (backends, bpt)
    # end def combiner

    @classmethod
    def create_nav (cls, cmd, app_type, db_url, ** kw) :
        from _JNJ.Media_Defaults import Media_Defaults
        CSS_Parameters = Media_Defaults ()
        home_url_root  = "http://localhost:9042"
        site_prefix    = pjoin (home_url_root, "")
        template_dirs  = [cls.jnj_src]
        result = GTW.NAV.Root \
            ( auto_delegate   = False
            , DB_Url          = db_url
            , App_Type        = app_type
            , CSS_Parameters  = CSS_Parameters
            , DEBUG           = cmd.debug
            , encoding        = cmd.output_encoding
            , HTTP            = cmd.HTTP
            , input_encoding  = cmd.input_encoding
            , language        = "de"
            , permissive      = False
            , site_url        = home_url_root
            , site_prefix     = site_prefix
            , src_dir         = cls.web_src_root
            , template_name   = cmd.template_file
            , version         = "html/5.jnj"
            , Templateer      = JNJ.Templateer
                ( encoding        = cmd.input_encoding
                , globals         = dict (site_base = cmd.template_file)
                , i18n            = True
                , load_path       = template_dirs
                , trim_blocks     = True
                , version         = "html/5.jnj"
                , CSS_Parameters  = CSS_Parameters
                )
            , TEST            = cmd.TEST
            , ** kw
            )
        result.add_entries \
            ( [ dict
                  ( sub_dir         = "Admin"
                  , short_title     = "Admin"
                  , pid             = "Admin"
                  , title           = u"Verwaltung der Homepage"
                  , head_line       = u"Administration der Homepage"
                  , login_required  = True
                  , Type            = GTW.NAV.E_Type.Site_Admin
                  , entries         =
                      [ cls.nav_admin_group
                          ( "Personenverwaltung"
                          , "Verwaltung von Personen und ihren Eigenschaften"
                          , "GTW.OMP.PAP"
                          )
                      , cls.nav_admin_group
                          ( "Benutzerverwaltung"
                          , "Verwaltung von Benutzer-Konten und Gruppen"
                          , "GTW.OMP.Auth"
                          , permission = GTW.NAV.Is_Superuser ()
                          )
                      , cls.nav_admin_group
                          ( "Regattaverwaltung"
                          , "Verwaltung von Regatten, Booten, "
                            "Teilnehmern und Ergebnissen"
                          , "GTW.OMP.SRM"
                          , show_aliases = True
                          )
                      , cls.nav_admin_group
                          ( "Webseitenverwaltung"
                          , "Verwaltung der Webseiten"
                          , "GTW.OMP.SWP", "GTW.OMP.EVT"
                          , show_aliases = True
                          )
                      ]
                  )
              , dict
                  ( src_dir         = _ ("Auth")
                  , pid             = "Auth"
                  , prefix          = "Auth"
                  , short_title     = _ (u"Authorization and Account handling")
                  , Type            = GTW.NAV.Auth
                  , hidden          = True
                  )
              , dict
                  ( src_dir         = _ ("L10N")
                  , prefix          = "L10N"
                  , short_title     =
                    _ (u"Choice of language used for localization")
                  , Type            = GTW.NAV.L10N
                  , country_map     = dict \
                      ( de          = "AT")
                  )
              ]
            )
        return result
    # end def create_nav

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
    def do_create (cls, cmd) :
        scope = cls.scope (cmd.db_url, cmd.db_name, create = True)
        cls.fixtures  (scope)
        scope.destroy ()
    # end def do_create

    @classmethod
    def fixtures (cls, scope) :
        if sos.environ.get ("GTW_FIXTURES") :
            from _GTW.__test__.form_app import fixtures
            fixtures (scope)
    # end def fixtures

    @Class_Property
    @Once_Property
    def jnj_src (cls) :
        return "/tmp/test"
    # end def jnj_src

    @classmethod
    def scope (cls, * args, ** kw) :
        verbose = kw.pop ("verbose", True)
        return super (Scaffold, cls).scope (* args, verbose = verbose, ** kw)
    # end def scope

    @Class_Property
    @Once_Property
    def web_src_root (cls) :
        return "/tmp/test"
    # end def web_src_root

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
    def _wsgi_app (cls, cmd) :
        cls.do_create (cmd)
        result = super (Scaffold, cls)._wsgi_app (cmd)
        return result
    # end def _wsgi_app

Scaffold = _GTW__test__Scaffold_ # end class

Scope = Scaffold.scope

_Command = Scaffold.cmd

if __name__ == "__main__" :
    _Command ()
### __END__ GTW.__test__.model
