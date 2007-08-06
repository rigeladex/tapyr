#! /swing/bin/python
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
#    Test
#
# Purpose
#    Test python metaclasses
#
# Revision Dates
#    15-May-2002 (CT) Creation
#     7-Sep-2002 (CT) Print statements and instances added
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ««revision-date»»···
#--



print "\nDefining Meta-Meta class"

class Meta_Meta (type) :

    A = "Meta_Meta A"
    B = "Meta_Meta B"
    C = "Meta_Meta C"

    def __new__ (meta, name, bases, dict) :
        print "Meta_Meta.__new__", meta, name
        result = super (Meta_Meta, meta).__new__ (meta, name, bases, dict)
        print "  ", result
        return result
    # end def __new__

    def __init__ (cls, name, bases, dict) :
        print "Meta_Meta.__init__", cls, name
        super (Meta_Meta, cls).__init__ (name, bases, dict)
    # end def __init__

    def __call__ (cls, * args, ** kw) :
        print "Meta_Meta.__call__", cls, args, kw
        result = super (Meta_Meta, cls).__call__ (* args, ** kw)
        print "  ", result
        return result
    # end def __call__

    def meta_meta_method (cls) :
        print "Meta_Meta.meta_meta_method", cls
    # end def meta_meta_method
# end class Meta_Meta

print "\nDefining Meta class"

class Meta (type) :

    __metaclass__ = Meta_Meta

    A = "Meta A"
    B = "Meta B"

    P = "Meta P"
    Q = "Meta Q"
    R = "Meta R"

    def __new__ (meta, name, bases, dict) :
        print "Meta.__new__", meta, name
        result = super (Meta, meta).__new__ (meta, name, bases, dict)
        print "  ", result
        return result
    # end def __new__

    def __init__ (cls, name, bases, dict) :
        print "Meta.__init__", cls, name
        super (Meta, cls).__init__ (name, bases, dict)
    # end def __init__

    def __call__ (cls, * args, ** kw) :
        print "Meta.__call__", cls, args, kw
        result = super (Meta, cls).__call__ (* args, ** kw)
        print "  ", result
        return result
    # end def __call__

    def meta_method (cls) :
        print "Meta.meta_method", cls
    # end def meta_method

    def foo (cls) :
        print "Meta.foo", cls
    # end def foo

# end class Meta

print "\nDefining Meta subclass"

class Sub_Meta (Meta) :

    A = "Sub_Meta A"

    P = "Sub_Meta P"
    Q = "Sub_Meta Q"

    def __new__ (meta, name, bases, dict) :
        print "Sub_Meta.__new__", meta, name
        result = super (Sub_Meta, meta).__new__ (meta, name, bases, dict)
        print "  ", result
        return result
    # end def __new__

    def __init__ (cls, name, bases, dict) :
        print "Sub_Meta.__init__", cls, name
        super (Sub_Meta, cls).__init__ (name, bases, dict)
    # end def __init__

    def __call__ (cls, * args, ** kw) :
        print "Sub_Meta.__call__", cls, args, kw
        result = super (Sub_Meta, cls).__call__ (* args, ** kw)
        print "  ", result
        return result
    # end def __call__

    def meta_method (cls) :
        print "Sub_Meta.meta_method", cls
        return super (Sub_Meta, cls)
    # end def meta_method
# end class Sub_Meta

print "\nDefining Class"

class Class (object) :

    __metaclass__ = Meta

    A = "Class A"

    P = "Class P"
    Q = "Class Q"

    def __new__ (cls) :
        print "Class.__new__", cls
        result = super (Class, cls).__new__ (cls)
        print "  ", result
        return result
    # end def __new__

    def __init__ (self) :
        print "Class.__init__", self
        super (Class, self).__init__ ()
    # end def __init__

    def __call__ (self) :
        print "Class.__call__", self
    # end def __call__

    def bar (cls) :
        print "Class.bar", cls
    bar = classmethod (bar)

    def baz (self) :
        print "Class.baz", self
    # end def baz

# end class Class

print "\nDefining sub Class"

class Sub_Class (Class) :

    __metaclass__ = Sub_Meta

    A = "Sub_Class A"

    P = "Sub_Class P"

    def __new__ (cls) :
        print "Sub_Class.__new__", cls
        result = super (Sub_Class, cls).__new__ (cls)
        print "  ", result
        return result
    # end def __new__

    def __init__ (self) :
        print "Sub_Class.__init__", self
        super (Sub_Class, self).__init__ ()
    # end def __init_

# end class Sub_Class

print "\nDefining instances"

c = Class ()
s = Sub_Class ()

print "\nCalling instances"

c ()
s ()
### __END__ Test
