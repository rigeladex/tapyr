# -*- coding: utf-8 -*-
# Copyright (C) 2012-2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.Werkzeug.
#
# This module is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public License
# along with this module; if not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.Werkzeug.deploy
#
# Purpose
#    Provide an extendable Command for the deployment of applications based
#    on GTW.Werkzeug
#
# Revision Dates
#    23-May-2012 (CT) Creation
#    24-May-2012 (CT) Add sub-command `setup_cache`
#     1-Jun-2012 (CT) Factor `_app_call` from `setup_cache`
#     1-Jun-2012 (CT) Add sub-command `fcgi`
#     1-Jun-2012 (CT) Add `py_options` to `_FCGI_._defaults`
#     1-Jun-2012 (CT) Derive from `GTW.OMP.deploy`, not `GTW.deploy`
#     1-Jun-2012 (CT) Add sub-command `ubycms`
#     3-Jun-2012 (CT) Add sub-command `fcgi_script`
#     3-Jun-2012 (CT) Use `self.lib_dir`, not `P.lib_dir`, in
#                     `_handle_fcgi_script`
#     5-Jun-2012 (CT) Add `exec` to output of `_handle_fcgi_script`
#    12-Dec-2013 (CT) Add `-script_path`, execute `chmod +x` on `fcgi_script`
#    16-Dec-2013 (CT) Add sub-command `create_config`,
#                     factor `_create_fcgi_script`
#    17-Dec-2013 (CT) Remove `lstrip_blocks` to allow jinja 2.6
#    17-Dec-2013 (CT) Add `verbose` to `_handle_create_config`
#    18-Dec-2013 (CT) Add `ca_path`, `ca_key_name` to `_handle_create_config`
#    20-Dec-2013 (CT) Split `addr_port` into `address` and `port`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function #, unicode_literals

from   _GTW                   import GTW
from   _TFL                   import TFL

import _GTW._OMP.deploy

from   _TFL                   import sos
from   _TFL.predicate         import uniq
from   _TFL.Regexp            import Re_Replacer, re

import sys

strip_empty_lines = Re_Replacer ("^( *\n)( *\n)+", r"\1", re.MULTILINE)

class _GT2W_Sub_Command_ (GTW.OMP.deploy._Sub_Command_) :

    _rn_prefix = "_GT2W"

_Sub_Command_ = _GT2W_Sub_Command_ # end class

_Ancestor = GTW.OMP.deploy.Command

