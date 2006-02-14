# -*- coding: iso-8859-1 -*-
# Copyright (C) 2000-2006 TTTech Computertechnik GmbH. All rights reserved
# Schönbrunnerstraße 7, A--1040 Wien, Austria. office@tttech.com
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
