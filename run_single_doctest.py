# -*- coding: utf-8 -*-
# Copyright (C) 2011-2020 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# #*** <License> ************************************************************#
# This program is licensed under the terms of the BSD 3-Clause License
# <https://www.gg32.com/license/bsd_3c.html>.
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
#    21-Oct-2015 (CT) Add `py_version`, adapt to Python 3
#    21-Jun-2016 (CT) Add `expect_except` to `module` before testing
#    17-Oct-2016 (CT) Add message if no test is found
#    23-Apr-2020 (CT) Use `importlib.import_module`, not `__import__`
#    ««revision-date»»···
#--

from   _TFL             import TFL
from   _TFL.Regexp      import *
from   _TFL.run_doctest import format_x, format_f, format_s

import _TFL.CAO
import _TFL.sos         as     os

import sys
import importlib
import doctest

def _main (cmd) :
    cmd_path              = list (cmd.path or [])
    replacer              = Re_Replacer (r"\.py[co]", ".py")
    a                     = cmd.argv [0]
    et                    = ""
    if not os.path.isfile (cmd.module) :
        raise ValueError ("Module %s not found" % (cmd.module, ))
    f                     = TFL.Filename (cmd.module)
    m                     = f.base
    py_version            = " [py %s]" % \
        ".".join (str (v) for v in sys.version_info [:3])
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
        module            = importlib.import_module (m)
        module.expect_except = TFL.CAO.expect_except
        tests             = cmd.argv [1:]
        test_set          = set  (tests)
        m_tests           = list (getattr (module, "__test__", {}))
        for tn in m_tests :
            if tn not in test_set :
                del module.__test__ [tn]
        if not module.__test__ :
            print \
                ( "Test not found: %s\n    Choose one of: %s"
                % (", ".join (tests), ", ".join (sorted (m_tests)))
                )
            raise SystemExit (23)
        f, t              = doctest.testmod \
            ( module
            , verbose     = cmd.verbose
            , optionflags = flags
            )
    except Exception as exc :
        msg = format_x % (replacer (a), py_version, exc, et)
        print (msg, file = sys.stderr)
        raise
    else :
        cases  = int (bool (t))
        format = format_f if f else format_s
        print (replacer (format % TFL.Caller.Scope ()), file = sys.stderr)
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
