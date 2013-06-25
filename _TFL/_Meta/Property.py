# -*- coding: iso-8859-15 -*-
# Copyright (C) 2002-2013 Mag. Christian Tanzer. All rights reserved
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
#    22-Sep-2011 (CT) `Class_Property` added
#    29-Jan-2013 (CT) Allow dotted names for `Alias_Property`
#    23-May-2013 (CT) Use `TFL.Meta.BaM` for Python-3 compatibility
#    25-Jun-2013 (CT) Make `_Class_Property_Function_.__get__` Python-2.6
#                     compatible
#    ««revision-date»»···
#--

from   __future__       import print_function

from   _TFL             import TFL
import _TFL._Meta.M_Class

import operator

class _Property_ (TFL.Meta.BaM (property, metaclass = TFL.Meta.M_Class)) :

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

class Data_Descriptor (TFL.Meta.BaM (property, metaclass = TFL.Meta.M_Class)) :
    """Data descriptor for an attribute.

       This is just an example how to define a data descriptor for an
       attribute.
    """

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

class Method_Descriptor (TFL.Meta.BaM (object, metaclass = TFL.Meta.M_Class)) :
    """Descriptor for special method types."""

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
        self.method  = self.__func__ = method
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

class _Class_Property_Descriptor_ (object) :

    def __init__ (self, getter) :
        self.getter  = getter
        self.__doc__ = getter.__func__.__doc__
    # end def __init__

    @property
    def __name__ (self) :
        return self.getter.__func__.__name__
    # end def __name__

    def __get__ (self, obj, cls = None) :
        if obj is None :
            obj = cls
            cls = cls.__class__
        result = self.getter.__get__ (obj, cls)
        if hasattr (result, "__call__") :
            result = result ()
        return result
    # end def __get__

# end class _Class_Property_Descriptor_

class _Class_Property_Function_ (object) :

    def __init__ (self, getter) :
        self.getter  = getter
        self.__doc__ = getter.__doc__
    # end def __init__

    @property
    def __name__ (self) :
        return self.getter.__name__
    # end def __name__

    def __get__ (self, obj, cls = None) :
        if obj is None :
            obj = cls
            cls = cls.__class__
        getter  = self.getter
        try :
            return getter (cls)
        except TypeError :
            if isinstance (getter, classmethod) :
                ### Python 2.6 doesn't support calling an instance of
                ### classmethod directly
                return getter.__get__ (obj, cls) ()
            else :
                raise
    # end def __get__

# end class _Class_Property_Function_

def Class_Property (getter) :
    """Return a descriptor for a property that is accessible via the class
       and via the instance.

       ::

        >>> from _TFL._Meta.Property import *
        >>> from _TFL._Meta.Once_Property import Once_Property
        >>> class Foo (object) :
        ...     @Class_Property
        ...     def bar (cls) :
        ...         "Normal method bar"
        ...         print ("Normal method bar called")
        ...         return 42
        ...     @Class_Property
        ...     @classmethod
        ...     def baz (cls) :
        ...         "classmethod baz"
        ...         print ("classmethod baz called")
        ...         return "Frozz"
        ...     @Class_Property
        ...     @Class_Method
        ...     def foo (cls) :
        ...         "Class_Method foo"
        ...         print ("Class_Method foo called")
        ...         return "Hello world"
        ...     @Class_Property
        ...     @Once_Property
        ...     def qux (cls) :
        ...         "Once property qux"
        ...         print ("Once property qux")
        ...         return 42 * 42
        ...
        >>> foo = Foo ()
        >>> Foo.bar
        Normal method bar called
        42
        >>> foo.bar
        Normal method bar called
        42
        >>>
        >>> Foo.baz
        classmethod baz called
        'Frozz'
        >>> foo.baz
        classmethod baz called
        'Frozz'
        >>>
        >>> Foo.foo
        Class_Method foo called
        'Hello world'
        >>> foo.foo
        Class_Method foo called
        'Hello world'
        >>>
        >>> Foo.qux
        Once property qux
        1764
        >>> foo.qux
        1764

        >>> foo2 = Foo ()
        >>> foo2.qux
        1764
        >>> Foo.qux
        1764

    """
    if hasattr (getter, "__func__") :
        return _Class_Property_Descriptor_ (getter)
    else :
        return _Class_Property_Function_   (getter)
