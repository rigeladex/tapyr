# -*- coding: iso-8859-1 -*-
# Copyright (C) 1998-2004 Mag. Christian Tanzer. All rights reserved
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
#    Import_Closure
#
# Purpose
#    Find all files imported by a given python module residing in a list of
#    user-specified directories (i.e., excluding standard Python modules)
#
# Revision Dates
#    25-Nov-1998 (CT) Creation
#    26-Nov-1998 (CT) `import_pat' corrected
#     7-Sep-2000 (CT) `expanded_path' applied
#    12-Apr-2001 (CT) `import_pat' changed ("[^#]*?" --> "^\s*")
#    12-Apr-2001 (CT) `-ignore' added
#     8-May-2001 (CT) Support for package imports added
#    18-May-2001 (CT) Use `_find_import' everywhere (factoring of
#                     `_find_import' finally completed)
#     2-Jul-2001 (CT) `pkg_namespace_import_pat' added and used
#     3-Jul-2001 (CT) `-Pathsep' added
#     3-Jul-2001 (CT) `pkg_namespace_pat' and `pkg_ns_dict' added and used
#    17-Jul-2001 (CT) Leading `_' removed from namespace-packages
#    17-Jul-2001 (CT) `pkg_namespace_pat' renamed to `pkg_namespace_def_pat'
#    17-Jul-2001 (CT) Global functions replaced by class Import_Finder
#    17-Jul-2001 (CT) Support for implicit imports from package namespaces
#                     added
#    28-Aug-2001 (MG) `pkg_namespace_def_pat` extended (match `From_Import`)
#    28-Aug-2001 (MG) Pass `pkg_path` for recursive calls of `_find_import`
#    13-Nov-2001 (CT) Adapted to nested packages
#    11-Dec-2001 (CT) `_import_module` factored
#    11-Dec-2001 (CT) `prefix` added `path_of` (and `_path_of` factored)
#    11-Dec-2001 (CT) `modules` handling added to `_import_module_from_pkg`
#                     (along with adding `modules` group to
#                     `pkg_namespace_import_pat` and `pkg_namespace_use_pat`)
#    12-Dec-2001 (CT) Argument `pkg_import_path` removed from `_find_import*`
#    12-Dec-2001 (CT) `_import_module_from_pkg` fixed (uses `_import_module`
#                     now and computes `imported` using `pkg_ns_dict [p]`
#                     instead of `p`)
#    12-Dec-2001 (CT) `pkg_ns_dict` replaced by `pkg_ns_adict` and
#                     `pkg_ns_rdict`
#    12-Dec-2001 (CT) Argument `rel_name` added to `_find_imports`
#    14-Mar-2002 (CT) `Package_Namespace` removed
#    14-Mar-2002 (CT) Nested packages supported properly
#    10-Jul-2002 (MG) Error in `path_of` corrected (use `prefix` as well)
#    24-Feb-2004 (CT) Modernizations (e.g., usages of `string` module removed)
#    24-Feb-2004 (CT) `file_dict` added, `_add` factored and changed as to
#                     not put the same file twice into `import_dict`
#                     (happened for TFL.Generator, because the doc-test
#                     imports `Generator` without package prefix)
#     9-Mar-2004 (CT) `_add` changed to write mixed relative and absolute
#                     imports to sys.stderr
#     8-Jun-2004 (CT) `Py_Module` added and used as value in `import_dict`
#     8-Jun-2004 (CT) `seen` added to avoid multiple lookups of irrelevant
#                     modules
#     8-Jun-2004 (CT) Debug code changed and extended
#     8-Jun-2004 (CT) Methods sorted alphabetically
#     8-Jun-2004 (CT) `__sub__` added to `Import_Finder` (and the `-Diff`
#                     option for testing it)
#     9-Jun-2004 (CT) s/Py_Module/P_M/
#     9-Jun-2004 (CT) `P_P` added
#     9-Jun-2004 (CT) `path_of` changed to return `P_M` instances instead of
#                     tuples
#     9-Jun-2004 (CT) `pkg_dict` and `tlp_dict` added
#     9-Jun-2004 (CT) `__sub__` and `__init__` changed so that `__sub__`
#                     returns another instance of `Import_Finder` instead of
#                     a `Record`
#    17-Jun-2004 (CT) Options `-files`, `-packages`, and `-toplevels` added
#    17-Jun-2004 (CT) `__sub__` corrected (call `_add` instead of `add`)
#    17-Jun-2004 (CT) `__sub__` changed to set `pkg_dict` and `tlp_dict` of
#                     result correctly
#    17-Jun-2004 (CT) s/Import_Finder/Import_Closure/g
#    17-Jun-2004 (CT) Debug code removed to make code clearer
#    18-Jun-2004 (CT) s/import_dict/pym_dict/
#    18-Jun-2004 (CT) Replaced `Import_Closure` attributes `file_name`,
#                     `base_name`, and `path_name` by a single attribute
#                     `root_pym`
#    18-Jun-2004 (CT) `_import_root` factored from `__init__` and changed so
#                     that `rel_name` and `pkg` are right
#    18-Jun-2004 (CT) `level` added to `P_M` and used to determine
#                     `is_toplevel`
#    19-Jun-2004 (CT) s/from_text/new/
#    19-Jun-2004 (CT) `remove` added
#    19-Jun-2004 (CT) `__sub__` changed to `_add` packages to delta closure
#                     if some of their modules are in the delta (up to now,
#                     these were only inserted into `pkg_dict` and `tlp_dict`)
#    20-Jun-2004 (CT) `base_name` added to `P_M`
#    21-Jun-2004 (CT) `base_path` added and semantics of `base_name` changed
#    22-Jun-2004 (CT) Creation (factored from find_import_closure.py)
#    ««revision-date»»···
#--

