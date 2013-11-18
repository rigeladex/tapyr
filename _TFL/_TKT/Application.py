# -*- coding: utf-8 -*-
# Copyright (C) 2005-2008 Mag. Christian Tanzer. All rights reserved
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
#    TFL.TKT.Application
#
# Purpose
#    Generic base class for toolkit-specific functionality
#
# Revision Dates
#    13-Aug-2008 (CT) Creation (factored from TTA.TKT.Application)
#    27-Aug-2008 (CT) `_setup_stdout_redirect` changed to use `TFL.Output`
#    28-Aug-2008 (CT) `_logfile` added
#    ««revision-date»»···
#--

from   _TFL               import TFL

import _TFL._TKT.Mixin
import _TFL.Output

class _TFL_TKT_Application_ (TFL.TKT.Mixin) :

    _real_name             = "Application"

    cmd                    = property (lambda s : s.model.cmd)
    verbose                = property (lambda s : s.model.verbose)

    edit_interfacers       = ("mb", )

    standard_option_files  = ()
    option_files           = ()

    _logfile               = None

    def __init__ (self, model, ** kw) :
        self.__super.__init__ (model.AC, ** kw)
        self.gauge     = model.AC.ui_state.gauge   = None
        self.message   = model.AC.ui_state.message = None
        self.model     = model
        self.stdout    = None
        self.rn_viewer = None
        self.State     = model.State
    # end def __init__

    def echo (self, * msg, ** kw) :
        verbose = kw.get ("verbose", self.default_verbosity)
        if self.verbose >= verbose :
            for m in msg :
                print m,
            if msg :
                print
    # end def echo

    def _del_rel_notes (self, event = None) :
        if self.rn_viewer :
            self.rn_viewer.destroy ()
        self.rn_viewer = None
    # end def _del_rel_notes

    def _destroy (self) :
        if self.stdout :
            self.stdout.destroy ()
            self.stdout = None
        if self._logfile :
            self._logfile.close ()
            self._logfile = None
    # end def _destroy

    def _kill_interact (self, event = None) :
        model = self.model
        if model.ipreter :
            model.ipreter.destroy ()
            model.ipreter = None
    # end def _kill_interact

    def _read_option_files (self) :
        pass
    # end def _read_option_files

    def _setup_clipboard (self) :
        self.clipboard = self.AC.ui_state.clipboard = self.ANS.UI.Clipboard \
            (AC = self.AC)
    # end def _setup_clipboard

    def _setup_event_binder (self) :
        return {}
    # end def _setup_event_binder

    def _setup_stdout_redirect (self) :
        streams = [self.TNS.Queued_Stdout (self.message)]
        lf = self.model._logfile_name ()
        if lf :
            self._logfile = open (lf, "w", 0)
            streams.append (self._logfile)
        self.stdout = TFL.Output.Redirect_Std \
            (TFL.Output.Tee (* streams), redirects = ("stdout", "stderr"))
        if lf :
            print "Logging to ", lf
        ### Allow the interactive interpreter to clear the message window
        self.stdout.out_widget = self.message
    # end def _setup_stdout_redirect

    def _synchronize_gui (self) :
        pass
    # end def _synchronize_gui

    def _write_bug_info (self, file) :
        if self.message :
            sep   = "\n" + ("-" * 79) + "\n"
            write = file.write
            write (sep)
            write ("Contents of message window")
            write (sep)
            write (self.message.get ())
            write ("\n")
    # end def _write_bug_info

Application = _TFL_TKT_Application_ # end class

if __name__ != "__main__" :
    TFL.TKT._Export ("Application")
### __END__ TFL.TKT.Application
