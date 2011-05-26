# -*- coding: iso-8859-15 -*-
# Copyright (C) 2011 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
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
#    ««revision-date»»···
#--

from   __future__  import unicode_literals

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
    print " ".join (opts)
# end def _Command

if __name__ != "__main__" :
    LNX._Export_Module ()
if __name__ == "__main__" :
    _Command ()
### __END__ LNX.options
