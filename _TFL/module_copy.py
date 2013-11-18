# -*- coding: utf-8 -*-
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
#    module_copy
#
# Purpose
#    Return an independent copy of a module
#
# Revision Dates
#    17-Dec-2003 (CT) Creation
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ««revision-date»»···
#--



import sys

def module_copy (name, ** kw) :
    """Return an independent copy of the module with `name` and assign all
       elements of `kw` to the result.
    """
    original = None
    if name in sys.modules :
        original = sys.modules [name]
        del sys.modules [name]
        try :
            result = __import__ (name, {}, {})
        finally :
            sys.modules [name] = original
    else :
        result = __import__ (name, {}, {})
        del sys.modules [name]
    for k, v in kw.iteritems () :
        setattr (result, k, v)
    return result
# end def module_copy

def import_module_copy (name, as_name, ** kw) :
    """Put a module_copy with `name` into `sys.modules`."""
    result = sys.modules [as_name] = module_copy (name, ** kw)
    return result
# end def import_module_copy

if __name__ != "__main__" :
    from _TFL import TFL
    TFL._Export ("*")
### __END__ module_copy
