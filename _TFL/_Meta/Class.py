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
#    17-Jan-2003 (CT) `Automethodwrap` added
#    ««revision-date»»···
#--

from   _TFL             import TFL
import _TFL._Meta

def _mangled_name (name, cls_name) :
    """Returns `name` as mangled by Python for occurences of `__%s` % name
       inside the definition of a class with name `cls_name`.

       >>> _mangled_name ("foo", "Bar")
       '_Bar__foo'
       >>> _mangled_name ("foo", "_Bar")
       '_Bar__foo'
       >>> _mangled_name ("foo", "_Bar_")
       '_Bar___foo'
    """
    if cls_name.startswith ("_") :
        format = "%s__%s"
    else :
        format = "_%s__%s"
    return format % (cls_name, name)
# end def _mangled_name

class _Type_ (type) :
    """Base class of TFL metaclasses."""

    def _mangled_name (cls, name) :
        return _mangled_name (name, cls.__name__)
    # end def _mangled_name

# end class _Type_

class Autorename (_Type_) :
    """Metaclass renaming the class to the value of the class attribute
       `_real_name` if existing.

       Python will use the name following the `class` keyword for mangling of
       private names. To avoid name clashes between private names of classes
       with the same name (e.g., Package_A.Class and Package_B.Class), define
       these classes with unique names and use `_real_name` to define the
       name to be used by clients of the class.

       The metaclass `Autorename` swaps `__name__` and `_real_name` before
       creating the class object. As this occurs after the name mangling done
       by Python (compiler), you can have your cake and eat it, too.
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

    def _mangled_name (cls, name) :
        return _mangled_name (name, cls.__dict__ ["__real_name"])
    # end def _mangled_name

# end class Autorename

class Autosuper (_Type_) :
    """Metaclass adding a private class variable `__super` containing
       `super (cls)`.

       `__super` can be used for cooperative method calls. For instance:

           def foo (self, bar, baz) :
               ...
               self.__super.foo (bar, baz)
               ...
           # end def foo
    """

    def __init__ (cls, name, bases, dict) :
        super   (Autosuper, cls).__init__ (name, bases, dict)
        setattr (cls, cls._mangled_name ("super"), super (cls))
    # end def __init__

# end class Autosuper

class Autoproperty (_Type_) :
    """Metaclass adding and initializing properties defined in
       `__properties`.

       `Autoproperty` expects `__properties` to contain instances of
       TFL.Meta.Property (or signature-compatible objects). For each element
       `p` of `__properties`,

       - `Autoproperty` will add a class attribute named `p.name` with value
         `p` to the class.

       - `Autoproperty` will add an instance attribute to all instances of
         the class if `p` provides a callable `init_instance` attribute.
    """

    def __init__ (cls, name, bases, dict) :
        super (Autoproperty, cls).__init__ (name, bases, dict)
        prop_name  = cls._mangled_name ("properties")
        properties = {}
        classes    = [cls] + list (bases)
        classes.reverse ()
        for c in classes :
            mangled_name = getattr (c, "_mangled_name", None)
            if mangled_name :
                for p in getattr (c, mangled_name ("properties"), []) :
                    setattr (cls, p.name, p)
                    properties [p.name] = p
        setattr (cls, prop_name, properties.values ())
    # end def __init__

    def __call__ (cls, * args, ** kw) :
        result = super (Autoproperty, cls).__call__ (* args, ** kw)
        for p in cls.__dict__.get (cls._mangled_name ("properties"), []) :
            init_instance = getattr (p, "init_instance", None)
            if callable (init_instance) :
                init_instance (result)
        return result
    # end def __call__

# end class Autoproperty

class Automethodwrap (_Type_) :
    """Metaclass automatically wrapping the methods specified in `__autowrap`.

       `__autowrap` must map method names to wrapper functions/objects (e.g.,
       to classmethod, staticmethod, or TFL.Meta.Class_and_Instance_Method).
    """

    def __init__ (cls, name, bases, dict) :
        super (Automethodwrap, cls).__init__ (name, bases, dict)
        cls._autowrap (bases, dict)
    # end def __init__

    def _autowrap (cls, bases, dict) :
        _aw = {}
        bss = list (bases)
        bss.reverse ()
        for b in bss :
            _aw.update (getattr (b, "__autowrap", {}))
        _aw.update (dict.get (cls._mangled_name ("autowrap"), {}))
        for name, wrapper in _aw.iteritems () :
            if callable (wrapper) :
                method = dict.get (name)
                if method :
                    ### this is tricky: we want to wrap the function found in
                    ### the dictionary, but only if it is an unbound method
                    ###     I didn't find any other way to check for
                    ###     unboundedness than comparing the `im_self` of
                    ###     `getattr (cls, name)` to `None`
                    if getattr (getattr (cls, name), "im_self", 42) is None :
                        try :
                            ### TFL wrappers like to get the class, too
                            setattr (cls, name, wrapper (method, cls))
                        except TypeError :
                            setattr (cls, name, wrapper (method))
        setattr (cls, "__autowrap", _aw)
    # end def _autowrap

# end class Automethodwrap

class Class (Autorename, Autosuper, Autoproperty, Automethodwrap) : pass

if __name__ == "__main__" :
    if __debug__ :
        class _X_ (object) :
           __metaclass__ = Class
           hugo          = 1
           __private     = 42
           _real_name    = "Y"

        class _Y_ (_X_) :
            hugo         = 2
            __private    = 137
            _real_name   = "ZZZ"

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

        T()
else :
    TFL.Meta._Export ("*")
### __END__ TFL.Meta.Class
