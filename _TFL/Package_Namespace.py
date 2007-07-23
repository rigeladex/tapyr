# -*- coding: iso-8859-1 -*-
# Copyright (C) 2001-2006 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
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
#    TFL.Package_Namespace
#
# Purpose
#    Implement a namespace for python packages providing direct access to
#    classes and functions implemented in the modules of the package
#
# Revision Dates
#     7-May-2001 (CT)  Creation
#     2-Jul-2001 (CT)  Docstring extended
#     2-Jul-2001 (CT)  Use `` instead of `' to quote inside docstrings and
#                      comments
#    27-Jul-2001 (CT)  `Import` changed to support `*`
#    30-Jul-2001 (CT)  `*` import corrected
#    30-Jul-2001 (CT)  `_import_1` and `_import_name` factored
#    31-Jul-2001 (CT)  `From_Import` added (and `_import_symbols` factored)
#     2-Aug-2001 (CT)  `_Module_Space` added and used to separate namespace
#                      for modules provided by the package from the namespace
#                      for classes and functions provided by the package
#     3-Aug-2001 (CT)  `Import_Module` added
#    16-Aug-2001 (CT)  `_import_1` fixed to correctly check for name clashes
#    19-Aug-2001 (CT)  `_import_names` changed to raise `ImportError` if
#                      necessary
#    19-Aug-2001 (CT)  `__getattr__` raises `AttributeError` instead of
#                      `ImportError` for `__*__`
#    22-Aug-2001 (CT)  `transitive` added
#    20-Sep-2001 (MG)  `_import_names`: import name they are defined in the
#                      modul to be imported or if `getmodule` returns `None`
#    20-Sep-2001 (CT)  Change of MG revoked
#    20-Sep-2001 (CT)  Don't *-import names with leading underscores
#     3-Nov-2001 (MG)  import `TFL.Caller` instead of `Caller`
#     8-Nov-2001 (CT)  `Essence` added to handle TOM.Class_Proxy correctly
#    13-Nov-2001 (CT)  `_import_symbols` corrected to handle empty `symbols`
#                      correctly
#    13-Nov-2001 (CT)  Unncessary restriction of nested packages removed
#     5-Dec-2001 (MG)  Special code for `Proxy_Type` changed
#    20-Feb-2002 (CT)  `_Export` and `XXX PPP` comments added
#    21-Feb-2002 (CT)  `_Module_Space._load` factored
#    22-Feb-2002 (CT)  `_leading_underscores` added and used to remove leading
#                      underscores from `Package_Namespace.__name`
#    22-Feb-2002 (CT)  `_debug` added and used to guard `XXX PPP` prints
#    25-Feb-2002 (CT)  `_complain_implicit` factored
#    25-Feb-2002 (CT)  Kludge to add `FOO` alias to sys.modules for package
#                      `_FOO` (otherwise binary databases with old-style
#                      packages don't load <sigh>)
#    26-Feb-2002 (CT)  `_debug` set to `__debug__`
#    26-Feb-2002 (CT)  `_complain_implicit` changed to provide more useful
#                      output (included addition of `last_caller`)
#    27-Feb-2002 (CT)  Argument `module_name` removed from `_Export` (get that
#                      from `caller_globals`)
#    12-Mar-2002 (CT)  `_Export_Module` added
#    12-Mar-2002 (CT)  Use `TFL.Module.names_of` instead of half-broken
#                      `inspect.getmodule`
#    15-Mar-2002 (CT)  `Import` renamed to `__Import`
#                      `_import_symbols` renamed to `__import_symbols`
#    15-Mar-2002 (CT)  `From_Import` and `Import_Module` removed
#    18-Mar-2002 (MG)  `_Add` added
#    18-Mar-2002 (CT)  `_complain_implicit` changed to write new syntax
#    28-Mar-2002 (CT)  Last remnants of implicit imports removed
#     3-Sep-2002 (CT)  Comment added to `_Module_Space._load` to explain why
#                      `__import__` is used in the particular way it is
#     8-Oct-2002 (CT)  Pass `None` as fourth argument to `__import__` to avoid
#                      annoying Gordon McMillan
#    11-Oct-2002 (CT)  Change of `8-Oct-2002` backed out because it doesn't
#                      work with McMillan
#     4-Feb-2003 (CT)  `Derived_Package_Namespace` added
#     8-Apr-2003 (CT)  `_leading_underscores` changed to consider `._` too
#     8-Apr-2003 (CT)  `qname` added
#     8-Apr-2003 (CT)  `pname` added
#     8-Apr-2003 (CT)  Compatibility kludge of putting `Package_Namespace`
#                      into `sys.modules` removed (it was too smelly)
#    28-Jul-2003 (CT)  `_Reload` added
#     1-Aug-2003 (CT)  `_Reload` changed to reload in same sequence as
#                      original import
#    12-Sep-2003 (CT)  `_Reload` changed to clear the damned `linecache`
#    20-Nov-2003 (CT)  `_Export_Module` changed to take `mod` from `kw` if
#                      there
#    16-Jun-2004 (CT)  `_Module_Space._load` changed to
#                      - use `sys.modules` instead of `__import__`
#                      - accept `q_name` as argument
#    16-Jun-2004 (CT)  `Package_Namespace._Load_Module` factored
#     5-Jul-2004 (CT)  `__name__` set for `Package_Namespace` instances to
#                      make them more similar to modules
#     4-Aug-2004 (MG)  `Package_Namespace._Import_Module` added
#    28-Sep-2004 (CT)  Use `isinstance` instead of type comparison
#    23-Oct-2004 (CT)  `_check_clashes` added
#    28-Oct-2004 (CT)  `_Export_Module` changed to honor `_check_clashes`
#    10-Jan-2005 (CT)  `__repr__` changed to not future warn about negative
#                      values of `id`
#    14-Jan-2005 (CT)  `_DPN_Auto_Importer_` added and called by
#                      `Derived_Package_Namespace`
#    20-Jan-2005 (CT)  `_DPN_Auto_Importer_.__call__` changed to ignore
#                      transitive import errors
#    24-Jan-2005 (CT)  Change of `20-Jan-2005` fixed
#    24-Jan-2005 (CT)  `_Import_Module` changed to return the imported module
#                      (and rest-args removed)
#    10-Feb-2005 (CT)  `_Export` changed to streamline `*` handling
#    10-Feb-2005 (CT)  More documentation added
#    24-Mar-2005 (CT)  Dependencies on non-standard-lib modules removed
#                      - Use `re` instead of `Regexp`
#                      - Unused import of `caller_info` removed
#                      - Import of `caller_globals` replaced by home-grown code
#    30-Mar-2005 (CED) `_name`, `_qname` added to `_Module_Space`
#    26-Apr-2006 (PGO) [rup18983] renamed classes with leading underscore
#    28-Jul-2006 (PGO) Replaced `_DPN_Auto_Importer_` with TFL.DPN_Importer
#    31-Jul-2006 (PGO) `DPN_Importer.register` introduced
#     7-Nov-2006 (PGO) Reloading now also works with `_Add`
#    23-Jul-2007 (CED) Activated absolute_import
#    ««revision-date»»···
#--
from __future__ import absolute_import


