# -*- coding: iso-8859-1 -*-
# Copyright (C) 2002-2009 Mag. Christian Tanzer. All rights reserved
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
#    Property
#
# Purpose
#    TFL.Meta.Property
#
# Revision Dates
#    13-May-2002 (CT) Creation
#    14-Jan-2002 (CT) _Property_ factored, Aesthetics
#    17-Jan-2003 (CT) `Class_and_Instance_Method` added
#    17-Jan-2003 (CT) `M_` prefixes added
#    20-Jan-2003 (CT) `Class_Method` factored
#    13-Feb-2003 (CT) `Alias_Property` added
#    17-Feb-2003 (CT) `Alias_Attribute` added
#     3-Mar-2003 (CT) `Alias_Class_and_Instance_Method` added
#     3-Mar-2003 (CT) `Alias_Meta_and_Class_Attribute` added
#    15-Jul-2004 (CT) `Method_Descriptor` factored
#    28-Mar-2005 (CT) `Lazy_Property` added
#    20-May-2005 (CT) `init_instance` changed to call `_set_value` instead of
#                     `set_value`
#    26-Jul-2005 (CT) `prop` added
#    29-Feb-2008 (CT) `Method_Descriptor.__name__` property added
#    26-Mar-2008 (CT) `Method_Descriptor.Bound_Method.__getattr__` added
#     3-Apr-2008 (CT) `Alias2_Class_and_Instance_Method` added
#    29-Aug-2008 (CT)  s/super(...)/__super/
#     3-Feb-2009 (CT) `RO_Property` and `RW_Property` removed (weren't used
#                     anywhere)
#     3-Feb-2009 (CT) Documentation improved
#     6-Mar-2009 (CT) `__doc__` added to `Method_Descriptor`
#                     (unfortunately, cannot use a property, because Sphinx
#                     crashes and burns with that)
#    24-Sep-2009 (CT) `prop` decorator removed
#    24-Sep-2009 (CT) `Data_Descriptor` added (as an example how to do it)
#    ««revision-date»»···
#--

from   _TFL             import TFL
import _TFL._Meta
import _TFL._Meta.M_Class

class _Property_ (property) :

    __metaclass__ = TFL.Meta.M_Class

    def __init__ (self) :
        self.__super.__init__ (self._get, self._set, self._del)
    # end def __init__

    def del_value (self, obj) :
        return delattr (obj, self.mangled_name)
    # end def del_value

    def get_value (self, obj) :
        return getattr (obj, self.mangled_name)
    # end def get_value

    def set_value (self, obj, value) :
        return setattr (obj, self.mangled_name, value)
    # end def set_value

    def set_doc (self, doc) :
        self.__doc__ = doc
    # end def set_doc

    _del       = None
    _get       = get_value
    _set       = None
    _set_value = set_value

# end class _Property_

class Property (_Property_) :
    """Base class for property classes."""

    def __init__ (self, name, doc = None) :
        self.name         = name
        self.mangled_name = "__%s" % name
        self.__super.__init__ ()
        if doc :
            self.set_doc (doc)
    # end def __init__

# end class Property

class Data_Descriptor (property) :
    """Data descriptor for an attribute.

       This is just an example how to define a data descriptor for an
       attribute.
    """

    __metaclass__ = TFL.Meta.M_Class

    def __init__ (self, name, doc = None) :
        self.name    = name
        self.__doc__ = doc
    # end def __init__

    def __delete__ (self, obj) :
        try :
            del obj.__dict__ [self.name]
        except KeyError :
            raise AttributeError (self.name)
    # end def __delete__

    def __get__ (self, obj, cls = None) :
        if obj is None :
            return self
        try :
            return obj.__dict__ [self.name]
        except KeyError :
            raise AttributeError \
                ( "%r object has no attribute %r"
                % (obj.__class__.__name__, self.name)
                )
    # end def __get__

    def __set__ (self, obj, value) :
        obj.__dict__ [self.name] = value
    # end def __set__

# end class Data_Descriptor

