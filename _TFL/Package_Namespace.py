#! /usr/bin/python
# Copyright (C) 2001 Mag. Christian Tanzer. All rights reserved
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
#    Package_Namespace
#
# Purpose
#    Implement a namespace for python packages providing direct access to
#    classes and functions implemented in the modules of the package
#
# Revision Dates
#     7-May-2001 (CT) Creation
#     2-Jul-2001 (CT) Docstring extended
#     2-Jul-2001 (CT) Use `` instead of `' to quote inside docstrings and
#                     comments
#    27-Jul-2001 (CT) `Import` changed to support `*`
#    30-Jul-2001 (CT) `*` import corrected
#    30-Jul-2001 (CT) `_import_1` and `_import_name` factored
#    31-Jul-2001 (CT) `From_Import` added (and `_import_symbols` factored)
#     2-Aug-2001 (CT) `_Module_Space` added and used to separate namespace
#                     for modules provided by the package from the namespace
#                     for classes and functions provided by the package
#     3-Aug-2001 (CT) `Import_Module` added
#    16-Aug-2001 (CT) `_import_1` fixed to correctly check for name clashes
#    19-Aug-2001 (CT) `_import_names` changed to raise `ImportError` if
#                     necessary
#    19-Aug-2001 (CT) `__getattr__` raises `AttributeError` instead of
#                     `ImportError` for `__*__`
#    22-Aug-2001 (CT) `transitive` added
#    20-Sep-2001 (MG) `_import_names`: import name they are defined in the
#                     modul to be imported or if `getmodule` returns `None`
#    20-Sep-2001 (CT) Change of MG revoked
#    20-Sep-2001 (CT) Don't *-import names with leading underscores
#     3-Nov-2001 (MG) import `TFL.Caller` instead of `Caller`
#     8-Nov-2001 (CT) `Essence` added to handle TOM.Class_Proxy correctly
#    13-Nov-2001 (CT) `_import_symbols` corrected to handle empty `symbols`
#                     correctly
#    13-Nov-2001 (CT) Unncessary restriction of nested packages removed
#     5-Dec-2001 (MG) Special code for `Proxy_Type` changed
#    20-Feb-2002 (CT) `_Export` and `XXX PPP` comments added
#    21-Feb-2002 (CT) `_Module_Space._load` factored
#    22-Feb-2002 (CT) `_leading_underscores` added and used to remove leading
#                     underscores from `Package_Namespace.__name`
#    ««revision-date»»···
#--

from   caller_globals import caller_globals as _caller_globals
from   caller_globals import caller_info    as _caller_info
import inspect                              as _inspect
from   Regexp         import Regexp

_debug = 0

class _Module_Space :

    def __init__ (self, name) :
        self.__name = name
    # end def __init__

    def __getattr__ (self, module_name) :
        if _debug :
            print "XXX PNS Implicit import %s._.%s by %s" \
                  % (self.__name, module_name, _caller_info ())
        return self._load (module_name)
    # end def __getattr__

    def _load (self, module_name) :
        module = __import__ \
            ("%s.%s" % (self.__name, module_name), {}, {}, (module_name, ))
        setattr (self, module_name, module)
        return module
    # end def _load

# end class _Module_Space