import re
import sys
from   _TFL.Importers  import  DPN_Importer

def _caller_globals () :
    return sys._getframe (1).f_back.f_globals
# end def _caller_globals

class _Module_Space_ :

    def __init__ (self, name, qname) :
        self.__name = self._name = name
        self._qname              = qname
    # end def __init__

    def _load (self, q_name, module_name) :
        module = sys.modules [q_name]
        setattr (self, module_name, module)
        return module
    # end def _load


# end class _Module_Space_

class Package_Namespace (object) :
    """Implement a namespace for python packages providing direct access to
       classes and functions implemented in the modules of the package.

       In the following, a package Foo_Package and module Bar are assumed as
       example.

       A Python package encapsulates a number of modules. Packages are useful
       for avoiding name clashes between modules of different domains. For
       instance, `Frame` might be used as module name by a GUI package and by
       a communications package.

       Many modules define a class or function with the same name as
       the module name. There are different styles how to access such a
       class::

           #1
           import Bar
           instance = Bar.Bar ()

           #2
           from Bar import Bar
           instance = Bar ()

       Many Pythoneers use the `Bar.Bar` notation to refer to the class `Bar`
       defined by module `Bar`. I strongly prefer to use `Bar` to refer to
       the class.

       In the presence of packages, there are even more possibilities::

           #3
           import Foo_Package.Bar
           instance = Foo_Package.Bar.Bar ()

           #4
           from Foo_Package import Bar
           instance = Bar.Bar ()

           #5
           from Foo_Package.Bar import Bar
           instance = Bar ()

       If one wants to avoid name clashes only #3 is usable. Unfortunately,
       this makes for very verbose and unreadable code. One way to avoid this
       is to import all classes/functions of all modules of the package in
       the `__init__.py`. The disadvantages of this approach are

       - Import bloat. Importing the package will pull in the entire contents
         of the package even if only a tiny part of it is needed.

       - If the package qualifier is to used inside the package too (strongly
         recommended), circular imports will result.

         Using the package name to qualify class and function names defined
         by the modules of the package considerably eases using grep for
         finding occurences of their use.

       `Package_Namespace` provides another option::

           #6
           from   Foo_Package import Foo
           import Foo_Package.Bar
           instance = Foo.Bar ()

       In order to support this, `Foo_Package/__init__.py` must export an
       instance `Foo` of class `Package_Namespace`::

           ### Foo_Package/__init__.py
           from _TFL.Package_Namespace import Package_Namespace
           Foo = Package_Namespace ()

       The Package_Namespace provides the `_Export` method called by modules
       of the package to export classes/functions module into the namespace::

           ### Foo_Package.Bar puts `Bar` and `Baz` into the Package_Namespace
           Foo._Export ("Bar", "Baz")

       `_Export` accepts "*" as a wild card and uses Python's rules to expand
       that with the important caveat, that here "*" only includes functions
       and classes defined by the calling module (i.e., "*" doesn't work
       transitively).

       If a module prefers to put itself instead of some of its attributes
       (functions/classes/whatever) into the Package_Namespace, it can do so
       by calling

           Foo._Export_Module ()

       The modules of the package can be accessed via the `_` attribute of
       the package namespace.
    """

    _leading_underscores = re.compile (r"(\.|^)_+")
    _check_clashes       = True

    def __init__ (self, name = None, pname = None) :
        if not pname :
            pname = _caller_globals () ["__name__"]
        if not name :
            name = pname
        qname = self._leading_underscores.sub (r"\1", name) ### XXX s/\._/_/
        bname = qname.split (".") [-1]
        self.__name         = bname
        self.__qname        = self.__name__ = qname
        self.__pname        = pname
        self.__module_space = self._ = _Module_Space_ (pname, qname)
        self.__modules      = {}
        self.__seen         = {}
        self.__reload       = 0
    # end def __init__

    def _import_names (self, mod, names, result, check_clashes) :
        for name in names :
            if isinstance (name, str) :
                name, as_name = name, name
            else :
                name, as_name = name
            try :
                p = getattr (mod, name)
                self._import_1 (mod, name, as_name, p, result, check_clashes)
            except AttributeError :
                raise ImportError, ( "cannot import name %s from %s"
                                   ) % (name, mod.__name__)
    # end def _import_names

    def _import_1 (self, mod, name, as_name, object, result, check_clashes) :
        if __debug__ :
            old = self.__dict__.get (name, object)
            if check_clashes and old is not object :
                raise ImportError, ( "ambiguous name %s refers to %s and %s"
                                   ) % (name, object, old)
        result [as_name] = object
    # end def _import_1

    def __repr__ (self) :
        return "<%s %s>" % \
               (self.__class__.__name__, self.__name)
    # end def __repr__

    def _Cache_Module (self, module_name, mod) :
        if not module_name in self.__modules :
            p = len (self.__modules)
        else :
            m, p = self.__modules [module_name]
        self.__modules [module_name] = (mod, p)
    # end def _Cache_Module

    def _Add (self, ** kw) :
        """Add elements of `kw` to Package_Namespace `self`."""
        module_name, mod = self._Load_Module (_caller_globals ())
        check_clashes    = self._check_clashes and not self.__reload
        self._Cache_Module (module_name, mod)
        for s, p in kw.items () :
            self._import_1 (mod, s, s, p, self.__dict__, check_clashes)
    # end def _Add

    def _Export (self, * symbols, ** kw) :
        """To be called by modules of Package_Namespace to inject their
           symbols into the package namespace `self`.
        """
        result         = {}
        caller_globals = _caller_globals ()
        transitive     = kw.get ("transitive")
        mod            = kw.get ("mod")
        if mod is None :
            module_name, mod = self._Load_Module (caller_globals)
        else :
            module_name      = caller_globals ["__name__"].split (".") [-1]
        primary        = getattr (mod, module_name, None)
        check_clashes  = self._check_clashes and not self.__reload
        if primary is not None :
            result [module_name] = primary
        self._Cache_Module (module_name, mod)
        if symbols [0] == "*" :
            all_symbols = getattr (mod, "__all__", ())
            if all_symbols :
                self._import_names (mod, all_symbols, result, check_clashes)
            else :
                from   _TFL import TFL
                import _TFL.Module
                for s in TFL.Module.names_of (mod) :
                    if not s.startswith ("_") :
                        p = getattr (mod, s)
                        self._import_1 (mod, s, s, p, result, check_clashes)
            symbols = symbols [1:]
        if symbols :
            self._import_names (mod, symbols, result, check_clashes)
        self.__dict__.update (result)
    # end def _Export

    def _Export_Module (self) :
        """To be called by modules to inject themselves into the package
           namespace `self`.
        """
        module_name, mod = self._Load_Module (_caller_globals ())
        if __debug__ :
            old = self.__dict__.get (module_name, mod)
            check_clashes = self._check_clashes and not self.__reload
            if old is not mod and check_clashes :
                raise ImportError, ( "ambiguous name %s refers to %s and %s"
                                   ) % (module_name, mod, old)
        self.__dict__  [module_name] = mod
        self._Cache_Module (module_name, mod)
    # end def _Export_Module

    def _Load_Module (self, caller_globals) :
        q_name = caller_globals ["__name__"]
        b_name = q_name.split   (".") [-1]
        return b_name, self.__module_space._load (q_name, b_name)
    # end def _Load_Module

    def _Reload (self, * modules) :
        old_reload = self.__reload
        if not modules :
            from _TFL.predicate import dusort
            second  = lambda (a, b) : b
            modules = \
                [m for (m, i) in dusort (self.__modules.values (), second)]
        try :
            self.__reload = 1
            print "Reloading", self.__name,
            for m in modules :
                print m.__name__,
                reload (m)
            print "finished"
        finally :
            self.__reload = old_reload
        import linecache
        linecache.clearcache ()
    # end def _Reload

    def _Import_Module (self, module) :
        import _TFL.import_module ### avoid circular imports !!!
        return _TFL.import_module.import_module \
            (".".join ((self.__pname, module)))
    # end def _Import_Module

