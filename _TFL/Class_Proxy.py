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
#    Class_Proxy
#
# Purpose
#    Transparent proxy for a class
#
# Revision Dates
#     5-Feb-2001 (CT) Creation
#    19-Jul-2001 (CT) Redefinition of `__call__` replaced by aliasing
#                     `__call__` to `Class`
#    17-Aug-2001 (CT) Define `__call__` as method instead of assigning it
#                     to `_Class` inside `__init__` (otherwise, descendent
#                     classes have a hard time redefining `__call__`)
#    ««revision-date»»···
#--

class Class_Proxy :
    """Transparent proxy for a class."""
    
    def __init__ (self, Class) :
        self.__dict__ ["_Class"]   = Class
    # end def __init__
    
    def __getattr__ (self, name) :
        if not (name.startswith ("__") and name.endswith ("__")) :
            return self._delegate_attribute (name)
        raise AttributeError, name
    # end def __getattr__

    def __call__ (self, * args, ** kw) :
        self._Class (* args, ** kw)
    # end def __call__
    
    def __hash__ (self) :
        return hash (self._Class)
    # end def __hash__
    
    def __str__ (self) :
        return str (self._Class)
    # end def __str__
    
    def __repr__ (self) :
        return "<%s for %s at 0x%X>" % ( self.__class__.__name__
                                       , repr (self._Class)
                                       , id   (self)
                                       )
    # end def __repr__
    
    def __setattr__ (self, name, value) :
        setattr (self._Class, name, value)
    # end def __setattr__
    
    def _delegate_attribute (self, name) :
        """Redefine in descendents as necessary"""
        return getattr (self._Class, name)
    # end def _delegate_attribute
    
# end class Class_Proxy

import __builtin__

def isinstance_cp (object, C, isinstance = __builtin__.isinstance) :
    ### print "isinstance", object, C
    ### from caller_globals import caller_info
    ### print "isinstance", caller_info ()
    if hasattr (C, "_Class") :
        C = C._Class
    return isinstance (object, C)
# end def isinstance_cp

def issubclass_cp (C, B, issubclass = __builtin__.issubclass) :
    ### print "issubclass", C, B
    ### from caller_globals import caller_info
    ### print "isinstance", caller_info ()
    if hasattr (C, "_Class") : C = C._Class
    if hasattr (B, "_Class") : B = B._Class
    return issubclass (C, B)
# end def issubclass_cp

del __builtin__

### the following would redefine the __builtin__ functions isinstance and
### issubclass which is too radical
### 
### def _fix_builtins () :
###     import __builtin__
### 
###     def isinstance (object, C, isinstance = __builtin__.isinstance) :
###         ### print "isinstance", object, C
###         from caller_globals import caller_info
###         print "isinstance", caller_info ()
###         if hasattr (C, "_Class") :
###             C = C._Class
###         return isinstance (object, C)
###     isinstance.__doc__     = __builtin__.isinstance.__doc__
###     __builtin__.isinstance = isinstance
### 
###     def issubclass (C, B, issubclass = __builtin__.issubclass) :
###         ### print "issubclass", C, B
###         from caller_globals import caller_info
###         print "isinstance", caller_info ()
###         if hasattr (C, "_Class") : C = C._Class
###         if hasattr (B, "_Class") : B = B._Class
###         return issubclass (C, B)
###     issubclass.__doc__     = __builtin__.issubclass.__doc__
###     __builtin__.issubclass = issubclass
###     
### _fix_builtins ()
### del _fix_builtins

from _TFL import TFL
TFL._Export ("*")

### __END__ Class_Proxy
