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
#    form_app
#
# Purpose
#    A test web application used for the javascript tests of the forms
#
# Revision Dates
#    22-Apr-2010 (MG) Creation
#     6-Mai-2010 (MG) Support for profiling added
#    20-Jun-2010 (MG) Support for `GTW.Tornado` added
#    25-Jun-2010 (MG) Werkzeug and Tornado now have a common interface ->
#                     application creation simplified
#     4-Aug-2010 (MG) Simplified to work with new `model.py`
#    12-Aug-2010 (MG) `nav` fixture support added
#    ««revision-date»»···
#--

from   _GTW.__test__.model import MOM, GTW, Scaffold
from   _JNJ                import JNJ
import _GTW._NAV.import_NAV
import _GTW.jQuery
import _GTW._NAV.Console
import _GTW.Media
import _GTW.File_Session
import _GTW._Werkzeug
import _JNJ.Templateer
import _TFL.SMTP

import _GTW._OMP._Auth.Nav
import _GTW._OMP._PAP.Nav
import _GTW._OMP._EVT.Nav
import _GTW._OMP._SRM.Nav
import _GTW._OMP._SWP.Nav

from   _TFL                   import TFL
from   _TFL.I18N              import _, _T, _Tn
from   _TFL                   import sos
import _TFL.CAO

import sys
import time
from   posixpath           import join  as pjoin

from   _GTW._Form._MOM.Field_Group_Description import \
    ( Field_Group_Description as FGD
    , Field_Prefixer          as FP
    , Wildcard_Field          as WF
    )
from  _GTW._Form.Widget_Spec    import Widget_Spec as WS
from   _GTW._Form._MOM.Inline_Description      import \
    ( Link_Inline_Description      as LID
    , Attribute_Inline_Description as AID
    )
import _GTW._Form._MOM.Javascript

class Regatta_C_Admin (GTW.NAV.E_Type.Admin) :
    """TEst"""

    class _RC_Changer_ (GTW.NAV.E_Type.Admin.Changer) :

        _real_name = "Changer"

        @TFL.Meta.Once_Property
        def form_parameters (self) :
            scope  = self.top.scope
            result = dict \
                ( initial_data =
                    { "boat_class.instance" :
                          lambda form : scope.SRM.Boat_Class.query ().first ()
                    }
                )
            return result
        # end def form_parameters

    Changer = _RC_Changer_ # end class

# end class Regatta_C_Admin

GTW.OMP.SRM.Nav.Admin.Regatta_C ["Type"] = Regatta_C_Admin
GTW.OMP.SRM.Nav.Admin.Regatta_C ["Form_kw"] = dict \
                ( initial_data =
                    { "left.instance" : lambda form :
                        form.et_man.home_scope.SRM.Regatta_Event.query ().first ()
                    }
                )

def fixtures (scope) :
    PAP   = scope.PAP
    SWP   = scope.SWP
    EVT   = scope.EVT
    MOM   = scope.MOM
    scope.Auth.Account_Anonymous (u"anonymous")
    p = scope.PAP.Person (u"Glücklich", u"Eddy", raw = True)
    p = scope.PAP.Person (u"Glücklos",  u"Eddy", raw = True)
    p = scope.PAP.Person (u"Glueck",    u"Martin", raw = True)
    a = PAP.Address      (u"Langstrasse 4", u"2244", u"Spannberg", u"Austria", raw = True)
    scope.PAP.Person_has_Address (p, a, desc = "Home")
    a = PAP.Address      (u"Oberzellergasse 14", u"1030", u"Wien", u"Austria", raw = True)
    scope.PAP.Person_has_Address (p, a, desc = "Wien")
    ### scope.PAP.Person_has_Address (p, a, desc = "Wien")
    ph = scope.PAP.Phone         ("43", "1", "123456")
    scope.PAP.Person_has_Phone   (p, ph, desc = "dummy")
    SRM = scope.SRM
    bc  = SRM.Boat_Class ("Optimist", max_crew = 1)
    re  = SRM.Regatta_Event \
        (dict (start = u"20080501", raw = True), u"Himmelfahrt", raw = True)

    page = SWP.Page \
        (perma_name = "test-page", text = "Test Page with an event", creator= p)
    EVT.Event (page, MOM.Date_Interval (start = "2010-01-01", raw = True))
    scope.commit                 () ### commit my `fixtures`
# end def fixtures

class File_Upload_Page (GTW.NAV.Page) :
    """just allow post request as well"""

    SUPPORTED_METHODS = set (("GET", "POST"))

    _Media           = GTW.Media \
        ( js_on_ready =
            ( '$(".ajax").GTW_File_Upload (); '
            ,
            )
        , css_links   =
            ( GTW.CSS_Link._.jQuery_UI
            , GTW.CSS_Link ("/media/GTW/css/inline_forms.css")
            )
        , scripts     =
            ( GTW.Script.jQuery_UI
            , GTW.Script (src = "/media/GTW/js/GTW_File_Upload.js")
            )
        )

    def _view (self, handler) :
        request = handler.request
        if request.method == "POST" :
            import os
            req_data = self.top.HTTP.Request_Data (handler)
            print req_data.files.keys ()
            for n, v in req_data.iteritems () :
                print n, v
            for f in req_data.files.itervalues () :
                if f :
                    path = os.path.join ("/tmp", f.filename)
                    f.save (path)
                    print "Saved", path
        return self.__super._view (handler)
    # end def _view

