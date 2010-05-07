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
#    ««revision-date»»···
#--

from   _GTW.__test__.model import MOM, GTW, Scope
from   _JNJ                import JNJ
import _GTW._NAV.import_NAV
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

def create_nav (scope) :
    home_url_root = "http://localhost:9042"
    site_prefix   = pjoin (home_url_root, "")
    GTW.NAV.scope = scope
    result        = GTW.NAV.Root \
        ( anonymous       = scope and scope.Auth.Account_Anonymous.singleton
        , encoding        = "ISO-8859-1"
        , src_dir         = "."
        , site_url        = home_url_root
        , site_prefix     = site_prefix
        , auto_delegate   = False
        , web_src_root    = sos.path.dirname (__file__)
        , HTTP            = GTW.Werkzeug
        , template        = "static.jnj"
        , Templateer      = JNJ.Templateer
            ( i18n        = True
            #, load_path   = template_dirs
            , trim_blocks = True
            , version     = "html/x.jnj"
            )
        , Media           = GTW.Media
            ( css_links   =
                ( GTW.CSS_Link ("screen.css")
                , GTW.CSS_Link ("/media/GTW/css/jquery.gritter.css", "screen")
                )
            , js_on_ready =
                ( '$.gritter.Convert_Patagraphs_to_Gitter ("notifications");'
                ,
                )
            , scripts     =
                ( GTW.Script (src  = "/media/GTW/js/jquery-1.4.2.min.js")
                , GTW.Script (src  = "/media/GTW/js/jquery.gritter.js")
                )
            )
        , permissive      = False
        , scope           = scope
        )
    result.add_entries \
        ( [ dict
              ( sub_dir         = "Admin"
              , title           = "Admin"
              , pid             = "Admin"
              , desc            = u"Admin Desc"
              , headline        = u"Admin Page"
              , login_required  = True
              , etypes          =
                  [ dict
                      ( ETM       = "GTW.OMP.PAP.Person"
                      , Form_args =
                          ( FGD (WF ("primary"), render_mode = "table")
                          , LID
                              ( "GTW.OMP.PAP.Person_has_Address"
                              , render_mode = "ui_display_table"
                              )
                          )
                      )
                  ##   GTW.OMP.PAP.Nav.Admin.Address
                  ## , GTW.OMP.PAP.Nav.Admin.Email
                  ## , GTW.OMP.PAP.Nav.Admin.Person
                  ## , GTW.OMP.PAP.Nav.Admin.Person_has_Address
                  ## , GTW.OMP.PAP.Nav.Admin.Person_has_Phone
                  ## , GTW.OMP.PAP.Nav.Admin.Person_has_Email
                  ## , GTW.OMP.PAP.Nav.Admin.Phone

                  ## , GTW.OMP.Auth.Nav.Admin.Account
                  ## , GTW.OMP.Auth.Nav.Admin.Group
                  ## , GTW.OMP.Auth.Nav.Admin.Account_in_Group

                  ## , GTW.OMP.EVT.Nav.Admin.Event
                  ## , GTW.OMP.EVT.Nav.Admin.Event_occurs

                  ## , GTW.OMP.SWP.Nav.Admin.Clip_X
                  ## , GTW.OMP.SWP.Nav.Admin.Gallery
                  ## , GTW.OMP.SWP.Nav.Admin.Page
                  ## , GTW.OMP.SWP.Nav.Admin.Picture

                  ## , GTW.OMP.SRM.Nav.Admin.Boat
                  ## , GTW.OMP.SRM.Nav.Admin.Boat_Class
                  ## , GTW.OMP.SRM.Nav.Admin.Boat_in_Regatta
                  ## , GTW.OMP.SRM.Nav.Admin.Page
                  ## , GTW.OMP.SRM.Nav.Admin.Regatta_C
                  ## , GTW.OMP.SRM.Nav.Admin.Regatta_H
                  ## , GTW.OMP.SRM.Nav.Admin.Regatta_Event
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
          ]
        )
    return result
# end def create_nav

def media_handler (nav) :
    prefix    = "media"
    media_dir = sos.path.join (nav.web_src_root, "media")
    return \
        ( "/" + prefix
        , GTW.Werkzeug.Static_File_Handler
        , (media_dir, GTW.static_file_map)
        )
# end def media_handler

def _main (cmd) :
    import _GTW._Werkzeug.Application
    import _GTW._Werkzeug.Static_File_Handler
    import _GTW._Werkzeug.Request_Handler
    import _GTW._Werkzeug.Request_Data
    import  threading
    scope = Scope ()
    NAV   = create_nav (scope)
    app = GTW.Werkzeug.Application \
        ( ("", GTW.Werkzeug.NAV_Request_Handler, (NAV, ))
        , cookie_secret  = "ahn*eTh:2uGu6la/weiwaiz1bieN;aNg0eetie$Chae^2eEjeuth7e"
        , i18n           = True
        , login_url      = NAV.SC.Auth.href_login
        , Session_Class  = GTW.File_Session
        , session_id     = "SESSION_ID"
        , static_handler = media_handler (NAV)
        , encoding       = NAV.encoding
        )
    ### XXX remove me
    PAP = scope.PAP
    p = scope.PAP.Person (u"Glücklich", u"Eddy", raw = True)
    p = scope.PAP.Person (u"Glücklos",  u"Eddy", raw = True)
    p = scope.PAP.Person (u"Glück",     u"Martin", raw = True)
    a = PAP.Address      (u"Langstrasse 4", u"2244", u"Spannberg", u"Austria", raw = True)
    scope.PAP.Person_has_Address (p, a)
    a = PAP.Address      (u"Oberzellergasse 14", u"1030", u"Wien", u"Austria", raw = True)
    scope.PAP.Person_has_Address (p, a)
    app.run_development_server \
        ( port                 = cmd.port
        , use_debugger         = cmd.debug
        , use_reloader         = cmd.reload
        , use_profiler         = cmd.profiler
        , profile_log_files    = cmd.p_logs
        , profile_restrictions = cmd.p_restrictions
        , profile_sort_by      = cmd.p_sort_by
        , profile_delete_logs  = cmd.p_delete_logs
        )
# end def _main

_Command = TFL.CAO.Cmd \
    ( _main
    , opts =
        ( "debug:B=Yes?Run with werkzeug debugger"
        , "reload:B=Yes?Run with autoreloader"
        , "port:I=9042?Port for the webserber"
        , "profiler:B=no?Run with werkzeug profiler"
        , "p_logs:S,=stderr,profile.log?Logfile for the profiler"
        , "p_sort_by:S,=time,calls?Profiling sort order"
        , "p_restrictions:S,=?Profiling restrictions"
        , "p_delete_logs:B=no?Delete old profile log files on server start"
        )
    )
if __name__ == "__main__" :
    _Command ()
### __END__ GTW.__test__.form_app


