#! /swing/bin/python
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
#    TFL.Meta.Class
#
# Purpose
#    Provide custom metaclass for new-style Python classes
#
# Revision Dates
#    10-May-2002 (CT) Creation
#    ««revision-date»»···
#--

class Autorename (type) :
    """Metaclass renaming the class to the value of the class attribute
       `_real_name` if existing.
    """

    def __new__ (cls, name, bases, dict) :
        if dict.has_key ("_real_name") :
            name, real_name = dict ["_real_name"], name
            del dict ["_real_name"]
        else :
            real_name = name
        dict ["__real_name"] = real_name
        return super (Autorename, cls).__new__ (cls, name, bases, dict)
    # end def __new__

    def __init__ (cls, name, bases, dict) :
        real_name = cls.__name__
        if real_name != dict ["__real_name"] :
            from caller_globals import caller_globals
            caller_globals () [real_name] = cls
        super (Autorename, cls).__init__ (real_name, bases, dict)
    # end def __init__

    def _mangled_name (cls, name) :
        cls_name = cls.__dict__ ["__real_name"]
        if cls_name.startswith ("_") :
            format = "%s__%s"
        else :
            format = "_%s__%s"
        return format % (cls_name, name)
    # end def _mangled_name

# end class Autorename

class Autosuper (type) :
    """Metaclass adding a private class variable containing `super (cls)`
       (the name of that variable is taken from `_super_attr` of the class).
    """

    _super_attr = "super"

    def __init__ (cls, name, bases, dict) :
        super   (Autosuper, cls).__init__ (name, bases, dict)
        setattr (cls, cls._mangled_name (cls._super_attr), super (cls))
    # end def __init__

    def _mangled_name (cls, name) :
        cls_name = cls.__name__
        if cls_name.startswith ("_") :
            format = "%s__%s"
        else :
            format = "_%s__%s"
        return format % (cls_name, name)
    # end def _mangled_name

# end class Autosuper

class Class (Autorename, Autosuper) :

    def __init__ (cls, name, bases, dict) :
        super (Class, cls).__init__ (name, bases, dict)
        for p in dict.get ("_properties_", []) :
            assert not dict.has_key (p.name)
            setattr (cls, p.name, p)
    # end def __init__

    def __call__ (cls, * args, ** kw) :
        result = super (Class, cls).__call__ (* args, ** kw)
        for p in cls.__dict__.get ("_properties_", []) :
            init_instance = getattr (p, "init_instance", None)
            if init_instance :
                init_instance (result)
        return result
    # end def __call__

# end class Class

from   _TFL import TFL
import _TFL._Meta
TFL.Meta._Export ("*")

if 0 and __debug__ :
    class _X_ (object) :
       __metaclass__ = Class
       hugo          = 1
       __private     = 42
       _real_name    = "Y"
       _super_attr   = "Ancestor"

    class _Y_ (_X_) :
        hugo         = 2
        __private    = 137
        _real_name   = "ZZZ"
        _super_attr  = "super"

    class Metatest (Class) :

        def __call__ (cls, * args, ** kw) :
            print cls, "__call__", args, kw
            return super (Metatest, cls).__call__ (* args, ** kw)
        # end def __call__

        def __init__ (cls, * args, ** kw) :
            print cls, "__init__", args, kw
            super (Metatest, cls).__init__ (* args, ** kw)
        # end def __init__

        def __new__ (cls, * args, ** kw) :
            print cls, "__new__", args, kw
            return super (Metatest, cls).__new__ (cls, * args, ** kw)
        # end def __new__

    # end class Metatest

    class T (object) :
        __metaclass__ = Metatest

### __END__ Class
