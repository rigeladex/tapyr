# -*- coding: iso-8859-15 -*-
# Copyright (C) 2011 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# #*** <License> ************************************************************#
# This module is part of the package GTW.Werkzeug.
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
#    GTW.Werkzeug.Scaffold
#
# Purpose
#    Provide a scaffold for creating instances of MOM.App_Type and MOM.Scope
#    , managing their databases, and creating a WSGI application or staring a
#    development web server based on the werkzeug framework
#
# Revision Dates
#    18-Nov-2011 (MG) Creation
#    ««revision-date»»···
#--

from   __future__          import unicode_literals
from   _TFL                import TFL
from   _GTW                import GTW
import _GTW._OMP.Scaffold
import _GTW._Werkzeug
import _GTW._NAV.Base
import _GTW._NAV.Console
import _GTW._NAV.Permission
import _GTW._NAV._E_Type.Admin
import _GTW._NAV._E_Type.Site_Admin
from   _TFL                import sos
import _TFL.SMTP
import _JNJ.Templateer

class _GTW_Werkzeug_Scaffold (GTW.OMP.Scaffold) :

    _real_name = "Scaffold"

    ### SALT should be change from every real application
    SALT                = bytes \
        ("Needs to defined in the application to a unique string")

    Default_Locale_Code = "de"
    base_template_dir   = sos.path.dirname (_JNJ.__file__)

    cmd___server__opts  = \
        [ "suppress_translation_loading:B?Don't load the the translation "
            "files during startup"
        ]
    cmd__run_server__opts = GTW.OMP.Scaffold.cmd__run_server__opts + \
       cmd___server__opts                                          + \
       [ "watch_media_files:B?Add the .media files to list files watched "
         "by automatic reloader"
       ]

    cmd__wsgi__opts       = GTW.OMP.Scaffold.cmd__wsgi__opts       + \
       cmd___server__opts

    @classmethod
    def _create_scope (cls, apt, url, verbose = False) :
        result = super  (Scaffold, cls)._create_scope (apt, url, verbose)
        cls.fixtures    (result)
        return result
    # end def _create_scope

    @classmethod
    def do_run_server (cls, cmd) :
        app = cls.do_wsgi (cmd)
        kw  = dict (port = cmd.port)
        if cmd.watch_media_files :
            kw ["reload_extra_files"] = getattr \
                (GTW.NAV.Root.top, "Media_Filenames", ())
        app.run_development_server (** kw)
    # end def do_run_server

    @classmethod
    def do_wsgi (cls, cmd) :
        apt, url = cls.app_type_and_url (cmd.db_url, cmd.db_name)
        ###    (cmd, apt, url, Create_Scope = cls._load_scope)
        if not cmd.suppress_translation_loading :
            try :
                ldir = sos.path.join (sos.path.dirname (__file__), "locale")
                translations = TFL.I18N.load \
                    ( "de", "en"
                    , domains    = ("messages", )
                    , use        = "de"
                    , locale_dir = ldir
                    )
            except ImportError :
                translations = None
        TFL.user_config.set_defaults \
            (time_zone = TFL.user_config.get_tz ("Europe/Vienna"))
        nav            = cls.create_nav \
            (cmd, apt, url, Create_Scope = cls._load_scope)
        HTTP           = nav.HTTP
        prefix         = "media"
        media_dir      = sos.path.join (nav.web_src_root, "media")
        static_handler = HTTP.Static_File_Handler \
            (prefix, media_dir, GTW.static_file_map)
        app            = HTTP.Application \
            ( ("", HTTP.NAV_Request_Handler, dict (nav_root = nav))
            , Session_Class       = GTW.File_Session
            , auto_reload         = cmd.auto_reload
            , cookie_salt         = cls.SALT
            , default_locale_code = cls.Default_Locale_Code
            , debug               = cmd.debug
            , edit_session_ttl    = cmd.edit_session_ttl.date_time_delta
            , encoding            = nav.encoding
            , i18n                = True
            , login_url           = nav.SC.Auth.href_login
            , session_id          = bytes ("SESSION_ID")
            , static_handler      = static_handler
            , user_session_ttl    = cmd.user_session_ttl.date_time_delta
            )
        nav.Templateer.env.static_handler = static_handler
        if cmd.Break :
            TFL.Environment.py_shell (vars ())
        return app
    # end def do_wsgi

    @classmethod
    def fixtures (cls, scope) :
        pass
    # end def fixtures

    @classmethod
    def init_app_cache (cls, nav) :
        map_path = sos.path.join (cls.jnj_src, "app_cache.pck")
        def load_cache () :
            try :
                nav.load_cache (map_path)
            except IOError :
                pass
        if nav.DEBUG :
            try :
                nav.store_cache   (map_path)
            except EnvironmentError :
                print "***", map_path
                load_cache ()
        else :
            load_cache ()
    # end def init_app_cache

    @staticmethod
    def _nav_admin_group (name, title, * pnss, ** kw) :
        return dict \
            ( sub_dir        = name
            , short_title    = kw.pop ("short_title", name)
            , title          = title
            , head_line      = kw.pop ("head_line", title)
            , PNSs           = pnss
            , Type           = kw.pop ("Type", GTW.NAV.E_Type.Admin_Group)
            , ** kw
            )
    # end def _nav_admin_group

Scaffold =_GTW_Werkzeug_Scaffold # end class

if __name__ != "__main__" :
    GTW.Werkzeug._Export ("*")
### __END__ GTW.Werkzeug.Scaffold
