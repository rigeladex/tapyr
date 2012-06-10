# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.
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
#    GTW.deploy
#
# Purpose
#    Provide an extendable Command for the deployment of applications based
#    on GTW
#
# Revision Dates
#    22-May-2012 (CT) Creation
#    23-May-2012 (CT) Continue creation
#    24-May-2012 (CT) Factor `_app_cmd`, add `print` to `_handle_...` methods
#    24-May-2012 (CT) Add `PYTHONPATH` to `.pbl.env`
#    25-May-2012 (CT) Add sub-command `shell`
#    25-May-2012 (CT) Add `path` to `_app_cmd`
#    30-May-2012 (CT) Add sub-command `app`
#    31-May-2012 (CT) Factor `-config` option to `TFL.Command`
#    31-May-2012 (CT) Change `_handle_app` to allow multiple arguments
#     1-Jun-2012 (CT) Move `-apply_to_version` to `_Sub_Command_` to allow
#                     sub-command specific defaults
#     1-Jun-2012 (CT) Factor `_app_call`
#     1-Jun-2012 (CT) Factor `P.app_dir`
#     1-Jun-2012 (CT) Add option `-py_path`; factor `P.python`
#     1-Jun-2012 (CT) Add `-py_options` to `_Sub_Command_`,
#                     remove `-python_options` from `_Pycompile_`
#     3-Jun-2012 (CT) Factor `Config` to `Root_Command`
#     3-Jun-2012 (CT) Add optional `_args` to `_app_cmd`
#     4-Jun-2012 (CT) Fix `app_dir` in `_handle_babel_compile`
#     4-Jun-2012 (CT) Change `Shell.handler` to `_handle_shell`
#     4-Jun-2012 (CT) Rewrite `_handle_update` to use `_handle_vc`
#    ��revision-date�����
#--

from   __future__  import absolute_import, division, print_function #, unicode_literals

from   _TFL                   import TFL
from   _GTW                   import GTW

from   _TFL                   import sos

import _TFL.Command

from   itertools              import chain as ichain
import sys

pjoin = sos.path.join

class _GTWD_Command_ (TFL.Command.Command) :

    _rn_prefix = "_GTWD"

_Command_ = _GTWD_Command_ # end class

class _GTWD_Sub_Command_ (TFL.Command.Sub_Command) :

    _rn_prefix              = "_GTWD"

    _defaults               = dict \
        ( apply_to_version  = "passive"
        , py_options        = "-O"
        )
    _opts                   = \
        ( "-apply_to_version:S?Name of version to apply command to"
        , "-py_options:T ?Options passed to python interpreter, e.g., -O"
        )

_Sub_Command_ = _GTWD_Sub_Command_ # end class

