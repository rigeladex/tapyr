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
#    ««revision-date»»···
#--

from   Caller  import globals as _caller_globals
import inspect

class Package_Namespace :
    """Implement a namespace for python packages providing direct access to
       classes and functions implemented in the modules of the package.

       Caveat: this doesn't work for nested packages.

       In the following, a package Foo_Package and module Bar are assumed as
       example. 

       A Python package encapsulates a number of module. Packages are useful
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
    """
    
    def __init__ (self, name = None) :
        if not name :
            name = _caller_globals () ["__name__"]
        self._name = name
        self._seen = {}
    # end def __init__
    
    def Import (self, module_name, * symbols) :
        """Import all `symbols` from module `module_name` of package
           `self._name`.
        """
        if not self._seen.has_key ((module_name, symbols)) :
            pkg = __import__ \
                ("%s.%s" % (self._name, module_name), _caller_globals ())
            mod = getattr (pkg, module_name)
            if len (symbols) == 1 and symbols [0] == "*" :
                symbols = getattr (mod, "__all__", ())
                if symbols :
                    for s in symbols :
                        try :
                            self._import_1 (mod, s.__name__, s)
                        except AttributeError :
                            self._import_name (mod, s)
                else :
                    for s, p in mod.__dict__.items () :
                        if inspect.getmodule (p) is mod :
                            self._import_1 (mod, s, p)
            elif symbols :
                for s in symbols :
                    self._import_name (mod, s)
            else :
                self.__dict__ [module_name] = mod
            self._seen [(module_name, symbols)] = 1
    # end def Import

    def _import_name (self, mod, name) :
        p = getattr (mod, name, None)
        if p is not None :
            self._import_1 (mod, name, p)
    # end def _import_name    

    def _import_1 (self, mod, name, object) :
        if __debug__ :
            if self.__dict__.get (name, object) is not object :
                raise ImportError, "%s %s %s" % \
                                   (name, object, self.__dict__.get (name))
        self.__dict__ [name] = object
        try :
            if not hasattr (object, "Module") :
                object.Module = mod
        except TypeError :
            pass
    # end def _import_1
    
    def __getattr__ (self, name) :
        if not (name.startswith ("__") and name.endswith ("__")) :
            self.Import (name, name)
            return self.__dict__ [name]
        raise AttributeError, name
    # end def __getattr__

    def __repr__ (self) :
        return "<%s %s at 0x%x>" % \
               (self.__class__.__name__, self._name, id (self))
    # end def __repr__
    
# end class Package_Namespace

### __END__ Package_Namespace
