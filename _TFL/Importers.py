# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006 Christian Eder, Philipp Gortan <{ced,pgo}@tttech.com>
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# ****************************************************************************
#
#++
# Name
#    TFL.Importers
#
# Purpose
#    Provide Custom import hooks
#
# Revision Dates
#    25-Jul-2006 (PGO) Creation
#    28-Jul-2006 (PGO) Creation continued
#    31-Jul-2006 (PGO) `register` added, `_find_module` for builtin import fixed
#     3-Aug-2006 (PGO) `_find_module` for TTP-View fixed
#    ««revision-date»»···
#--

import imp
import os
import sys
import zipimport

DERIVED_PNS_TOKEN = "?Derived"

class M_DPN_Importer (type) :
    """Metaclass for derived package namespace importer.
       When called with a path item that marks derived package namespaces,
       it returns the appropriate DPN importer.
    """

    def __call__ (cls, path) :
        if path.startswith (DERIVED_PNS_TOKEN) :
            token_lst = path.split (",")
            name      = token_lst [1 ]
            pns_chain = token_lst [2:]
            i         = \
                (   getattr (sys, "frozen", False)
                and _DPN_ZipImporter_ or _DPN_Builtin_Importer_
                )
            return super (M_DPN_Importer, i).__call__ (name, pns_chain)
        else :
            raise ImportError ### not derived - pass on to next importer
    # end def __call__

# end class M_DPN_Importer

class DPN_Importer (object) :
    """Implements an import hook for derived package namesapces,
       according PEP 302. For the derived and all parent namespaces,
       try to find the module.
    """
    __metaclass__ = M_DPN_Importer

    def __init__ (self, name, pns_chain) :
        self.name      = name
        self.pns_chain = pns_chain
        self._cache    = {}
    # end def __init__

    def find_module (self, fullmodule, path = None) :
        assert not path
        for pns in self.pns_chain :
            cand = fullmodule.replace (self.name, pns, 1)
            i    = self._find_module (cand, fullmodule)
            if i :
                return i
        raise ImportError
    # end def find_module

    def load_module (self, fullmodule) :
        realmodule, finder_info = self._cache.pop (fullmodule)
        if realmodule in sys.modules :
            return sys.modules [realmodule]
        mod            = self._load_module (realmodule, finder_info)
        mod.__loader__ = self
        assert realmodule in sys.modules
        sys.modules [fullmodule] = mod
        return mod
    # end def load_module

    @classmethod
    def register (cls, mod, name, parent) :
        if not hasattr (mod, "__path__") :
            return ### a Package_Namespace is not always a package *argh*
        token = [DERIVED_PNS_TOKEN, name]
        while parent :
            token.append (parent._._name)
            parent = getattr (parent, "_parent", None)
        mod.__path__.append (",".join (token))
    # end def register

    def __repr__ (self) :
        return \
            ( "<%s for %s p=[%s]>"
            % (self.__class__.__name__, self.name, " ".join (self.pns_chain))
            )
    # end def __repr__

# end class DPN_Importer

class _DPN_Builtin_Importer_ (DPN_Importer) :
    """Use the builtin import mechanism (as exposed by the imp module) for
       importing.
    """
    def _find_module (self, cand, fullmodule) :
        pkg, mod = cand.rsplit (".", 1)
        path     = sys.modules [pkg].__path__ ### the pkg is already imported
        try :
            res = imp.find_module (mod, path)
        except ImportError :
            return
        self._cache [fullmodule] = (cand, res)
        return self
    # end def _find_module

    def _load_module (self, realmodule, res) :
        return imp.load_module (realmodule, * res)
    # end def _load_module

# end class _DPN_Builtin_Importer_

class _DPN_ZipImporter_ (DPN_Importer) :
    """Use the executable itself in conjunction with Python's zipimporter
       for importing.
    """
    def __init__ (self, name, pns_chain) :
        super (_DPN_ZipImporter_, self).__init__ (name, pns_chain)
        self._path = reversed (sys.path) ### currently it's always the last one
    # end def __init__

    def _find_module (self, cand, fullmodule) :
        cand_lst = cand.split (".")
        for p in self._path :
            zip_path = os.sep.join ([p] + cand_lst [:-1])
            zi       = \
                (  sys.path_importer_cache.get (zip_path)
                or zipimport.zipimporter       (zip_path)
                )
            if zi :
                break
        else :
            return
        mod = cand_lst [-1]
        res = zi.find_module (mod)
        if res :
            self._cache [fullmodule] = (cand, (mod, res))
            return self
    # end def _find_module

    def _load_module (self, realmodule, (module, loader)) :
        mod = loader.load_module (module)
        sys.modules [realmodule] = mod
        return mod
    # end def _load_module

# end class _DPN_ZipImporter_

if __name__ != '__main__' :
    if DPN_Importer not in sys.path_hooks :
        sys.path_hooks.insert (0, DPN_Importer)

### end TFL.Importers