# end class Package_Namespace


class Derived_Package_Namespace (Package_Namespace) :
    """Implement a derived Package_Namespace which adds to an existing
       Package_Namespace.

       Derivation of Package_Namespaces is similar to inheritance between
       classes -- the derived Package_Namespace

       - can add new modules to the ones inherited

       - can modify some properties of inherited modules (by defining a
         module of the same name which defines sub-classes and/or
         functions overriding the original functions)

       To transparently support inheritance-like import behavior,
       Derived_Package_Namespace allows to import modules of the base
       Package_Namespace through the Derived_Package_Namespace. For instance,
       consider a package `_B` defining a Package_Namespace `B` and a
       package `_D` defining a Derived_Package_Namespace `D` based on `B`::

           ### _B/__init__.py  <---derived-from----  _D/__init__.py
           ###    X.py                                  X.py
           ###    Y.py
           ###                                          Z.py

           from   _D import D
           import _D.X        ### imports from _D/X.py
           import _D.Y        ### imports from _B/Y.py
           import _D.Z        ### imports from _D/Z.py

       For derived imports to work, the Derived_Package_Namespace must be
       imported before the module needing import derivation is imported (this
       only is important for nested Package_Namespaces).
    """

    def __init__ (self, parent, name = None) :
        pname = _caller_globals () ["__name__"]
        if not name :
            name = pname
        Package_Namespace.__init__ (self, name, pname)
        self._parent  = parent
        self.__cached = {}
        mod           = sys.modules [pname]
        DPN_Importer.register (mod, pname, parent)
    # end def __init__

    def __getattr__ (self, name) :
        result  = getattr (self._parent, name)
        self.__cached [name] = result
        setattr (self, name, result)
        return  result
    # end def __getattr__

    def _Reload (self, * modules) :
        for c in self.__cached.iterkeys () :
            delattr (self, c)
        self.__cached = {}
        self._parent._Reload ()
        Package_Namespace._Reload (self, * modules)
    # end def _Reload

# end class Derived_Package_Namespace

### __END__ TFL.Package_Namespace
