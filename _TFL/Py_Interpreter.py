# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 DI Christian Eder
# eder@tttech.com
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
#    Py_Interpreter
#
# Purpose
#    Provides classes and functions to access the python interpreter
#
# Revision Dates
#     8-Mar-2005 (CED) Creation (moved multiple implemented stuff into here)
#    ««revision-date»»···
#--
#

from _TFL        import TFL
from predicate   import *

class Pycode_Compiler (object) :
    """A class to eval/exec python code lines."""

    def __init__ (self, str) :
        lines = str.split ("\n")
        if len (lines) <= 1 :
            self.src = str
        else :
            self.src  = "\n".join (lines) + "\n"
        try :
            self.code     = compile (self.src, "<stdin>", "eval")
            self.can_eval = True
        except SyntaxError :
            self.code     = compile (self.src, "<stdin>", "exec")
            self.can_eval = False
    # end def __init__

    def __call__ (self, globals) :
        if self.can_eval :
            print eval (self.code, globals)
        else :
            exec self.code in globals
    # end def __call__

# end class Pycode_Compiler

def complete_command (line, globals) :
    ### XXX beautify and refactor me
    base_obj  = None
    start     = line.split (" ")
    if len (start) > 1 :
        line  = start [-1]
        start = " ".join (start [:-1])
    else :
        start = ""
    tail = line.split (".")[-1]
    base = ".".join (line.split (".")[:-1])
    try :
        if base :
           base_obj = eval (base, globals)
        if base_obj :
           list  = [s for s in dir (base_obj) if s.startswith (tail)]
           mc = getattr (base_obj, "__metaclass__", None)
           if mc :
              list += [s for s in dir (mc) if s.startswith (tail)]
        else :
           list = [s for s in globals.keys () if s.startswith (tail)]
    except (NameError, AttributeError, SyntaxError) :
        list = []
    if not list :
        return None, None
    longest_match = common_head (list)
    if base :
        base += "."
    line = base + longest_match
    choices = ""
    if len (list) > 1 :
        choices = "%s\n\n" % (", ".join (list))
    if start :
        line = start + " " + line
    return (line, choices)
# end def complete_command

if __name__ != "__main__" :
    TFL._Export ("*")

### __END__ Py_Interpreter


