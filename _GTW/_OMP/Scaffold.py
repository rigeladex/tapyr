# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010-2011 Mag. Christian Tanzer All rights reserved
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
#    GTW.OMP.Scaffold
#
# Purpose
#    Provide a scaffold for creating instances of MOM.App_Type and MOM.Scope
#    and managing their databases
#
# Revision Dates
#    25-Jun-2010 (CT) Creation
#    28-Jun-2010 (CT) `HTTP_Opt` added
#    29-Jun-2010 (CT) `HTTP_Opt` changed to `_Import_Module ("Application")`
#    29-Jun-2010 (CT) Command for `wsgi` added
#     3-Aug-2010 (MG) Additional options added to `shell` sub-command
#    10-Aug-2010 (CT) Command `description` defined as doc-string of `handler`
#    10-Feb-2011 (CT) Injection of `GTW` into essential classes added
#    ««revision-date»»···
#--

from   _GTW                   import GTW
from   _MOM                   import MOM
from   _TFL                   import TFL

import _MOM.Scaffold

import _TFL.CAO
import _TFL._Meta.Once_Property

### Inject a class-valued  class attribute `GTW` into the essential classes
### (due to `_nested_classes_to_combine`, each essential class gets their own
### `GTW` class with proper inheritance)
import _MOM._Meta.M_Entity, _MOM.Entity
MOM.Meta.M_Entity._nested_classes_to_combine += ("GTW", )
MOM.Entity.GTW = type ("GTW", (), dict (__module__ = MOM.Entity.__module__))

class HTTP_Opt (TFL.CAO._Spec_) :
    """Select HTTP server framework to use."""

    def __init__ (self, ** kw) :
        assert "name" not in kw
        kw ["name"] = "HTTP"
        if "description" not in kw :
            kw ["description"] = self.__class__.__doc__
        self.__super.__init__ (max_number = 1, ** kw)
    # end def __init__

    def cook (self, value, cao = None) :
        if not value :
            value = "Werkzeug"
        m = GTW._Import_Module ("_" + value)
        result = getattr (m, value)
        result._Import_Module ("Application")
        return result
    # end def cook

    def _set_default (self, default) :
        ### Make `Werkzeug` sticky
        self.__super._set_default (default or "Werkzeug")
    # end def _set_default

# end class HTTP_Opt

class _GTW_M_Scaffold_ (MOM.Scaffold.__class__) :

    @TFL.Meta.Once_Property
    def cmd__run_server (cls) :
        """Sub-command for running the application server"""
        return TFL.CAO.Cmd \
            ( name        = "run_server"
            , handler     = cls.__do_run_server
            , opts        = cls.cmd__run_server__opts
            )
    # end def cmd__run_server

    @TFL.Meta.Once_Property
    def cmd__wsgi (cls) :
        """Sub-command for running as wsgi application"""
        return TFL.CAO.Cmd \
            ( name        = "wsgi"
            , handler     = cls.__do_wsgi
            , opts        = cls.cmd__wsgi__opts
            )
    # end def cmd__run_server

    def __do_run_server (cls, cmd) :
        """Run as application server."""
        return cls.do_run_server (cmd)
    # end def __do_run_server

    def __do_wsgi (cls, cmd) :
        """Run as wsgi application."""
        return cls.do_wsgi (cmd)
    # end def __do_wsgi

# end class _GTW_M_Scaffold_

class _GTW_Scaffold_ (MOM.Scaffold) :

    __metaclass__         = _GTW_M_Scaffold_
    _real_name            = "Scaffold"
    _lists_to_combine     = MOM.Scaffold._lists_to_combine + \
        ( "cmd__run_server__opts"
        , "cmd__wsgi__opts"
        )

    ANS                   = GTW

    cmd___server__opts = \
        ( "auto_reload:B=yes?Autoload of werkzeug, only works with no sqlite db"
        , "Break:B?Enter debugger before starting tornado/werkzeug"
        , "-debug:B=no"
        , HTTP_Opt (default = "Tornado")
        , TFL.CAO.Opt.Input_Encoding
            ( default     = "iso-8859-15"
            , description = "Default encoding for source files"
            )
        , TFL.CAO.Opt.Output_Encoding
            ( default     = "utf-8"
            , description = "Default encoding for generated html"
            )
        , "port:I=8090?Server port"
        , "-smtp_server:S=localhost?SMTP server used to send emails"
        , "-template_file:S=html/static.jnj"
        , "-TEST:B"
        )
    cmd__run_server__opts = cmd___server__opts
    cmd__wsgi__opts       = cmd___server__opts
    cmd__shell__opts      = \
        ( "wsgi:B?Create the wsgi application before entering the shell"
        ,
        ) + cmd___server__opts
    cmd__sub_commands     = ("cmd__run_server", "cmd__wsgi")

    @classmethod
    def do_run_server (cls, cmd) :
        raise NotImplementedError
    # end def do_run_server

    @classmethod
    def do_shell (cls, cmd) :
        scope = cls.do_load      (cmd)
        if cmd.wsgi :
            wsgi = cls.do_wsgi   (cmd)
            top  = GTW.NAV.Root.top
        TFL.Environment.py_shell ()
    # end def do_shell

    @classmethod
    def do_wsgi (cls, cmd) :
        raise NotImplementedError
    # end def do_wsgi

Scaffold = _GTW_Scaffold_ # end class

if __name__ != "__main__" :
    GTW.OMP._Export ("*")
### __END__ GTW.OMP.Scaffold
