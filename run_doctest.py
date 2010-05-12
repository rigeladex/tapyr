# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004-2010 Mag. Christian Tanzer. All rights reserved
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
#    run_doctest
#
# Purpose
#    Run doctest on all modules specified on command line
#
# Revision Dates
#     8-Jan-2004 (CT) Creation
#    23-Feb-2004 (CT) `min_args = 1` added
#    20-Oct-2004 (CT) `_main` changed to use `sos.system` to test multiple
#                     modules in separate interpreter invocations (avoid
#                     interactions between the tests)
#    21-Oct-2004 (CT) `_main` changed to add path of module to be tested to
#                     `sys.path`
#    23-Oct-2004 (CT) `TFL.Package_Namespace._check_clashes` set to False
#     1-Jun-2005 (CT) `run_command` factored to take care of `PYTHONPATH`
#     2-Oct-2006 (CT) `replacer` added
#    11-Nov-2009 (CT) Support for directories added
#    19-Nov-2009 (CT) `has_doctest` added and used
#    17-Dec-2009 (CT) Pass `optionflags` to `doctest.testmod`:
#                       `doctest.NORMALIZE_WHITESPACE | doctest.REPORT_NDIFF`
#    18-Dec-2009 (CT) `-nodiff` added to disable `doctest.REPORT_NDIFF`
#    29-Apr-2010 (MG) Support for running the doctest in optimized mode added
#    12-May-2010 (MG) Summary generation added
#    ««revision-date»»···
#--

from   _TFL             import TFL
from   _TFL             import Environment
from   _TFL             import sos
from   _TFL.Filename    import Filename
from   _TFL.Regexp      import *
import _TFL.Record

import _TFL.Caller
import _TFL.Package_Namespace
import  doctest
import  sys
import  subprocess
import  os

_doctest_pat = Regexp (r"^ *>>> ", re.MULTILINE)

def has_doctest (fn) :
    with open (fn, "rb") as f :
        code = f.read ()
    return _doctest_pat.search (code)
# end def has_doctest

def run_command (cmd, regex = False) :
    kw = dict ()
    t  = f = "0"
    if regex :
        kw ["stdout"] = subprocess.PIPE
    subp = subprocess.Popen \
        ( cmd
        , shell = True
        , env   = dict (PYTHONPATH = os.path.pathsep.join (sys.path))
        , ** kw
        )
    if regex :
        while subp.poll () is None :
            out, err = subp.communicate ()
            if regex.match (out) :
                f = regex.failed
                t = regex.total
            sys.stdout.write (out)
        try :
            out, err = subp.communicate ()
            if regex.match (out) :
                f = regex.failed
                t = regex.total
            sys.stdout.write (out)
        except ValueError :
            pass
    else :
        subp.wait ()
    return f, t
# end def run_command

TFL.Package_Namespace._check_clashes = False ### avoid spurious ImportErrors

def _command_spec (arg_array = None) :
    from _TFL.Command_Line import Command_Line
    return Command_Line \
        ( arg_spec    = ("module:S?Module(s) to test")
        , option_spec =
            ( "format:S="
                 """%(module.__file__)s fails %(f)s of %(t)s doc-tests"""
            , "nodiff:B?Don't specify doctest.REPORT_NDIFF flag"
            , "path:S,?Path to add to sys.path"
            , "summary:B?Summary of failed tests"
            , "transitive:B"
                "?Include all subdirectories of directories specified "
                  "as arguments"
            )
        , min_args    = 1
        , arg_array   = arg_array
        )
# end def _command_spec

total = failed = 0

def _main (cmd) :
    format   = cmd.format
    cmd_path = list (cmd.path)
    replacer = Re_Replacer (r"\.py[co]", ".py")
    a        = cmd.argv [0]
    if len (cmd.argv) == 1 and not sos.path.isdir (a) :
        f = Filename (a)
        m = f.base
        sys.path [0:0] = cmd_path
        if f.directory :
            sys.path [0:0] = [f.directory]
        elif not cmd_path :
            sys.path [0:0] = ["./"]
        if cmd.nodiff :
            flags = doctest.NORMALIZE_WHITESPACE
        else :
            flags = doctest.NORMALIZE_WHITESPACE | doctest.REPORT_NDIFF
        try :
            module = __import__      (m)
            f, t   = doctest.testmod \
                ( module
                , verbose     = 0
                , optionflags = flags
                )
        except KeyboardInterrupt :
            raise
        except StandardError, exc :
            print "Testing of %s resulted in exception" % (replacer (a), )
            raise
        else :
            print replacer (format % TFL.Caller.Scope ())
    else :
        regex = None
        path  = nodiff = optimize = ""
        if cmd.nodiff :
            nodiff = "-nodiff"
        if cmd_path :
            path = " -path %r" % (",".join (cmd_path), )
        if sys.flags.optimize :
            optimize = "-%s" % ("O" * sys.flags.optimize, )
        head = "%s %s %s -format %r%s%s" % \
            ( sys.executable
            , optimize
            , sos.path.join
                  (Environment.script_path (), Environment.script_name ())
            , format
            , path
            , nodiff
            )
        if cmd.summary :
            t      = "(?P<total>\d+)"
            f      = "(?P<failed>\d+)"
            module = TFL.Record (__file__ = ".+?")
            regexp = Regexp \
                (cmd.format % TFL.Caller.Scope (module = module))
        def run (a) :
            global total, failed
            f, t    = run_command ("%s %s" % (head, a), regexp)
            failed += int (f)
            total  += int (t)
        for a in cmd.argv :
            if sos.path.isdir (a) :
                for f in sorted (sos.listdir_exts (a, ".py")) :
                    if has_doctest (f) :
                        run (f)
                if cmd.transitive :
                    from _TFL.subdirs import subdirs
                    for d in subdirs (a) :
                        run (d)
            else :
                if has_doctest (a) :
                    run (a)
        if cmd.summary :
            print "=" * 79
            print "%d tests of %d failed" % (failed, total)
# end def _main

if __name__ == "__main__" :
    _main (_command_spec ())
### __END__ run_doctest
