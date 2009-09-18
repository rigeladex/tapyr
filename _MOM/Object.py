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

    __metaclass__ = MOM.Meta.M_Object

    ### redefine in descendents if object name must match a certain pattern
    name_pattern          = None

    entity_kind           = "object"

    _name_of_define_stmt  = "define"
    _name_of_remove_stmt  = "destroy"

    def __new__ (cls, name, ** kw) :
        result       = super (Object, cls).__new__ (cls)
        result.name  = name
        return result
    # end def __new__

    def __init__ (self, name, ** kw) :
        if not name :
            raise MOM.Error.Invalid_Name ("<empty>")
        if self.name_pattern and not self.name_pattern.match (name) :
            raise MOM.Error.Invalid_Name (name)
        self.implicit = None
        self.home_scope.add (self)
        ### Call the __init__ of the Ancestor as late as possible.
        self.__super.__init__ ()
        if kw :
            self.set (** kw)
    # end def __init__

    def destroy (self) :
        """Remove object from `extension'."""
        if self is self.home_scope.root :
            self.home_scope.destroy ()
        else :
            assert (not self.home_scope._locked)
            self.home_scope.remove (self.name)
    # end def destroy

    def rename (self, new_name) :
        """Rename object to `new_name'."""
        if self.home_scope._roots.get (self.Essence.type_base_name) is self :
            raise MOM.Error.Cannot_Rename_Root_Object (self, new_name)
        if self.name_pattern and not self.name_pattern.match (new_name) :
            raise MOM.Error.Invalid_Name (new_name)
        old_name  = self.name
        self.home_scope.rename (self, new_name)
        self.name = new_name
        for d in self.dependencies.keys () :
            try :
                d.update_dependency_names (self, old_name)
            except :
                print self.__class__, old_name, new_name, d
                raise
    # end def rename

    def _names (self) :
        return (self.name, )
    # end def _names

    def _define_stmt_name_arg (self) :
        return '"%s"' % self.name
    # end def _define_stmt_name_arg

    def _remove_stmt_name_arg (self) :
        return "%s.instance (%r)" % (self.type_name, self.name)
    # end def _remove_stmt_name_arg

    def journal_stmt (self, result_dict) :
        args = self._journal_items \
             (result_dict, [self._define_stmt_name_arg ()])
        if len (args) > 1 :
            return """%s.%s (%s, raw=1)\n""" % \
                (self.type_name, self._name_of_define_stmt, ", ".join (args))
        else :
            return ""
    # end def journal_stmt

    def _repr (self, type_name) :
        return """%s.instance ("%s")""" % (type_name, self.name)
    # end def _repr

    def __str__ (self) :
        return self.type_name + " `" + self.name + "'"
    # end def __str__

    def __hash__ (self) :
        return self.id
    # end def __hash__

    def __cmp__  (self, other) :
        if isinstance (other, Object) :
            return cmp (self.name, other.name)
        return cmp (self.name, other)
    # end def __cmp__

# end class Object

_Essence = Object

__doc__ = """
Class `MOM.Object`
==================

.. moduleauthor:: Christian Tanzer <tanzer@swing.co.at>

.. class:: Object

   `MOM.Object` provides the framework for defining essential classes. It is
   based on :class:`~_MOM.Entity.Entity`. In addition to the
   properties defined by `Entity`, each instance of `Object` is characterized
   by a unique name that must be specified when the instance is created.

Object Queries
--------------

For each essential class `E`, a number of queries is defined:

- `E.count` gives the number of strict instances of `E` (i.e., excluding
  instances of descendent classes). For partial classes, `count` always
  returns zero.

- `E.exists(name)` returns True if an instance of `E` (or one of its
  descendent classes) with the specific `name` exists.

- `E.extension()` returns all instances of `E` and its descendent classes.

- `E.extension_strict()` returns all instances of `E` but none of its
  descendent classes.

- `E.instance(name)` returns the instance of `E` (or one of its descendent
  classes) with the specific `name`.

    .. note::
      For historical reasons, `instance` tries to create an instance with
      `name` if none exists.

- `E.root` gives the root object of `E` in the current scope, if any.

All these queries can be applied to all classes derived from `Object` and to
`Object` itself.

"""

if __name__ != "__main__" :
    MOM._Export ("Object")
### __END__ MOM.Object
