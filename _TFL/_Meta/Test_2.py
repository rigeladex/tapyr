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
#    Test_2
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


class Meta_Meta(type) :
    def __str__(cls) :
        return "Meta_Meta.__str__ %r" % (cls, )
    def str(cls) :
        return "Meta_Meta.str %r" % (cls, )

class Meta(type) :
    __metaclass__ = Meta_Meta
    def __str__(cls) :
        return "Meta.__str__ %r" % (cls, )
    def str(cls) :
        return "Meta.str %r" % (cls, )
    def meta_only(cls) :
        print "Meta.meta_only", cls
    def class_and_meta(cls) :
        print "Meta.class_and_meta", cls

class Class(object) :
    __metaclass__ = Meta
    def __str__(self) :
        return "Class.__str__ %r" % (self, )
    def str(self) :
        return "Class.str %r" % (self, )
    def class_and_meta(self) :
        print "Class.class_and_meta", self
    def class_only(self) :
        print "Class.class_only", self

instance = Class()

for x in instance,Class,Meta,Meta_Meta :
    print x

for x in instance,Class,Meta :
    print x.str()


### __END__ Test_2
