# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012-2013 Mag. Christian Tanzer All rights reserved
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
#    GTW.__test__.Test_Command
#
# Purpose
#    Test-specific descendent of GTW.Werkzeug.Command
#
# Revision Dates
#    18-Sep-2012 (CT) Creation (factored from _GTW/__test__/model.py)
#    18-Sep-2012 (CT) Redefine `__init__` to set `ANS.Version`
#    25-Sep-2012 (CT) Add `smtp_server` default `<Tester>`
#     9-Jan-2013 (CT) Factor in `GTW_RST_Test_Command` from `RST`
#    21-Jan-2013 (CT) Add `reset`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, unicode_literals

from   _GTW                     import GTW
from   _JNJ                     import JNJ
from   _MOM                     import MOM
from   _TFL                     import TFL

from   _MOM.import_MOM          import *
from   _MOM.inspect             import show_ref_map, show_ref_maps
from   _MOM.Product_Version     import Product_Version, IV_Number

from   _TFL                     import sos
from   _TFL._Meta.Once_Property import Once_Property
from   _TFL._Meta.Property      import Class_Property
from   _TFL.I18N                import _, _T, _Tn

from   _TFL.Formatter           import Formatter, formatted_1

formatted = Formatter (width = 240)

import _GTW._Werkzeug.Command

import _GTW._RST._TOP.import_TOP
import _GTW._RST._TOP._MOM.import_MOM
import _JNJ.Templateer

import _GTW._AFS._MOM.Spec

import _TFL.Filename
import _TFL.Generators

from    werkzeug.test     import Client
from    werkzeug.wrappers import BaseResponse
import  pyquery
import  lxml.html

model_src        = sos.path.dirname (__file__)
form_pickle_path = sos.path.join    (model_src, "afs_form_table.pck")

Version = Product_Version \
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

class Test_Response (BaseResponse) :
    """Enhance the reponse for the test setup"""

    @Once_Property
    def PQ (self) :
        return pyquery.PyQuery (self.data)
    # end def PQ

# end class Test_Response

def _as_string (self) :
    return lxml.html.tostring (self)
# end def _as_string
lxml.html.HtmlElement.string = Once_Property (_as_string)

_Ancestor = GTW.Werkzeug.Command

class GTW_Test_Command (_Ancestor) :

    ANS                   = GTW
    nick                  = u"MOMT"
    default_db_name       = "test"

    SALT                  = bytes ("4418c024-c51f-42b5-9032-be3ef10b1a61")

    _defaults             = dict \
        ( config          = "~/.gtw-test.config"
        , smtp_server     = "<Tester>"
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

    class _Create_ (_Ancestor._Create_) :

        _opts             = \
            ( "fixtures:B?Run the fixtures after the scope has been created"
            ,
            )

    # end class _Create_

    class _WSGI_ (_Ancestor._WSGI_) :

        _opts             = \
            ( "create:B=Create a new scope during WSGI application creation"
            , "fixtures:B?Run the fixtures after the scope has been created"
            )

    # end class _WSGI_

    @Once_Property
    def src_dir (self) :
        return "/tmp/test"
    # end def src_dir

    @Once_Property
    def web_src_root (self) :
        return "/tmp/test"
    # end def web_src_root

    def __init__ (self, * args, ** kw) :
        self.ANS.Version = Version
        self.__super.__init__ (* args, ** kw)
    # end def __init__

    def combiner (self, backends, bpt) :
        if bpt > 1 :
            backends = backends + [backends [0]]
        return TFL.window_wise (backends, bpt)
    # end def combiner

    def create_top (self, cmd, ** kw) :
        RST            = GTW.RST
        TOP            = RST.TOP
        result         = TOP.Root \
            ( language = "de"
            , ** kw
            )
        result.add_entries \
            ( TOP.MOM.Admin.Site
                ( name            = "Admin"
                , short_title     = "Admin"
                , pid             = "Admin"
                , title           = u"Verwaltung der Homepage"
                , head_line       = u"Administration der Homepage"
                , login_required  = True
                , entries         = self._nav_admin_groups ()
                )
            , TOP.Auth
                ( name            = _ ("Auth")
                , pid             = "Auth"
                , short_title     = _ ("Authorization and Account handling")
                , hidden          = True
                )
            , TOP.L10N
                ( name            = _ ("L10N")
                , short_title     =
                    _ ("Choice of language used for localization")
                , country_map     = dict (de = "AT")
                )
            )
        return result
    # end def create_top

    def create_test_dict \
            ( self, test_spec
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
                key  = "_".join (p for p in (name, ) + w if p)
                test = "%s\n\n    %s\n" % \
                    ( code % dict (self._backend_spec (w))
                    , "\n    ".join \
                        ( ( ">>> try :"
                          , "...     Scaffold.reset ()"
                          , "... except Exception :"
                          , "...     pass"
                          )
                        )
                    )
                result [key] = test
        return result
    # end def create_test_dict

    def do_create (self, cmd) :
        scope = self.scope (cmd.db_url, cmd.db_name, create = True)
        self.fixtures  (scope)
        scope.destroy ()
    # end def do_create

    def fixtures (self, scope) :
        pass
    # end def fixtures

    def reset (self) :
        self.root = None
        try :
            del self.Test_Client
        except AttributeError :
            pass
        MOM.Scope.destroy_all ()
    # end def reset

    def scope (self, * args, ** kw) :
        verbose = kw.pop ("verbose", True)
        return self.__super.scope (* args, verbose = verbose, ** kw)
    # end def scope

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

    def _create_templateer (self, cmd, ** kw) :
        return self.__super._create_templateer \
            (cmd, load_path = [self.src_dir], ** kw)
    # end def _create_templateer

    def _nav_admin_groups (self) :
        return []
    # end def _nav_admin_groups

    def _wsgi_app (self, cmd) :
        self._handle_create (cmd)
        result = self.__super._wsgi_app (cmd)
        return result
    # end def _wsgi_app

    @Once_Property
    def Test_Client (self) :
        return Client (self.root, Test_Response)
    # end def Test_Client

    def test_post (self, url, ** options) :
        return self.Test_Client.post (url, ** options)
    # end def test_post

    def test_get (self, url, ** options) :
        return self.Test_Client.get (url, ** options)
    # end def test_get

# end class GTW_Test_Command

class GTW_RST_Test_Command (GTW_Test_Command) :

    _defaults               = dict \
        ( fixtures          = "yes"
        , port              = 9090
        , UTP               = "RST"
        )

    def create_rst (self, cmd, ** kw) :
        import _GTW._RST._MOM.Doc
        import _GTW._RST._MOM.Scope
        result = GTW.RST.Root \
            ( language          = "de"
            , entries           =
                [ GTW.RST.MOM.Scope        (name = "v1")
                , GTW.RST.MOM.Doc.App_Type (name = "Doc")
                , GTW.RST.Raiser           (name = "RAISE")
                ]
            , ** kw
            )
        if cmd.log_level :
            print (formatted (result.Table))
        return result
    # end def create_rst

# end class GTW_RST_Test_Command

### __END__ GTW.__test__.Test_Command