# end def Class_Property

class Class_and_Instance_Method (Method_Descriptor) :
    """Flexible method wrapper: wrapped method can be used as
       class method **and** as instance method.

       ::

           >>> class T (object) :
           ...     foo = 42
           ...     def __init__ (self) :
           ...         self.foo = 137
           ...     def chameleon (soc) :
           ...         print (type (soc).__name__, soc.foo)
           ...     chameleon = Class_and_Instance_Method (chameleon)
           ...
           >>> T.chameleon ()
           type 42
           >>> T ().chameleon ()
           T 137
           >>> class U (T) :
           ...     foo = 84
           ...     def __init__ (self) :
           ...         self.foo = 2 * 137
           ...
           >>> U.chameleon ()
           type 84
           >>> U ().chameleon ()
           U 274
    """

    def __get__ (self, obj, cls = None) :
        if obj is None :
            obj = cls
        return self.Bound_Method (self.method, obj, self.cls or cls)
    # end def __get__

# end class Class_and_Instance_Method

class Alias_Property (TFL.Meta.BaM (object, metaclass = TFL.Meta.M_Class)) :
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

    def __init__ (self, aliased_name) :
        self.aliased_name = aliased_name
        self.getter       = operator.attrgetter (aliased_name)
        if "." in aliased_name :
            head, tail  = aliased_name.rsplit (".", 1)
            head_getter = operator.attrgetter (head)
            def setter (obj, value) :
                o = head_getter (obj)
                setattr (o, tail, value)
        else :
            def setter (obj, value) :
                setattr (obj, aliased_name, value)
        self.setter = setter
    # end def __init__

    def __get__ (self, obj, cls = None) :
        if obj is None :
            obj = cls
        return self.getter (obj)
    # end def __get__

    def __set__ (self, obj, value) :
        self.setter (obj, value)
    # end def __set__

# end class Alias_Property

class Alias_Attribute (Alias_Property) :
    """Property defining an attribute alias for a computed value"""

    def __get__ (self, obj, cls = None) :
        return self.__super.__get__ (obj, cls) ()
    # end def __get__

    def __set__ (self, obj, value) :
        raise TypeError ("Cannot assign `%s` to object `%s`" % (value, object))
    # end def __set__

# end class Alias_Attribute

class Alias_Class_and_Instance_Method (Class_Method) :
    """Property defining an alias name for a instance-method/class-method
       pair with different definitions.

       ::

         >>> class Meta_T (TFL.Meta.M_Class) :
         ...   def foo (cls) :
         ...     print ("Class method foo <%s.%s>" % (cls.__name__, cls.__class__.__name__))
         >>> class T (TFL.Meta.BaM (object, metaclass = Meta_T)) :
         ...   chameleon = Alias_Class_and_Instance_Method ("foo")
         ...   def foo (self) :
         ...     print ("Instance method foo <%s>" % (self.__class__.__name__, ))
         ...
         >>> T.chameleon()
         Class method foo <T.Meta_T>
         >>> T ().chameleon ()
         Instance method foo <T>
         >>> class U (T) :
         ...   pass
         ...
         >>> U.chameleon()
         Class method foo <U.Meta_T>
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
         ...     print ("Class method foo <%s>" % (cls.__name__, ))
         ...   def bar (self) :
         ...     print ("Instance method bar <%s>" % (self.__class__.__name__, ))
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
            m      = getattr (cls, self.cm_alias)
            result = self.Bound_Method (m.__func__, cls, cls)
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

         >>> class Meta_T (TFL.Meta.M_Class) :
         ...   foo = 42
         >>> class T (TFL.Meta.BaM (object, metaclass = Meta_T)) :
         ...   chameleon = Alias_Meta_and_Class_Attribute ("foo")
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
        self.computer = self.__func__ = computer
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