class Method_Descriptor (object) :
    """Descriptor for special method types."""

    __metaclass__ = TFL.Meta.M_Class

    class Bound_Method (object) :

        def __init__ (self, method, target, cls) :
            self.method  = method
            self.target  = target
            self.cls     = cls
            self.__doc__ = method.__doc__
        # end def __init__

        @property
        def __name__ (self) :
            return self.method.__name__
        # end def __name__

        def __call__ (self, * args, ** kw) :
            return self.method (self.target, * args, ** kw)
        # end def __call__

        def __getattr__ (self, name) :
            return getattr (self.method, name)
        # end def __getattr__

        def __repr__ (self) :
            return "<bound method %s.%s of %r>" % \
                   (self.cls.__name__, self.method.__name__, self.target)
        # end def __repr__

    # end class Bound_Method

    def __init__ (self, method, cls = None) :
        self.method  = method
        self.__doc__ = method.__doc__
        self.cls     = cls
    # end def __init__

    @property
    def __name__ (self) :
        return self.method.__name__
    # end def __name__

    def __get__ (self, obj, cls = None) :
        if obj is None :
            return self.method
        return self.Bound_Method (self.method, obj, self.cls or cls)
    # end def __get__

# end class Method_Descriptor

class Class_Method (Method_Descriptor) :
    """Method wrapper for class methods. This class can be used just like the
       built-in `classmethod`.

       If the optional argument `cls` is passed to the `__init__` call, it
       will provide better introspection, though (by showing which class
       actually defined a class method).

       Normally, it is best to use
       :class:`~_TFL._Meta.M_Class.M_Automethodwrap` as metaclass,
       which does everything the right way.
    """

    def __get__ (self, obj, cls = None) :
        return self.Bound_Method (self.method, cls, self.cls or cls)
    # end def __get__

# end class Class_Method

class Class_and_Instance_Method (Method_Descriptor) :
    """Flexible method wrapper: wrapped method can be used as
       class method **and** as instance method.

       ::

           >>> class T (object) :
           ...     foo = 42
           ...     def __init__ (self) :
           ...         self.foo = 137
           ...     def chameleon (soc) :
           ...         print type (soc), soc.foo
           ...     chameleon = Class_and_Instance_Method (chameleon)
           ...
           >>> T.chameleon ()
           <type 'type'> 42
           >>> T ().chameleon ()
           <class 'Property.T'> 137
           >>> class U (T) :
           ...     foo = 84
           ...     def __init__ (self) :
           ...         self.foo = 2 * 137
           ...
           >>> U.chameleon ()
           <type 'type'> 84
           >>> U ().chameleon ()
           <class 'Property.U'> 274
    """

    def __get__ (self, obj, cls = None) :
        if obj is None :
            obj = cls
        return self.Bound_Method (self.method, obj, self.cls or cls)
    # end def __get__

# end class Class_and_Instance_Method

class Alias_Property (object) :
    """Property defining an alias name for another attribute.

       ::

           >>> class X (object) :
           ...     def __init__ (self) :
           ...         self.foo = 137
           ...     @classmethod
           ...     def foo (self) :
           ...         return 42
           ...     bar = Alias_Property ("foo")
           ...
           >>> X.bar
           <bound method type.foo of <class 'Property.X'>>
           >>> X.bar()
           42
           >>> x = X()
           >>> x.bar
           137
           >>> x.bar=7
           >>> x.bar
           7
           >>> X.bar()
           42
    """

    __metaclass__ = TFL.Meta.M_Class

    def __init__ (self, aliased_name) :
        self.aliased_name = aliased_name
    # end def __init__

    def __get__ (self, obj, cls = None) :
        if obj is None :
            obj = cls
        return getattr (obj, self.aliased_name)
    # end def __get__

    def __set__ (self, obj, value) :
        setattr (obj, self.aliased_name, value)
    # end def __set__

# end class Alias_Property

class Alias_Attribute (Alias_Property) :
    """Property defining an attribute alias for a computed value"""

    def __get__ (self, obj, cls = None) :
        return self.__super.__get__ (obj, cls) ()
    # end def __get__

    def __set__ (self, obj, value) :
        raise TypeError, "Cannot assign `%s` to object `%s`" % (value, object)
    # end def __set__

