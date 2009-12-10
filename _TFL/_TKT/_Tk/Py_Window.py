# -*- coding: iso-8859-1 -*-
# Copyright (C) 2008-2009 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
#++
# Name
#    TFL.TKT.Tk.Py_Window
#
# Purpose
#    Python interaction window
#
# Revision Dates
#    21-Aug-2008 (CT) Creation (factored from lib/python/Py_Window)
#    10-Dec-2009 (CT) Adapted to change of `TFL.Context.attr_let`
#    ««revision-date»»···
#--

from   __future__         import with_statement

from   _TFL               import TFL

from   _TFL               import sos
from   _TFL._TKT._Tk.CTK  import *
from   _TFL.predicate     import *

import   _TFL.Environment
import   _TFL.import_module
import   _TFL.Py_Interpreter

import   code
import   sys
import   traceback

HIST_FILE = ".poweruser_history"
MAX_HIST  = 5000

class Py_Window (CTK.C_Frame) :
    """Widget providing interactive access to the Python interpreter."""

    widget_class = "Py_Window"

    def __init__ (self, master, controller, globals, locals, name = None) :
        self.cmd        = ""
        self.controller = controller
        self.locals     = locals
        self.globals    = globals
        self._history   = []
        self._histptr   = 0
        self._sizes     = (6, 8, 10, 14)
        self._cur_size  = 1
        globals ["os"]  = sos
        CTK.C_Frame.__init__ \
            ( self, master
            , class_    = self.widget_class
            , name      = name
            )
        btag = "%s_%d" % (self.widget_class, id (self))
        self.bind_class  (btag, "<Return>",     self.execute)
        self.bind_class  (btag, "<Alt-d>",      self.complete)
        self.bind_class  (btag, "<Alt-space>",  self.complete)
        self.bind_class  (btag, "<Alt-k>",      self.clear_line)
        self.bind_class  (btag, "<Alt-p>",      self.set_previous)
        self.bind_class  (btag, "<Up>",         self.set_previous)
        self.bind_class  (btag, "<Alt-n>",      self.set_next)
        self.bind_class  (btag, "<Down>",       self.set_next)
        self.bind_class  (btag, "<Alt-s>",      self.font_size)
        self.bind_class  (btag, "<Alt-c>",      self.clear_output)
        self.bind_class  (btag, "<Alt-o>",      self.clear_msg_window)
        self.bind_class  (btag, "<Alt-i>",      self.cookie)
        self.output = CTK.Message_Window  \
            ( self
            , name  = "output"
            , width = 80
            , fill  = BOTH
            )
        self.output.configure (height = 20 )
        self.output.txt_widget.configure \
            (font = ("Helvetica", self._sizes [self._cur_size]))
        self.input        = CTK.Editor_Entry \
            ( self
            , name        = "input"
            , label       = "Python code"
            , bindtag     = btag
            )
        self.buttons      = CTK.Buttongroup   ()
        self.comp_btn     = self.buttons.add \
            ( master      = self
            , button_name = "Complete"
            , command     = self.complete
            )
        self.size_btn     = self.buttons.add \
            ( master      = self
            , button_name = "FontSize"
            , command     = self.font_size
            )
        self.clr_btn      = self.buttons.add \
            ( master      = self
            , button_name = "ClearOutput"
            , command     = self.clear_all
            )
        self.output.pack   (fill = BOTH, expand = YES)
        self.input.pack    (fill = X)
        self.comp_btn.pack (side = LEFT)
        self.size_btn.pack (side = LEFT)
        self.clr_btn.pack  (side = LEFT)
        self.output.txt_widget.tag_configure ( "all",     lmargin1 = "1c")
        self.output.txt_widget.tag_configure ( "command", lmargin1 = 0)
        self.cookie       ()
        self.read_history ()
    # end def __init__

    def cookie (self, event = None) :
        try :
            cookie = sos.popen3 ("which fortune && fortune") [1].readlines ()
            if len (cookie) > 1 :
                for l in cookie [1:] :
                    self.output.put (l)
                self.output.put ("\n")
        except KeyboardInterrupt :
            raise
        except StandardError :
            pass
    # end def cookie

    def clear_all (self, event = None) :
        self.clear_line        ()
        self.clear_output      ()
        self.clear_msg_window  ()
    # def clear_all

    def clear_output (self, event = None) :
        self.output.clear ()
    # end def clear_output

    def clear_msg_window (self, event = None) :
        try :
            sys.stderr.out_widget.clear ()
        except KeyboardInterrupt :
            raise
        except StandardError :
            pass
    # end def clear_msg_window

    def font_size (self, event = None) :
        self._cur_size = (self._cur_size + 1) % len (self._sizes)
        self.output.txt_widget.configure \
            (font = ("Helvetica", self._sizes [self._cur_size]))
        self.input.entry.configure \
            (font = ("Helvetica", self._sizes [self._cur_size]))
        try :
            sys.stderr.out_widget.wtk_widget.configure \
                (font = ("Helvetica", self._sizes [self._cur_size]))
        except KeyboardInterrupt :
            raise
        except StandardError :
            pass
   # end def font_size

    def _set_from_history (self) :
        if self._history :
            cmd = self._history [self._histptr]
            self.input.set (cmd)
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
        self.input.set ("")
    # end def clear_line

    def complete (self, event = None) :
        line = self.input.get ()
        cmd, choices = TFL.complete_command (line, self.globals, self.locals)
        if choices :
            self.output.put (choices)
        if cmd :
            self.input.set  (cmd)
    # end def complete

    def execute (self, event = None) :
        """Execute command in `self.input'"""
        cmd = self.input.get ()
        if not self._history or cmd != self._history [-1] :
           self._history.append (cmd)
        self._histptr = len (self._history)
        if not cmd :
            return
        echo_cmd = cmd
        if cmd.startswith ("$") :
            cmd = cmd [1:].strip ()
            cmd = \
                ( "_last_shell_output = sos.popen ('%s').read (); "
                  "print _last_shell_output" % cmd
                )
        code = TFL.Pycode_Compiler (cmd)
        with TFL.Context.attr_let (sys, stdout = self.output) :
            self.output.put (echo_cmd + "\n", "command")
            try :
                code (self.globals, self.locals)
            except (SystemExit, KeyboardInterrupt) :
                raise
            except :
                    print "Exception during execution of", cmd
                    print traceback.print_exc ()
            self.input.set ("")
    # end def execute

    def destroy (self, * args, ** kw) :
        self.save_history ()
    # end def destroy

    def compacted_history (self) :
        _hist = [s.replace ("\n", "#<NL>") for s in self._history]
        hdict = dict ([(l, n) for (n, l) in enumerate (_hist)])
        slist = dusort (hdict.iteritems (), lambda (l, n) : n)
        return [l for (l, n) in slist] [(-MAX_HIST):]
    # end def compacted_history

    def read_history (self) :
        history   = self._history
        hist_file = sos.path.join (TFL.Environment.home_dir, HIST_FILE)
        try :
            with open (hist_file, "r") as f :
                for l in f.readlines () :
                    history.append (l [:-1].replace ("#<NL>", "\n"))
            self._histptr = len (history)
        except IOError :
            pass
    # end def read_history

    def save_history (self) :
        history   = self.compacted_history ()
        hist_file = sos.path.join (TFL.Environment.home_dir, HIST_FILE)
        try :
            with open (hist_file, "w") as f :
                for l in history :
                    f.write ("%s\n" % l)
        except IOError :
            pass
    # end def save_into_history

# end class Py_Window

if __name__ != "__main__" :
    TFL.TKT.Tk._Export ("Py_Window")
### __END__ TFL.TKT.Tk.Py_Window
