# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
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
#    ««revision-date»»···
#--

from   _GTW                   import GTW
from   _MOM                   import MOM
from   _TFL                   import TFL

import _MOM.Scaffold

import _TFL.CAO
import _TFL._Meta.Once_Property

class _GTW_M_Scaffold_ (MOM.Scaffold.__class__) :

    @TFL.Meta.Once_Property
    def cmd__run_server (cls) :
        """Sub-command for running the application server"""
        return TFL.CAO.Cmd \
            ( name        = "run_server"
            , description = "Run the application server."
            , handler     = cls.__do_run_server
            , opts        = cls.cmd__run_server__opts
            )
    # end def cmd__run_server

    def __do_run_server (cls, cmd) :
        """Handler for sub-command `run_server`."""
        cls.do_run_server (cmd)
    # end def __do_run_server

# end class _GTW_M_Scaffold_

class _GTW_Scaffold_ (MOM.Scaffold) :

    __metaclass__         = _GTW_M_Scaffold_
    _real_name            = "Scaffold"
    _lists_to_combine     = MOM.Scaffold._lists_to_combine + \
        ( "cmd__run_server__opts"
        ,
        )

    ANS                   = GTW

    cmd__run_server__opts = \
        ( "Break:B?Enter debugger before starting tornado/werkzeug"
        , "-copyright_start:I=2010"
        , "-debug:B=yes"
        , TFL.CAO.Opt.Output_Encoding
            ( default     = "utf-8"
            , description = "Default encoding for generated html"
            )
        , TFL.CAO.Opt.Input_Encoding
            ( default     = "iso-8859-15"
            , description = "Default encoding for source files"
            )
        , "-template_file:S=static.html"
        , "werkzeug:B?Run the application with the werkzeug server"
        , "auto_reload:B=yes=Autoload of werkzeug, only works with no sqlite db"
        , "-TEST:B"
        )
    cmd__sub_commands     = ("cmd__run_server", )

    @classmethod
    def do_run_server (cls, cmd) :
        raise NotImplementedError
    # end def do_run_server

Scaffold = _GTW_Scaffold_ # end class

if __name__ != "__main__" :
    GTW.OMP._Export ("*")
### __END__ GTW.OMP.Scaffold