# end class Alias_Attribute

class Alias_Class_and_Instance_Method (Class_Method) :
    """Property defining an alias name for a instance-method/class-method
       pair with different definitions.

       ::

         >>> class T (object) :
         ...   chameleon = Alias_Class_and_Instance_Method ("foo")
         ...   class __metaclass__ (TFL.Meta.M_Class) :
         ...     def foo (cls) :
         ...       print "Class method foo <%s.%s>" % (cls.__name__, cls.__class__.__name__)
         ...   def foo (self) :
         ...     print "Instance method foo <%s>" % (self.__class__.__name__, )
         ...
         >>> T.chameleon()
         Class method foo <T.__metaclass__>
         >>> T ().chameleon ()
         Instance method foo <T>
         >>> class U(T) :
         ...   pass
         ...
         >>> U.chameleon()
         Class method foo <U.__metaclass__>
         >>> U().chameleon()
         Instance method foo <U>
    """

    def __init__ (self, aliased_name, cls = None) :
        self.aliased_name = aliased_name
        self.cls          = cls
    # end def __init__

    def __get__ (self, obj, cls = None) :
        if obj is None :
            obj = cls
            cls = cls.__class__
        return self.Bound_Method (getattr (cls, self.aliased_name), obj, cls)
    # end def __get__

# end class Alias_Class_and_Instance_Method

class Alias2_Class_and_Instance_Method (Class_Method) :
    """Property defining an alias name for a instance-method/class-method
       pair with different names and definitions.

       ::

         >>> class T (object) :
         ...   chameleon = Alias2_Class_and_Instance_Method ("foo", "bar")
         ...   @classmethod
         ...   def foo (cls) :
         ...     print "Class method foo <%s>" % (cls.__name__, )
         ...   def bar (self) :
         ...     print "Instance method bar <%s>" % (self.__class__.__name__, )
         ...
         >>> T.chameleon()
         Class method foo <T>
         >>> T ().chameleon ()
         Instance method bar <T>
         >>> class U(T) :
         ...   pass
         ...
         >>> U.chameleon()
         Class method foo <U>
         >>> U().chameleon()
         Instance method bar <U>
    """

    def __init__ (self, cm_alias, im_alias, cls = None) :
        self.cm_alias = cm_alias
        self.im_alias = im_alias
        self.cls      = cls
    # end def __init__

    def __get__ (self, obj, cls = None) :
        if obj is None :
            result = self.Bound_Method \
                (getattr (cls, self.cm_alias).im_func, cls, cls)
        else :
            result = self.Bound_Method \
                (getattr (cls, self.im_alias), obj, cls)
        return result
    # end def __get__

# end class Alias2_Class_and_Instance_Method

class Alias_Meta_and_Class_Attribute (Class_Method) :
    """Property defining an alias name for a instance-method/class-method
       pair with different definitions.

       ::

         >>> class T (object) :
         ...   chameleon = Alias_Meta_and_Class_Attribute ("foo")
         ...   class __metaclass__ (TFL.Meta.M_Class) :
         ...     foo = 42
         ...   foo = 137
         ...
         >>> T.chameleon
         42
         >>> T ().chameleon
         137
    """

    def __init__ (self, aliased_name, cls = None) :
        self.aliased_name = aliased_name
        self.cls          = cls
    # end def __init__

    def __get__ (self, obj, cls = None) :
        if obj is None :
            cls = cls.__class__
        return getattr (cls, self.aliased_name)
    # end def __get__

# end class Alias_Meta_and_Class_Attribute

class Lazy_Property (object) :
    """Property caching a computed value"""

    def __init__ (self, name, computer, doc = None) :
        self.name     = self.__name__ = name
        self.computer = computer
        self.__doc__  = doc
    # end def __init__

    def __get__ (self, obj, cls = None) :
        if obj is None :
            return self
        result = self.computer (obj)
        setattr (obj, self.name, result)
        return result
    # end def __get__

# end class Lazy_Property

if __name__ != "__main__" :
    TFL.Meta._Export ("*", "_Property_")
### __END__ TFL.Meta.Property
