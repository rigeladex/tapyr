# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
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
#    GTW.Werkzeug.Command
#
# Purpose
#    Provide an extendable Command for creating instances of MOM.App_Type
#    and MOM.Scope, managing their databases, and creating a WSGI application
#    or starting a development web server based on the werkzeug framework
#
# Revision Dates
#    27-Jan-2012 (CT) Recreation (re-factored from SC-AMS specific code)
#    27-Jan-2012 (CT) Factor `_wsgi_app`
#    30-Jan-2012 (CT) Change `_wsgi_app` to `cmd.GET ("cookie_salt")`
#     1-Feb-2012 (CT) Use newly factored `GTW.AFS.MOM.Form_Cache`
#    30-Apr-2012 (MG) Allow none existing `Auth`
#     3-May-2012 (CT) Pass `languages` to `HTTP.Application`
#     4-May-2012 (CT) Use `nav.login_url` instead of home-grown code
#    15-May-2012 (CT) Implement sub-command `setup_cache`, factor `cache_path`
#    17-May-2012 (CT) Derive from `GTW.OMP.Command` instead of `.Scaffold`,
#                     rename from `Scaffold` to `Command`
#    22-May-2012 (CT) Remove unused imports
#    22-May-2012 (CT) Use `app_dir`, not `app_path`
#     1-Jun-2012 (CT) Add sub-command `fcgi`
#     2-Jun-2012 (CT) Rename `suppress_translation_loading` to `load_I18N`
#     4-Jun-2012 (CT) Add `-log_level`, pass to `HTTP.Application`
#     4-Jun-2012 (MG) `_handle_run_server` support for `host` added
#    20-Jun-2012 (CT) Use `cmd.UTP` instead of hard-coded `GTW.NAV`
#    21-Jun-2012 (CT) Factor `_load_I18N`, `_static_handler`
#    28-Jun-2012 (CT) Call `init_app_cache` unconditionally
#    17-Jul-2012 (MG) `_wsgi_app` move `Break` after the generation of the
#                     app cache
#    ««revision-date»»···
#--

from   __future__          import unicode_literals

from   _TFL                import TFL
from   _GTW                import GTW

import _GTW._AFS._MOM.Form_Cache
import _GTW._OMP.Command
import _GTW._Werkzeug

import _JNJ.Templateer

from   _TFL                import sos
import _TFL.SMTP

class _GT2W_Sub_Command_ (GTW.OMP._Sub_Command_) :

    _rn_prefix              = "_GT2W"

_Sub_Command_ = _GT2W_Sub_Command_ # end class

