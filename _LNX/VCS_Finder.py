# -*- coding: utf-8 -*-
# Copyright (C) 2011-2018 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************
# This module is part of the package LNX.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    LNX.VCS_Finder
#
# Purpose
#    Find repositories in directories/links specified as arguments
#
# Revision Dates
#    13-May-2011 (CT) Creation
#    17-May-2011 (CT) Use `LNX.options.split`
#    22-Mar-2018 (CT) Make Python-3 compatible
#    ««revision-date»»···
#--

from   __future__     import absolute_import
from   __future__     import division
from   __future__     import print_function
from   __future__     import unicode_literals

from   _LNX           import LNX
from   _TFL           import TFL

from   _TFL           import sos
from   _TFL.predicate import dusplit

import _LNX.options
import _LNX.VCS_Typer
import sys

path    = sos.path

def gen (pref, dols, pred) :
    for d in dols :
        dol = path.join (pref, d) if pref else d
        if path.islink (dol) :
            dol = path.realpath (dol)
        if path.isdir (dol) :
            if pred (dol) :
                yield d
            elif path.exists (path.join (dol, ".VX")):
                for r in gen (dol, sos.listdir (dol), pred) :
                    yield path.join (d, r)
# end def gen

def _Command () :
    result     = set ()
    add        = result.update
    opts, args = LNX.options.split (sys.argv [1:])
    for a in args :
        for dol in sos.expanded_glob (a) :
            add (gen ("", [dol], LNX.vcs_typer))
    print ("\n".join (sorted (result)))
# end def _main

if __name__ != "__main__" :
    LNX._Export_Module ()
if __name__ == "__main__" :
    _Command ()
### __END__ LNX.VCS_Finder
