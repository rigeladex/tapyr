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
#    22-Jun-2012 (CT) Remove dependency on `HTTP.Application`,
#                     use `Static_File_App`, not `Static_File_Handler`
#    28-Jun-2012 (CT) Factor `App_Cache`, `_get_root`
#     9-Jul-2012 (CT) Pass `static_handler` to `_get_root`
#    17-Jul-2012 (MG) Change `_wsgi_app` to `Break` after `init_app_cache`
#    20-Jul-2012 (CT) Change `nav_admin_group` to use `GTW.RST`, not `GTW.NAV`
#    26-Jul-2012 (CT) Redefine `-UTP` as `Opt.Key` for `RST_App`, `TOP_App`
#    29-Jul-2012 (MG) Add and use `external_media_path`
#    30-Jul-2012 (CT) Move defaults to `_defaults`, merge `external_media_path`
#    30-Jul-2012 (CT) Add option `-port` (was in GTW.OMP.Command)
#     2-Aug-2012 (MG) Close database connections before starting the server
#     2-Aug-2012 (CT) Change `_wsgi_app` to avoid loading of `scope`
#     2-Aug-2012 (MG) Correct implementation of `watch_media_files`
#     5-Aug-2012 (MG) Change handling of `watch_media_files`
#     6-Aug-2012 (CT) Move `-watch_media_files` to `_GT2W_Server_Base_`
#    10-Aug-2012 (CT) Pass `verbose` to `root.Cacher` and `App_Cache`
#    14-Aug-2012 (MG) Add option `media_domain`
#    19-Aug-2012 (MG) Commit scope after cache init
#    25-Aug-2012 (CT) Import `_MOM.inspect` if `cmd.debug`
#    ««revision-date»»···
#--

from   __future__ import unicode_literals

from   _TFL                     import TFL
from   _GTW                     import GTW

import _GTW.File_Session
import _GTW._OMP.Command
import _GTW._Werkzeug.App_Cache
import _GTW._Werkzeug.Static_File_App
import _GTW.Media

import _JNJ.Templateer

from   _TFL                     import sos
from   _TFL._Meta.Once_Property import Once_Property

import _TFL.SMTP

class RST_App (TFL.Meta.Object) :

    cache_prefix   = "rst_"
    use_templateer = False

    def cachers (self, command, cmd) :
        return []
    # end def cachers

    def create (self, command, cmd, * args, ** kw) :
        return command.create_rst (cmd, * args, ** kw)
    # end def create

    def do_import (self) :
        import _GTW._RST.import_RST
    # end def do_import

    def __repr__ (self) :
        self.do_import ()
        return repr (GTW.RST)
    # end def __repr__

# end class RST_App

class TOP_App (TFL.Meta.Object) :

    cache_prefix   = ""
    use_templateer = True

    def cachers (self, command, cmd) :
        import _GTW._AFS._MOM.Form_Cache
        return [GTW.AFS.MOM.Form_Cache]
    # end def cachers

    def create (self, command, cmd, * args, ** kw) :
        return command.create_top (cmd, * args, ** kw)
    # end def create

    def do_import (self) :
        import _GTW._RST._TOP._MOM.import_MOM
    # end def do_import

    def __repr__ (self) :
        self.do_import ()
        return repr (GTW.RST.TOP)
    # end def __repr__

# end class TOP_App

class _GT2W_Sub_Command_ (GTW.OMP._Sub_Command_) :

    _rn_prefix              = "_GT2W"

_Sub_Command_ = _GT2W_Sub_Command_ # end class

