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
#    ««revision-date»»···
#--

from caller_globals import caller_globals as _caller_globals

class Package_Namespace :
    """Implement a namespace for python packages providing direct access to
       classes and functions implemented in the modules of the package.

       This doesn't work for nested packages.
    """
    
    def __init__ (self, name = None) :
        if not name :
            name = _caller_globals () ["__name__"]
        self._name = name
        self._seen = {}
    # end def __init__
    
    def Import (self, module_name, * symbols) :
        """Import all `symbols' from module `module_name' of package
           `self._name'.
        """
        if not self._seen.has_key ((module_name, symbols)) :
            pkg = __import__ \
                ("%s.%s" % (self._name, module_name), _caller_globals ())
            mod = getattr (pkg, module_name)
            for s in symbols or [module_name] :
                self.__dict__ [s] = getattr (mod, s)
            self._seen [(module_name, symbols)] = 1
    # end def Import
    
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
