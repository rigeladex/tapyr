#! /swing/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2002 Mag. Christian Tanzer. All rights reserved
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
#    Module
#
# Purpose
#    Convenience functions for accessing features of python modules
#
# Revision Dates
#    12-Mar-2002 (CT) Creation
#    ««revision-date»»···
#--

def module_of (object) :
    """Returns the name of the module defining `object`, if possible.

       `module_of` works for classes, functions, and class proxies. 
    """
    try :
        object = object.__dict__ ["Essence"]
    except (AttributeError, KeyError, TypeError) :
        pass
    result = getattr (object, "__module__", None)
    if not result :
        globals = getattr (object, "func_globals", None)
        if globals :
            result = globals.get ("__name__")
    return result
# end def module_of

def defined_by (object, module) :
    """Returns true, if `object` is defined by `module`, false otherwise.

       Unfortunately, this currently only works for `object`s for which
       `module_of` returns a non-None result.
    """
    return module_of (object) == module.__name__
# end def defined_by

def names_of (module) :
    """Returns the names of all functions and classes defined by `module`
       itself. 

       Unfortunately, this currently only returns objects for which
       `module_of` returns a non-None result.
    """
    result = []
    for n, f in module.__dict__.items () :
        if defined_by (f, module) :
            result.append (n)
    return result
# end def names_of

from _TFL import TFL
TFL._Export_Module ()

### __END__ Module
