
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2002-2004 Mag. Christian Tanzer. All rights reserved
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
#    TFL.Meta.M_Class
#
# Purpose
#    Provide custom metaclass for new-style Python classes
#
# Revision Dates
#    10-May-2002 (CT) Creation
#    17-Jan-2003 (CT) `M_Automethodwrap` added
#    17-Jan-2003 (CT) `M_` prefixes added
#    20-Jan-2003 (CT) Docstring of `M_Automethodwrap` improved
#     3-Feb-2003 (CT) File renamed from `Class.py` to `M_Class.py`
#     1-Apr-2003 (CT) `M_Class_SW` factored
#     1-Apr-2003 (CT) `M_Autoproperty` removed from `M_Class`
#                     (optimize, optimize)
#    28-Apr-2003 (CT) `M_Autorename` changed to not manipulate `caller_globals`
#    23-Jul-2004 (CT) `_M_Type_` added to `_Export`
#    25-Jan-2005 (CT) `New` added
#    10-Feb-2005 (MG) `_M_Type_.New`: `mangled_attributes` added
#    28-Mar-2005 (CT) `M_Class_SWRP` added
#    23-Mar-2006 (CED) `_fixed_type_` added
#    ««revision-date»»···
#--

from   _TFL             import TFL
import _TFL._Meta

import types

def _m_mangled_attr_name (name, cls_name) :
    """Returns `name` as mangled by Python for occurences of `__%s` % name
       inside the definition of a class with name `cls_name`.

       >>> _m_mangled_attr_name ("foo", "Bar")
       '_Bar__foo'
       >>> _m_mangled_attr_name ("foo", "_Bar")
       '_Bar__foo'
       >>> _m_mangled_attr_name ("foo", "_Bar_")
       '_Bar___foo'
    """
    if cls_name.startswith ("_") :
        format = "%s__%s"
    else :
        format = "_%s__%s"
    return format % (cls_name, name)
# end def _m_mangled_attr_name

class _fixed_type_ (type) :
    """This class fixes a python problem in context of
       multiple inheritence and custom metaclasses.
       For a discussion of this problem, see:
       http://groups.google.de/group/comp.lang.python/tree/browse_frm/thread/2b7a60d08d4a99c4/72346462866e6497?rnum=1&q=eder&_done=%2Fgroup%2Fcomp.lang.python%2Fbrowse_frm%2Fthread%2F2b7a60d08d4a99c4%2F36e83cab80f1dbaf%3Fq%3Deder%26rnum%3D2%26#doc_72346462866e6497
    """

    def __call__ (meta, name, bases, dict) :
        meta = meta._get_meta (bases, dict)
        cls  = meta.__new__   (meta, name, bases, dict)
        meta.__init__         (cls, name, bases, dict)
        return cls
    # end def __call__

    def _get_meta (meta, bases, dict) :
        if "__metaclass__" in dict :
            return dict ["__metaclass__"]
        winner = meta
        for b in bases :
            cand = type (b)
            if cand in (types.ClassType, type) :
                 pass
            elif issubclass (cand, winner) :
                winner = cand
            elif issubclass (winner, cand) :
                pass
            else :
                raise TypeError ("Metatype conflict among bases")
        return winner
    # end def _get_meta

# end class _fixed_type_

class _M_Type_ (type) :
    """Base class of TFL metaclasses."""

    __metaclass__ = _fixed_type_ ### to fix metaclasses, we need
                                 ### meta-meta classes

    def _m_mangled_attr_name (cls, name) :
        return _m_mangled_attr_name (name, cls.__name__)
    # end def _m_mangled_attr_name

    def New (cls, name_postfix = None, mangled_attributes = {}, ** kw) :
        """Returns a new class derived from `cls` with `kw` in __dict__"""
        name = cls.__name__
        if name_postfix :
            name = "_".join ((name, name_postfix))
        new_dict = dict (__module__ = cls.__module__)
        for attr_name, value in mangled_attributes.iteritems () :
            new_dict [_m_mangled_attr_name (attr_name, name)] = value
        new_dict.update (kw)
        return type (cls) (name, (cls, ), new_dict)
    # end def New

# end class _M_Type_

class M_Autorename (_M_Type_) :
    """Metaclass renaming the class to the value of the class attribute
       `_real_name` if existing.

       Python will use the name following the `class` keyword for mangling of
       private names. To avoid name clashes between private names of classes
       with the same name (e.g., Package_A.Class and Package_B.Class), define
       these classes with unique names and use `_real_name` to define the
       name to be used by clients of the class.

       The metaclass `M_Autorename` swaps `__name__` and `_real_name` before
       creating the class object. As this occurs after the name mangling done
       by Python (compiler), you can have your cake and eat it, too.

       To make the class visible in the defining module under the
       `_real_name` you'll have to add an explicit assignment after the class
       definition.
    """

    def __new__ (meta, name, bases, dict) :
        real_name = name
        if "_real_name" in dict :
            name = dict ["_real_name"]
            del dict ["_real_name"]
