# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.cluster
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
#    PMA.UI.Starter
#
# Purpose
#    Provide starter class for PMA
#
# Revision Dates
#    20-May-2005 (CT) Creation
#    21-May-2005 (MG) `batch` command line option replaced by `interface`
#     3-Jun-2005 (MG) `max_args` set to `0`
#    ««revision-date»»···
#--

from   _TFL                   import TFL
from   _PMA                   import PMA

import _TFL._Meta.M_Auto_Combine
import _TFL._UI.App_Context

import _PMA._UI
import _PMA._UI.App_Context
import _PMA._UI.Application
import _PMA._UI.Mixin

from   _TFL.Command_Line      import Command_Line, Opt, Arg
from   _TFL.Filename          import Filename

import _TFL.Environment
import _TFL.Abbr_Key_Dict

import sys
import traceback

class Starter (PMA.UI.Mixin) :
    """Starter class for PMA"""

    __metaclass__        = TFL.Meta.M_Auto_Combine
    _lists_to_combine    = ("Args", "Opts")
    toolkits             = TFL.Abbr_Key_Dict \
        ( Batch = "Batch", GTK = "GTK", Tk = "Tk")
    cmd_description      = ""
    min_args             = 0
    max_args             = 0
    process_keywords     = True
    Opts                 = \
        [ "-interface:S=Tk?Run the tool using this toolkit for the GUI"
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
        self.__super.__init__   (PMA.UI.App_Context (ANS))
        if cmd.Version :
            pass ### print ANS.Version.product_info ()
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
            yield PMA, "%s.Application" % (pkg, )
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
            raise SystemExit, 9999
    # end def _protected_start

    def _start (self, cmd) :
        return self.ANS.UI.Application (self.AC, cmd, self._globals)
    # end def _start

# end class Starter

if __name__ != "__main__" :
    PMA.UI._Export ("*")
### __END__ PMA.UI.Starter
