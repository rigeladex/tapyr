#! /swing/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2003 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.cluster
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
#    Test_3
#
# Purpose
#    Some more tests regarding python metaclasses
#
# Revision Dates
#    13-Mar-2003 (CT) Creation
#    23-Jul-2007 (CED) Activated absolute_import
#    ««revision-date»»···
#--
from __future__ import absolute_import


class Meta(type) :
    def m_new(cls, a) :
        print "Meta.new", cls, a
    def m_init(cls, a) :
        print "Meta.init", cls, a
    def __new__(meta, name, bases, dict) :
        result = super(Meta, meta).__new__(meta, name, bases, dict)
        print result.new
        result.m_new(name)
        return result
    def __init__(cls, name, bases, dict) :
        super(Meta, cls).__init__(name, bases, dict)
        cls.m_init(name)

class Class(object) :
    __metaclass__ = Meta
    def new(self, b, c) :
        print "Class.new", self, b, c
    def init(self, b, c):
        print "Class.init", self, b, c
    def __new__(self, b, c) :
        result = super(Class, self).__new__(self)
        result.new(1, 2)
        return result
    def __init__(self, b, c) :
        super(Class, self).__init__()
        self.init(3, 4)

instance = Class()

### __END__ Test_2
