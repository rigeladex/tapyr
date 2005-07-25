# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. office@spannberg.com
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
#    TGL.TKT.GTK.Interpreter_Window
#
# Purpose
#    A toplevel which allows the execution of python code
#
# Revision Dates
#    21-May-2005 (MG) Creation
#    25-Jul-2005 (CT) `locals` added
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
from   _TFL                   import TFL
import _TFL.import_module
import _TFL.Py_Interpreter
import _TGL._TKT._GTK.Window
import _TGL._TKT._GTK.Signal
import _TGL._TKT._GTK.V_Box
import _TGL._TKT._GTK.H_Box
import _TGL._TKT._GTK.Combo_Box_Entry
import _TGL._TKT._GTK.Label
import _TGL._TKT._GTK.Model
import _TGL._TKT._GTK.Message_Window
import  sys
import  traceback
import _TGL._UI
import _TGL._UI.Style
from   _TFL.predicate   import dusort
import _TFL.Environment as     Environment
import _TFL.sos         as sos

HIST_FILE = ".poweruser_history"
MAX_HIST  = 5000

class Interpreter_Window (GTK.Window) :
    """Widget providing interactive access to the Python interpreter."""

    complete_key = GTK.Key_Binder ("<Alt>d")

    def __init__ (self, master, global_dict = None, AC = None, ** kw) :
        self.__super.__init__ (AC = AC, ** kw)
        TNS            = self.TNS
        Signal         = TNS.Signal
        Style          = self.ANS.UI.Style
        self.cmd_style = Style \
            ("cmd",   foreground = "blue", lmargin1 = 10, lmargin2 = 0)
        self.err_style = Style ("error", foreground = "red")
        self.com_style = Style ("error", foreground = "gray")
        normal         = Style ("normal", wrap      = "word")
        if global_dict is None :
            global_dict = globals ().copy ()
            global_dict.update    (vars ())
        self.globals  = global_dict
        self.locals   = {}
        self._history = []
        self._histptr = 0
        self.vbox     = TNS.V_Box           (AC = AC)
        self.hbox     = TNS.H_Box           (AC = AC)
        self.label    = TNS.Label           ("Python code", AC = AC)
        self.entry    = TNS.Combo_Box_Entry (AC = AC)
        self.output   = TNS.Message_Window  (name = "py_putput", AC = AC)
        self.vbox.pack (self.output, expand = True,  fill = True)
        self.vbox.pack (self.hbox,   expand = False, fill = True)
        self.hbox.pack (self.label,  expand = False, fill = True)
        self.hbox.pack (self.entry,  expand = True,  fill = True)
        for w in self.hbox, self.vbox, self.entry, self.label, self.output :
            w.show ()
        self.add (self.vbox)
        self.entry.focus_on_click = False
        real_entry = self.entry.wtk_object.child
        real_entry.connect        ("activate", self.execute)
        real_entry.set_data       ("ktw_object", self)
        self.bind_add             (Signal.Destroy, self.destroy)
        self.complete_key.connect (real_entry, self.complete, (), {})
        self.output.apply_style   (normal)
        self.read_history         ()
    # end def __init__

    def clear_output (self, event = None) :
        self.output.clear ()
    # end def clear_output

    def clear_msg_window (self, event = None) :
        try :
            sys.stderr.out_widget.clear ()
        except :
            pass
    # end def clear_msg_window

    def _set_from_history (self) :
        if self._history :
            cmd = self._history [self._histptr]
            self.entry.set (cmd)
    # end def _set_from_history

    def set_previous (self, event = None) :
        self._histptr -= 1
        if self._histptr < 0 :
            self._histptr = 0
        self._set_from_history ()
    # end def set_previous

    def set_next (self, event = None) :
        self._histptr += 1
        if self._histptr >= len (self._history) :
            self._histptr = len (self._history) - 1
        self._set_from_history ()
    # end def set_next

    def clear_line (self, event = None) :
        self.entry.set ("")
    # end def clear_line

    def complete (self, event = None) :
        line = self.entry.get ()
        cmd, choices = TFL.complete_command (line, self.globals)
        if choices :
            self.output.put (choices, self.com_style)
        if cmd :
            self.entry.set  (cmd)
    # end def complete

    def execute (self, event = None) :
        """Execute command in `self.entry'"""
        cmd = self.entry.get ()
        if not cmd : return
        if not self._history or cmd != self._history [-1] :
           self._history.append   (cmd)
           self.entry.append_text (cmd)
        self._histptr = len (self._history)
        stdout = sys.stdout
        try :
            echo_cmd = cmd
            if cmd.startswith ("$") :
                cmd = cmd [1:].strip ()
                cmd = \
                    ( "_last_shell_output = sos.popen ('%s').read (); "
                      "print _last_shell_output" % cmd
                    )
            obj        = TFL.Pycode_Compiler (cmd)
            sys.stdout = self.output
            self.output.put (echo_cmd + "\n", self.cmd_style)
            try :
                obj (self.globals, self.locals)
            except (SystemExit, KeyboardInterrupt), exc :
                raise
            except :
                self.output.push_style (self.err_style)
                print "Exception during execution of %s" % (cmd, )
                traceback.print_exc   ()
                self.output.pop_style ()
            self.entry.set  ("")
            self.output.see ()
        finally :
            sys.stdout = stdout
    # end def execute

    def destroy (self, * args, ** kw) :
        self.save_history       ()
    # end def destroy

    def compacted_history (self) :
        _hist = [s.replace ("\n", "#<NL>") for s in self._history]
        hdict = dict ([(l, n) for (n, l) in enumerate (_hist)])
        slist = dusort (hdict.iteritems (), lambda (l, n) : n)
        return [l for (l, n) in slist] [(-MAX_HIST):]
    # end def compacted_history

    def read_history (self) :
        try :
            hist_file = sos.path.join (Environment.home_dir, HIST_FILE)
            inf       = open (hist_file, "r")
            for l in inf.readlines () :
                cmd = l [:-1].replace  ("#<NL>", "\n")
                self._history.append   (cmd)
                self.entry.append_text (cmd)
            self._histptr  = len (self._history)
            inf.close ()
        except IOError :
            pass
    # end def read_history

    def save_history (self) :
        history = self.compacted_history ()
        try :
           hist_file = sos.path.join (Environment.home_dir, HIST_FILE)
           outf      = open (hist_file, "w")
           for l in history :
               outf.write ("%s\n" % l)
           outf.close ()
        except IOError :
            pass
    # end def save_into_history

# end class Interpreter_Window

if __name__ != "__main__" :
    GTK._Export ("Interpreter_Window")
else :
    from _TGL import TGL
    from   _TGL._UI.App_Context   import App_Context
    AC  = App_Context     (TGL)

    w = Interpreter_Window (global_dict = globals (), AC = AC)
    w.show                 ()
    GTK.main               ()
### __END__ TGL.TKT.GTK.Interpreter_Window


