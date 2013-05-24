# -*- coding: iso-8859-15 -*-
# Copyright (C) 2004-2013 Mag. Christian Tanzer. All rights reserved
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
#    17-May-2010 (CT) `failures` added to `_main`
#    19-May-2010 (CT) Support for keywords->environment added
#                     (and ported to use TFL.CAO instead of TFL.Command_Line)
#    22-Jun-2010 (CT) Use `TFL.CAO.put_keywords` instead of
#                     `TFL.CAO.do_keywords` and home-grown code
#    11-Aug-2010 (CT) Summary generation totally revamped
#    11-Aug-2010 (CT) `_main` changed to avoid starting subprocesses for
#                     directory traversal (factored and changed `run_dir`)
#    11-Aug-2010 (CT) Option `-format` replaced by module-level variables
#                     `format_f` and `format_s`
#    17-Aug-2010 (CT) `__test__` added to `_doctest_pat`
#    14-Jun-2011 (MG) `timing` command line option added
#    10-Aug-2012 (MG) Add new command line option for `exclude`
#    17-Jan-2013 (CT) Add package-path to `sys.path`
#    29-Jan-2013 (CT) Improve DRY of _main
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division
from   __future__  import print_function, unicode_literals

from   _TFL             import TFL
from   _TFL             import Environment
from   _TFL             import sos
from   _TFL.Filename    import Filename
from   _TFL.Regexp      import *
import _TFL.Record

import _TFL.Caller
import _TFL.CAO
import _TFL.Package_Namespace

import  doctest
import  sys
import  subprocess
import  time
import  fnmatch

TFL.Package_Namespace._check_clashes = False ### avoid spurious ImportErrors

_doctest_pat   = Regexp (r"^( *>>> |__test__ *=)", re.MULTILINE)

summary        = TFL.Record \
    ( excluded = []
    , failed   = 0
    , failures = []
    , modules  = 0
    , total    = 0
    )

format_f = """%(module.__file__)s fails %(f)s of %(t)s doc-tests%(et)s"""
format_s = """%(module.__file__)s passes all of %(t)s doc-tests%(et)s"""
format_x = """%s raises exception `%r` during doc-tests%s"""
sum_pat  = Regexp \
    ( "(?P<module>.+?) (?:fails (?P<failed>\d+)|passes all) of "
      "(?P<total>\d+) doc-tests"
    )
exc_pat  = Regexp \
    ("(?P<module>.*?) raises exception `(?P<exc>[^`]+)` during doc-tests")

def has_doctest (fn) :
    with open (fn, "rb") as f :
        code = f.read ()
    return _doctest_pat.search (code)
# end def has_doctest

def run_command (cmd) :
    subp = subprocess.Popen (cmd, shell = True, env = dict (sos.environ))
    subp.wait ()
# end def run_command

def _subp_step (subp) :
    try :
        out, err = subp.communicate ()
    except ValueError :
        pass
    else :
        err = err.decode ("latin-1")
        out = out.decode ("latin-1")
        sys.stdout.write (out)
        sys.stderr.write (err)
        if err :
            for l in err.split ("\n") :
                if sum_pat.match (l) :
                    summary.total += int (sum_pat.total)
                    f = int (sum_pat.failed or 0)
                    if f :
                        summary.failed += f
                        summary.failures.append ((sum_pat.module, f))
                elif exc_pat.match (l) :
                    summary.failed += 1
                    summary.total  += 1
                    summary.failures.append \
                        ((exc_pat.module, "Exception %s" % (exc_pat.exc, )))
# end def _subp_step

def run_command_with_summary (cmd) :
    subp = subprocess.Popen \
        ( cmd
        , shell   = True
        , env     = dict (sos.environ)
        , stderr  = subprocess.PIPE
        , stdout  = subprocess.PIPE
        )
    while subp.poll () is None :
        _subp_step (subp)
    _subp_step (subp)
# end def run_command_with_summary

