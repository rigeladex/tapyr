# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 Mag. Christian Tanzer. All rights reserved
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
#    Plugin_Packager
#
# Purpose
#    Package a plugin so that it can be added to a McMillanized application
#
# Revision Dates
#    18-Jun-2004 (CT) Creation
#    19-Jun-2004 (CT) Creation continued
#    20-Jun-2004 (CT) Creation continued..
#    21-Jun-2004 (CT) Creation continued....
#    22-Jun-2004 (CT) Creation (repackaged)
#    22-Jun-2004 (CT) Code for `-AP_Closure` changed to pass
#                     `TFL._.Import_Closure.__dict__` to `eval`
#    ««revision-date»»···
#--

from   _TFL import TFL

import sos
import sys
import _TFL.Import_Closure
import _TFL.import_module
import _TFL._Meta.Object

from   Filename            import Filename, Dirname
from   predicate           import *
from   Regexp              import *

class Replacer (TFL.Meta.Object) :
    """Replace a specific pattern in text"""

    def __init__ (self, pattern, replacement) :
        self.regexp      = Regexp (pattern, re.VERBOSE | re.MULTILINE)
        self.replacement = replacement
    # end def __init__

    def __call__ (self, text) :
        try :
            return self.regexp.sub (self.replacement, text)
        except TypeError :
            print self.regexp.pattern, self.replacement
            raise
    # end def __call__

# end class Replacer

