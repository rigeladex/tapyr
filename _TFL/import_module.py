# -*- coding: iso-8859-1 -*-
# Copyright (C) 2003 Mag. Christian Tanzer. All rights reserved
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
#    import_module
#
# Purpose
#    Import a module of specified name
#
# Revision Dates
#     9-Dec-2003 (CT) Creation
#    ««revision-date»»···
#--

def import_module (module_name) :
    """Returns the imported module named `module_name`. If `module_name` is
       naming a module living inside a package (e.g., `A.B.C`), the rightmost
       module (i.e., `C`) is returned.
    """
    ### >>> help(__import__ )
    ### __import__(...)
    ###     __import__(name, globals, locals, fromlist) -> module
    ###
    ### Import a module. The globals are only used to determine the
    ### context; they are not modified. The locals are currently unused.
    ### The fromlist should be a list of names to emulate ``from name
    ### import ...'', or an empty list to emulate ``import name''.
    ###
    ### When importing a module from a package, note that
    ### __import__('A.B', ...) returns package A when fromlist is empty,
    ### but its submodule B when fromlist is not empty.
    ###
    result = __import__ (module_name, {}, {}, ())
    for n in module_name.split (".") [1:] :
        try :
            result = getattr (result, n)
        except AttributeError, exc :
            raise ImportError, "%s: %s, %s" % (exc, module_name, result)
    return result
# end def import_module

if __name__ != "__main__" :
    from _TFL import TFL
    TFL._Export ("*")
### __END__ import_module