from   _TFL         import TFL
from   Filename     import Filename
from   Regexp       import *
from   predicate    import *
import sos
import sys

import _TFL._Meta.Object

class P_M (TFL.Meta.Object) :
    """Encapsulate a python module found by Import_Closure"""

    is_package = False

    def __init__ (self, rel_name, path_name, pkg) :
        self.rel_name     = rel_name
        self.path_name    = path_name
        _, self.base_path = sos.path.split    (path_name)
        self.base_name, _ = sos.path.splitext (self.base_path)
        self.pkg          = pkg
        self.level        = pkg.count (".")
    # end def __init__

    def __cmp__ (self, rhs) :
        try :
            return cmp (self.path_name, rhs.path_name)
        except AttributeError :
            return cmp (self.path_name, rhs)
    # end def __cmp__

    def __hash__ (self) :
        return hash (self.path_name)
    # end def __hash__

    def __repr__ (self) :
        return "%s (%r, %r, %r)" % \
            (self.__class__.__name__, self.rel_name, self.path_name, self.pkg)
    # end def __repr__

    def __str__ (self) :
        return self.path_name
    # end def __str__

# end class P_M

class P_P (P_M) :
    """Encapsulate a python package found by Import_Closure"""

    is_package   = True
    is_toplevel  = property (lambda s : s.level == 0)

# end class P_P