class GT2W_Command (GTW.OMP.Command) :

    _rn_prefix              = "GT2W"

    SALT                    = bytes \
        ("Needs to defined uniquely for each application")

    base_template_dir       = sos.path.dirname (_JNJ.__file__)
    root                    = None

    _defaults               = dict \
        ( host              = "localhost"
        , load_I18N         = "yes"
        , log_level         = 1
        , port              = 8090
        )

    ### Sub-commands defined as class attributes to allow redefinition by
    ### derived classes; meta class puts their names into `_sub_commands`
    class _GT2W_Server_Base_ (_Sub_Command_, GTW.OMP.Command._Server_Base_) :
        ### Base for server-related commands

        is_partial              = True
        _opts                   = \
            ( "-external_media_path:P"
                "?Path where the /media/X url should be bound to"
            , "-host:S?Host name or IP-Address the server should be bound to"
            , "-load_I18N:B"
                "?Load the translation files during startup"
            , "-log_level:I?Verbosity of logging"
            , "-port:I?Port the server should use"
            , "-watch_media_files:B"
                "?Add the .media files to list files watched by "
                "automatic reloader"
            , TFL.CAO.Opt.Key
                ( name        = "UTP"
                , dct         = dict
                    ( RST     = RST_App ()
                    , TOP     = TOP_App ()
                    )
                , default     = "TOP"
                , description = "Select Url Tree Package to use."
                )
            )

    # end class _GT2W_Server_Base_

    class _GT2W_Run_Server_ (_GT2W_Server_Base_, GTW.OMP.Command._Run_Server_) :
        pass
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

    def cache_path (self, UTP) :
        return sos.path.join (self.src_dir, UTP.cache_prefix + "app_cache.pck")
    # end def cache_path

    def fixtures (self, scope) :
        pass
    # end def fixtures

    def init_app_cache (self) :
        def load_cache () :
            try :
                self.cacher.load ()
            except IOError :
                pass
        if self.cacher.DEBUG :
            try :
                self.cacher.store ()
            except EnvironmentError as exc :
                load_cache    ()
        else :
            load_cache        ()
        self.root.scope.commit ()
    # end def init_app_cache

    def nav_admin_group (self, name, title, * pnss, ** kw) :
        return GTW.RST.TOP.MOM.Admin.Group \
            ( name           = name
            , short_title    = kw.pop ("short_title", name)
            , title          = title
            , head_line      = kw.pop ("head_line", title)
            , PNSs           = pnss
            , ** kw
            )
    # end def nav_admin_group

    def _create_scope (self, apt, url, verbose = False) :
        result = self.__super._create_scope (apt, url, verbose)
        self.fixtures (result)
        return result
    # end def _create_scope

    def _create_templateer \
            (self, cmd, trim_blocks = True, version = "html/5.jnj", ** kw) :
        if cmd.UTP.use_templateer :
            from   _JNJ import JNJ
            import _JNJ.Templateer
            from _JNJ.Media_Defaults import Media_Defaults
            globs = kw.pop ("globals", {})
            media = kw.get ("Media_Parameters", None)
            if media is None :
                kw ["Media_Parameters"] = Media_Defaults ()
            return JNJ.Templateer \
                ( encoding    = cmd.input_encoding
                , globals     = dict (site_base = cmd.template_file, ** globs)
                , i18n        = cmd.load_I18N
                , trim_blocks = trim_blocks
                , version     = version
                , ** kw
                )
    # end def _create_templateer

    def _get_root (self, cmd, apt, url, ** kw) :
        result = self.root
        if result is None :
            cookie_salt = cmd.GET ("cookie_salt", self.SALT)
            if cookie_salt == Command.SALT :
                warnings.warn \
                    ( "Cookie salt should be specified for every application! "
                      "Using default `cookie_salt`!"
                    , UserWarning
                    )
            UTP     = cmd.UTP
            UTP.do_import ()
            cachers = UTP.cachers (self, cmd)
            result  = self.root = UTP.create \
                ( self, cmd
                , App_Type            = apt
                , Create_Scope        = self._load_scope
                , DB_Url              = url
                , DEBUG               = cmd.debug
                , HTTP                = cmd.HTTP
                , Session_Class       = GTW.File_Session
                , Templateer          = self._create_templateer (cmd)
                , TEST                = cmd.TEST
                , cookie_salt         = cookie_salt
                , copyright_start     = cmd.copyright_start
                , default_locale_code = cmd.locale_code
                , edit_session_ttl    = cmd.edit_session_ttl.date_time_delta
                , email_from          = cmd.email_from or None
                , encoding            = cmd.output_encoding
                , i18n                = cmd.load_I18N
                , input_encoding      = cmd.input_encoding
                , languages           = set (cmd.languages)
                , log_level           = cmd.log_level
                , page_template_name  = cmd.template_file
                , session_id          = bytes ("SESSION_ID")
                , smtp                =
                    TFL.SMTP (cmd.smtp_server) if cmd.smtp_server else None
                , use_www_debugger    = cmd.debug
                , user_session_ttl    = cmd.user_session_ttl.date_time_delta
                , ** kw
                )
            if result.Cacher :
                mc_fix = "media/v"
                mc_dir = sos.path.join (self.web_src_root, mc_fix)
                cachers.append \
                    ( result.Cacher
                        ( mc_dir, mc_fix
                        , cache_filenames = cmd.watch_media_files
                        , verbose         = cmd.verbose
                        )
                    )
                self._tmc_filenames = cachers [-1].tmc.filenames
            self.cacher = GTW.Werkzeug.App_Cache \
                ( self.cache_path (UTP)
                , * cachers
                , root    = result
                , DEBUG   = result.DEBUG
                , verbose = cmd.verbose
                )
        return result
    # end def _get_root

    def _handle_run_server (self, cmd) :
        import werkzeug.serving
        app = self._wsgi_app (cmd)
        kw  = dict \
            ( application  = app
            , hostname     = cmd.host
            , port         = cmd.port
            , use_debugger = cmd.debug
            , use_reloader = cmd.auto_reload
            )
        kw ["extra_files"] = self._tmc_filenames
        werkzeug.serving.run_simple (** kw)
    # end def _handle_run_server

    def _handle_setup_cache (self, cmd) :
        self._wsgi_app    (cmd)
        self.cacher.store ()
    # end def _handle_setup_cache

    def _handle_wsgi (self, cmd) :
        return self._wsgi_app (cmd)
    # end def _handle_wsgi

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

    def _static_file_app (self, cmd) :
        prefix  = "media"
        dir_map = []
        if cmd.external_media_path :
            dir_map.append \
                ( ("X",   sos.path.abspath (cmd.external_media_path)))
        dir_map.extend \
            ( (   ("GTW", sos.path.join (self.lib_dir,      "_GTW", prefix))
              ,   ("",    sos.path.join (self.web_src_root,         prefix))
              )
            )
        return GTW.Werkzeug.Static_File_App (dir_map, prefix = prefix)
    # end def _static_file_app

    def _wsgi_app (self, cmd) :
        if cmd.media_domain :
            GTW.Media_Base.Domain = cmd.media_domain
        apt, url = self.app_type_and_url (cmd.db_url, cmd.db_name)
        self._load_I18N (cmd)
        sf_app = self._static_file_app (cmd)
        result = root = self._get_root (cmd, apt, url, static_handler = sf_app)
        if cmd.serve_static_files :
            sf_app.wrap = root
            result      = sf_app
        if root.Templateer is not None :
            root.Templateer.env.static_handler = sf_app
        self.init_app_cache ()
        scope = root.__dict__.get ("scope")
        if scope is not None :
            scope.close_connections ()
        if cmd.debug :
            import _MOM.inspect
        if cmd.Break :
            TFL.Environment.py_shell (vars ())
        return result
    # end def _wsgi_app

Command = GT2W_Command # end class

if __name__ != "__main__" :
    GTW.Werkzeug._Export ("*")
### __END__ GTW.Werkzeug.Command