class GT2W_Command (_Ancestor) :
    """Manage deployment applications based on GTW.Werkzeug."""

    _rn_prefix              = "GT2W"

    class _GT2W_HTTP_Config_ (TFL.Command.Root_Command.Config) :
        """Config file for HTTP-config specific options"""

        rank                    = -80
        _name                   = "HTTP_Config"

    HTTP_Config = _GT2W_HTTP_Config_ # end class

    class _GT2W_Babel_ (_Sub_Command_, _Ancestor._Babel_) :

        _package_dirs           = [ "_JNJ", "_ReST"]

    _Babel_ = _GT2W_Babel_ # end class

    class _GT2W_FCGI_ (_Sub_Command_) :
        """Run application as a FastCGI server."""

        _defaults               = dict \
            ( apply_to_version  = "active"
            )

    _FCGI_ = _GT2W_FCGI_ # end class

    class _GT2W_FCGI_Script_ (_FCGI_) :
        """Create script for running the application as a FastCGI server."""

        _opts                   = \
            ( "-script_path:Q?Path of script created"
            ,
            )

    _FCGI_Script_ = _GT2W_FCGI_Script_ # end class

    class _GT2W_Create_Config_ (_FCGI_Script_) :
        """Create config file and fcgi-script for http-server"""

        _defaults               = dict \
            ( address           = "*"
            , port              = "80"
            , ca_key_name       = "CA_crt"
            , ca_path           = "~/CA"
            , host_macro        = "gtw_host"
            , macro_module      = "httpd_config/apache.m.jnj"
            , root_dir          = "~/active"
            )

        _opts                   = \
            ( "-address:S?Address of virtual host"
            , "-ca_key_name:S?Name of CA key file"
            , "-ca_path:Q?Path for server-specific CA for client certificates"
            , "-config_path:Q?Path for config file"
            , "-host_macro:S?Name of macro to create virtual host"
            , "-macro_module:S"
                "?Name of jinja module providing config-generation macros"
            , "-port:S?Port for virtual host"
            , "-root_dir:Q?Root path of web app"
            , "-server_admin:S?Email address of server admin of virtual host"
            , "-server_aliases:T#8?Alias names for virtual host"
            , "-server_name:S?Fully qualified domain name of virtual host"
            , "-ssl_key_name:S?Name of SSL key to use for HTTPS"
            , "-template_dirs:P?Directories containing templates for config"
            , "-verbose:B=yes"
            )

        def dynamic_defaults (self, defaults) :
            import _JNJ
            result = self.__super.dynamic_defaults (defaults)
            tdirs  = list (result.get ("template_dirs", ()))
            tdirs.extend  ([self.app_dir, sos.path.dirname (_JNJ.__file__)])
            result ["template_dirs"] = tuple (uniq (tdirs))
            return result
        # end def dynamic_defaults

    _Create_Config_ = _GT2W_Create_Config_ # end class

    class _GT2W_Setup_Cache_ (_Sub_Command_) :
        """Setup the cache of the application."""

    _Setup_Cache_ = _GT2W_Setup_Cache_ # end class

    class _GT2W_UBYCMS_ (TFL.Command.Sub_Command_Combiner) :
        """Update, Babel compile, pYcompile, setup Cache, Migrate, Switch."""

        _rn_prefix       = "_GT2W"

        _sub_command_seq = \
            [ "update"
            , ["babel", "compile"]
            , "pycompile"
            , ["migrate", "-Active", "-Passive"]
            , "setup_cache"
            , "switch"
            ]

    _UBYCMS_ = _GT2W_UBYCMS_ # end class

    def _create_fcgi_script (self, cmd, argv = (), script_path = None) :
        P      = self._P (cmd)
        a_conf = cmd.app_config
        h_conf = cmd._spec ["HTTP_Config"].pathes
        config = self.App_Config.auto_split.join (a_conf + h_conf)
        args   = ("fcgi", "-config", config) + tuple (argv)
        app    = self._app_cmd (cmd, P, args = args)
        s_path = script_path or cmd.script_path
        def write (f, app, lib_dir) :
            f.write ("#!/bin/sh\n")
            f.write ("export PYTHONPATH=%s\n" % (lib_dir, ))
            f.write ("exec %s\n" % (app, ))
        if s_path and s_path not in ("-", "stdout") :
            with open (s_path, "w") as f :
                write (f, app, self.lib_dir)
            self.pbl ["chmod"] ("+x", s_path)
            if cmd.verbose :
                print ("Created fcgi script", s_path)
        else :
            write (sys.stdout, app, self.lib_dir)
    # end def _create_fcgi_script

    def _handle_create_config (self, cmd) :
        self._create_fcgi_script (cmd, cmd.argv, cmd.script_path)
        from   _JNJ import JNJ
        import _JNJ.Templateer
        templateer           = JNJ.Templateer \
            ( encoding       = cmd.input_encoding
            , globals        = dict ()
            , load_path      = cmd.template_dirs
            , trim_blocks    = True
            )
        config               = templateer.call_macro \
            ( macro_name     = cmd.host_macro
            , templ_name     = cmd.macro_module
            , address        = cmd.address
            , admin          = cmd.server_admin
            , aliases        = cmd.server_aliases
            , ca_key_name    = cmd.ca_key_name
            , ca_path        = cmd.ca_path
            , cmd            = cmd
            , port           = cmd.port
            , root           = cmd.root_dir
            , script         = cmd.script_path
            , server_name    = cmd.server_name
            , ssl_key_name   = cmd.ssl_key_name
            )
        config_s = strip_empty_lines (config).strip ()
        c_path   = cmd.config_path
        def write (f, config) :
            f.write (config)
            f.write ("\n")
        if c_path and c_path not in ("-", "stdout") :
            with open (c_path, "w") as f :
                write (f, config_s)
            if cmd.verbose :
                print ("Created config file", c_path)
        else :
            write (sys.stdout, config_s)
    # end def _handle_create_config

    def _handle_fcgi (self, cmd) :
        P     = self._P (cmd)
        app   = self._app_cmd (cmd, P)
        args  = ("fcgi", ) + tuple (cmd.argv)
        self._app_call (cmd, P, app, args)
    # end def _handle_fcgi

    def _handle_fcgi_script (self, cmd) :
        self._create_fcgi_script (cmd, cmd.argv, cmd.script_path)
    # end def _handle_fcgi_script

    def _handle_setup_cache (self, cmd) :
        P    = self._P (cmd)
        app  = self._app_cmd (cmd, P)
        args = ("setup_cache", ) + tuple (cmd.argv)
        self._app_call (cmd, P, app, args)
    # end def _handle_setup_cache

Command = GT2W_Command # end class

if __name__ != "__main__" :
    GTW.Werkzeug._Export_Module ()
### __END__ GTW.Werkzeug.deploy