##         elif __debug__ :
##             assert name not in (b.__name__ for b in bases), \
##                 "Class `%s` inherits from class with same name!" % name
        dict ["__real_name"] = real_name
        return super (M_Autorename, meta).__new__ (meta, name, bases, dict)
    # end def __new__

    def __init__ (cls, name, bases, dict) :
        ### Need to pass `cls.__name__` as it might defer from `name`
        super (M_Autorename, cls).__init__ (cls.__name__, bases, dict)
    # end def __init__

    def _m_mangled_attr_name (cls, name) :
        return _m_mangled_attr_name (name, cls.__dict__ ["__real_name"])
    # end def _m_mangled_attr_name

# end class M_Autorename

class M_Autosuper (_M_Type_) :
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
        super   (M_Autosuper, cls).__init__ (name, bases, dict)
        setattr (cls, cls._m_mangled_attr_name ("super"), super (cls))
    # end def __init__

# end class M_Autosuper

class M_Autoproperty (_M_Type_) :
    """Metaclass adding and initializing properties defined in
       `__properties`.

       `M_Autoproperty` expects `__properties` to contain instances of
       TFL.Meta.Property (or signature-compatible objects). For each element
       `p` of `__properties`,

       - `M_Autoproperty` will add a class attribute named `p.name` with value
         `p` to the class.

       - `M_Autoproperty` will add an instance attribute to all instances of
         the class if `p` provides a callable `init_instance` attribute.
    """

    def __init__ (cls, name, bases, dict) :
        super (M_Autoproperty, cls).__init__ (name, bases, dict)
        prop_name  = cls._m_mangled_attr_name ("properties")
        properties = {}
        classes    = [cls] + list (bases)
        classes.reverse ()
        for c in classes :
            mangled_name = getattr (c, "_m_mangled_attr_name", None)
            if mangled_name :
                for p in getattr (c, mangled_name ("properties"), []) :
                    setattr (cls, p.name, p)
                    properties [p.name] = p
        setattr (cls, prop_name, properties.values ())
    # end def __init__

    def __call__ (cls, * args, ** kw) :
        result = super (M_Autoproperty, cls).__call__ (* args, ** kw)
        props  = cls.__dict__.get (cls._m_mangled_attr_name ("properties"), [])
        for p in props :
            init_instance = getattr (p, "init_instance", None)
            if callable (init_instance) :
                init_instance (result)
        return result
    # end def __call__

# end class M_Autoproperty

class M_Automethodwrap (_M_Type_) :
    """Metaclass automatically wrapping the methods specified in `__autowrap`.

       `__autowrap` must map method names to wrapper functions/objects (e.g.,
       to staticmethod, TFL.Meta.Class_Method (a TFL replacement to
       classmethod), or TFL.Meta.Class_and_Instance_Method).
    """

    def __init__ (cls, name, bases, dict) :
        super (M_Automethodwrap, cls).__init__ (name, bases, dict)
        cls._m_autowrap (bases, dict)
    # end def __init__

    def _m_autowrap (cls, bases, dict) :
        _aw = {}
        bss = list (bases)
        bss.reverse ()
        for b in bss :
            _aw.update (getattr (b, "__autowrap", {}))
        _aw.update (dict.get (cls._m_mangled_attr_name ("autowrap"), {}))
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
    # end def _m_autowrap

# end class M_Automethodwrap

class M_Class_SW (M_Autosuper, M_Automethodwrap) :
    pass
# end class M_Class_SW

class M_Class (M_Autorename, M_Class_SW) :
    pass
# end class M_Class

class M_Class_SWRP (M_Autoproperty, M_Class) :
    pass
# end class M_Class_SWRP

if __name__ != "__main__" :
    TFL.Meta._Export ("*", "_M_Type_")
else :
    if __debug__ :
        class _X_ (object) :
           __metaclass__ = M_Class
           hugo          = 1
           __private     = 42
           _real_name    = "Y"
        Y = _X_

        class _Y_ (_X_) :
            hugo         = 2
            __private    = 137
            _real_name   = "ZZZ"
        ZZZ = _Y_

        class Metatest (M_Class) :

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
### __END__ TFL.Meta.M_Class
