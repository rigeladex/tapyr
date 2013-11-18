# -*- coding: utf-8 -*-
# Copyright (C) 2011-2013 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# #*** <License> ************************************************************#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    run_single_doctest
#
# Purpose
#    Run a single doc test from the specified module
#
# Revision Dates
#    25-Jul-2011 (MG) Creation
#    28-Mar-2013 (CT) Add `-summary` to be more compatible with `run_doctest`
#     7-Aug-2013 (CT) Add `cases` (adapt to change of `run_doctest`)
#    ««revision-date»»···
#--

from   __future__   import unicode_literals
from   _TFL         import TFL
import _TFL.CAO
from   _TFL.Regexp  import *
import _TFL.sos     as     os
from    run_doctest import format_x, format_f, format_s
import  new
import  sys
import  doctest

def _main (cmd) :
    cmd_path              = list (cmd.path or [])
    replacer              = Re_Replacer (r"\.py[co]", ".py")
    a                     = cmd.argv [0]
    et                    = ""
    if not os.path.isfile (cmd.module) :
        raise ValueError ("Module %s not found" % (cmd.module, ))
    f                     = TFL.Filename (cmd.module)
    m                     = f.base
    sys.path [0:0]        = cmd_path
    if f.directory :
        sys.path [0:0]    = [f.directory]
    elif not cmd_path :
       sys.path [0:0]     = ["./"]
    if cmd.nodiff :
        flags             = doctest.NORMALIZE_WHITESPACE
    else :
        flags             = doctest.NORMALIZE_WHITESPACE | doctest.REPORT_NDIFF
    try :
        module            = __import__ (m)
        tests             = set (cmd.argv [1:])
        for tn in getattr (module, "__test__", {}).keys () :
            if tn not in tests :
                del module.__test__ [tn]
        f, t              = doctest.testmod \
            ( module
            , verbose     = cmd.verbose
            , optionflags = flags
            )
    except KeyboardInterrupt :
        raise
    except StandardError, exc :
        print >> sys.stderr, format_x % (replacer (a), exc, et)
        raise
    else :
        cases  = int (bool (t))
        format = format_f if f else format_s
        print >> sys.stderr, replacer (format % TFL.Caller.Scope ())
# end def _main

_Command = TFL.CAO.Cmd \
    ( handler      = _main
    , args         =
          ( "module:P?Module to test"
          , "test_name:S?Name of test(s) of the module"
          )
    , opts         =
        ( "nodiff:B?Don't specify doctest.REPORT_NDIFF flag"
        , "path:P:?Path to add to sys.path"
        , "summary:B?Just for compatibility with `run_doctest`"
        , "timing:B?Add timing information"
        , "verbose:B?Turn verbosity on"
        )
    , min_args     = 1
    , put_keywords = True
    )

if __name__ == "__main__" :
    _Command ()
### __END__ run_single_doctest
