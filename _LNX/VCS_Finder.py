# -*- coding: iso-8859-1 -*-
# Copyright (C) 2011 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This script is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this script. If not, see <http://www.gnu.org/licenses/>.
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
#    ««revision-date»»···
#--

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
    print "\n".join (sorted (result))
# end def _main

if __name__ != "__main__" :
    LNX._Export_Module ()
if __name__ == "__main__" :
    _Command ()
### __END__ LNX.VCS_Finder
