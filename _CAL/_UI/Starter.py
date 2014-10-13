# -*- coding: utf-8 -*-
# Copyright (C) 2005-2014 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    CAL.UI.Starter
#
# Purpose
#    Provide starter class for CAL
#
# Revision Dates
#    20-May-2005 (CT) Creation
#    21-May-2005 (MG) `batch` command line option replaced by `interface`
#     3-Jun-2005 (MG) `max_args` set to `0`
#    ««revision-date»»···
#--

from   __future__             import print_function

from   _TFL                   import TFL
from   _CAL                   import CAL

import _TFL._Meta.M_Auto_Combine
import _TFL._UI.App_Context

import _CAL._UI
import _CAL._UI.App_Context
import _CAL._UI.Application
import _CAL._UI.Mixin

from   _TFL.Command_Line      import Command_Line, Opt, Arg
from   _TFL.Filename          import Filename

import _TFL.Abbr_Key_Dict
import _TFL.Environment

import sys
import traceback

class Starter (CAL.UI.Mixin) :
    """Starter class for CAL"""

    __metaclass__        = TFL.Meta.M_Auto_Combine
    _lists_to_combine    = ("Args", "Opts")
    toolkits             = TFL.Abbr_Key_Dict \
        ( Batch = "Batch", GTK = "GTK", Tk = "Tk")
    cmd_description      = ""
    min_args             = 0
    max_args             = 0
    process_keywords     = True
    Opts                 = \
        [ "-interface:S=GTK?Run the tool using this toolkit for the GUI"
        , "-commands:S,?"
            """Command(s) to run after mailboxes are loaded."""
        , "-prescripts:S,?"
            """Script(s) to be run before mailboxes are loaded. To run
               several scripts in a row, they must be separated by commas,
               i.e., -prescript script1.py,script2.py.
            """
        , "-scripts:S,?"
            """Script(s) to run after mailboxes are loaded.
               The same rules apply as for -prescripts.
            """
        , "-verbose:I?"
            "Higher levels of verbosity generate more detailed output."
        , "-Version?Show information about product version."
        ]

    def __init__ (self, ANS, cmd, start_mainloop = True) :
        self.__super.__init__   (CAL.UI.App_Context (ANS))
        if cmd.Version :
            pass ### print (ANS.Version.product_info ())
        self._do_imports        (cmd)
        self._protected_start   (cmd)
        if start_mainloop :
            self.start_mainloop (cmd)
    # end def __init__

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
    command_spec = classmethod (command_spec)

    def implicit_imports (cls, ANS, * TNS_names) :
        for pkg in ["_TKT._%s" % (n, ) for n in TNS_names] + ["_UI"] :
            yield CAL, "%s.Application" % (pkg, )
            yield ANS, pkg
            yield ANS, "%s.Application" % (pkg, )
    implicit_imports = classmethod (implicit_imports)

    def start_mainloop (self, cmd) :
        app = self.app
        app.start_mainloop ()
        raise SystemExit
    # end def start_mainloop

    def _do_import (self, PNS, module) :
        m = PNS._Import_Module (module)
        return m.__dict__
    # end def _do_import

    def _do_imports (self, cmd) :
        ANS           = self.ANS
        self._globals = _g = {}
        TNS_name      = self.toolkits [cmd.interface]
        cmd.batch     = \
            ( TNS_name == "Batch"
            or "_batch" in TFL.Environment.script_name ().lower ()
            )
        for PNS, module in self.implicit_imports (ANS, TNS_name) :
            _g.update (self._do_import (PNS, module))
    # end def _do_imports

    def _protected_start (self, cmd) :
        try :
            app = self.app = self._start  (cmd)
        except KeyboardInterrupt :
            raise
        except :
            ANS       = self.ANS
            appl_name = ANS.__name__
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
                file      = open ("%s.errors" % appl_name, "w")
                show_error  (self, file)
                file.flush  ()
                file.close  ()
            except (SystemExit, KeyboardInterrupt) :
                raise
            except :
                pass
            raise SystemExit (9999)
    # end def _protected_start

    def _start (self, cmd) :
        return self.ANS.UI.Application (self.AC, cmd, self._globals)
    # end def _start

# end class Starter

if __name__ != "__main__" :
    CAL.UI._Export ("*")
### __END__ CAL.UI.Starter