class Plugin_Packager (TFL.Meta.Object) :

    _leading_underscore  = Regexp ("^_")
    _pip_import_pat      = \
        ( r"""^(?P<head> \s* from \s+ _Plugins._)"""
          r""" (?P<pns>  %s) \s+ """
          r""" (?P<midd> import \s+)"""
          r""" (?P=pns)"""
          r"""\s*$"""
        )
    _pns_import_pat      = \
        ( r"""^(?P<head> \s* from \s+)"""
          r"""_(?P<pns>  %s) \s+ """
          r""" (?P<midd> import \s+)"""
          r""" (?P=pns)"""
          r"""\s*$"""
        )
    _mod_import_pat      = \
        ( r"""^(?P<head>   \s* import \s+)"""
          r""" (?P<module> %s)"""
          r"""\s*$"""
        )
    _mod_from_import_pat = \
        ( r"""^(?P<head>   \s* from \s+)"""
          r""" (?P<module> %s)"""
          r""" (?P<midd>   \s+ import \s+)"""
        )
    _pip_access_pat      = r"""(?<! [A-Za-z0-9_]) %s (?= \.)"""

    def __init__ (self, pi_root_name, ap_closure, import_path, target_root, ignore = None) :
        assert "_Plugins" not in ap_closure.pym_dict
        self.pi_root_name  = pi_root_name
        self.ap_closure    = ap_closure
        self.import_path   = import_path
        self.target_root   = Dirname (target_root)
        self.pi_closure    = TFL.Import_Closure \
            (pi_root_name, import_path, ignore)
        self.delta_closure = dc = self.pi_closure - ap_closure
        pi_packages        = \
            [ p for p in dc.pkg_dict.itervalues ()
                if p.pkg.startswith ("_Plugins") and p.level == 1
            ]
        assert len (pi_packages) == 1
        self.pi_package = pip = pi_packages [0]
        assert dc.root_pym.pkg == pip.pkg, "%s:%s" % (dc.root_pym.pkg, pip.pkg)
        dc.remove ("_Plugins")
        self._setup_target_packages (pip)
        self._setup_replacers       ()
        self._rewrite_modules       (self._m_replacers)
        self._rewrite_packages      ()
    # end def __init__

    def _get_version (self, pip) :
        try :
            sys_path = list (sys.path)
            sys.path [0:0] = self.import_path
            m = TFL.import_module ("%s.Version" % pip.pkg)
            return m.Version
        finally :
            sys.path = sys_path
    # end def _get_version

    def _pns_from_pkg (self, pkg) :
        return ".".join \
            ([self._leading_underscore.sub ("", p) for p in pkg.split (".")])
    # end def _pns_from_pkg

    def _read_source_file (self, pym) :
        source = file        (pym.path_name)
        code   = source.read ()
        source.close         ()
        return code
    # end def _read_source_file

    def _rewrite_module (self, pym, replacers) :
        code = self._read_source_file (pym)
        for r in replacers :
            code = r (code)
        self._write_target_file (pym, code)
    # end def _rewrite_module

    def _rewrite_modules (self, replacers) :
        for pym in self.py_modules :
            self._rewrite_module (pym, replacers)
    # end def _rewrite_modules

    def _rewrite_package_derived (self, pym) :
        name = pym.pkg.split (".") [-1] [1:]
        repl = Replacer \
            ( r"%s \s* = \s* Package_Namespace \s* \(\)" % (name, )
            , ( r"""from %s import %s"""
                 """\n"""
                r"""%s = Derived_Package_Namespace (%s)"""
              ) % (pym.pkg, name, name, name)
            )
        self._rewrite_module (pym, self._m_replacers + [repl])
    # end def _rewrite_package_derived

    def _rewrite_package_plugin (self, pym) :
        name = pym.pkg.split (".") [-1] [1:]
        repl = Replacer \
            ( r"%s \s* = \s* Package_Namespace \s* \(\)" % (name, )
            , r"""%s_%s = Package_Namespace ()""" % (name, self.target_vrsn)
            )
        self._rewrite_module \
            ( pym
            , self._m_replacers
            + [ Replacer
                  ( r"%s \s* = \s* Package_Namespace \s* \(\)" % (name, )
                  , r"""%s_%s = Package_Namespace ()"""
                    % (name, self.target_vrsn)
                  )
              , Replacer
                  ( r"""\._Export \s*\("%s"\)""" % (name, )
                  , r"""._Export ("%s_%s")"""    % (name, self.target_vrsn)
                  )
              ]
            )
    # end def _rewrite_package_plugin

    def _rewrite_packages (self) :
        pip = self.pi_package
        for pym in self.py_packages :
            if pym == pip :
                self._rewrite_package_plugin (pym)
            elif pym.pkg.startswith ("_Plugins") :
                raise NotImplementedError, \
                    ( "Inner packages under plugin package not yet "
                      "supported: %s"
                    % pym.rel_name
                    )
            else :
                if pym.rel_name in self.ap_closure.pym_dict :
                    self._rewrite_package_derived (pym)
                else :
                    self._rewrite_module (pym, self._m_replacers)
    # end def _rewrite_packages

    def _setup_replacers (self) :
        self._m_replacers = []
        add               = self._m_replacers.append
        tpkg              = self.target_pkg
        tlp_pns           = sorted \
            ( [ pym.source_pns
                for pym in self.delta_closure.tlp_dict.itervalues ()
              ]
            )
        modules           = dusort \
            ( [ pym.source_mod
                for pym in self.delta_closure.pym_dict.itervalues ()
                if  not (  pym.pkg.startswith ("_Plugins")
                        or (pym.is_package and pym.is_toplevel)
                        )
              ]
            , lambda m : -len (m)
            )
        pi_modules        = dusort \
            ( [ pym.source_mod
                for pym in self.delta_closure.pym_dict.itervalues ()
                if  pym.pkg.startswith ("_Plugins")
                    and not (pym.is_package and pym.is_toplevel)
              ]
            , lambda m : -len (m)
            )
        add ( Replacer
                ( self._pns_import_pat % ("|".join (tlp_pns), )
                , r"\g<head>%s._\g<pns> \g<midd>\g<pns>" % (tpkg, )
                )
            )
        add ( Replacer
                ( self._pip_import_pat
                  % (self.pi_package.pkg [len ("_Plugins._") : ], )
                , r"\g<head>\g<pns>_%s \g<midd>\g<pns>_%s"
                  % (self.target_vrsn, self.target_vrsn)
                )
            )
        add ( Replacer
                ( self._mod_import_pat % ("|".join (modules), )
                , r"\g<head>%s.\g<module>" % (tpkg, )
                )
            )
        add ( Replacer
                ( self._mod_from_import_pat % ("|".join (modules), )
                , r"\g<head>%s.\g<module>\g<midd>" % (tpkg, )
                )
            )
        add ( Replacer
                ( self._mod_import_pat % ("|".join (pi_modules), )
                , lambda m : r"%s %s"
                      % ( m.group ("head")
                        , self.pym_dict [m.group ("module")].target_mod
                        )
                )
            )
        add ( Replacer
                ( self._pip_access_pat
                  % (self.pi_package.source_pns [len ("Plugins.") : ], )
                ,    self.pi_package.target_pns [len ("Plugins.") : ]
                )
            )
    # end def _setup_replacers

    def _setup_target_packages (self, pip) :
        Version = self._get_version (pip)
        dc      = self.delta_closure
        path    = sos.path
        sep     = sos.sep
        self.pym_dict    = pym_dict    = {}
        self.py_modules  = pyms        = []
        self.py_packages = pyps        = []
        self.target_vrsn = vrsn = Version.version.replace (".", "_").strip ()
        self.target_pkg  = target_pkg  = "%s_%s" % (pip.pkg, vrsn)
        self.target_path = target_path = path.join \
            (self.target_root.name, target_pkg.replace (".", sep))
        for pym in dc.pym_dict.itervalues () :
            if pym.pkg.startswith (pip.pkg) :
                if pym.pkg == pip.pkg :
                    pym.target_pkg  = target_pkg
                    pym.target_path = path.join (target_path, pym.base_path)
                else :
                    pn              = pym.pkg [len ("_Plugins.") : ]
                    pym.target_pkg  = ".".join ((target_pkg, pn))
                    pym.target_path = path.join \
                        (target_path, pn.replace (".", sep), pym.base_path)
            else :
                pym.target_pkg  = ".".join ((target_pkg, pym.pkg))
                pym.target_path = path.join \
                    (target_path, pym.pkg.replace (".", sep), pym.base_path)
            pym.source_pns = self._pns_from_pkg (pym.pkg)
            pym.target_pns = self._pns_from_pkg (pym.target_pkg)
            if pym.is_package :
                pym_dir = path.split (pym.target_path) [0]
                if not path.isdir (pym_dir) :
                    sos.mkdir_p (pym_dir)
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
        target = file (pym.target_path, "w")
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
    import_path = map (sos.expanded_path, cmd.import_path.split (cmd.Pathsep))
    ignore      = dict_from_list (cmd.ignore)
    if cmd.AP_Closure :
        assert not cmd.Diff
        ap_closure = eval \
            (file (cmd.AP_Closure).read (), TFL._.Import_Closure.__dict__)
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
    #print packager.target_pkg, packager.target_path
    if 1 :
        for pym in sorted (packager.delta_closure.pym_dict.itervalues ()) :
            print "tkdiff %-80s %s" % (pym.path_name, pym.target_path)
            #print "%-50s --> %s" % (pym.pkg, pym.target_pkg)
            #print "%-50s --> %s" % (pym.source_pns, pym.target_pns)
    if 0 :
        print sorted ([pym.source_pns for pym in
                       packager.delta_closure.tlp_dict.itervalues ()
                      ]
                     )
    #print [r.regexp.pattern for r in packager._m_replacers]
# end def main

if __name__ == "__main__":
    main (command_spec ())
### to test:
### python ~/lib/python/_TFL/Plugin_Packager.py -Diff ~/NCO/external/ttpbuild/src/code/NDT.py ~/NCO/lib/python/_Plugins/_MPC555_AS8202/Board.py /tmp/PIP_Test ~/NCO/external/ttpbuild/src/code:~/NCO/external/ttpostool/src/code:~/NCO/lib/python
else :
    TFL._Export ("Plugin_Packager")
### __END__ Plugin_Packager
