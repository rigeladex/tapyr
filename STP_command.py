# -*- coding: utf-8 -*-
# Copyright (C) 2017-2020 Christian Tanzer All rights reserved
# tanzer@gg32.com                                      https://www.gg32.com
# #*** <License> ************************************************************
# This module is licensed under the terms of the BSD 3-Clause License
# <https://www.gg32.com/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    STP_command
#
# Purpose
#    Provide commands to ease use of setup.py of TFL-based packages
#
# Revision Dates
#    23-Feb-2017 (CT) Creation
#    24-Feb-2017 (CT) Use `twine` for upload
#    24-Feb-2017 (CT) Update `__doc__` doctest output
#    16-Apr-2018 (CT) Adapt to New `PyPI`
#    26-Mar-2020 (CT) Add `sys.executable` and `dist/*` to `_do_twine`
#    20-Apr-2020 (CT) Add option `-skip`
#    ««revision-date»»···
#--

r"""
`STP_command` provides commands to ease use of setup.py of TFL-based
packages.

The output of::

    # python STP_command.py -help=cmds

looks like::

    >>> _ = Command () (["-help=cmds"]) # doctest:+ELLIPSIS
    Sub commands of .../STP_command.py
        clean   : Clean everything created by setup.py
        list    : List packages selected by `-package`, `-all`, `-py-path`
        release : Use setup.py to package and upload the packages selected
        setup   : Apply the specified setup.py commands to the packages selected
        tag     : Tag repository version
        twine   : Apply the specified twine commands to the packages selected
        version : Show version of packages

`STP_command clean` cleans **all** files created by `setup.py`::

    # python STP_command.py -all -verbose clean

will result in::

    >>> _ = Command () (["-all", "-verbose", "clean"])
    Cleaning TFL_STP
    Cleaning _TFL
    Cleaning _CAL
    Cleaning _CHJ
    Cleaning _ReST
    Cleaning _ATAX
    Cleaning _JNJ
    Cleaning _MOM
    Cleaning _GTW

`STP_command release` will build wheels and upload them for all packages
specified. For instance, ::

    # python STP_command.py release -all -tag=2.0.42 -message "..."

Adding the `-test` option to a `release` command will upload to
https://test.pypi.org instead of the real thing.

"""

from   _TFL                       import TFL

from   _TFL.Filename              import Dirname
from   _TFL.Generators            import iter_split
from   _TFL._Meta.Once_Property   import Once_Property
from   _TFL                       import sos

import _TFL.Command

import TFL_STP

import itertools
import subprocess
import sys

class _STP_Sub_Command_ (TFL.Command.Sub_Command) :

    _rn_prefix              = "_STP"

_Sub_Command_ = _STP_Sub_Command_ # end class

