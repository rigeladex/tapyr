# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package TFL.
#
# This module is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    TFL.relative_to_search_path
#
# Purpose
#    Convert an absolute path to a path relative to one of the elements of a
#    search path, if possible
#
# Revision Dates
#    25-Jan-2010 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL import TFL
from   _TFL import sos

import _TFL._Meta.Object
import _TFL.CAO

import sys

class Relative_To_Search_Path (TFL.Meta.Object) :
    """Return `abs_path` as path relative to one of the elements in
       `search_path`, if possible.
    """

    if sos.path.altsep :
        seps = (sos.path.sep, sos.path.altsep)
    else :
        seps = (sos.path.sep, )

    def __init__ (self, search_path) :
        self.search_path = list \
            (p for p in (self._normalized (p) for p in search_path) if p)
    # end def __init__

    def __call__ (self, abs_path) :
        p = self._normalized (abs_path)
        if sos.path.isabs (abs_path) :
            for sp in self.search_path :
                if p.startswith (sp) :
                    result = p [len (sp):]
                    for s in self.seps :
                        result = result.lstrip (s)
                    return result
        return abs_path
    # end def __call__

    def _normalized (self, p) :
        path = sos.path
        return path.realpath (path.normpath (path.normcase (p)))
    # end def _normalized

# end class Relative_To_Search_Path

def relative_to_search_path (search_path, abs_path) :
    """Return `abs_path` as path relative to one of the elements in
       `search_path`, if possible.
    """
    return Relative_To_Search_Path (search_path) (abs_path)
# end def relative_to_search_path

relative_to_python_path = Relative_To_Search_Path \
    (sos.environ.get ("PYTHONPATH").split (sos.path.pathsep) or sys.path)

def _main (cmd) :
    rtsp = Relative_To_Search_Path (cmd.search_path)
    print cmd.Sep.join (rtsp (p) for p in cmd.argv)
# end def _main

_Command = TFL.CAO.Cmd \
    ( handler     = _main
    , args        =
        ( "path:P?Path(es) to convert to relative to `search_path`"
        ,
        )
    , opts        =
        ( "-search_path:P:?Search path"
        , "-Sep:S=\n?Separator between pathes printed to stdout"
        )
    , description =
        "Convert absolute pathes to pathes relative to one of the "
        "elements of a search path, if possible"
    )

if __name__ != "__main__" :
    TFL._Export ("*")
else :
    _Command ()
### __END__ TFL.relative_to_search_path