class GT2W_Command (GTW.OMP.Command) :

    _rn_prefix              = "GT2W"

    SALT                    = bytes \
        ("Needs to defined uniquely for each application")

    base_template_dir       = sos.path.dirname (_JNJ.__file__)

    ### Sub-commands defined as class attributes to allow redefinition by
    ### derived classes; meta class puts their names into `_sub_commands`
    class _GT2W_Server_Base_ (_Sub_Command_, GTW.OMP.Command._Server_Base_) :
        ### Base for server-related commands

        is_partial              = True
        _opts                   = \
            ( "load_I18N:B=yes"
                "?Load the translation files during startup"
            , "log_level:I=1?Verbosity of logging"
            )

    # end class _GT2W_Server_Base_

    class _GT2W_Run_Server_ (_GT2W_Server_Base_, GTW.OMP.Command._Run_Server_) :

        _opts                   = \
            ( "watch_media_files:B"
                "?Add the .media files to list files watched by "
                "automatic reloader"
            ,
            )

    _Run_Server_ = _GT2W_Run_Server_ # end class

    class _GT2W_FCGI_ (_GT2W_Server_Base_, GTW.OMP.Command._FCGI_) :
        pass
    _FCGI_ = _GT2W_FCGI_ # end class

    class _GT2W_Setup_Cache_ (_GT2W_Server_Base_, GTW.OMP.Command._Setup_Cache_) :
        pass
    _Setup_Cache_ = _GT2W_Setup_Cache_ # end class

    class _GT2W_Shell_ (_GT2W_Server_Base_, GTW.OMP.Command._Shell_) :
        pass
    _Shell_ = _GT2W_Shell_ # end class

    class _GT2W_WSGI_ (_GT2W_Server_Base_, GTW.OMP.Command._WSGI_) :
        pass
    _WSGI_ = _GT2W_WSGI_ # end class

    _setup_cache_p          = False

    def cache_path (self) :
        return sos.path.join (self.jnj_src, "app_cache.pck")
    # end def cache_path

    def fixtures (self, scope) :
        pass
    # end def fixtures

    def init_app_cache (self, root) :
        cache_path = self.cache_path ()
        def load_cache () :
            try :
                root.load_cache  (cache_path)
            except IOError :
                pass
        if root.DEBUG :
            try :
                root.store_cache (cache_path)
            except EnvironmentError as exc :
                print "***", exc, cache_path
                load_cache ()
        else :
            load_cache ()
    # end def init_app_cache

    def nav_admin_group (self, name, title, * pnss, ** kw) :
        import _GTW._NAV._E_Type.Site_Admin
        return dict \
            ( sub_dir        = name
            , short_title    = kw.pop ("short_title", name)
            , title          = title
            , head_line      = kw.pop ("head_line", title)
            , PNSs           = pnss
            , Type           = kw.pop ("Type", GTW.NAV.E_Type.Admin_Group)
            , ** kw
            )
    # end def nav_admin_group

    def _handle_run_server (self, cmd) :
        app = self._wsgi_app (cmd)
        kw  = dict (port = cmd.port, host = getattr (cmd, "host", "localhost"))
        if cmd.watch_media_files :
            kw ["reload_extra_files"] = getattr \
                (cmd.UTP.Root.top, "Media_Filenames", ())
        app.run_development_server (** kw)
    # end def _handle_run_server

    def _handle_setup_cache (self, cmd) :
        app  = self._wsgi_app (cmd)
        root = cmd.UTP.Root.top
        if not root.DEBUG :
            root.store_cache (self.cache_path ())
    # end def _handle_setup_cache

    def _handle_wsgi (self, cmd) :
        return self._wsgi_app (cmd)
    # end def _handle_wsgi

    def _create_scope (self, apt, url, verbose = False) :
        result = self.__super._create_scope (apt, url, verbose)
        self.fixtures (result)
        return result
    # end def _create_scope

    def _load_I18N (self, cmd) :
        result = None
        if cmd.load_I18N :
            try :
                result = TFL.I18N.load \
                    ( * cmd.languages
                    , domains    = ("messages", )
                    , use        = cmd.locale_code or "en"
                    , locale_dir = sos.path.join (self.app_dir, "locale")
                    )
            except ImportError :
                pass
        return result
    # end def _load_I18N

    def _setup_cache (self, cmd) :
        if not self._setup_cache_p :
            CP = getattr (cmd.UTP.Root, "Cache_Pickler", None)
            if CP is not None :
                import _GTW._NAV.Template_Media_Cache
                mc_fix = "media/v"
                mc_dir = sos.path.join (self.web_src_root, mc_fix)
                CP.add (GTW.AFS.MOM.Form_Cache)
                CP.add (GTW.NAV.Template_Media_Cache (mc_dir, mc_fix))
        self._setup_cache_p = True
    # end def _setup_cache

    def _static_handler (self, cmd) :
        if cmd.serve_static_files :
            prefix         = "media"
            media_dir      = sos.path.join (self.web_src_root, "media")
            return cmd.HTTP.Static_File_Handler \
                (prefix, media_dir, GTW.static_file_map)
    # end def _static_handler

    def _wsgi_app (self, cmd) :
        apt, url = self.app_type_and_url (cmd.db_url, cmd.db_name)
        self._load_I18N   (cmd)
        self._setup_cache (cmd)
        HTTP           = cmd.HTTP
        nav            = self.create_nav \
            (cmd, apt, url, Create_Scope = self._load_scope)
        static_handler = self._static_handler (cmd)
        app            = HTTP.Application \
            ( ("", HTTP.NAV_Request_Handler, dict (nav_root = nav))
            , Session_Class       = GTW.File_Session
            , auto_reload         = cmd.auto_reload
            , cookie_salt         = cmd.GET ("cookie_salt", self.SALT)
            , default_locale_code = cmd.locale_code
            , debug               = cmd.debug
            , edit_session_ttl    = cmd.edit_session_ttl.date_time_delta
            , encoding            = nav.encoding
            , i18n                = True
            , languages           = set (cmd.languages)
            , login_url           = nav.login_url
            , log_level           = cmd.log_level
            , session_id          = bytes ("SESSION_ID")
            , static_handler      = static_handler
            , user_session_ttl    = cmd.user_session_ttl.date_time_delta
            )
        nav.Templateer.env.static_handler = app.handlers [0]
        self.init_app_cache (nav)
        if cmd.Break :
            TFL.Environment.py_shell (vars ())
        return app
    # end def _wsgi_app

Command = GT2W_Command # end class

if __name__ != "__main__" :
    GTW.Werkzeug._Export ("*")
### __END__ GTW.Werkzeug.Command
