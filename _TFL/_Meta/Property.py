# -*- coding: iso-8859-1 -*-
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

    _del = None
    _get = get_value
    _set = None

# end class _Property_

class Property (_Property_) :

    def __init__ (self, name, doc = None) :
        self.name         = name
        self.mangled_name = "__%s" % name
        self.__super.__init__ ()
        if doc :
            self.set_doc (doc)
    # end def __init__

# end class Property

class RO_Property (Property) :
    """Readonly property which is automatically initialized for each
       instance.
    """

    def __init__ (self, name, init_value = None, doc = None) :
        self.init_value = init_value
        self.__super.__init__ (name, doc)
    # end def __init__

    def init_instance (self, obj) :
        self.set_value (obj, self.init_value)
    # end def init_instance

# end class RO_Property

class RW_Property (RO_Property) :
    """Read/write property automatically initialized for each instance"""

    _del = RO_Property.del_value
    _set = RO_Property.set_value

# end class Read_Write

class Class_Method (object) :
    """Method wrapper for class methods. This class can be used just like the
       built-in `classmethod`.

       If the optional argument `cls` is passed to the `__init__` call, it
       will provide better introspection, though (by showing which class
       actually defined a class method).

       Normally, it is best to use `TFL.Meta.M_Automethodwrap` as metaclass,
       which does everything the right way.
    """

    class Bound_Method (object) :
        def __init__ (self, method, target, cls) :
            self.method = method
            self.target = target
            self.cls    = cls
        # end def __init__

        def __call__ (self, * args, ** kw) :
            return self.method (self.target, * args, ** kw)
        # end def __call__

        def __repr__ (self) :
            return "<bound method %s.%s of %r>" % \
                   (self.cls.__name__, self.method.__name__, self.target)
        # end def __repr__

    # end class Bound_Method

    def __init__ (self, method, cls = None) :
        self.method = method
        self.cls    = cls
    # end def __init__

    def __get__ (self, obj, cls = None) :
        return self.Bound_Method (self.method, cls, self.cls or cls)
    # end def __get__

# end class Class_Method

class Class_and_Instance_Method (Class_Method) :
    """Flexible method wrapper: wrapped method can be used as class method
       and as instance method.

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

       >>> class X (object) :
       ...     def __init__ (self) :
       ...         self.foo = 137
       ...     def foo (self) :
       ...         return 42
       ...     foo = classmethod (foo)
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
        return super (Alias_Attribute, self).__get__ (obj, cls) ()
    # end def __get__

    def __set__ (self, obj, value) :
        raise TypeError, "Cannot assign `%s` to object `%s`" % (value, object)
    # end def __set__

# end class Alias_Attribute

class Alias_Class_and_Instance_Method (Class_Method) :
    """Property defining an alias name for a instance-method/class-method
       pair with different definitions.

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

class Alias_Meta_and_Class_Attribute (Class_Method) :
    """Property defining an alias name for a instance-method/class-method
       pair with different definitions.

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

if __name__ == "__main__" :
    ### unit-test code ############################################################
    if __debug__ :
        import U_Test

        def _doc_test () :
            import Property
            return U_Test.run_module_doc_tests (Property)
        # end def _doc_test

        def _test () :
            _doc_test  ()
        # end def _test

        _test ()

        import _TFL.d_dict
        class T (object) :
            __metaclass__ = TFL.Meta.M_Automethodwrap
            __autowrap    = TFL.d_dict \
                ( chameleon = Class_and_Instance_Method
                , piggy     = Class_and_Instance_Method
                )
            foo = 42
            def __init__ (self) :
                self.foo = 137
            def chameleon (soc) :
                print "T.chameleon>", type (soc), soc.foo
            def piggy (soc) :
                print "T.piggy>", type (soc), soc.foo

        T.chameleon ()
        T ().chameleon ()
        class U (T) :
            foo = 84
            __autowrap = TFL.d_dict (bar = Class_Method)
            def __init__ (self) :
                self.foo = 2 * 137
            def chameleon (soc) :
                print "U.chameleon>", type (soc), soc.foo
            def bar (cls) :
                print "U.bar>", cls, "bar"
        U.chameleon ()
        U ().chameleon ()
        U.bar       ()
        U ().bar    ()

        class T (object) :
            __metaclass__ = TFL.Meta.M_Class
            __properties  = \
              ( RO_Property ("x", 42,  "readonly  property")
              , RW_Property ("y", 137, "writeable property")
              )

        class U (T) :
            __properties = \
              ( RW_Property ("x", 3.1415926, "redefined attribute")
              , RO_Property ("z", "fubar")
              )
    # end if __debug__

    ### end unit-test code ########################################################
else :
    TFL.Meta._Export ("*", "_Property_")
### __END__ TFL.Meta.Property
