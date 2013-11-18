# -*- coding: utf-8 -*-
# Copyright (C) 2008-2013 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
#++
# Name
#    TFL.UI.Starter
#
# Purpose
#    Provide starter class for TFL applications
#
# Revision Dates
#    19-Aug-2008 (CT) Creation (factored from TTA.UI.Starter)
#    20-Aug-2008 (CT) Creation finished
#    28-Aug-2008 (CT) `-logfile` and `-unique_logfile` added
#    10-Sep-2008 (CT) Guard added to `_do_import` (not every `PNS` needs to
#                     actually exist [provided the existing ones define
#                     everything necessary])
#    19-Nov-2008 (CT) `hide` added to option `-batch`
#    23-May-2013 (CT) Use `TFL.Meta.BaM` for Python-3 compatibility
#    ««revision-date»»···
#--

from   __future__             import with_statement

from   _TFL                   import TFL
from   _TFL._Meta             import Meta

import _TFL._Meta.M_Auto_Combine
import _TFL._UI.Application
import _TFL._UI.App_Context
import _TFL._UI.Mixin
import _TFL.Environment

from   _TFL.Command_Line      import Command_Line, Opt, Arg

import sys
import traceback

class _TFL_UI_Starter_ (Meta.BaM (UI.Mixin, metaclass = Meta.M_Auto_Combine)) :
    """Starter class for TFL applications."""

    _real_name           = "Starter"
    _lists_to_combine    = ("Args", "Opts")
    _gui_toolkit_name    = "Tk"

    cmd_description      = ""
    min_args             = 0
    max_args             = 1
    product_name         = "TFL" ### override
    process_keywords     = True
    Args                 = []
    Opts                 = \
        [ Opt
            ("batch"
            , type        = "B"
            , description =
                """Runs the tool in batch mode without any GUI. This option has
                   the same effect as starting the `_batch.exe` version of the
                   tool directly.
                """
            , hide        = True
            )
        , "-commands:S,?"
            """Command(s) to be executed after startup.

               To execute several commands in a row, they must be separated
               by commas, without any spaces, as described for -prescripts.
            """
        , "-logfile:S?"
            """Name of a file to log all output into."""
        , "-prescripts:S,?"
            """Script(s) to be run before any files are loaded (in interactive
               mode, this is the place to add script categories to
               the menus). To run several scripts in a row, they must be
               separated by commas, without any spaces, i.e.,
               -prescripts script1.py,script2.py. Else the tool will interpret
               the second script as input argument and fail.
            """
        , "-scripts:S,?"
            """Script(s) to be run after input files were loaded, if any were
               specified. The same rules apply as for -prescripts.
            """
        , "-unique_logfile:B?"
            """Append date, time, and user to value specified by `-logfile`."""
        , "-verbose:I?"
            """Higher levels of verbosity generate more detailed output.
               Note, however, that this may cause a loss in performance,
               especially for large volumes of output.
            """
        , "-Version?"
            """Shows information about the product version. In interactive
               mode, this information can also be obtained by selecting
               `About` from the `Help` menu.
            """
        , Opt ( "__plugins", "T", auto_split = ",")
        ]

    def __init__ (self, ANS, cmd, start_mainloop = True) :
        self.__super.__init__   (TFL.UI.App_Context (ANS))
        self._do_imports        (cmd)
        self._protected_start   (cmd)
        if start_mainloop :
            self.start_mainloop (cmd)
    # end def __init__

    @classmethod
    def command_spec (cls, arg_array = None) :
        return Command_Line \
            ( option_spec      = cls.Opts
            , arg_spec         = cls.Args
            , description      = cls.cmd_description
            , min_args         = cls.min_args
            , max_args         = cls.max_args
            , process_keywords = cls.process_keywords
            , arg_array        = arg_array
            )
    # end def command_spec

    @classmethod
    def implicit_imports (cls, ANS, * TNS_names) :
        for pkg in ["_TKT._%s" % (n, ) for n in TNS_names] + ["_UI"] :
            for P, m in cls._implicit_imports (ANS, pkg) :
                yield P, m
    # end def implicit_imports

    def start_mainloop (self, cmd) :
        app = self.app
        try :
            app.start_mainloop ()
            raise SystemExit
        except SystemExit :
            raise
    # end def start_mainloop

    def _do_import (self, PNS, module) :
        try :
            m = PNS._Import_Module (module)
        except ImportError :
            return {}
        else :
            return m.__dict__
    # end def _do_import

    def _do_imports (self, cmd) :
        ANS = self.ANS
        self._globals = _g = {}
        if cmd.batch or "_batch" in TFL.Environment.script_name ().lower () :
            cmd.batch = True
            TNS_name  = "Batch"
        else :
            TNS_name = self._gui_toolkit_name
        for PNS, module in self.implicit_imports (ANS, TNS_name) :
            _g.update (self._do_import (PNS, module))
    # end def _do_imports

    @classmethod
    def _implicit_imports (cls, ANS, pkg) :
        yield ANS, pkg
        yield ANS, "%s.Application" % (pkg, )
    # end def _implicit_imports

    def _protected_start (self, cmd) :
        try :
            self.app = self._start (cmd)
        except KeyboardInterrupt :
            raise
        except :
            appl_name = self.product_name
            def show_error (self, file = sys.__stderr__) :
                file.write \
                    ( ("Exception during startup -- %s's "
                       "installation might be corrupted\n"
                      )
                    % appl_name
                    )
                traceback.print_exc (file = file)
            try :
                show_error (self)
            except (SystemExit, KeyboardInterrupt) :
                raise
            except :
                pass
            try :
                with open ("%s.errors" % appl_name, "w") as file :
                    show_error (self, file)
                    file.flush ()
            except (SystemExit, KeyboardInterrupt) :
                raise
            except :
                pass
            raise SystemExit, 9999
    # end def _protected_start

    def _start (self, cmd) :
        result = TFL.UI.Application.root = self._ui_application (cmd)
        return result
    # end def _start

    def _ui_application (self, cmd) :
        return self.ANS.UI.Application (self.AC, cmd, self._globals)
    # end def _ui_application

Starter = _TFL_UI_Starter_ # end class

if __name__ != "__main__" :
    TFL.UI._Export ("*")
### __END__ TFL.UI.Starter
