# -*- coding: iso-8859-15 -*-
# Copyright (C) 2000-2006 Mag. Christian Tanzer. All rights reserved
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
#    TFL.object_globals
#
# Purpose
#    Return the globals of an object or class
#
# Revision Dates
#     6-Mar-2000 (CT) Creation
#     6-Nov-2002 (CT) `assert` removed from `class_globals`
#    14-Feb-2006 (CT) Moved into package `TFL`
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ««revision-date»»···
#--



from   _TFL import TFL

import sys

def object_globals (o) :
    """Return the globals associated to object `o'."""
    return object_module (o).__dict__
# end def object_globals

def class_globals (c) :
    """Return the globals associated to class `c'."""
    return class_module (c).__dict__
# end def class_globals

def class_module (c) :
    """Return the module defining the class `c'."""
    return sys.modules [c.__module__]
# end def class_module

object_module = class_module

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.object_globals