class Import_Closure :
    """Find all imports from a given python module"""

    import_pat = Regexp \
        ( r"^\s* (?: from | import) \s* "
          r"(?P<imported> [_A-Za-z0-9]+)"
          r"(?: \. (?P<modules> [_A-Za-z0-9.]+))?"
        , re.X
        )

    script_pat = Regexp \
        ( """^if \s+ __name__ \s* == \s* "__[a-z]+__" \s* : $"""
        , re.X
        )

    def __init__ (self, file_name = None, import_path = ("./", ), ignore = None, debug = False) :
        self.import_path  = tuple (import_path)
        self.pym_dict     = {} ### rel-name-sans-extension --> P_M
        self.file_dict    = {} ### path --> rel-name-sans-extension
        self.pkg_dict     = {}
        self.tlp_dict     = {}
        self.seen         = {}
        self.ignore       = ignore or {}
        self.debug        = debug
        self.root_pym     = None
        if file_name :
            self.root_pym = pym = self._import_root (file_name)
            if not pym :
                print "Where is %s?" % (file_name, )
                print "...didn't find it in %s" % (self.import_path, )
                raise ValueError
    # end def __init__

    def as_code (self) :
        pyps = self.pkg_dict.values ()
        pyms = [m for m in self.pym_dict.values ()
                  if not (m.is_package or m == self.root_pym)
               ]
        return "\n    ".join \
            ( [ "%s.new \\"   % (self.__class__.__name__, )
              , "( %r"        % (self.root_pym, )
              , ", %r"        % (self.import_path, )
              , ", %r"        % (self.ignore, )
              ]
            + sorted ([", %r" % (m, ) for m in pyps])
            + sorted ([", %r" % (m, ) for m in pyms])
            + [")"]
            )
    # end def as_code

    def _add (self, pym) :
        if pym.path_name not in self.file_dict :
            self.pym_dict  [pym.rel_name]  = pym
            self.file_dict [pym.path_name] = pym.rel_name
            if pym.is_package :
                self.pkg_dict [pym.pkg] = pym
                if pym.is_toplevel :
                    self.tlp_dict [pym.pkg] = pym
            return True
        else :
            if self.debug :
                print >> sys.stderr, \
                    ( "%s is imported absolutely and relatively: `%s` vs. `%s`"
                    % ( pym.path_name
                      , self.file_dict [pym.path_name], pym.rel_name
                      )
                    )
    # end def _add

    def _find_import (self, imported, prefix = "") :
        if imported in self.seen :
            return True
        else :
            self.seen [imported] = True
            pym = self.path_of (imported, prefix)
            if pym :
                file = Filename (pym.path_name, absolute = True)
                if not self.ignore.has_key (file.base) :
                    if self._add (pym) :
                        self._find_imports (pym.path_name, imported, pym.pkg)
                        return True
    # end def _find_import

    def _find_imports (self, file_name, rel_name, prefix = "") :
        file = open (file_name, "r")
        try :
            import_pat = self.import_pat
            for line in file :
                if self.script_pat.match (line) :
                    break
                if import_pat.match (line) :
                    imported = import_pat.imported
                    self._import_module \
                        (imported, import_pat.last_match, prefix)
        finally :
            file.close ()
    # end def _find_imports

    def _import_module (self, imported, match, prefix) :
        self._find_import (imported, prefix)
        try :
            modules = match.group ("modules")
        except (IndexError, AttributeError) :
            pass
        else :
            package = self.pym_dict.get (imported)
            if modules and package :
                for m in modules.split (".") :
                    imported = sos.path.join (imported, m)
                    if not self._find_import (imported, prefix) :
                        break
    # end def _import_module

    def _import_root (self, file_name) :
        if file_name.startswith (sos.path.sep) :
            for dir in self.import_path :
                if file_name.startswith (dir) :
                    file_name = file_name [len (dir) + 1:]
                    break
        base, _ = sos.path.splitext (file_name)
        name    = base.replace (sos.path.sep, ".")
        line    = "import %s" % (name, )
        match   = self.import_pat.match (line)
        if match :
            self._import_module      (match.group ("imported"), match, "")
            return self.pym_dict.get (base)
        else :
            print name, "doesn't match import pattern"
    # end def _import_root

    def new (cls, root_pym, import_path, ignore, * pyms) :
        result           = cls (import_path = import_path, ignore = ignore)
        result.root_pym  = root_pym
        result._add (root_pym)
        for pym in pyms :
            result._add (pym)
        return result
    new = classmethod (new)

    def path_of (self, py_name, prefix = "") :
        """Return the full path of `py_name' in the list of directories
           `import_path' or `None'.
        """
        if prefix :
            py_names = (py_name, sos.path.join (prefix, py_name))
        else :
            py_names = (py_name, )
        for py_name in py_names :
            for dir in self.import_path :
                result = self._path_of (dir, py_name)
                if result :
                    return result
    # end def path_of

    def _path_of (self, dir, py_name) :
        b_name = sos.path.join (dir, py_name)
        m_name = b_name + ".py"
        p_name = sos.path.join (b_name, "__init__.py")
        if sos.path.isfile (m_name) :
            prefix = ".".join (py_name.split (sos.sep) [:-1])
            return P_M (py_name, m_name, prefix)
        if sos.path.isfile (p_name) :
            prefix = ".".join (py_name.split (sos.sep))
            return P_P (py_name, p_name, prefix)
    # end def _path_of

    def remove (self, pym) :
        """Remove `pym` from import closure"""
        if isinstance (pym, str) :
            pym = self.pym_dict [pym]
        del self.pym_dict [pym.rel_name]
        if pym.pkg in self.pkg_dict :
            del self.pkg_dict [pym.pkg]
        if pym.pkg in self.tlp_dict :
            del self.tlp_dict [pym.pkg]
    # end def remove

    def __sub__ (self, rhs) :
        result = self.__class__.new \
            (self.root_pym, self.import_path, self.ignore)
        for k, pym in self.pym_dict.iteritems () :
            if k not in rhs.pym_dict :
                result._add (pym)
                pn = pym.pkg
                if pn in self.pkg_dict and pn not in result.pkg_dict :
                    result._add (self.pkg_dict [pn])
        return result
    # end def __sub__

