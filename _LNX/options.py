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
#    LNX.options
#
# Purpose
#    Split options and arguments
#
# Revision Dates
#    17-May-2011 (CT) Creation
#    22-Mar-2018 (CT) Make Python-3 compatible
#    ««revision-date»»···
#--

from   _LNX           import LNX
from   _TFL           import TFL

from   _TFL.predicate import dusplit

import sys

def split (argv) :
    try :
        eoo = argv.index ("--")
    except ValueError :
        args, opts = dusplit (argv, lambda x : x.startswith ("-"), 2)
    else :
        opts = argv [:eoo]
        args = argv [eoo + 1:]
    return opts, args
# end def split

def _Command () :
    opts, args = split (sys.argv [1:])
    print (" ".join (opts))
# end def _Command

if __name__ != "__main__" :
    LNX._Export_Module ()
if __name__ == "__main__" :
    _Command ()
### __END__ LNX.options