class Package_Namespace :
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
           from Foo_Package import Foo
           instance = Foo.Bar ()

       In order to support this, `Foo_Package/__init__.py` must export an
       instance `Foo` of class `Package_Namespace`::

           ### Foo_Package/__init__.py
           from TFL.Package_Namespace import Package_Namespace
           Foo = Package_Namespace ()

       The Package_Namespace provides the `Import` method to import
       classes/functions from a module into the namespace::

           ### import `Bar` and `Baz` from Foo.Bar
           Foo.Import ("Bar", "Bar", "Baz")

       To make up for the slight clumsiness of the `Import` call, the
       Package_Namespace instance will automagically import any
       classes/modules into the namespace when an unknown attribute is
       referenced via an expression like `Foo.Fubar`.

       The modules of the package will be visible via the `_` attribute of
       the package namespace. Modules can be imported explicitly into `_` by
       calling `Import_Module`.
    """

    _leading_underscores = Regexp ("^_+")

    def __init__ (self, name = None) :
        if not name :
            name = _caller_globals () ["__name__"]
        self.__name    = self._leading_underscores.sub ("", name)
        self.__modules = self._ = _Module_Space (name)
        self.__seen    = {}
    # end def __init__

    def Import (self, module_name, * symbols) :
        ### XXX PNS remove after Package_Namespace transition is complete
        """Import all `symbols` from module `module_name` of package
           `self.__name`. A `*` is supported as the first element of
           `symbols` and imports the contents of `__all__` (if defined) or
           all objects defined by the module itself (i.e., no transitive
           imports).

           The elements of `symbols` can be strings or 2-tuples. Each 2-tuple
           specifies a named to be imported followed by the name used for the
           imported object (i.e., `(foo, bar)` is analogous to
           `import foo as bar`)
        """
        if not self.__seen.has_key ((module_name, symbols)) :
            self.__dict__.update \
                (self._import_symbols (module_name, 1, * symbols))
            self.__seen [(module_name, symbols)] = 1
    # end def Import

    def Import_Module (self, module_name) :
        ### XXX PNS remove after Package_Namespace transition is complete
        """Import module `module_name` into `self._`."""
        return self.__modules._load (module_name)
    # end def Import_Module

    def From_Import (self, module_name, * symbols, ** kw) :
        ### XXX PNS remove after Package_Namespace transition is complete
        """Import all `symbols` from module `module_name` of package
           `self.__name` into caller's namespace. A `*` is supported as the
           first element of `symbols` and imports the contents of `__all__`
           (if defined) or all objects defined by the module itself (i.e., no
           transitive imports).

           The elements of `symbols` can be strings or 2-tuples. Each 2-tuple
           specifies a named to be imported followed by the name used for the
           imported object (i.e., `(foo, bar)` is analogous to
           `import foo as bar`)
        """
        _caller_globals ().update \
            (self._import_symbols (module_name, 0, * symbols, ** kw))
    # end def From_Import

    def _import_symbols (self, module_name, check_clashes, * symbols, ** kw) :
        ### XXX PNS remove after Package_Namespace transition is complete
        result     = {}
        mod        = self.__modules._load (module_name)
        star       = None
        transitive = kw.get ("transitive")
        if not symbols :
            symbols = (module_name, )
        if symbols [0] == "*" :
            all_symbols = getattr (mod, "__all__", ())
            if all_symbols :
                self._import_names (mod, all_symbols, result, check_clashes)
            else :
                for s, p in mod.__dict__.items () :
                    if s.startswith ("_") :
                        continue
                    p_mod = _inspect.getmodule (p)
                    if p_mod is None :
                        ### handle Class_Proxy correctly
                        try :
                            if isinstance (p, type (self)) :
                                p_mod = _inspect.getmodule \
                                    (p.__dict__.get ("Essence", p))
                        except :
                            print s, p, mod
                            raise
                    if transitive or p_mod is mod :
                        self._import_1 (mod, s, s, p, result, check_clashes)
            symbols = symbols [1:]
            star    = 1
        if symbols :
            self._import_names (mod, symbols, result, check_clashes)
        return result
    # end def _import_symbols

    def _import_names (self, mod, names, result, check_clashes) :
        for name in names :
            if isinstance (name, type ("")) :
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
            if (   check_clashes
               and self.__dict__.get (name, object) is not object
               ) :
                raise ImportError, ( "ambiguous name %s refers to %s and %s"
                                   ) % (name, object, self.__dict__.get (name))
        result [as_name] = object
    # end def _import_1

    def __getattr__ (self, name) :
        if not (name.startswith ("__") and name.endswith ("__")) :
            if _debug :
                print "XXX PNS Implicit import %s.%s by %s" \
                      % (self.__name, name, _caller_info ())
            self.Import (name, name)
            return self.__dict__ [name]
        raise AttributeError, name
    # end def __getattr__

    def __repr__ (self) :
        return "<%s %s at 0x%x>" % \
               (self.__class__.__name__, self.__name, id (self))
    # end def __repr__

    def _Export (self, module_name, * symbols, ** kw) :
        """Called by module of Package_Namespace to inject their symbols into
           the package namespace.
        """
        transitive = kw.get ("transitive")
        result     = {}
        mod        = self.__modules._load (module_name)
        primary    = getattr (mod, module_name, None)
        if primary is not None :
            result [module_name] = primary
        if symbols [0] == "*" :
            all_symbols = getattr (mod, "__all__", ())
            if all_symbols :
                self._import_names (mod, all_symbols, result, 1)
            else :
                for s, p in mod.__dict__.items () :
                    if s.startswith ("_") :
                        continue
                    p_mod = _inspect.getmodule (p)
                    if p_mod is None :
                        ### handle Class_Proxy correctly
                        try :
                            if isinstance (p, type (self)) :
                                p_mod = _inspect.getmodule \
                                    (p.__dict__.get ("Essence", p))
                        except :
                            print s, p, mod
                            raise
                    if transitive or p_mod is mod :
                        self._import_1 (mod, s, s, p, result, 1)
            symbols = symbols [1:]
        if symbols :
            self._import_names (mod, symbols, result, 1)
        self.__dict__.update (result)
    # end def _Export

# end class Package_Namespace

### __END__ Package_Namespace