# end class Import_Closure

def command_spec (arg_array = None) :
    from   Command_Line import Command_Line
    return Command_Line \
        ( arg_spec    =
            ( "python_module"
            , "import_path=./"
            , "separator= "
            )
        , option_spec =
            ( "-as_code:B?Print import closure as executable python code"
            , "-debug:I=0"
            , "-Diff:S"
                  "?Name of python_module which import closure gets subtracted"
            , "-files:B?Show all files in import closure"
            , "-ignore:S,=U_Test?Ignore modules specified"
            , "-packages:B?Show all packages in import closure"
            , "-Pathsep:S=:?Path separator used by `import_path'"
            , "-toplevels:B?Show all toplevel packages in import closure"
            )
        , min_args    = 1
        , max_args    = 3
        , arg_array   = arg_array
        )
# end def command_spec

def main (cmd) :
    import_path = map (sos.expanded_path, cmd.import_path.split (cmd.Pathsep))
    ignore      = dict_from_list (cmd.ignore)
    out_opts    = sum \
        ( [  bool (o) for o
          in cmd.as_code, cmd.files, cmd.packages, cmd.toplevels
          ]
        )
    result = finder = Import_Closure \
        ( file_name   = cmd.python_module
        , import_path = import_path
        , ignore      = ignore
        , debug       = cmd.debug
        )
    if cmd.Diff :
        result = finder - Import_Closure \
            ( file_name   = cmd.Diff
            , import_path = import_path
            , ignore      = ignore
            , debug       = cmd.debug
            )
    sep = cmd.separator
    if sep == r"\n" :
        sep = "\n"
    if cmd.as_code :
        print result.as_code ()
    if cmd.toplevels :
        print sep.join \
            (sorted ([m.pkg for m in result.tlp_dict.values ()]))
    if cmd.packages :
        print sep.join \
            (sorted ([m.pkg for m in result.pkg_dict.values ()]))
    if cmd.files or not out_opts :
        print sep.join \
            (sorted ([str (m) for m in result.pym_dict.values ()]))
# end def main

if __name__ == "__main__":
    main (command_spec ())
else :
    TFL._Export ("Import_Closure")
### __END__ Import_Closure
