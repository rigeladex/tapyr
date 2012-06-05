# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
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
#     5-Jun-2012 (CT) Add logging to `_handle_fcgi`
#    ��revision-date�����
#--

from   __future__  import absolute_import, division, print_function #, unicode_literals

from   _GTW                   import GTW
from   _TFL                   import TFL

import _GTW._OMP.deploy

import datetime

class _GT2W_Sub_Command_ (GTW.OMP.deploy._Sub_Command_) :

    _rn_prefix = "_GT2W"

_Sub_Command_ = _GT2W_Sub_Command_ # end class

_Ancestor = GTW.OMP.deploy.Command

class GT2W_Command (_Ancestor) :
    """Manage deployment applications based on GTW.Werkzeug."""

    _rn_prefix              = "GT2W"

    class _GT2W_Babel_ (_Sub_Command_, _Ancestor._Babel_) :

        _package_dirs       = [ "_JNJ", "_ReST"]

    _Babel_ = _GT2W_Babel_ # end class

    class _GT2W_FCGI_ (_Sub_Command_) :
        """Run application as a FastCGI server."""

        _defaults               = dict \
            ( apply_to_version  = "active"
            )

    _FCGI_ = _GT2W_FCGI_ # end class

    class _GT2W_FCGI_Script_ (_FCGI_) :
        """Create script for running the application as a FastCGI server."""

    _FCGI_Script_ = _GT2W_FCGI_Script_ # end class

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
            , "setup_cache"
            , ["migrate", "-Active", "-Passive"]
            , "switch"
            ]

    _UBYCMS_ = _GT2W_UBYCMS_ # end class

    @property
    def now (self) :
        return datetime.datetime.now ().replace (microsecond = 0)
    # end def now

    def _handle_fcgi (self, cmd) :
        P     = self._P (cmd)
        app   = self._app_cmd (cmd, P)
        args  = ("fcgi", ) + tuple (cmd.argv)
        start = self.now
        if cmd.log_level :
            logging.warning \
                ("[%s] Starting %s %s" % (start, app, " ".join (args)))
        try :
            self._app_call (cmd, P, app, args)
        finally :
            if cmd.log_level :
                logging.warning \
                    ( "[%s <-- %s] Finished %s %s"
                    % (self.now, start, app, " ".join (args))
                    )
    # end def _handle_fcgi

    def _handle_fcgi_script (self, cmd) :
        P      = self._P (cmd)
        config = self.App_Config.auto_split.join (cmd.app_config)
        args   = ("fcgi", "-config", config) + tuple (cmd.argv)
        app    = self._app_cmd (cmd, P, args = args)
        print  ("#!/bin/sh")
        print  ("export PYTHONPATH=%s" % self.lib_dir)
        print  ("exec", app)
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