# end class File_Upload_Page

def nav ( cmd
        , App_Type      = None
        , DB_Url        = None
        , auto_delegate = False
        , version       = "html/5.jnj"
        , permissive    = True
        ) :
    home_url_root = "http://localhost:9042"
    site_prefix   = pjoin (home_url_root, "")
    template_dirs = \
        [ sos.path.join (sos.path.dirname (__file__))
        ]
    result        = GTW.NAV.Root \
        ( encoding        = "ISO-8859-1"
        , src_dir         = "."
        , site_url        = home_url_root
        , site_prefix     = site_prefix
        , auto_delegate   = auto_delegate
        , web_src_root    = sos.path.dirname (__file__)
        , HTTP            = cmd.HTTP
        , template        = "static.jnj"
        , Templateer      = JNJ.Templateer
            ( i18n        = True
            , load_path   = template_dirs
            , trim_blocks = True
            , version     = "html/x.jnj"
            )
        , Media           = GTW.Media
            ( css_links   =
                ( GTW.CSS_Link ("screen.css")
                , GTW.CSS_Link.jQuery_Gritter
                )
            , js_on_ready =
                ( '$.gritter.Convert_Patagraphs_to_Gitter ("notifications");'
                ,
                )
            , scripts     =
                ( GTW.Script.jQuery
                , GTW.Script.jQuery_Gritter
                )
            )
        , permissive            = permissive
        , DB_Url                = DB_Url
        , App_Type              = App_Type
        )
    if getattr (cmd, "create", False) :
        from model import Scaffold
        result.scope = Scaffold.scope (DB_Url.value, create = True)
        if getattr (cmd, "fixtures", False) :
            fixtures (result.scope)
    result.add_entries \
        ( [
            dict
              ( sub_dir         = "Admin"
              , title           = "Admin"
              , pid             = "Admin"
              , desc            = u"Admin Desc"
              , headline        = u"Admin Page"
              , login_required  = False
              , etypes          =
                  [ GTW.OMP.PAP.Nav.Admin.Person
                  , GTW.OMP.Auth.Nav.Admin.Account
                  , GTW.OMP.SRM.Nav.Admin.Boat_Class
                  , GTW.OMP.SRM.Nav.Admin.Regatta_C
                  , GTW.OMP.SRM.Nav.Admin.Regatta_Event
                  , GTW.OMP.SWP.Nav.Admin.Page
                  ]
              , Type            = GTW.NAV.Site_Admin
              )
          , dict
              ( src_dir         = _ ("Auth")
              , pid             = "Auth"
              , prefix          = "Auth"
              , title           = _ (u"Authorization and Account handling")
              , Type            = GTW.NAV.Auth
              , hidden          = True
              )
          , dict
              ( src_dir         = _ ("L10N")
              , prefix          = "L10N"
              , title           =
                _ (u"Choice of language used for localization")
              , Type            = GTW.NAV.L10N
              , country_map     = dict \
                  ( de          = "AT")
              )
          , dict
              ( src_dir         = _ ("Console")
              , name            = "Console"
              , title           = _ (u"Console")
              , Type            = GTW.NAV.Console
              )
          , dict
              ( name            = "file-upload.html"
              , title           =
                _ (u"File upload test")
              , Type            = File_Upload_Page
              , template        = "file-upload.jnj"
              )
          ]
        )
    return result
# end def nav

def wsgi (cmd, app_type, db_url) :
    try :
        ldir = sos.path.join (sos.path.dirname (__file__), "locale")
        TFL.I18N.load \
            ( "de", "en"
            , domains    = ("messages", )
            , use        = "de"
            , locale_dir = ldir
            , log_level  = 0
            )
    except ImportError :
        pass
    NAV       = nav (cmd, app_type, db_url)
    HTTP      = NAV.HTTP
    prefix    = "media"
    media_dir = sos.path.join (NAV.web_src_root, "media")
    app       = HTTP.Application \
        ( ("", HTTP.NAV_Request_Handler, dict (nav_root = NAV))
        , cookie_secret  = "ahn*eTh:2uGu6la/weiwaiz1b43N;aNg0eetie$Chae^2eEjeuth7e"
        , i18n           = True
        , login_url      = NAV.SC.Auth.href_login
        , Session_Class  = GTW.File_Session
        , session_id     = "SESSION_ID"
        , static_handler = HTTP.Static_File_Handler
            (prefix, media_dir, GTW.static_file_map)
        , encoding       = NAV.encoding
        , debug          = cmd.debug
        , auto_reload    = cmd.auto_reload
        )
    if cmd.Break :
        TFL.Environment.py_shell (vars ())
    return app
# end def wsgi

def run (cmd, apt, url) :
    app = wsgi                 (cmd, apt, url)
    app.run_development_server (port = cmd.port)
# end def run

### __END__ GTW.__test__.form_app


