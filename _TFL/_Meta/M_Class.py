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

class _Type_ (type) :
    """Base class of TFL metaclasses."""

    def mangled_name (cls, name) :
        return cls._mangled_name (name, cls.__name__)
    # end def mangled_name

    def _mangled_name (self, name, cls_name) :
        if cls_name.startswith ("_") :
            format = "%s__%s"
        else :
            format = "_%s__%s"
        return format % (cls_name, name)
    # end def _mangled_name

# end class _Type_

class Autorename (_Type_) :
    """Metaclass renaming the class to the value of the class attribute
       `_real_name` if existing.
    """

    def __new__ (meta, name, bases, dict) :
        if dict.has_key ("_real_name") :
            name, real_name = dict ["_real_name"], name
            del dict ["_real_name"]
        else :
            real_name = name
        dict ["__real_name"] = real_name
        return super (Autorename, meta).__new__ (meta, name, bases, dict)
    # end def __new__

    def __init__ (cls, name, bases, dict) :
        real_name = cls.__name__
        if real_name != dict ["__real_name"] :
            from caller_globals import caller_globals
            caller_globals () [real_name] = cls
        super (Autorename, cls).__init__ (real_name, bases, dict)
    # end def __init__

    def mangled_name (cls, name) :
        return cls._mangled_name (name, cls.__dict__ ["__real_name"])
    # end def mangled_name

# end class Autorename

class Autosuper (_Type_) :
    """Metaclass adding a private class variable containing `super (cls)`
       (the name of that variable is taken from `_super_attr` of the class).
    """

    _super_attr = "super"

    def __init__ (cls, name, bases, dict) :
        super   (Autosuper, cls).__init__ (name, bases, dict)
        setattr (cls, cls.mangled_name (cls._super_attr), super (cls))
    # end def __init__

# end class Autosuper

class Autoproperty (_Type_) :
    """Metaclass adding and initializing properties defined in
       `__properties`.
    """

    def __init__ (cls, name, bases, dict) :
        super (Autoproperty, cls).__init__ (name, bases, dict)
        prop_name  = cls.mangled_name ("properties")
        properties = {}
        classes    = [cls] + list (bases)
        classes.reverse ()
        for c in classes :
            mangled_name = getattr (c, "mangled_name", None)
            if mangled_name :
                for p in getattr (c, mangled_name ("properties"), []) :
                    setattr (cls, p.name, p)
                    properties [p.name] = p
        setattr (cls, prop_name, properties.values ())
    # end def __init__

    def __call__ (cls, * args, ** kw) :
        result = super (Autoproperty, cls).__call__ (* args, ** kw)
        for p in cls.__dict__.get (cls.mangled_name ("properties"), []) :
            init_instance = getattr (p, "init_instance", None)
            if callable (init_instance) :
                init_instance (result)
        return result
    # end def __call__

# end class Autoproperty

class Class (Autorename, Autosuper, Autoproperty) : pass

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

        def __new__ (meta, * args, ** kw) :
            print meta, "__new__", args, kw
            return super (Metatest, meta).__new__ (meta, * args, ** kw)
        # end def __new__

    # end class Metatest

    class T (object) :
        __metaclass__ = Metatest

### __END__ TFL.Meta.Class
