# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004-2006 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.cluster
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
#++
# Name
#    TFL.Plugin_Packager
#
# Purpose
#    Package a plugin so that it can be added to a McMillanized application
#
# Revision Dates
#    18-Jun-2004 (CT)  Creation
#    19-Jun-2004 (CT)  Creation continued
#    20-Jun-2004 (CT)  Creation continued..
#    21-Jun-2004 (CT)  Creation continued....
#    22-Jun-2004 (CT)  Creation (repackaged)
#    22-Jun-2004 (CT)  Code for `-AP_Closure` changed to pass
#                      `TFL._.Import_Closure.__dict__` to `eval`
#    22-Jun-2004 (CT)  Special casing for `_Plugins.__init__` added
#    23-Jun-2004 (CT)  `_setup_replacers` changed to not create replacement
#                      pattern for `_Plugins` package itself
#    23-Jun-2004 (CT)  `_rewrite_package_derived` changed to import/del
#                      `Derived_Package_Namespace` instead of
#                      `Package_Namespace`
#    24-Aug-2004 (CT)  `_Hide` added to avoid `_import _XXX` to be interpreted
#                      relatively instead of absolutely (RUP 11203)
#    24-Aug-2004 (CT)  Rewrite all occurrences of `pi_package.pkg` in
#                      `__init__` instead of specific patterns only
#    28-Sep-2004 (CT)  Use `open` instead of `file` to open a file
#    27-Oct-2004 (CED) `self.hides` saved
#     4-Nov-2004 (CT)  `_make_target_dir` factored and called from
#                      `_rewrite_package_plugin`
#    25-Mar-2005 (MG)  Import of `Filename` changed
#     7-Jun-2006 (CT)  `Re_Replacer` factored to `TFL.Regexp`
#    20-Jul-2006 (PGO) `_populate_dirs` creates init files in empty dirs
#     6-Nov-2006 (CED) No rewriting anymore
#    ��revision-date�����
#--

from   _TFL import TFL

import copy
import md5
import sys

import _TFL.Accessor
import _TFL.Import_Closure
import _TFL.import_module
import _TFL._Meta.Object
import _TFL.sos

from   _TFL.Filename       import Filename, Dirname
from   _TFL.Regexp         import Regexp
from   _TFL.predicate      import *

