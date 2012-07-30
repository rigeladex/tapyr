# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.OMP.
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
#    GTW.OMP.Command
#
# Purpose
#    Provide an extendable Command for applications based on GTW.OMP
#
# Revision Dates
#    25-Jun-2010 (CT) Creation
#    28-Jun-2010 (CT) `HTTP_Opt` added
#    29-Jun-2010 (CT) `HTTP_Opt` changed to `_Import_Module ("Application")`
#    29-Jun-2010 (CT) Command for `wsgi` added
#     3-Aug-2010 (MG) Additional options added to `shell` sub-command
#    10-Aug-2010 (CT) Command `description` defined as doc-string of `handler`
#    10-Feb-2011 (CT) Injection of `GTW` into essential classes added
#    14-Mar-2011 (CT) Injection of `GTW` factored to `_GTW._OMP.MOM_injector`
#    15-Mar-2011 (CT) `_load_afs` and `_setup_afs` added
#     5-Apr-2011 (MG) Default for `HTTP` changed to `Werkzeug`
#     3-May-2011 (CT) Options `edit_session_ttl` and `user_session_ttl` added
#    10-Jun-2011 (MG) `shell` parameter `echo` added
#    15-Jun-2011 (MG) `_load_afs` and `_setup_afs` moved into `GTW.NAV.Base`
#    27-Jan-2012 (CT) Add `-languages`, `-locale_code`, and `-time_zone` to
#                     `cmd___server__opts`
#    15-May-2012 (CT) Add sub-command `setup_cache`
#    17-May-2012 (CT) Derive from `MOM.Command` instead of `MOM.Scaffold`,
#                     rename from `Scaffold` to `Command`
#     1-Jun-2012 (CT) Add sub-command `fcgi`
#     5-Jun-2012 (CT) Add logging to `_handle_fcgi`
#    18-Jun-2012 (CT) Add option `-email_from` to `_GTW_Server_Base_._opts`
#    20-Jun-2012 (CT) Add option `-UTP`, factor `_Pkg_Selector_Opt_`
#    21-Jun-2012 (CT) Use `TFL.CAO.Opt.Time_Zone`, not home-grown code
#    21-Jun-2012 (CT) Add option `-serve_static_files`
#    26-Jul-2012 (CT) Remove option `-UTP`
#    26-Jul-2012 (CT) Add local variables `Q` and `root` to `_handle_shell`
#    30-Jul-2012 (CT) Remove import of `HTTP.Application`
#    ««revision-date»»···
#--

from   _CAL                   import CAL
from   _GTW                   import GTW
from   _MOM                   import MOM
from   _TFL                   import TFL

import _CAL.Delta

import _GTW._OMP.MOM_injector

import _MOM.Command

from   _TFL                   import sos

import _TFL.CAO
import _TFL._Meta.Once_Property

import datetime, logging, sys

class _Pkg_Selector_Opt_ (TFL.CAO._Spec_) :
    ### Base class for options selecting a specific GTW package

    _name    = None ### redefine
    _default = None ### redefine

    def __init__ (self, ** kw) :
        assert "name" not in kw
        kw ["name"] = self._name
        if "description" not in kw :
            kw ["description"] = self.__class__.__doc__
        self.__super.__init__ (max_number = 1, ** kw)
    # end def __init__

    def cook (self, value, cao = None) :
        if not value :
            value = self._default
        m = GTW._Import_Module ("_" + value)
        result = getattr (m, value)
        return result
    # end def cook

    def _set_default (self, default) :
        ### Make `cls._default` sticky
        self.__super._set_default (default or self._default)
    # end def _set_default

# end class _Pkg_Selector_Opt_

class HTTP_Opt (_Pkg_Selector_Opt_) :
    """Select HTTP server framework to use."""

    _name    = "HTTP"
    _default = "Werkzeug"

# end class HTTP_Opt

class _GTW_Sub_Command_ (MOM._Sub_Command_) :

    _rn_prefix              = "_GTW"

_Sub_Command_ = _GTW_Sub_Command_ # end class