class STP_Command (TFL.Command.Root_Command) :
    """Extendable command around setup.py"""

    _rn_prefix              = "STP_"

    min_args                = 1
    max_args                = 1

    pkg_order               = \
        ( "TFL_STP"
        , "_TFL"
        , "_CAL",  "_CHJ", "_ReST"
        , "_ATAX", "_JNJ", "_MOM"
        , "_GTW"
        )

    _defaults               = dict \
        ( PY_Path           = sos.environ.get ("PYTHONPATH")
        )
    _opts                   = \
        ( "-all:B?Process all known packages"
        , "-dry_run:B?Display setup commands instead of applying them"
        , "-package:P:?Package(s) to process"
        , "-PY_Path:P:?Search path for packages"
        , "-skip:P:?Don't include specified packages"
        , "-verbose:B?Verbose output"
        )

    @Once_Property
    def pkg_priority (self) :
        return { k : i for (i, k) in enumerate (self.pkg_order)}
    # end def pkg_priority

    class _STP_Clean_ (_Sub_Command_) :
        """Clean everything created by setup.py"""

    _Clean_ = _STP_Clean_ # end class

    class _STP_List_ (_Sub_Command_) :
        """List packages selected by `-package`, `-all`, `-py-path`"""

    _List_ = _STP_List_ # end class

    class _STP_SR_Base_ (_Sub_Command_) :
        """Base for release and setup commands"""

        is_partial              = True
        _opts                   = \
            ( "-message:S?Annotate the tag with message specified"
            , "-tag:S?New tag value (`+` means increment)"
            , "-test:B?Use the repository test.pypi.org"
            )

    # end class _STP_SR_Base_

    class _STP_Release_ (_STP_SR_Base_) :
        """Use setup.py to package and upload the packages selected"""

        _opts                   = \
            ( "-source:B?Upload source distribution, too [sdist]"
            ,
            )

    _Release_ = _STP_Release_ # end class

    class _STP_Setup_ (_STP_SR_Base_) :
        """Apply the specified setup.py commands to the packages selected"""

        max_args                = -1
        _args                   = \
            ( "setup_cmd:S?Command(s) passed to `setup.py`"
            ,
            )

    _Setup_ = _STP_Setup_ # end class

    class _STP_Tag_ (_Sub_Command_) :
        """Tag repository version"""

        _args                  = \
            ( "message:S?Annotate the tag with message specified"
            ,
            )
        _opts                   = \
            ( "-Value:S=+?New tag value (`+` means increment)"
            ,
            )

    _Tag_ = _STP_Tag_ # end class

    class _STP_Twine_ (_STP_SR_Base_) :
        """Apply the specified twine commands to the packages selected"""

        max_args                = -1
        _args                   = \
            ( "twine_cmd:S?Command(s) passed to `twine`"
            ,
            )

    _Twine_ = _STP_Twine_ # end class

    class _STP_Version_ (_Sub_Command_) :
        """Show version of packages"""

        _opts                   = \
            ( "-update:B?Update VERSION.py"
            ,
            )

    _Version_ = _STP_Version_ # end class

    def _do_clean (self, cao, packages) :
        for pn, pp in packages :
            with sos.changed_dir (pp) :
                if cao.verbose :
                    print ("Cleaning", pn)
                to_clean = \
                    ( [".eggs", "build", "dist"]
                    + sos.expanded_glob ("*.egg-info")
                    )
                if to_clean :
                    TFL_STP.run_command (["rm", "-rf"] + to_clean)
    # end def _do_clean

    def _do_setup (self, cao, argv, packages) :
        r_args   = ["--repository", "testpypi"] \
            if cao.test and ("register" in argv or "upload" in argv) else []
        setup_cmd  = [sys.executable, "setup.py"] + argv + r_args
        args       = " ".join (argv)
        for pn, pp in packages :
            with sos.changed_dir (pp) :
                if cao.verbose :
                    print ("Starting", args, "for", pn, "...")
                if cao.dry_run :
                    print (" ", " ".join (setup_cmd [1:]))
                else :
                    try :
                        subprocess.call (setup_cmd)
                    except subprocess.CalledProcessError as exc :
                        print (exc)
                        raise SystemExit (127)
                if cao.verbose :
                    print ("... Finished", pn)
    # end def _do_setup

    def _do_tag (self, cao, new_tag, msg) :
        if new_tag.startswith ("+") :
            new = self._tag_incremented (new_tag)
        else :
            new = new_tag
        cmd = ["git", "tag", new]
        if msg :
            cmd += ["-m", msg]
        if cao.dry_run :
            print (* cmd)
        else :
            try :
                out = TFL_STP.run_command (cmd)
            except subprocess.CalledProcessError as exc :
                print ("Error from tag", new, "\n   ", exc.output)
                raise SystemExit (126)
            if cao.verbose :
                print (out)
        return new
    # end def _do_tag

    def _do_twine (self, cao, cmd, args, packages) :
        r_args   = ["--repository", "testpypi"] if cao.test else []
        twc_head = [sys.executable, "-m", "twine", cmd] + r_args
        for pn, pp in packages :
            with sos.changed_dir (pp) :
                twc_tail = args
                if cmd == "register" :
                    dist     = sos.expanded_glob (args [-1])
                    twc_tail = args [:-1] + dist
                elif cmd == "upload" :
                    twc_tail = ["dist/*"]
                twc = twc_head + twc_tail
                if cao.verbose :
                    print ("Starting twine upload for", pn, "...")
                if cao.dry_run :
                    print (" ", " ".join (twc))
                else :
                    try :
                        subprocess.call (twc)
                    except subprocess.CalledProcessError as exc :
                        print (exc)
                        raise SystemExit (127)
                if cao.verbose :
                    print ("... Finished", pn)
    # end def _do_setup

    def _git_version (self, abort_on_error = False) :
        d_v = TFL_STP.git_date_version  (abort_on_error = abort_on_error)
        if d_v :
            result = d_v [1]
        return result
    # end def _git_version

    def _handle_clean (self, cao) :
        self._do_clean (cao, self._packages (cao))
    # end def _handle_clean

    def _handle_list (self, cao) :
        packages = self._packages (cao)
        if cao.verbose :
            for pn, pp in packages :
                print ("%-8s : %s" % (pn, pp))
        else :
            print (" ".join (pn for pn, pp in packages))
    # end def _handle_list

    def _handle_release (self, cao) :
        git_version = self._git_version ()
        if "+" in git_version :
            if "modified" in git_version :
                print ("Please commit the uncommitted changes")
                raise SystemExit (128)
        if cao.message or cao.tag :
            if not cao.message :
                print ("Please specify -message when using -tag", cao.tag)
                raise SystemExit (125)
            if not cao.tag :
                print ("Please specify -tag when using -message", cao.message)
                raise SystemExit (125)
            self._do_tag (cao, cao.tag, cao.message)
        if not cao.dry_run :
            git_version = self._git_version ()
            if not git_version :
                print ("Please use `git tag` to define your package's version.")
                raise SystemExit (128)
        packages    = self._packages (cao)
        argv_groups = \
            (  ["-q", "check"]
            ,  ["-q", "bdist_wheel"]
            ,  ["-q", "sdist"] if cao.source else []
            )
        self._do_clean (cao, packages)
        for argv in argv_groups :
            if argv :
                self._do_setup (cao, argv, packages)
        self._do_twine (cao, "upload", ["dist/*"], packages)
    # end def _handle_release

    def _handle_setup (self, cao) :
        if cao.message or cao.tag :
            if not cao.message :
                print ("Please specify -message when using -tag", cao.tag)
                raise SystemExit (125)
            if not cao.tag :
                print ("Please specify -tag when using -message", cao.message)
                raise SystemExit (125)
            self._do_tag (cao, cao.tag, cao.message)
        packages    = self._packages (cao)
        argv_groups = iter_split (cao, "--", list)
        for argv in argv_groups :
            self._do_setup (cao, argv, packages)
    # end def _handle_setup

    def _handle_tag (self, cao) :
        packages = self._packages (cao)
        new_tag  = cao.Value
        message  = " ".join (cao.argv)
        if packages :
            for pn, pp in packages :
                with sos.changed_dir (pp) :
                    nt = self._do_tag (cao, new_tag, message)
                    print ("Repository tag: %s" % (nt, ))
        else :
            nt = self._do_tag (cao, new_tag, message)
            print ("Repository tag: %s" % (nt, ))
    # end def _handle_tag

    def _handle_twine (self, cao) :
        packages = self._packages (cao)
        argv_groups = iter_split (cao, "--", list)
        for argv in argv_groups :
            if argv :
                self._do_twine (cao, argv [0], argv [1:], packages)
    # end def _handle_twine

    def _handle_version (self, cao) :
        packages = self._packages (cao)
        if packages :
            for pn, pp in packages :
                with sos.changed_dir (pp) :
                    if cao.update :
                        v   = TFL_STP.update_version_py ()
                    else :
                        v   = self._git_version () or "unknown"
                    print ("%-8s : %s" % (pn, v))
        else :
            v = self._git_version () or "unknown"
            print ("Repository tag: %s" % (v, ))
    # end def _handle_version

    def _packages (self, cao) :
        if cao.all or cao.package == ["*"] :
            p_specs = self.pkg_order
        else :
            p_specs = cao.package or ()
        py_path = cao.PY_Path or [self.app_dir]
        skip    = set (cao.skip or ())
        result  = tuple \
            ( x for x in (self._package_path (p, py_path) for p in p_specs)
                if  x and not x [0] in skip
            )
        def sk (x) :
            b, r = x
            return self.pkg_priority.get (b, 1 << 32)
        return sorted (result, key = sk)
    # end def _packages

    def _package_path (self, ps, py_path) :
        for p in py_path :
            r = sos.path.join (p, ps)
            if sos.path.exists (r) :
                rd = Dirname (r)
                if sos.path.isfile (sos.path.join (rd.name, "setup.py")) :
                    return rd.base, rd.name
    # end def _package_path

    def _tag_incremented (self, new_tag) :
        gv  = None
        inc = int (new_tag [1:] or 1)
        try :
            gv = self._git_version (abort_on_error = False)
        except subprocess.CalledProcessError :
            raw_tags = TFL_STP.run_command \
                (["git", "tag", "--list"]).split ("\n")
            if raw_tags :
                def _gen (tags) :
                    for t in tags :
                        try :
                            ps  = t.strip ().split (".")
                            tag = tuple (int (p) for p in ps)
                        except Exception :
                            pass
                        else :
                            yield tag
                tags = sorted (_gen (raw_tags))
                if tags :
                    gv  = ".".join (str (s) for s in tags [-1])
        if gv :
            old    = gv.split  ("+", 1) [0]
            ps     = old.split (".")
            result = ".".join (ps [:-1] + [str (int (ps [-1]) + inc)])
        else :
            result = "0.0.1"
        return result
    # end def _tag_incremented

Command = STP_Command # end class

if __name__ == "__main__" :
    Command () ()
### __END__ STP_command
