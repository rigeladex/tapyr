# -*- coding: iso-8859-15 -*-
# Copyright (C) 2005-2010 DI Christian Eder <eder@tttech.com>
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
#     9-Jun-2005 (CED) `locals` added to `__call__`
#    25-Jul-2005 (CT)  `__call__` fixed (`or {}` considered harmful)
#    25-Jul-2007 (PGO) Reduced not-invented-here-ness
#    ««revision-date»»···
#--

from   _TFL             import TFL
from   _TFL.predicate   import *

import rlcompleter

class Pycode_Compiler (object) :
    """A class to eval/exec python code lines."""

    def __init__ (self, s) :
        lines = s.split ("\n")
        if len (lines) <= 1 :
            self.src = s
        else :
            self.src  = "\n".join (lines) + "\n"
        try :
            self.code     = compile (self.src, "<stdin>", "eval")
            self.can_eval = True
        except SyntaxError :
            self.code     = compile (self.src, "<stdin>", "exec")
            self.can_eval = False
    # end def __init__

    def __call__ (self, glob_dct, loc_dct = None) :
        if loc_dct is None :
            loc_dct = {}
        if self.can_eval :
            print eval (self.code, glob_dct, loc_dct)
        else :
            exec self.code in glob_dct, loc_dct
    # end def __call__

# end class Pycode_Compiler

def complete_command (line, glob_dct, loc_dct = None) :
    prefix, space, line = line.rpartition       (" ")
    d                   = dict (glob_dct)
    d.update (loc_dct or {})
    c                   = rlcompleter.Completer (d)
    try :
        c.complete (line, 0)
    except StandardError :
        return None, None
    match = "".join ((prefix, space, common_head (c.matches)))
    cands = ", ".join (sorted (s.split (".") [-1] for s in set (c.matches)))
    return match, ("%s\n\n" % cands if cands else "")
# end def complete_command

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ Py_Interpreter
