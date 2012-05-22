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
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function #, unicode_literals

from   _TFL                   import TFL
from   _GTW                   import GTW

from   _TFL                   import sos

import _TFL.Command

from   itertools              import chain as ichain
import sys

class _GTWD_Command_ (TFL.Sub_Command) :

    _rn_prefix = "_GTWD"

_Command_ = _GTWD_Command_ # end class

class GTWD_Command (TFL.Command) :
    """Extendable deployment command for applications based on GTW"""

    _rn_prefix = "GTWD"

    _defaults               = dict \
        ( active_name       = "active"
        , app_dir           = "app"
        , apply_to_version  = "passive"
        , lib_dir           = "lib"
        , passive_name      = "passive"
        , root_path         = "./"
        , skip_modules      = "_pyk3.py"
        , vcs               = "git"
        )

    _opts                   = \
        ( "-active_name:S?Name of symbolic link for active version"
        , "-app_dir:S?Name of directory holding the application"
        , "-apply_to_version:S?Name of version to apply command to"
        , "-config:C:?File(s) specifying defaults for options"
        , "-dry_run:B?Don't run the command, just print what would be done"
        , "-lib_dir:S"
            "?Name of directory with the library used by the application"
        , "-passive_name:S?Name of symbolic link for passive version"
        , "-root_path:P?Root path of application versioning"
        , "-verbose:B"
        )

    _vcs_update_map         = dict \
        ( git               = "pull"
        , hg                = "pull"
        , svn               = "update"
        )

    class _GTWD_Info_ (_Command_) :
        """Show info about the application."""

    _Info_ = _GTWD_Info_     # end class

    class _GTWD_Pycompile_ (_Command_) :
        """Compile python bytecode of the application."""

        _opts               = \
            ( "-compile_options:S,?Options passed to compileall, e.g., -q"
            , "-python_options:S,"
                "?Options passed to python interpreter, e.g., -O"
            , "-skip_modules:S,?Python modules to skip compilation for"
            )

    _Pycompile_ = _GTWD_Pycompile_ # end class

    class _GTWD_Switch_ (_Command_) :
        """Switch links to active and passive version."""

    _Switch_ = _GTWD_Switch_ # end class

    class _GTWD_Update_ (_Command_) :
        """Update the source code of the application."""

        _opts               = \
            ( "-vcs:S?Name of version control system used"
            ,
            )

    _Update_ = _GTWD_Update_ # end class

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

    def _handle_info (self, cmd) :
        P = self._P (cmd)
        print ("prefix",         "-->", P.prefix)
        print (cmd.active_name,  "-->", P.active)
        print (cmd.passive_name, "-->", P.passive)
    # end def _handle_info

    def _handle_pycompile (self, cmd) :
        cwd  = self.pbl.cwd
        root = sos.path.join (cmd.root_path, cmd.apply_to_version)
        with cwd (root) :
            args = tuple \
                ( ichain
                    ( ["-m"]
                    , cmd.python_options
                    , ["compileall"]
                    , cmd.compile_options
                    , ((["-x"] + cmd.skip_modules) if cmd.skip_modules else [])
                    , [cmd.app_dir, cmd.lib_dir]
                    )
                )
            if cmd.verbose or cmd.dry_run :
                print ("cd", root, "; python", " ".join (args))
            if not cmd.dry_run :
                self.pbc.python (* args)
    # end def _handle_pycompile

    def _handle_switch (self, cmd) :
        P    = self._P (cmd)
        ln_s = self.pbl ["ln"] ["-f", "-s", "-T" ]
        cmd1 = ln_s [P.passive, cmd.active_name]
        cmd2 = ln_s [P.active,  cmd.passive_name]
        cwd  = self.pbl.cwd
        with cwd (P.root) :
            if cmd.verbose or cmd.dry_run :
                print (cmd1, ";", cmd2)
            if not cmd.dry_run :
                cmd1 ()
                cmd2 ()
    # end def _handle_switch

    def _handle_update (self, cmd) :
        cwd  = self.pbl.cwd
        root = sos.path.join (cmd.root_path, cmd.apply_to_version)
        vcs  = cmd.vcs
        upd  = self.pbl [vcs] [self._vcs_update_map [vcs]]
        with cwd (root) :
            for d in cmd.app_dir, cmd.lib_dir :
                with cwd (d) :
                    if cmd.verbose or cmd.dry_run :
                        print ("cd", self.pbl.path (), ";", upd)
                    if not cmd.dry_run :
                        upd ()
    # end def _handle_update

    def _P (self, cmd) :
        active  = sos.path.realpath (cmd.active_name)
        passive = sos.path.realpath (cmd.passive_name)
        root    = sos.path.realpath (cmd.root_path)
        prefix  = sos.path.commonprefix ([active, passive, root])
        if prefix :
            active  = active  [len (prefix):].lstrip ("/")
            passive = passive [len (prefix):].lstrip ("/")
        return TFL.Record \
            ( active   = active
            , passive  = passive
            , prefix   = prefix
            , root     = root
            )
    # end def _P

Command = GTWD_Command # end class

if __name__ != "__main__" :
    GTW._Export_Module ()
if __name__ == "__main__" :
    Command () ()
### __END__ GTW.deploy