def _main (cmd) :
    cmd_path = list (cmd.path or [])
    replacer = Re_Replacer (r"\.py[co]", ".py")
    a        = cmd.argv [0]
    et       = ""
    if len (cmd.argv) == 1 and not sos.path.isdir (a) :
        f  = Filename (a)
        m  = f.base
        sys.path [0:0] = cmd_path
        mod_path = f.directory if f.directory else "./"
        if sos.path.exists \
               (Filename ("__init__.py", default_dir = mod_path).name) :
            sys.path [0:0] = [sos.path.join (mod_path, "..")]
        sys.path [0:0] = [mod_path]
        flags = doctest.NORMALIZE_WHITESPACE
        if not cmd.nodiff :
            flags |= doctest.REPORT_NDIFF
        try :
            start  = time.time ()
            module = __import__ (m)
            f, t   = doctest.testmod \
                ( module
                , verbose     = cmd.verbose
                , optionflags = flags
                )
            exec_time = time.time () - start
        except KeyboardInterrupt :
            raise
        except Exception as exc :
            exec_time = time.time () - start
            if cmd.timing :
                et = " in %7.5fs" % (exec_time, )
            print (format_x % (replacer (a), exc, et), file = sys.stderr)
            raise
        else :
            format = format_f if f else format_s
            if cmd.timing :
                et = " in %7.5fs" % (exec_time, )
            print (replacer (format % TFL.Caller.Scope ()), file = sys.stderr)
    else :
        head_pieces = \
            [ sys.executable
            , "-%s" % ("O" * sys.flags.optimize, )
                if sys.flags.optimize else ""
            , sos.path.join
                (Environment.script_path (), Environment.script_name ())
            , "-path %r" % (",".join (cmd_path), ) if cmd_path else ""
            ]
        for opt in ("nodiff", "timing", "verbose") :
            if getattr (cmd, opt) :
                head_pieces.append ("-" + opt)
        head = " ".join (hp for hp in head_pieces if hp)
        if cmd.summary :
            run_cmd = run_command_with_summary
        else :
            run_cmd = run_command
        def run_mod (a) :
            if cmd.exclude and fnmatch.fnmatch (a, cmd.exclude):
                summary.excluded.append (a)
                print ("%s excluded" % (a, ))
            else :
                summary.modules += 1
                run_cmd ("%s %s" % (head, a))
        def run_mods (d) :
            for f in sorted (sos.listdir_exts (d, ".py")) :
                if has_doctest (f) :
                    run_mod (f)
        if cmd.transitive :
            from _TFL.subdirs import subdirs
            def run_dir (d) :
                run_mods (d)
                for s in subdirs (d) :
                    run_dir (s)
        else :
            run_dir = run_mods
        start = time.time ()
        for a in cmd.argv :
            if sos.path.isdir (a) :
                run_dir (a)
            else :
                if has_doctest (a) :
                    run_mod (a)
        if cmd.summary :
            format = format_f if summary.failed else format_s
            if cmd.timing :
                et = " in %7.5fs" % (time.time () - start, )
            print ("=" * 79)
            print \
                ( format % TFL.Caller.Scope
                    ( f      = summary.failed
                    , module = TFL.Record (__file__ = " ".join (cmd.argv))
                    , t      = summary.total
                    , et     = et
                    )
                , "[%s/%s modules fail]" %
                    (len (summary.failures), summary.modules)
                )
            print \
                ( "    %s"
                % ("\n    ".join ("%-68s : %s" % f for f in summary.failures))
                )
            if summary.excluded :
                print ("    %s excluded" % (", ".join (summary.excluded), ))
# end def _main

_Command = TFL.CAO.Cmd \
    ( handler      = _main
    , args         = ("module:P?Module(s) to test", )
    , opts         =
        ( "exclude:S?Glob pattern to exclude certain tests"
        , "nodiff:B?Don't specify doctest.REPORT_NDIFF flag"
        , "path:P:?Path to add to sys.path"
        , "summary:B?Summary of failed tests"
        , "timing:B?Add timing information"
        , "transitive:B"
            "?Include all subdirectories of directories specified "
              "as arguments"
        , "verbose:B?Turn verbosity on"
        )
    , min_args     = 1
    , put_keywords = True
    )

if __name__ == "__main__" :
    _Command ()
### __END__ run_doctest