class GTWD_Command (TFL.Command.Root_Command) :
    """Extendable deployment command for applications based on GTW"""

    _rn_prefix              = "GTWD_"

    min_args                = 1

    _defaults               = dict \
        ( active_name       = "active"
        , app_dir           = "app"
        , bugs_address      = "tanzer@swing.co.at,martin@mangari.org"
        , copyright_holder  = "Mag. Christian Tanzer, Martin Gl�ck"
        , lib_dir           = "lib"
        , output_encoding   = "utf-8"
        , passive_name      = "passive"
        , py_path           = sys.executable
        , root_path         = "./"
        , skip_modules      = "_pyk3.py"
        , vcs               = "git"
        )

    _opts                   = \
        ( "-active_name:S?Name of symbolic link for active version"
        , "-app_dir:S?Name of directory holding the application"
        , "-app_module:S=app.py?Name of main module of application"
        , "-bugs_address:S?Email address to send bug reports to"
        , "-copyright_holder:S?Name of copyright holders"
        , "-dry_run:B?Don't run the command, just print what would be done"
        , "-lib_dir:S"
            "?Name of directory with the library used by the application"
        , "-passive_name:S?Name of symbolic link for passive version"
        , "-project_name:S?Name of project"
        , "-py_path:P?Path for nested python interpreter"
        , "-root_path:P?Root path of application versioning"
        , "-verbose:B"
        , "-vcs:S?Name of version control system used"
        , TFL.CAO.Opt.Output_Encoding
            ( description   = "Default encoding for generated files"
            )
        )

    _vcs_update_map         = dict \
        ( git               = "pull"
        , hg                = "pull"
        , svn               = "update"
        )

    class _GTWD_App_ (_Sub_Command_) :
        """Run a command of the web application."""

        min_args            = 1

    _App_ = _GTWD_App_ # end class

    class _GTWD_Babel_ (_Command_) :
        """Extract or compile translations."""

        _lists_to_combine   = ("_package_dirs", )

        min_args            = 1

        _defaults           = dict \
            ( languages     = "en"
            )

        _opts               = \
            ( "-babel_config:S?File with global babel configuration"
            , "-languages:S,?Languages to extract/compile translations for"
            , "-package_dirs:P,"
                "?Package directories (relative to Python path) to "
                "include in extraction/compilation of translations"
            )

        _babel_config       = "_MOM/base_babel.cfg"
        _package_dirs       = []

        class _GTWD_Babel_Sub_Command_ (_Sub_Command_) :

            _handler_prefix = "babel_"

            is_partial      = True

        _Babel_Sub_Command_ = _GTWD_Babel_Sub_Command_ # end class

        class _GTWD_Extract_ (_Babel_Sub_Command_) :
            """Extract strings to translate."""

        _Extract_ = _GTWD_Extract_ # end class

        class _GTWD_Compile_ (_Babel_Sub_Command_) :
            """Compile translations."""

        _Compile_ = _GTWD_Compile_ # end class

        def dynamic_defaults (self, defaults) :
            result = self.__super.dynamic_defaults (defaults)
            if "babel_config" not in result :
                bc = self._babel_config
                if bc :
                    if not sos.path.isabs (bc) :
                        bc = pjoin (self.lib_dir, bc)
                    result ["babel_config"] = bc
            if "package_dirs" not in result :
                result ["package_dirs"] = self._package_dirs
            return result
        # end def dynamic_defaults

    _Babel_ = _GTWD_Babel_ # end class

    class _GTWD_Info_ (_Sub_Command_) :
        """Show info about the application."""

    _Info_ = _GTWD_Info_     # end class

    class _GTWD_Pycompile_ (_Sub_Command_) :
        """Compile python bytecode of the application."""

        _opts               = \
            ( "-compile_options:S,?Options passed to compileall, e.g., -q"
            , "-skip_modules:S,?Python modules to skip compilation for"
            )

    _Pycompile_ = _GTWD_Pycompile_ # end class

    class _GTWD_Shell_ (_Sub_Command_) :
        """Open interactive python shell."""

    _Shell_ = _GTWD_Shell_ # end class

    class _GTWD_Switch_ (_Sub_Command_) :
        """Switch links to active and passive version."""

    _Switch_ = _GTWD_Switch_ # end class

    class _GTWD_Update_ (_Sub_Command_) :
        """Update the source code of the application."""

    _Update_ = _GTWD_Update_ # end class

    class _GTWD_VC_ (_Sub_Command_) :
        """Run a command of the version control system."""

        min_args            = 1

    _VC_ = _GTWD_VC_ # end class

    @TFL.Meta.Once_Property
    def pbc (self) :
        import plumbum
        return sys.modules ["plumbum.cmd"]
    # end def pbc

    @TFL.Meta.Once_Property
    def pbl (self) :
        from plumbum import local
        return local
    # end def pbl

    def _app_call (self, cmd, P, app, args = (), app_dir = None) :
        pbl = self.pbl
        cwd = pbl.cwd
        if not args :
            args = tuple (cmd.argv)
        if app_dir is None :
            app_dir = P.app_dir
        with cwd (app_dir) :
            if cmd.verbose or cmd.dry_run :
                print ("cd", pbl.path ())
                print (app, " ".join (args))
            if not cmd.dry_run :
                print (app (* args))
    # end def _app_call

    def _app_cmd (self, cmd, P, version = None, args = ()) :
        if version is None :
            version = cmd.apply_to_version
        result = P.python \
            [P.root / version / cmd.app_dir / cmd.app_module]
        if cmd.verbose :
            result = result ["-verbose"]
        if args :
            result = result [args]
        return result
    # end def _app_cmd

    def _handle_app (self, cmd, * args) :
        P   = self._P (cmd)
        app = self._app_cmd (cmd, P)
        self._app_call (cmd, P, app, args)
    # end def _handle_app

    def _handle_babel_compile (self, cmd) :
        P       = self._P (cmd)
        cwd     = self.pbl.cwd
        args    = \
             ( "-m", "_TFL.Babel", "compile"
             , "-combine"
             , "-import_file",     cmd.app_module
             , "-use_fuzzy"
             )
        app_dir = sos.path.dirname (sos.path.join (P.app_dir, cmd.app_module))
        with cwd (app_dir) :
            if cmd.verbose or cmd.dry_run :
                print ("cd", self.pbl.path ())
            for l in cmd.languages :
                l_dir  = pjoin ("locale", l, "LC_MESSAGES")
                l_args = args + \
                    ( "-languages",   l
                    , "-output_file", pjoin (l_dir, "messages.mo")
                    )
                if cmd.verbose or cmd.dry_run :
                    print ("mkdir -p", l_dir)
                    print ("python", " ".join (l_args))
                if not cmd.dry_run :
                    if not sos.path.isdir (l_dir) :
                        sos.makedirs (l_dir)
                    print (P.python (* l_args))
    # end def _handle_babel_compile

    def _handle_babel_extract (self, cmd) :
        head_args = ("-m", "_TFL.Babel")
        tail_args = ("-sort", ) + tuple (cmd.package_dirs)
        extr_args = \
            ( head_args
            + ( "extract"
              , "-bugs_address",     cmd.bugs_address
              , "-charset",          cmd.output_encoding
              , "-copyright_holder", cmd.copyright_holder
              , "-global_config",    cmd.babel_config
              , "-project",          cmd.project_name
              )
            + tail_args
            )
        lang_args = \
            ( head_args
            + ( "language", ",".join (cmd.languages))
            + tail_args
            )
        if cmd.verbose or cmd.dry_run :
            print ("python", " ".join (extr_args))
            print ("python", " ".join (lang_args))
        if not cmd.dry_run :
            print (P.python (* extr_args))
            print (P.python (* lang_args))
    # end def _handle_babel_extract

    def _handle_info (self, cmd) :
        P       = self._P (cmd)
        fmt     = "%-15s : %s"
        print (fmt % (cmd.active_name,  P.active))
        print (fmt % (cmd.passive_name, P.passive))
        print (fmt % ("selected",       P.selected))
        print (fmt % ("prefix",         P.prefix))
        print (fmt % ("app-dir",        P.app_dir))
        print (fmt % ("python",         P.python))
        print (fmt % ("python-library", self.lib_dir))
        print (fmt % ("nested-library", P.lib_dir))
        print (fmt % ("PYTHONPATH",     sys.path))
        print \
            ( fmt
            % ( "NESTEDPATH"
              , P.python ("-c", "import sys; print sys.path")
              )
            )
    # end def _handle_info

    def _handle_pycompile (self, cmd) :
        P    = self._P (cmd)
        cwd  = self.pbl.cwd
        root = pjoin (cmd.root_path, cmd.apply_to_version)
        args = tuple \
            ( ichain
                ( ["-m", "compileall"]
                , cmd.compile_options
                , ((["-x"] + cmd.skip_modules) if cmd.skip_modules else [])
                , [cmd.app_dir, cmd.lib_dir]
                )
            )
        with cwd (root) :
            if cmd.verbose or cmd.dry_run :
                print ("cd", self.pbl.path ())
                print (P.python, " ".join (args))
            if not cmd.dry_run :
                P.python (* args)
    # end def _handle_pycompile

    def _handle_shell (self, cmd) :
        import _TFL.Environment
        P       = self._P (cmd)
        command = self._root
        TFL.Environment.py_shell ()
    # end def _handle_shell

    def _handle_switch (self, cmd) :
        P    = self._P (cmd)
        ln_s = self.pbl ["ln"] ["-f", "-s", "-T" ]
        cmda = ln_s [P.active,  cmd.passive_name]
        cmdp = ln_s [P.passive, cmd.active_name]
        cwd  = self.pbl.cwd
        with cwd (P.root) :
            if cmd.verbose or cmd.dry_run :
                print (cmda, ";", cmdp)
            if not cmd.dry_run :
                cmda ()
                cmdp ()
    # end def _handle_switch

    def _handle_update (self, cmd) :
        return self._handle_vc (cmd, self._vcs_update_map [cmd.vcs])
    # end def _handle_update

    def _handle_vc (self, cmd, * args) :
        P    = self._P (cmd)
        cwd  = self.pbl.cwd
        vcs  = self.pbl [cmd.vcs] [args]
        argv = tuple (cmd.argv)
        for d in P.app_dir, P.lib_dir :
            with cwd (d) :
                p = self.pbl.path ()
                if cmd.verbose or cmd.dry_run :
                    print ("cd", p)
                    print (vcs, " ".join (argv))
                if not cmd.dry_run :
                    if not cmd.verbose :
                        print ("*" * 3, p, "*" * 20)
                    print (vcs (* argv))
    # end def _handle_vc

    def _P (self, cmd) :
        pbl     = self.pbl
        active  = sos.path.realpath     (cmd.active_name)
        passive = sos.path.realpath     (cmd.passive_name)
        root    = sos.path.realpath     (cmd.root_path)
        prefix  = sos.path.commonprefix ([active, passive, root])
        if prefix :
            active     = active  [len (prefix):].lstrip ("/")
            passive    = passive [len (prefix):].lstrip ("/")
        result = TFL.Record \
            ( active   = active
            , passive  = passive
            , prefix   = prefix
            , python   = pbl [cmd.py_path]
                [tuple (o for o in cmd.py_options if o)]
            , root     = pbl.path (root)
            )
        result.selected = getattr (result, cmd.apply_to_version)
        result.app_dir  = sos.path.abspath \
            (pjoin (result.selected, cmd.app_dir))
        result.lib_dir  = pbl.env ["PYTHONPATH"] = sos.path.abspath \
            (pjoin (result.selected, cmd.lib_dir))
        return result
    # end def _P

Command = GTWD_Command # end class

if __name__ != "__main__" :
    GTW._Export_Module ()
if __name__ == "__main__" :
    Command () ()
### __END__ GTW.deploy