class GTW_Command (MOM.Command) :

    _rn_prefix              = "GTW"

    ANS                     = GTW

    _defaults               = dict \
        ( edit_session_ttl  = CAL.Date_Time_Delta (hours = 3)
        , input_encoding    = "iso-8859-15"
        , languages         = "en,de"
        , local_code        = "en_US"
        , output_encoding   = "utf-8"
        , template_file     = "html/static.jnj"
        , user_session_ttl  = CAL.Date_Time_Delta (days = 3)
        )

    ### Sub-commands defined as class attributes to allow redefinition by
    ### derived classes; meta class puts their names into `_sub_commands`
    class _GTW_Server_Base_ (_Sub_Command_) :
        ### Base for server-related commands

        is_partial              = True
        _opts                   = \
            ( "-auto_reload:B"
                  "?Autoload of werkzeug, only works with no sqlite db"
            , "-Break:B?Enter debugger right after creating wsgi app"
            , "-debug:B=no"
            , "-email_from:S"
                "?Email address to use as from-address for emails sent "
                "by the app"
            , "-languages:T,?Languages for which to load translations"
            , "-locale_code:S?Code of locale to use"
            , "-port:I=8090?Server port"
            , "-serve_static_files:B?Serve static files"
            , "-smtp_server:S=localhost?SMTP server used to send emails"
            , "-template_file:S"
            , "-TEST:B"
            , HTTP_Opt (default = "Werkzeug")
            , TFL.CAO.Opt.Date_Time_Delta
                ( name          = "edit_session_ttl"
                , description   = "Time to live for edit session"
                )
            , TFL.CAO.Opt.Input_Encoding
                ( description   = "Default encoding for source files"
                )
            , TFL.CAO.Opt.Output_Encoding
                ( description   = "Default encoding for generated html"
                )
            , TFL.CAO.Opt.Time_Zone ()
            , TFL.CAO.Opt.Date_Time_Delta
                ( name          = "user_session_ttl"
                , description   = "Time to live for user session (cookie)"
                )
            )

    _Server_Base_ = _GTW_Server_Base_ # end class

    class _GTW_FCGI_ (_GTW_Server_Base_) :
        """Run as a FastCGI server."""

    _FCGI_ = _GTW_FCGI_ # end class

    class _GTW_Run_Server_ (_GTW_Server_Base_) :
        """Run as application server."""

        _defaults           = dict \
            ( auto_reload        = True
            , serve_static_files = True
            )

    _Run_Server_ = _GTW_Run_Server_ # end class

    class _GTW_Setup_Cache_ (_GTW_Server_Base_) :
        """Setup the cache of the application."""

    _Setup_Cache_ = _GTW_Setup_Cache_ # end class

    class _GTW_Shell_ (_GTW_Server_Base_, MOM.Command._Shell_) :

        _opts                   = \
            ( "wsgi:B?Create the wsgi application before entering the shell"
            , "echo:B?Set the echo flag of the SQLAlchemy engine"
            )

    _Shell_ = _GTW_Shell_ # end class

    class _GTW_WSGI_ (_GTW_Server_Base_) :
        """Run as wsgi application."""

    _WSGI_ = _GTW_WSGI_ # end class

    @property
    def now (self) :
        return datetime.datetime.now ().replace (microsecond = 0)
    # end def now

    def _handle_fcgi (self, cmd) :
        from flup.server.fcgi import WSGIServer
        start = self.now
        exe   = "%s fcgi" % sos.path.abspath (self.app_path)
        if cmd.log_level :
            logging.warning ("[%s] Starting %s" % (start, exe))
        try :
            return WSGIServer (self._handle_wsgi (cmd)).run ()
        finally :
            if cmd.log_level :
                logging.warning \
                    ("[%s <-- %s] Finished %s" % (self.now, start, exe))
    # end def _handle_fcgi

    def _handle_run_server (self, cmd) :
        raise NotImplementedError
    # end def _handle_run_server

    def _handle_setup_cache (self, cmd) :
        raise NotImplementedError
    # end def _handle_setup_cache

    def _handle_shell (self, cmd) :
        if cmd.echo :
            from _MOM._DBW._SAS.DBS import Postgresql
            Postgresql.Engine_Parameter ["echo"] = True
        from _MOM.import_MOM import Q
        scope = self._handle_load (cmd)
        if cmd.wsgi :
            wsgi = self._handle_wsgi (cmd)
            root = top = self.root
        TFL.Environment.py_shell ()
    # end def _handle_shell

    def _handle_wsgi (self, cmd) :
        raise NotImplementedError
    # end def _handle_wsgi

Command = GTW_Command # end class

if __name__ != "__main__" :
    GTW.OMP._Export ("*", "_Sub_Command_")
### __END__ GTW.OMP.Command