class Plugin_Packager (TFL.Meta.Object) :

    _leading_underscore = Regexp ("^_")

    def __init__ \
        ( self, pi_root_name, ap_closure, import_path, target_root
        , ignore = None
        ) :
        assert "_Plugins" not in ap_closure.pym_dict
        self.pi_root_name  = pi_root_name
        self.ap_closure    = ap_closure
        self.import_path   = import_path
        self.target_root   = Dirname (target_root).name
        self.pi_closure    = TFL.Import_Closure \
            (pi_root_name, import_path, ignore)
        self.delta_closure = dc = self.pi_closure - ap_closure
        pi_packages        = \
            [ p for p in dc.pkg_dict.itervalues ()
                if  p.pkg.startswith ("_Plugins") and p.level == 1
            ]
        assert len (pi_packages) == 1
        self.pi_package    = pip  = pi_packages [0]
        assert dc.root_pym.pkg   == pip.pkg, "%s:%s" % (dc.root_pym.pkg, pip.pkg)
        self.plugin_name          = self._get_name (pip)
        self._setup_target_packages (pip)
        self._copy_modules          ()
        self._make_setup_file       ()
    # end def __init__

    def _copy_modules (self) :
        for pym in self.py_modules + self.py_packages :
            code = self._read_source_file (pym)
            self._write_target_file       (pym, code)
    # end def _copy_modules

    def _get_name (self, pip) :
        try :
            sys_path = list (sys.path)
            sys.path [0:0] = self.import_path
            m = TFL.import_module ("%s.Version" % pip.pkg)
            return m.Version.productid
        finally :
            sys.path = sys_path
    # end def _get_name

    def _make_setup_file (self) :
        pname = self.plugin_name
        fname = TFL.sos.path.join (self.target_root, "_setup.py")
        sf    = open (fname, "w")
        sf.write     ("# Setup code for plugin %s\n\n" % pname)
        sf.write     ("from _TFL.Importers import Plugin_Importer\n\n")
        for pyp in sorted (self.py_packages, key = TFL.Attribute.pkg) :
            sf.write \
                ( "Plugin_Importer.register ('%s', '%s')\n"
                % (pname, pyp.pkg)
                )
        for pym in sorted (self.py_modules, key = TFL.Attribute.rel_name) :
            code = self._read_source_file (pym)
            m    = md5.new (code)
            sf.write \
              ( "Plugin_Importer.tag_module ('%s', '%s', '%s')\n"
              % (pname, pym.rel_name, m.hexdigest ())
              )
        sf.close     ()
    # end def _make_setup_file

    def _make_target_dir (self, pym) :
        pym_dir = TFL.sos.path.split (pym.target_path) [0]
        if not TFL.sos.path.isdir (pym_dir) :
            TFL.sos.mkdir_p (pym_dir)
    # end def _make_target_dir

    def _pns_from_pkg (self, pkg) :
        return ".".join \
            ([self._leading_underscore.sub ("", p) for p in pkg.split (".")])
    # end def _pns_from_pkg

    def _read_source_file (self, pym) :
        source = open        (pym.path_name)
        code   = source.read ()
        source.close         ()
        return code
    # end def _read_source_file

    def _setup_target_packages (self, pip) :
        dc      = self.delta_closure
        path    = TFL.sos.path
        sep     = TFL.sos.sep
        self.pym_dict    = pym_dict    = {}
        self.py_modules  = pyms        = []
        self.py_packages = pyps        = []
        for pym in dc.pym_dict.values () :
           for pyp in pym.pkg_chain () :
               if pyp.rel_name not in dc.pym_dict :
                   dc._add (pyp)
        for pym in dc.pym_dict.itervalues () :
            pym.target_pkg  = pym.pkg
            pym.target_path = path.join \
                (self.target_root, pym.pkg.replace (".", sep), pym.base_path)
            pym.source_pns = self._pns_from_pkg (pym.pkg)
            pym.target_pns = self._pns_from_pkg (pym.target_pkg)
            if pym.is_package :
                self._make_target_dir (pym)
                pym.source_mod = pym.pkg
                pym.target_mod = pym.target_pkg
                pyps.append (pym)
            else :
                pym.source_mod = ".".join ((pym.pkg,        pym.base_name))
                pym.target_mod = ".".join ((pym.target_pkg, pym.base_name))
                pyms.append (pym)
            pym_dict [pym.source_mod] = pym
    # end def _setup_target_packages

    def _write_target_file (self, pym, code) :
        target = open (pym.target_path, "w")
        target.write  (code)
        target.close  ()
    # end def _write_target_file

# end class Plugin_Packager

def command_spec (arg_array = None) :
    from   Command_Line import Command_Line
    return Command_Line \
        ( arg_spec    =
            ( "pi_root_name"
            , "target_root"
            , "import_path=./"
            )
        , option_spec =
            ( "-AP_Closure:S"
                  "?Name of file containing the import closure of application"
            , "-Diff:S"
                  "?Name of python_module which import closure gets subtracted"
            , "-ignore:S,=U_Test?Ignore modules specified"
            , "-Pathsep:S=:?Path separator used by `import_path'"
            )
        , min_args    = 2
        , max_args    = 3
        , arg_array   = arg_array
        )
# end def command_spec

def main (cmd) :
    import_path = map \
        (TFL.sos.expanded_path, cmd.import_path.split (cmd.Pathsep))
    ignore      = dict_from_list (cmd.ignore)
    if cmd.AP_Closure :
        assert not cmd.Diff
        ap_closure = eval \
            (open (cmd.AP_Closure).read (), TFL._.Import_Closure.__dict__)
    elif cmd.Diff :
        ap_closure = TFL.Import_Closure \
            ( file_name   = cmd.Diff
            , import_path = import_path
            , ignore      = ignore
            )
    else :
        print "One of the options -AP_Closure or -Diff must be specified"
        raise SystemExit, 9
    packager = Plugin_Packager \
        (cmd.pi_root_name, ap_closure, import_path, cmd.target_root, ignore)
# end def main

if __name__ == "__main__":
    main (command_spec ())
### to test:
### python ~/lib/python/_TFL/Plugin_Packager.py -Diff TTP_Build.py ~/NCO/lib/python/_Plugins/_MPC555_AS8202/Board.py /tmp/PIP_Test ~/NCO/external/ttpbuild/src/code:~/NCO/lib/python
else :
    TFL._Export ("Plugin_Packager")
### __END__ TFL.Plugin_Packager
