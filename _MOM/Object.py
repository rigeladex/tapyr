# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Mag. Christian Tanzer. All rights reserved
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
#    MOM.Object
#
# Purpose
#    Root class for object-types of MOM meta object model
#
# Revision Dates
#    18-Sep-2009 (CT) Creation (factored from TOM.Object)
#    23-Sep-2009 (CT) Journal-related methods removed
#    23-Sep-2009 (CT) `name` replaced by `epk`
#    ««revision-date»»···
#--

from   _TFL      import TFL
from   _MOM      import MOM

import _MOM.Entity
import _MOM._Meta.M_Object

from   _MOM._Attr.Type import *
from   _MOM._Attr      import Attr

_Ancestor_Essence = MOM.Entity

class Object (_Ancestor_Essence) :
    """Root class for object-types of Tanzer's Object Model."""

    __metaclass__         = MOM.Meta.M_Object

    entity_kind           = "object"

    def __init__ (self, ** kw) :
        kw.pop ("scope", None)
        self.home_scope.add   (self)
        ### Call the __init__ of the Ancestor as late as possible.
        self.__super.__init__ ()
        if kw :
            self.set (** kw)
    # end def __init__

    def destroy (self) :
        """Remove object from `extension`."""
        if self is self.home_scope.root :
            self.home_scope.destroy ()
        else :
            assert (not self.home_scope._locked)
            self.home_scope.remove (self)
    # end def destroy

    def rename (self, new_epk) :
        """Rename object to essential primary key `new_epk`."""
        if self.home_scope._roots.get (self.Essence.type_base_name) is self :
            raise MOM.Error.Cannot_Rename_Root_Object (self, new_epk)
        old_epk  = self.epk
        self.epk = new_epk
        self.home_scope.rename (self, old_epk, new_epk)
        for d in self.dependencies.keys () :
            try :
                d.update_dependency_names (self, old_epk)
            except :
                print self.__class__, old_epk, new_epk, d
                raise
    # end def rename

    def _repr (self, type_name) :
        return """%s.instance (%r)""" % (type_name, self.epk)
    # end def _repr

    def __str__ (self) :
        return "%s `%s`" % (self.type_name, self.epk)
    # end def __str__

    def __hash__ (self) :
        return self.id
    # end def __hash__

    def __cmp__  (self, other) :
        rhs = getattr (other, "epk", other)
        return cmp (self.epk, rhs)
    # end def __cmp__

# end class Object

_Essence = Object

__doc__ = """
Class `MOM.Object`
==================

.. moduleauthor:: Christian Tanzer <tanzer@swing.co.at>

.. class:: Object

   `MOM.Object` provides the framework for defining essential classes. It is
   based on :class:`~_MOM.Entity.Entity`. In addition to the properties
   defined by `Entity`, each instance of `Object` is characterized by a
   unique *essential primary key* (short `epk`) that must be specified when
   the instance is created.

Object Queries
--------------

For each essential class `E`, a number of queries is defined:

### XXX base on `query`

- `E.count` gives the number of strict instances of `E` (i.e., excluding
  instances of descendent classes). For partial classes, `count` always
  returns zero.

- `E.exists(epk)` returns True if an instance of `E` (or one of its
  descendent classes) with the essential primary key `epk` exists.

- `E.extension()` returns all instances of `E` and its descendent classes.

- `E.extension_strict()` returns all instances of `E` but none of its
  descendent classes.

- `E.instance(epk)` returns the instance of `E` (or one of its descendent
  classes) with the essential primary key `epk`.

- `E.root` gives the root object of `E` in the current scope, if any.

All these queries can be applied to all classes derived from `Object` and to
`Object` itself.

"""

if __name__ != "__main__" :
    MOM._Export ("Object")
### __END__ MOM.Object
